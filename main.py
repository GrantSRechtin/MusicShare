import os
import subprocess
import yaml
import sqlite3
from datetime import date
import pandas as pd
from mutagen.flac import FLAC

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

    # || Wait for command ||
    while(True):
        command = input("Please enter a command and press Enter: ")
        if command == "s":
            sync_music()
        elif command == "g":
            swap_harmonoid_folder("Grant")
        elif command == "n":
            swap_harmonoid_folder("Nathaniel")
        elif command == "c":
            compare()
        elif command == "u":
            update_git()
        else:
            print("That is not an option")
            

# ── Commands ──────────────────────────────────────────────────────────────────────
def update_git():
    cfg = load_config()
    user = cfg["user"]

    print("Pulling latest changes...")
    subprocess.run(["git", "pull"], check=True)

    subprocess.run(["git", "add", "."])

    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if status.stdout.strip():
        print("Committing changes...")
        subprocess.run(["git", "commit", "-m", f"{user}-{date.today()}"], check=True)

    print("Pushing...")
    subprocess.run(["git", "push"], check=True)
    print("Done.")

def sync_music():
    cfg = load_config()
    user = cfg["user"]
    onedrive = cfg["ONEDRIVE_PATH"]

    src = os.path.abspath(user)
    dst = os.path.join(onedrive, "MusicShare", user)

    print(f"Syncing {user} -> OneDrive (this may take a while for new files)...")
    result = subprocess.run(
        ["robocopy", src, dst, "/MIR", "/MT:8", "/R:3", "/W:5"],
        text=True
    )
    if result.returncode < 8:
        print("Sync complete. OneDrive will upload changes in the background.")
    else:
        print(f"Sync failed with code {result.returncode}")
    
def swap_harmonoid_folder(folder):
    cfg = load_config()

    db_path = cfg["DB_PATH"]
    key = cfg["KEY"]

    with sqlite3.connect(db_path) as conn:
        current = get_directories(conn, key)
        print("Current directories:", current)

        file_path = os.path.join(cfg["ONEDRIVE_PATH"], "MusicShare", folder)

        new_dirs = [file_path]
        set_directories(conn, new_dirs, key)
        print("Updated directories:", get_directories(conn, key))

def compare(folder1="Grant", folder2="Nathaniel", artist=None, album=None):
    cfg = load_config()
    base = os.path.join(cfg["ONEDRIVE_PATH"], "MusicShare")
    lib1 = build_library(os.path.join(base, folder1))
    lib2 = build_library(os.path.join(base, folder2))

    if artist is not None:
        pass
    elif album is not None:
        pass
    else:
        missing = []
        for _, song in lib2.iterrows():
            match = (lib1[(lib1["title"] == song["title"]) & (lib1["artist"] == song["artist"])])
            if len(match) == 0:
                missing.append({
                        "artist": song["artist"],
                        "title": song["title"],
                        "album": song["album"],
                    })

        missing = pd.DataFrame(missing, columns=["artist", "title", "album"])        
        
        print("Missing Songs:\n")
        print(missing)

# ── Helper Functions ──────────────────────────────────────────────────────────────────────
def init_message():
    print("||-------------------------------||")
    print("            Music Share            ")
    print("||-------------------------------||")
    print("\nCommands:")
    print("s = sync music")
    print("g = swap harmonoid to Grant's folder")
    print("n = swap harmonoid to Nathaniel's folder")
    print("c = compare music")
    print("\nPress Ctrl+C to exit")

def get_tag(audio, key):
    try:
        return audio[key][0]
    except (KeyError, IndexError):
        return ""

def build_library(folder):
    songs = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".flac"):
                audio = FLAC(os.path.join(root, file))
                songs.append({
                    "artist": get_tag(audio, "artist"),
                    "title": get_tag(audio, "title"),
                    "album": get_tag(audio, "album"),
                })

    return pd.DataFrame(songs, columns=["artist", "title", "album"])

if __name__ == "__main__":
    main()