import os

# =============================================================================
# MODEL CONFIGURATION
# =============================================================================
REPO_NAME = "Jayanth2002/dinov2-base-finetuned-SkinDisease"

CLASS_NAMES = [
    'Basal Cell Carcinoma', 'Darier_s Disease', 'Epidermolysis Bullosa Pruriginosa', 
    'Hailey-Hailey Disease', 'Herpes Simplex', 'Impetigo', 'Larva Migrans', 
    'Leprosy Borderline', 'Leprosy Lepromatous', 'Leprosy Tuberculoid', 
    'Lichen Planus', 'Lupus Erythematosus Chronicus Discoides', 'Melanoma', 
    'Molluscum Contagiosum', 'Mycosis Fungoides', 'Neurofibromatosis', 
    'Papilomatosis Confluentes And Reticulate', 'Pediculosis Capitis', 
    'Pityriasis Rosea', 'Porokeratosis Actinic', 'Psoriasis', 'Tinea Corporis', 
    'Tinea Nigra', 'Tungiasis', 'actinic keratosis', 'dermatofibroma', 'nevus', 
    'pigmented benign keratosis', 'seborrheic keratosis', 'squamous cell carcinoma', 
    'vascular lesion'
]

# =============================================================================
# FILE CONFIGURATION
# =============================================================================
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATABASE_PATH = os.path.join(BASE_DIR, 'skincheck.db')

# Pastikan folder uploads ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Confidence thresholds untuk validasi multi-level
CONFIDENCE_THRESHOLD = 0.75  # Threshold untuk hasil "baik"
CONFIDENCE_MINIMUM = 0.35    # Threshold minimum (di bawah ini = reject)
CONFIDENCE_WARNING = 0.50    # Threshold untuk warning

# =============================================================================
# DISEASE INFORMATION DATABASE
# =============================================================================
DISEASE_INFO = {
    "Melanoma": {
        "description": "Melanoma adalah jenis kanker kulit yang berkembang dari sel-sel melanosit. Ini adalah bentuk kanker kulit yang paling serius.",
        "severity": "high",
        "recommendation": ""
    },
    "Basal Cell Carcinoma": {
        "description": "Karsinoma sel basal adalah kanker kulit yang paling umum. Biasanya tumbuh lambat dan jarang menyebar.",
        "severity": "medium",
        "recommendation": ""
    },
    "squamous cell carcinoma": {
        "description": "Karsinoma sel skuamosa adalah kanker kulit yang dapat menyebar jika tidak diobati.",
        "severity": "high",
        "recommendation": ""
    },
    "Psoriasis": {
        "description": "Psoriasis adalah penyakit autoimun yang menyebabkan sel kulit berkembang terlalu cepat.",
        "severity": "medium",
        "recommendation": ""
    },
    "Herpes Simplex": {
        "description": "Herpes simplex adalah infeksi virus yang menyebabkan luka lepuh di kulit.",
        "severity": "low",
        "recommendation": ""
    },
    "Impetigo": {
        "description": "Impetigo adalah infeksi bakteri kulit yang menular, sering pada anak-anak.",
        "severity": "low",
        "recommendation": ""
    },
    "Tinea Corporis": {
        "description": "Tinea corporis (kurap) adalah infeksi jamur yang menyebabkan ruam berbentuk cincin.",
        "severity": "low",
        "recommendation": ""
    },
    "nevus": {
        "description": "Nevus (tahi lalat) adalah pertumbuhan kulit jinak dari sel pigmen.",
        "severity": "low",
        "recommendation": ""
    },
    "actinic keratosis": {
        "description": "Keratosis aktinik adalah bercak kasar akibat paparan sinar UV. Dapat berkembang menjadi kanker.",
        "severity": "medium",
        "recommendation": ""
    },
    "dermatofibroma": {
        "description": "Dermatofibroma adalah benjolan keras jinak di kulit, biasanya di kaki.",
        "severity": "low",
        "recommendation": ""
    },
    "pigmented benign keratosis": {
        "description": "Keratosis jinak berpigmen adalah pertumbuhan kulit non-kanker berwarna gelap.",
        "severity": "low",
        "recommendation": ""
    },
    "seborrheic keratosis": {
        "description": "Keratosis seboroik adalah pertumbuhan kulit jinak seperti tempelan lilin.",
        "severity": "low",
        "recommendation": ""
    },
    "vascular lesion": {
        "description": "Lesi vaskular adalah kelainan pembuluh darah yang terlihat di kulit.",
        "severity": "low",
        "recommendation": ""
    },
    "Lichen Planus": {
        "description": "Lichen planus adalah peradangan kulit yang menyebabkan benjolan ungu kemerahan.",
        "severity": "low",
        "recommendation": ""
    },
    "Pityriasis Rosea": {
        "description": "Pityriasis rosea adalah ruam kulit yang biasanya hilang sendiri dalam 6-8 minggu.",
        "severity": "low",
        "recommendation": ""
    }
}

DEFAULT_DISEASE_INFO = {
    "description": "Kondisi kulit yang terdeteksi oleh sistem AI. Silakan konsultasikan dengan dokter untuk diagnosis akurat.",
    "severity": "unknown",
    "recommendation": ""
}