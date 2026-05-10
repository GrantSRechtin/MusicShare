import os
import yaml
import sqlite3
from datetime import date
from git import Repo

from change_harmonoid_dirs import get_directories, set_directories


def load_config(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(path) as f:
        return yaml.safe_load(f)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # || Send initial Message ||
    init_message()

    # || Wait for command
    while(True):
        command = input("Please enter a command and press Enter: ")
        if command == "u":
            u()
        elif command == "g":
            swap_harmonoid_folder("Grant")
        elif command == "n":
            swap_harmonoid_folder("Nathaniel")
        elif command == "c":
            swap_harmonoid_folder("Combined")
        else:
            print("That is not an option")
            


# ── Commands ──────────────────────────────────────────────────────────────────────
def u():
    cfg = load_config()
    user = cfg["user"]

    repo = Repo(os.path.abspath("")) # Open existing repo
    origin = repo.remote(name='origin')

    print("Git Pulling")
    origin.pull()

    print("Git Adding")
    repo.index.add([user])
    repo.index.commit(f"{user}-{date.today()}")

    print("Git Pushing")
    origin.push()
    
def swap_harmonoid_folder(folder):
    cfg = load_config()

    db_path = cfg["DB_PATH"]
    key = cfg["KEY"]

    with sqlite3.connect(db_path) as conn:
        current = get_directories(conn, key)
        print("Current directories:", current)

        file_path = os.path.abspath(folder)

        new_dirs = [file_path]
        set_directories(conn, new_dirs, key)
        print("Updated directories:", get_directories(conn, key))


# ── Helper Functions ──────────────────────────────────────────────────────────────────────
def init_message():
    print("||-------------------------------||")
    print("            Music Share            ")
    print("||-------------------------------||")
    print("\nCommands:")
    print("u = update")
    print("g = swap harmonoid to Grant's folder")
    print("n = swap harmonoid to Nathaniel's folder")
    print("c = swap harmonoid to combined folder")
    print("\nPress Ctrl+C to exit")

if __name__ == "__main__":
    main()