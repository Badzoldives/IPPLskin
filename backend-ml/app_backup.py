# backend-ml/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from src.inference import predict_skin_disease
from src.utils import allowed_file
from src.config import UPLOAD_FOLDER, CONFIDENCE_THRESHOLD
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# TAMBAHKAN INI:
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY tidak ditemukan!")
    print("Chatbot tidak akan berfungsi. Silakan set API key di file .env")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini AI configured successfully")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Tambahkan dictionary informasi penyakit (atau pindahkan ke config.py)
DISEASE_INFO = {
    "Melanoma": {
        "description": "Melanoma adalah jenis kanker kulit yang berkembang dari sel-sel yang memberi warna pada kulit (melanosit). Ini adalah bentuk kanker kulit yang paling serius.",
        "severity": "high",
        "recommendation": "Segera konsultasikan dengan dokter kulit atau onkologi. Jangan mencoba mengobati sendiri. Deteksi dini sangat penting untuk prognosis yang baik."
    },
    "Basal Cell Carcinoma": {
        "description": "Karsinoma sel basal adalah jenis kanker kulit yang paling umum. Biasanya tumbuh lambat dan jarang menyebar ke bagian tubuh lain.",
        "severity": "medium",
        "recommendation": "Konsultasikan dengan dokter kulit untuk diagnosis dan penanganan yang tepat. Hindari paparan sinar matahari berlebihan."
    },
    # Tambahkan info untuk penyakit lainnya...
}

# Default info untuk penyakit yang belum memiliki detail
DEFAULT_DISEASE_INFO = {
    "description": "Kondisi kulit yang terdeteksi oleh sistem AI. Silakan konsultasikan dengan dokter untuk diagnosis yang akurat.",
    "severity": "unknown",
    "recommendation": "Konsultasikan dengan dokter kulit untuk pemeriksaan lebih lanjut dan penanganan yang tepat."
}

@app.route('/predict', methods=['POST'])
def handle_prediction():
    # 1. Validasi File Upload
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Tidak ada bagian 'file' dalam request"}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "File tidak valid atau ekstensi tidak diizinkan"}), 400
        
    # 2. Simpan File Sementara
    filename = secure_filename(file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # 3. Panggil Logika Prediksi
        prediction_result = predict_skin_disease(file_path)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        # 4. Bersihkan File
        if os.path.exists(file_path):
            os.remove(file_path)
    
    if "error" in prediction_result:
        return jsonify({"status": "error", "message": prediction_result["error"]}), 500
    
    # 5. Format response sesuai yang diharapkan frontend
    predicted_label = prediction_result["prediction"]
    confidence = float(prediction_result["confidence"])
    
    # Ambil info penyakit
    disease_info = DISEASE_INFO.get(predicted_label, DEFAULT_DISEASE_INFO)
    
    # Cek confidence threshold
    warning = None
    if confidence < CONFIDENCE_THRESHOLD:
        warning = f"Tingkat kepercayaan AI rendah ({confidence*100:.1f}%). Hasil mungkin kurang akurat."
    
    response = {
        "status": "success",
        "prediction": {
            "label": predicted_label,
            "confidence": confidence,  # Harus number, bukan string
            "description": disease_info["description"],
            "severity": disease_info["severity"],
            "recommendation": disease_info["recommendation"]
        },
        "top_3_predictions": [],  # Bisa ditambahkan nanti dari inference.py
        "warning": warning
    }
    
    return jsonify(response), 200

@app.route('/chatbot', methods=['POST'])
def handle_chatbot():
    """
    Endpoint untuk chatbot berbasis Gemini AI
    """
    try:
        # Cek API key dulu
        if not GEMINI_API_KEY:
            return jsonify({
                "status": "error",
                "error": "Chatbot belum dikonfigurasi. API key tidak ditemukan."
            }), 503
        
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "status": "error",
                "error": "Message tidak boleh kosong"
            }), 400
        
        user_message = data['message']
        context = datalkiuu.get('context', '')
        
        # System prompt khusus untuk skin disease assistant
        system_prompt = """Anda adalah asisten AI medis yang ahli dalam penyakit kulit (dermatologi). 
Tugas Anda adalah membantu pengguna dengan pertanyaan tentang:
- Penyakit kulit dan gejalanya
- Cara perawatan kulit yang sehat
- Penjelasan hasil diagnosis dari sistem deteksi penyakit kulit
- Saran umum perawatan (bukan diagnosis medis)

PENTING: 
1. Selalu ingatkan bahwa jawaban Anda bersifat informasi umum dan bukan pengganti konsultasi dengan dokter.
2. Berikan jawaban dalam bahasa Indonesia yang mudah dipahami.
3. Jika pertanyaan di luar topik kesehatan kulit, arahkan kembali ke topik yang relevan.
4. Berikan informasi yang akurat dan berbasis pengetahuan medis."""

        # Buat prompt lengkap
        full_prompt = system_prompt + "\n\n"
        if context:
            full_prompt += f"Konteks: {context}\n\n"
        full_prompt += f"Pertanyaan: {user_message}"
        
        # Call Gemini API dengan SDK baru (gemini-2.0-flash adalah versi lite/cepat)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(full_prompt)

        
        bot_reply = response.text
        
        return jsonify({
            "status": "success",
            "reply": bot_reply,
            "model": "gemini-2.0-flash-lite"
        }), 200
        
    except Exception as e:
        print(f"❌ Chatbot Error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": "Maaf, terjadi kesalahan pada chatbot. Silakan coba lagi.",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    # Jalankan server di port 8000
    app.run(debug=True, host='0.0.0.0', port=8000)