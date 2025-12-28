# backend-ml/src/utils.py
from werkzeug.utils import secure_filename
from .config import ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Memeriksa apakah ekstensi file diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS