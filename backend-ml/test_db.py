import sys
import traceback
from src.database import get_db_connection, init_db

try:
    print("Testing DB connection...")
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 as ok")
        row = cur.fetchone()
        print("SELECT 1 result:", row)

    print("Calling init_db() to ensure tables exist...")
    init_db()
    print("init_db() completed successfully")
    sys.exit(0)
except Exception as e:
    traceback.print_exc()
    print("ERROR:", str(e))
    sys.exit(2)
