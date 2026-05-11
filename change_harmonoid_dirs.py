import json

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
