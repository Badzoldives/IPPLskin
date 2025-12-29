import os
import uuid
import bcrypt
import google.generativeai as genai
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask import jsonify

# Import modules
from src.inference import predict_skin_disease, get_model_info
from src.utils import allowed_file
from src.config import (
    UPLOAD_FOLDER, CONFIDENCE_THRESHOLD, 
    DISEASE_INFO, DEFAULT_DISEASE_INFO, CLASS_NAMES
)
from src.database import (
    create_user, get_user_by_email, get_user_by_id,
    save_diagnosis, get_user_history, get_diagnosis_by_id,
    delete_diagnosis, delete_all_user_history, get_user_statistics
)

# Load environment variables
load_dotenv()

# =============================================================================
# GEMINI AI CONFIGURATION
# =============================================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        instruction = (
            "Kamu adalah asisten AI kesehatan kulit bernama SkinCheck AI. "
            "Bantu pengguna dengan pertanyaan seputar kesehatan kulit. "
            "Berikan jawaban informatif, ramah, dalam Bahasa Indonesia, "
            "dan selalu ingatkan untuk konsultasi dengan dokter. "
            "Jangan memberikan diagnosis pasti."
        )
        gemini_model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-lite',
            system_instruction=instruction
        )
        print("Gemini AI Berhasil")
    except Exception as e:
        print(f"Gagal konfigurasi Gemini: {e}")
else:
    print("API Key tidak ditemukan")

# =============================================================================
# FLASK APP INITIALIZATION
# =============================================================================

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'skincheck-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173", 
            "http://localhost:5174",
            "http://localhost:5175",
            "http://127.0.0.1:5173",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# =============================================================================
# AUTH ENDPOINTS
# =============================================================================

@app.route('/auth/register', methods=['POST'])
def register():
    """Register user baru"""
    try:
        data = request.get_json()
        
        # Validasi input
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "status": "error",
                    "message": f"Field '{field}' wajib diisi"
                }), 400
        
        username = data['username'].strip().lower()
        email = data['email'].strip().lower()
        password = data['password']
        full_name = data.get('full_name', '').strip()
        
        # Validasi email format
        if '@' not in email or '.' not in email:
            return jsonify({
                "status": "error",
                "message": "Format email tidak valid"
            }), 400
        
        # Validasi password
        if len(password) < 6:
            return jsonify({
                "status": "error",
                "message": "Password minimal 6 karakter"
            }), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        user = create_user(username, email, password_hash, full_name)
        
        # Generate tokens
        access_token = create_access_token(identity=str(user['id']))
        refresh_token = create_refresh_token(identity=str(user['id']))
        
        return jsonify({
            "status": "success",
            "message": "Registrasi berhasil",
            "data": {
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email']
                },
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }), 201
        
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 409
    except Exception as e:
        print(f"Register error: {e}")
        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan server"
        }), 500


@app.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email dan password wajib diisi"
            }), 400
        
        # Cari user
        user = get_user_by_email(email)
        if not user:
            return jsonify({
                "status": "error",
                "message": "Email atau password salah"
            }), 401
        
        # Verifikasi password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({
                "status": "error",
                "message": "Email atau password salah"
            }), 401
        
        # Generate tokens
        access_token = create_access_token(identity=str(user['id']))
        refresh_token = create_refresh_token(identity=str(user['id']))
        
        return jsonify({
            "status": "success",
            "message": "Login berhasil",
            "data": {
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email'],
                    "full_name": user.get('full_name', '')
                },
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        })
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan server"
        }), 500


@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({
        "status": "success",
        "access_token": access_token
    })


@app.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    user_id = get_jwt_identity()
    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({
            "status": "error",
            "message": "User tidak ditemukan"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": {
            "id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "full_name": user.get('full_name', '')
        }
    })

#endpoint health check

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "SkinCheck AI Backend",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        "status": "success",
        "data": get_model_info()
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"healthy"}), 200

@app.route('/classes', methods=['GET'])
def get_classes():
    """Get list of all disease classes"""
    return jsonify({
        "status": "success",
        "total": len(CLASS_NAMES),
        "classes": CLASS_NAMES
    })

#endpoint prediksi penyakit kulit

@app.route('/predict', methods=['POST'])
@jwt_required(optional=True)  # Optional: bisa dengan atau tanpa login
def predict():
    """Prediksi penyakit kulit dari gambar"""
    try:
        # Check file
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "Tidak ada file dalam request. Gunakan field 'file'."
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "Tidak ada file yang dipilih"
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "status": "error",
                "message": "Format file tidak didukung. Gunakan JPG, JPEG, atau PNG."
            }), 400
        
        # Save file
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        # Predict
        result = predict_skin_disease(filepath)
        
        if result is None:
            return jsonify({
                "status": "error",
                "message": "Gagal memproses gambar"
            }), 500
        
        # Check for validation errors (not skin / low confidence)
        if result.get('error'):
            error_type = result.get('error')
            if error_type == 'not_skin':
                return jsonify({
                    "status": "error",
                    "message": result.get('message', 'Gambar bukan foto kulit'),
                    "reason": result.get('reason', ''),
                    "suggestion": result.get('suggestion', 'Upload foto kulit yang jelas')
                }), 400
            elif error_type == 'low_confidence':
                return jsonify({
                    "status": "error",
                    "message": result.get('message', 'Hasil tidak dapat dipercaya'),
                    "reason": result.get('reason', ''),
                    "suggestion": result.get('suggestion', 'Upload foto dengan kualitas lebih baik'),
                    "top_3": result.get('top_3', [])
                }), 400
        
        # Get disease info
        condition = result['prediction']
        confidence = result['confidence']
        disease_data = DISEASE_INFO.get(condition, DEFAULT_DISEASE_INFO)
        

        # Prepare response (format compatible dengan frontend)
        prediction_data = {
            "label": condition,
            "confidence": confidence,
            "confidence_percent": round(confidence * 100, 1),
            "severity": disease_data.get('severity', 'unknown'),
            "description": disease_data.get('description', '')
        }
        
        response_data = {
            "prediction": prediction_data,
            "top_3_predictions": result.get('top_3', []),
            "image_filename": filename
        }
        
        # Save to database if user is logged in
        user_id = get_jwt_identity()
        if user_id:
            diagnosis_id = save_diagnosis(
                user_id=int(user_id),
                condition=condition,
                confidence=confidence,
                severity=disease_data.get('severity'),
                description=disease_data.get('description'),
                image_filename=filename,
                top_3_predictions=result.get('top_3', [])
            )
            response_data['diagnosis_id'] = diagnosis_id
            response_data['saved'] = True
        else:
            response_data['saved'] = False
        
        # Add warning if confidence is low
        if confidence < CONFIDENCE_THRESHOLD:
            response_data['warning'] = f"Tingkat kepercayaan AI rendah ({confidence*100:.1f}%). Hasil mungkin kurang akurat."
        
        return jsonify({
            "status": "success",
            **response_data
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500

#histroy endpoint

@app.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Ambil riwayat diagnosis user"""
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    result = get_user_history(user_id, page, per_page)
    return jsonify({
        "status": "success",
        **result
    })


@app.route('/history/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Ambil statistik diagnosis user"""
    user_id = int(get_jwt_identity())
    stats = get_user_statistics(user_id)
    return jsonify({
        "status": "success",
        "data": stats
    })


@app.route('/history/<int:diagnosis_id>', methods=['GET'])
@jwt_required()
def get_history_detail(diagnosis_id):
    """Ambil detail diagnosis"""
    user_id = int(get_jwt_identity())
    diagnosis = get_diagnosis_by_id(diagnosis_id, user_id)
    
    if not diagnosis:
        return jsonify({
            "status": "error",
            "message": "Diagnosis tidak ditemukan"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": diagnosis
    })


@app.route('/history/<int:diagnosis_id>', methods=['DELETE'])
@jwt_required()
def delete_history_item(diagnosis_id):
    """Hapus diagnosis"""
    user_id = int(get_jwt_identity())
    success = delete_diagnosis(diagnosis_id, user_id)
    
    if success:
        return jsonify({
            "status": "success",
            "message": "Diagnosis berhasil dihapus"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Diagnosis tidak ditemukan"
        }), 404


@app.route('/history', methods=['DELETE'])
@jwt_required()
def delete_all_history():
    """Hapus semua riwayat user"""
    user_id = int(get_jwt_identity())
    count = delete_all_user_history(user_id)
    return jsonify({
        "status": "success",
        "message": f"{count} diagnosis berhasil dihapus"
    })

#chatbot endpoint

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """AI Chatbot untuk konsultasi kulit"""
    if not gemini_model:
        return jsonify({
            "status": "error",
            "message": "Chatbot tidak tersedia."
        }), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"status": "error", "message": "Pesan kosong"}), 400
        
        # LANGSUNG KIRIM user_message. 
        # Model sudah tahu perannya dari konfigurasi awal.
        response = gemini_model.generate_content(user_message)
        
        return jsonify({
            "status": "success",
            "data": {"reply": response.text}
        })
        
    except Exception as e:
        print(f"Chatbot error: {e}")
        return jsonify({"status": "error", "message": "Gagal memproses pesan"}), 500

# =============================================================================
# STATIC FILES
# =============================================================================

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        "status": "error",
        "message": "File terlalu besar. Maksimal 16MB."
    }), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "Endpoint tidak ditemukan"
    }), 404

# JWT Error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "status": "error",
        "message": "Token sudah expired. Silakan login ulang."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "status": "error",
        "message": "Token tidak valid"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "status": "error",
        "message": "Token diperlukan untuk mengakses endpoint ini"
    }), 401

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 50)
    print("SkinCheck AI Backend v2.0")
    print("=" * 50)
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"AI Model: {len(CLASS_NAMES)} skin conditions")
    print(f"Chatbot: {'Ready' if gemini_model else 'Not configured'}")
    print(f"Database: MySQL")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8000, debug=True)
