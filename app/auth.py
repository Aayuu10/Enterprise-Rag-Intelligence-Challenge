from app.db import get_connection

def get_user_role(user_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None