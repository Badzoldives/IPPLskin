"""
Database module untuk MySQL
- User management (register, login)
- Diagnosis history per user
"""
import os
import json
import pymysql
from datetime import datetime
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'skincheck_db'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

@contextmanager
def get_db_connection():
    """Context manager untuk MySQL connection"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Inisialisasi database - buat tabel jika belum ada"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ''')
            
            # Create diagnosis_history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS diagnosis_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    condition_name VARCHAR(100) NOT NULL,
                    confidence DECIMAL(5,4) NOT NULL,
                    severity VARCHAR(20),
                    description TEXT,
                    recommendation TEXT,
                    image_filename VARCHAR(255),
                    top_3_predictions JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            print("✅ MySQL Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        raise e

# =============================================================================
# USER MANAGEMENT
# =============================================================================

def create_user(username, email, password_hash, full_name=None):
    """Buat user baru"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password, full_name)
                VALUES (%s, %s, %s, %s)
            ''', (username, email, password_hash, full_name))
            conn.commit()
            return {'id': cursor.lastrowid, 'username': username, 'email': email}
        except pymysql.err.IntegrityError as e:
            if 'username' in str(e):
                raise ValueError("Username sudah digunakan")
            elif 'email' in str(e):
                raise ValueError("Email sudah terdaftar")
            raise e

def get_user_by_email(email):
    """Cari user berdasarkan email"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        return cursor.fetchone()

def get_user_by_username(username):
    """Cari user berdasarkan username"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        return cursor.fetchone()

def get_user_by_id(user_id):
    """Cari user berdasarkan ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, full_name, created_at FROM users WHERE id = %s', (user_id,))
        return cursor.fetchone()

# =============================================================================
# DIAGNOSIS HISTORY
# =============================================================================

def save_diagnosis(user_id, condition, confidence, severity=None, description=None, 
                   recommendation=None, image_filename=None, top_3_predictions=None):
    """Simpan hasil diagnosis ke database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        top_3_json = json.dumps(top_3_predictions) if top_3_predictions else None
        cursor.execute('''
            INSERT INTO diagnosis_history 
            (user_id, condition_name, confidence, severity, description, recommendation, 
             image_filename, top_3_predictions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, condition, confidence, severity, description, recommendation,
              image_filename, top_3_json))
        conn.commit()
        return cursor.lastrowid

def get_user_history(user_id, page=1, per_page=10):
    """Ambil riwayat diagnosis user dengan pagination"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Count total
        cursor.execute('SELECT COUNT(*) as total FROM diagnosis_history WHERE user_id = %s', (user_id,))
        total = cursor.fetchone()['total']
        
        # Calculate pagination
        offset = (page - 1) * per_page
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        
        # Fetch data
        cursor.execute('''
            SELECT * FROM diagnosis_history WHERE user_id = %s
            ORDER BY created_at DESC LIMIT %s OFFSET %s
        ''', (user_id, per_page, offset))
        
        rows = cursor.fetchall()
        data = []
        for row in rows:
            item = dict(row)
            # Rename condition_name to condition for frontend compatibility
            item['condition'] = item.pop('condition_name', '')
            # Parse top_3_predictions
            if item.get('top_3_predictions'):
                try:
                    if isinstance(item['top_3_predictions'], str):
                        item['top_3_predictions'] = json.loads(item['top_3_predictions'])
                except:
                    item['top_3_predictions'] = []
            else:
                item['top_3_predictions'] = []
            # Split recommendation into list
            if item.get('recommendation'):
                item['recommendations'] = [r.strip() for r in item['recommendation'].split('.') 
                                          if r.strip() and len(r.strip()) > 10][:5]
            else:
                item['recommendations'] = []
            # Format created_at
            if item.get('created_at'):
                item['created_at'] = item['created_at'].isoformat() if hasattr(item['created_at'], 'isoformat') else str(item['created_at'])
            data.append(item)
        
        return {
            'data': data, 
            'page': page, 
            'per_page': per_page, 
            'total': total, 
            'pages': total_pages
        }

def get_diagnosis_by_id(diagnosis_id, user_id=None):
    """Ambil satu diagnosis berdasarkan ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute('SELECT * FROM diagnosis_history WHERE id = %s AND user_id = %s', 
                          (diagnosis_id, user_id))
        else:
            cursor.execute('SELECT * FROM diagnosis_history WHERE id = %s', (diagnosis_id,))
        row = cursor.fetchone()
        if row:
            item = dict(row)
            item['condition'] = item.pop('condition_name', '')
            if item.get('top_3_predictions'):
                try:
                    if isinstance(item['top_3_predictions'], str):
                        item['top_3_predictions'] = json.loads(item['top_3_predictions'])
                except:
                    item['top_3_predictions'] = []
            if item.get('recommendation'):
                item['recommendations'] = [r.strip() for r in item['recommendation'].split('.') 
                                          if r.strip() and len(r.strip()) > 10][:5]
            else:
                item['recommendations'] = []
            if item.get('created_at'):
                item['created_at'] = item['created_at'].isoformat() if hasattr(item['created_at'], 'isoformat') else str(item['created_at'])
            return item
        return None

def delete_diagnosis(diagnosis_id, user_id):
    """Hapus diagnosis (hanya pemilik yang bisa hapus)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM diagnosis_history WHERE id = %s AND user_id = %s', 
                      (diagnosis_id, user_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_all_user_history(user_id):
    """Hapus semua riwayat user"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM diagnosis_history WHERE user_id = %s', (user_id,))
        conn.commit()
        return cursor.rowcount

def get_user_statistics(user_id):
    """Ambil statistik diagnosis user"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM diagnosis_history WHERE user_id = %s', (user_id,))
        total = cursor.fetchone()['total']
        
        cursor.execute('''
            SELECT severity, COUNT(*) as count FROM diagnosis_history 
            WHERE user_id = %s GROUP BY severity
        ''', (user_id,))
        severity_dist = {row['severity'] or 'unknown': row['count'] for row in cursor.fetchall()}
        
        return {
            'total_diagnoses': total, 
            'severity_distribution': severity_dist
        }

# Initialize database on import
try:
    init_db()
except Exception as e:
    print(f"⚠️ Warning: Could not initialize database: {e}")

