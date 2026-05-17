import pandas as pd
from app.db import init_db, get_connection

init_db()
conn = get_connection()

users = pd.read_csv("data/permissions/users.csv")
docs = pd.read_csv("data/metadata/documents.csv")

users.to_sql("users", conn, if_exists="replace", index=False)
docs.to_sql("documents", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("SQLite seeded.")