import sqlite3
import json

DB_PATH = r"C:\Users\grechtin\.Harmonoid\Configuration.DB"
KEY = "MEDIA_LIBRARY_DIRECTORIES"


def get_directories(conn, key):
    row = conn.execute(
        "SELECT json FROM entries WHERE key = ?", (key,)
    ).fetchone()
    return json.loads(row[0]) if row else []


def set_directories(conn, directories, key):
    conn.execute(
        "UPDATE entries SET json = ? WHERE key = ?",
        (json.dumps(directories), key),
    )
    conn.commit()
