# ===== STRUKTUR FOLDER BACKEND-ML =====

## Struktur Lengkap:

```
backend-ml/
│
├── src/                      # Source code
│   ├── __init__.py          # Package initializer
│   ├── config.py            # Konfigurasi (model, classes, disease info)
│   ├── inference.py         # Model loading & inference logic
│   └── utils.py             # Helper functions
│
├── uploads/                  # Temporary upload folder (gitignored)
│   └── .gitkeep
│
├── .venv/                    # Virtual environment (gitignored)
│
├── __pycache__/             # Python cache (gitignored)
│
├── app.py                   # FastAPI main application
├── requirements.txt         # Python dependencies
├── test_api.py             # API testing script
├── .gitignore              # Git ignore file
└── README.md               # Dokumentasi

```

## File Explanations:

### 1. app.py
- Main FastAPI application
- Endpoints: /, /health, /classes, /model-info, /predict, /predict-simple
- CORS middleware untuk allow cross-origin requests
- Startup event untuk load model
- Error handling & validation

### 2. src/config.py
- Konfigurasi aplikasi
- MODEL_REPO: Hugging Face model repository
- CLASS_NAMES: List nama penyakit kulit
- DISEASE_INFO: Dictionary informasi lengkap setiap penyakit
- IMG_SIZE: Ukuran input image (512x512)

### 3. src/inference.py
- Model loading dari Hugging Face
- Image preprocessing
- Prediction logic
- Model info retrieval

### 4. src/utils.py
- validate_image(): Validasi file gambar
- get_file_size(): Get ukuran file
- format_prediction_result(): Format hasil prediksi menjadi response

### 5. requirements.txt
- fastapi: Web framework
- uvicorn[standard]: ASGI server
- python-multipart: File upload support
- tensorflow: ML framework
- pillow: Image processing
- numpy: Array operations
- huggingface_hub: Model download

### 6. test_api.py
- Script untuk testing API endpoints
- Test health, classes, model-info, predict

## Improvements dari Struktur Lama:

### ✅ Sebelumnya:
```
backend-ml/
├── app.py
└── src/
    └── inference.py
```

### ✅ Sekarang:
```
backend-ml/
├── app.py                   # Lebih lengkap (CORS, error handling, multiple endpoints)
├── src/
│   ├── __init__.py         # BARU: Package initializer
│   ├── config.py           # BARU: Centralized configuration
│   ├── inference.py        # DIPERBAIKI: Menggunakan tf.saved_model.load
│   └── utils.py            # BARU: Helper functions
├── uploads/                 # BARU: Upload folder
├── requirements.txt         # BARU: Dependencies list
├── test_api.py             # BARU: Testing script
├── .gitignore              # BARU: Git ignore
└── README.md               # BARU: Documentation
```

## Error yang Diperbaiki:

### 1. Import Error (Keras/TensorFlow)
**Masalah**: Konflik import keras dan tensorflow  
**Solusi**: Menggunakan `tf.saved_model.load` langsung tanpa keras

### 2. No Package Structure
**Masalah**: src/ tidak memiliki __init__.py  
**Solusi**: Ditambahkan src/__init__.py

### 3. No Configuration Management
**Masalah**: Hard-coded values  
**Solusi**: Centralized config dalam src/config.py

### 4. No Error Handling
**Masalah**: Tidak ada validation dan error handling  
**Solusi**: Added validation untuk file type, size, dll

### 5. No Documentation
**Masalah**: Tidak ada README dan struktur folder tidak jelas  
**Solusi**: Added comprehensive README.md dan dokumentasi

## Cara Menggunakan:

### 1. Install Dependencies:
```powershell
cd "d:\SEMESTER 5\Skincheck_IPPL\backend-ml"
pip install -r requirements.txt
```

### 2. Jalankan Server:
```powershell
uvicorn app:app --reload --port 8000
```

### 3. Test API:
```powershell
# Test basic endpoints
python test_api.py

# Test predict dengan gambar
python test_api.py path/to/image.jpg
```

### 4. Access API Documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints:

1. **GET /** - Root/Health check
2. **GET /health** - Health status
3. **GET /classes** - List semua classes
4. **GET /model-info** - Model information
5. **POST /predict** - Predict dengan detail info
6. **POST /predict-simple** - Predict simple (no detail)
