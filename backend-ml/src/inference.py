# backend-ml/src/inference.py
import torch
import numpy as np
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
from .config import REPO_NAME, CLASS_NAMES, CONFIDENCE_THRESHOLD # Impor dari config yang sudah dibuat

# Pemuatan Model (Hanya dilakukan sekali saat aplikasi dimulai)
print(f"Mengunduh dan memuat model: {REPO_NAME}...")
try:
    # Try to load from cache first (offline mode)
    image_processor = AutoImageProcessor.from_pretrained(REPO_NAME, local_files_only=True)
    model = AutoModelForImageClassification.from_pretrained(REPO_NAME, local_files_only=True)
    print("Model dimuat dari cache lokal.")
except Exception as e:
    print(f"Cache lokal tidak ditemukan, download dari HuggingFace...")
    # If cache not found, download from internet
    image_processor = AutoImageProcessor.from_pretrained(REPO_NAME)
    model = AutoModelForImageClassification.from_pretrained(REPO_NAME)
    print("Model berhasil didownload dan dimuat.")
print("Model siap.")

def is_likely_skin_image(image: Image.Image) -> dict:
    """
    Validasi apakah gambar kemungkinan berisi kulit manusia.
    Menggunakan analisis warna HSV untuk deteksi rentang warna kulit.
    
    Returns:
        dict: {"is_skin": bool, "confidence": float, "reason": str}
    """
    try:
        # Convert ke RGB jika perlu
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize untuk performa (analisis warna tidak perlu resolusi tinggi)
        img_small = image.resize((200, 200))
        img_array = np.array(img_small)
        
        # Convert RGB ke HSV untuk deteksi warna kulit
        # HSV lebih robust untuk deteksi warna kulit
        from PIL import ImageStat
        
        # Hitung statistik warna
        stat = ImageStat.Stat(img_small)
        mean_rgb = stat.mean[:3]
        
        # Rentang warna kulit manusia (simplified)
        # R: 95-255, G: 40-200, B: 20-170
        # Plus ratio: R>G>B (umumnya berlaku untuk kulit)
        r, g, b = mean_rgb
        
        # Check 1: Rentang RGB untuk kulit
        in_skin_range = (95 <= r <= 255) and (40 <= g <= 200) and (20 <= b <= 170)
        
        # Check 2: Ratio R > G > B (karakteristik kulit)
        proper_ratio = r > g > b
        
        # Check 3: Tidak terlalu gelap atau terlalu terang
        brightness = (r + g + b) / 3
        proper_brightness = 60 <= brightness <= 220
        
        # Hitung persentase pixel dalam rentang kulit (metode alternatif)
        hsv_array = np.array(img_small.convert('HSV'))
        h, s, v = hsv_array[:,:,0], hsv_array[:,:,1], hsv_array[:,:,2]
        
        # Rentang HSV untuk kulit (dari penelitian skin detection)
        # Hue: 0-50 (merah-orange), Saturation: 0.23-0.68, Value: 0.35-1.0
        skin_mask = (
            ((h >= 0) & (h <= 50)) &
            ((s >= 58) & (s <= 173)) &  # 0.23*255 to 0.68*255
            ((v >= 89) & (v <= 255))     # 0.35*255 to 1.0*255
        )
        
        skin_percentage = np.sum(skin_mask) / skin_mask.size
        
        # Decision logic
        is_skin = False
        confidence = 0.0
        reason = ""
        
        if skin_percentage > 0.15:  # Minimal 15% pixel adalah warna kulit
            is_skin = True
            confidence = min(skin_percentage * 2, 0.95)  # Scale to 0-0.95
            reason = f"Terdeteksi {skin_percentage*100:.1f}% area kulit"
        elif in_skin_range and proper_ratio and proper_brightness:
            is_skin = True
            confidence = 0.6
            reason = "Warna rata-rata konsisten dengan kulit"
        else:
            reason = f"Warna tidak konsisten dengan kulit (RGB: {r:.0f},{g:.0f},{b:.0f}, Skin%: {skin_percentage*100:.1f}%)"
        
        return {
            "is_skin": is_skin,
            "confidence": confidence,
            "reason": reason,
            "skin_percentage": skin_percentage
        }
        
    except Exception as e:
        # Jika gagal validasi, lebih baik reject untuk keamanan
        return {
            "is_skin": False,
            "confidence": 0.0,
            "reason": f"Gagal validasi: {str(e)}",
            "skin_percentage": 0.0
        }

def predict_skin_disease(image_path: str) -> dict:
    """
    Melakukan inferensi pada gambar yang diberikan dan mengembalikan hasil klasifikasi.
    """
    try:
        # 1. Load Gambar & Pra-Pemrosesan
        image = Image.open(image_path)
        
        # STEP 1: Validasi apakah gambar adalah kulit
        skin_check = is_likely_skin_image(image)
        if not skin_check["is_skin"]:
            return {
                "error": "not_skin",
                "message": "Gambar yang diupload bukan foto kulit",
                "reason": skin_check["reason"],
                "suggestion": "Silakan upload foto kulit yang jelas. Pastikan fokus pada area kulit dengan pencahayaan yang baik.",
                "prediction": None
            }
        
        # Sesuai deskripsi model, prosesor menyiapkan image patches dan token [CLS]
        encoding = image_processor(image.convert("RGB"), return_tensors="pt")

        # 2. Inferensi
        with torch.no_grad():
            outputs = model(**encoding)
            logits = outputs.logits # Logit dari lapisan linear di atas token [CLS]

        # 3. Pasca-Pemrosesan
        predicted_class_idx = logits.argmax(-1).item()
        
        # Hitung skor kepercayaan (probabilitas)
        probabilities = torch.softmax(logits, dim=1)[0]
        confidence = probabilities[predicted_class_idx].item()
        
        predicted_class_name = CLASS_NAMES[predicted_class_idx]
        
        # Get top 3 predictions
        top_3_indices = probabilities.argsort(descending=True)[:3]
        top_3 = [
            {
                "label": CLASS_NAMES[idx.item()],
                "confidence": round(probabilities[idx].item() * 100, 1)
            }
            for idx in top_3_indices
        ]
        
        # STEP 2: Validasi confidence threshold
        # Untuk aplikasi medis, confidence rendah = reject
        if confidence < 0.35:  # 35% threshold untuk reject
            return {
                "error": "low_confidence",
                "message": "Hasil prediksi tidak dapat dipercaya",
                "reason": f"Tingkat kepercayaan AI terlalu rendah ({confidence*100:.1f}%)",
                "suggestion": "Coba upload foto dengan kualitas lebih baik: pencahayaan cukup, fokus jelas, dan area kulit terlihat dengan baik.",
                "prediction": None,
                "top_3": top_3  # Tetap kirim untuk debugging
            }

        return {
            "prediction": predicted_class_name,
            "confidence": confidence,  # float 0-1
            "class_index": predicted_class_idx,
            "top_3": top_3,
            "skin_validation": skin_check  # Info tambahan
        }

    except Exception as e:
        return {"error": f"Gagal dalam prediksi: {str(e)}", "prediction": "Gagal"}


def get_model_info() -> dict:
    """Mengembalikan informasi tentang model yang digunakan"""
    return {
        "model_name": REPO_NAME,
        "total_classes": len(CLASS_NAMES),
        "class_names": CLASS_NAMES,
        "framework": "PyTorch + HuggingFace Transformers"
    }