# Backend ML - Skin Disease Detection API

API untuk deteksi penyakit kulit menggunakan machine learning model dari Hugging Face.

## Struktur Folder

```
backend-ml/
├── src/
│   ├── __init__.py
│   ├── inference.py      # Model loading dan inference
│   ├── config.py         # Konfigurasi aplikasi
│   └── utils.py          # Helper functions
├── uploads/              # Temporary folder untuk upload
├── app.py                # FastAPI main application
├── requirements.txt      # Dependencies
└── README.md            # Dokumentasi
```

## Instalasi

```bash
pip install -r requirements.txt
```

## Cara Menjalankan

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /predict
Upload gambar untuk deteksi penyakit kulit.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image file)

**Response:**
```json
{
  "label": "Nevus",
  "confidence": 0.95,
  "raw": [0.01, 0.02, 0.03, 0.95, 0.01, 0.02, 0.01, 0.01],
  "all_classes": {
    "Acitinic Keratosis": 0.01,
    "Basal Cell Carcinoma": 0.02,
    ...
  }
}
```

### GET /
Health check endpoint.

### GET /classes
Mendapatkan daftar semua kelas penyakit.

## Penyakit yang Dapat Dideteksi

1. Acitinic Keratosis
2. Basal Cell Carcinoma
3. Dermatofibroma
4. Nevus
5. Pigmented Benign Keratosis
6. Seborrheic Keratosis
7. Squamous Cell Carcinoma
8. Vascular Lesion

## Testing dengan cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"
```

## Environment Variables

Tidak ada environment variables yang diperlukan saat ini.
