# Music Share (via OneDrive)

## TLDR
Github can't handle the amount of music we have, but OneDrive has a lot of space (as opposed to google drive). This repository makes it easy to share using OneDrive (theoretically).

## Setup

#### 1: Clone the repo
```Bash
git clone https://github.com/GrantSRechtin/MusicShare
```

#### 2: Install requirements
```Bash
pip install -r requirements.txt
```

#### 3: Adjust config file
Replace with correct names for user
```yaml
# ── User ────────────────────────────────────────────────────────
user: "Grant" # Make same as folder name (made later) so "Nathaniel"

# ── File Locations ────────────────────────────────────────────────────────
DB_PATH: 'C:\Users\[USER]\.Harmonoid\Configuration.DB' # Change [USER]
KEY: "MEDIA_LIBRARY_DIRECTORIES" # Don't change
ONEDRIVE_PATH: 'C:\Users\[USER]\OneDrive - Olin College of Engineering' # Change [USER]
```

#### 4: Add the shared OneDrive folder
Grant must first share the `MusicShare` folder with your Olin email from his OneDrive.

Once shared:
1. Go to [onedrive.live.com](https://onedrive.live.com) and sign in with your Olin account
2. Click **Shared** in the left sidebar
3. Find Grant's **MusicShare** folder
4. Right-click it → **Add shortcut to My files**
5. Open File Explorer and confirm the folder appears at:
   `OneDrive - Olin College of Engineering\MusicShare`
6. Wait for it to finish syncing before continuing

#### 5: Create temp music folder
Create a new folder under the same name as the `user: <name>` so in this case Nathaniel

#### 6: Move music
Either move or copy your current music into the new temp folder

#### 7: Sync music
Run main.py and select `s` (sync music).

#### 8: Delete temporary folder
CHECK TO MAKE SURE MUSIC IS NOW WITHIN SHARED ONEDRIVE FOLDER `MusicShare`. If the music is there, you are good to fully delete the temporary folder and everything inside as all the music should now be within the shared OneDrive folder.

#### 9: Add config.yaml to .gitignore
As the config file is specific to you, add it to .gitignore and untrack it so your paths don't overwrite Grant's:
```bash
echo config.yaml >> .gitignore
git rm --cached config.yaml
git commit -m "untrack personal config"
git push
```

## Commands

| Command | Description |
|---------|-------------|
| `u` | Pull latest code, commit any local changes, and push |
| `s` | Sync your local music folder to the shared OneDrive (initial setup only) |
| `g` | Point Harmonoid at Grant's music folder |
| `n` | Point Harmonoid at Nathaniel's music folder |
| `c` | Compare libraries and print songs Nathaniel has that Grant doesn't |
