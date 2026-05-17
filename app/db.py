import sqlite3
from app.config import settings

def get_connection():
    return sqlite3.connect(settings.SQLITE_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        role TEXT,
        department TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        title TEXT,
        source_type TEXT,
        department TEXT,
        sensitivity TEXT,
        allowed_roles TEXT,
        location TEXT
    )
    """)

    conn.commit()
    conn.close()