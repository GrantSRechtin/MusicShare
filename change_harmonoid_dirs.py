import sqlite3
import json

DB_PATH = r"C:\Users\grechtin\.Harmonoid\Configuration.DB"
KEY = "MEDIA_LIBRARY_DIRECTORIES"


def get_directories(conn):
    row = conn.execute(
        "SELECT json FROM entries WHERE key = ?", (KEY,)
    ).fetchone()
    return json.loads(row[0]) if row else []


def set_directories(conn, directories):
    conn.execute(
        "UPDATE entries SET json = ? WHERE key = ?",
        (json.dumps(directories), KEY),
    )
    conn.commit()


if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        current = get_directories(conn)
        print("Current directories:", current)

        new_dirs = [r"C:\Users\grechtin\Music", r"D:\MyMusic"]
        set_directories(conn, new_dirs)
        print("Updated directories:", get_directories(conn))
