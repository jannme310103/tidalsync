# TIDAL Playlist Synchronizer

A command-line tool written in Python that lets you synchronize songs from one TIDAL playlist to another. Ideal for maintaining shared playlists, backups, or syncing between multiple accounts.

---

## 🚀 Features

- 🔐 OAuth login using the official TIDAL API
- 🎵 Manual input for source and target playlist IDs
- ✅ UUID format validation for IDs
- ⚠️ Handles empty source playlists gracefully
- 🔁 Detects and adds only missing songs
- 📋 Supports playlists with over 1000 tracks
- 🧾 Daily logging inside `logs/YYYY-MM-DD_sync.txt`
- 🎨 Color-coded terminal output for better clarity
- 🔢 Summary of added tracks after each sync
- 🔄 Repeat syncs without restarting the script

---

## 📦 Requirements

- Python 3.8+
- A valid TIDAL account (HiFi or HiFi Plus)
- `tidalapi`, `colorama` Python packages

---

## 🛠 Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/jannme310103/tidalsync.git
    cd tidalsync
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:
    ```bash
    python tidalsync.py
    ```
---

## 📁 Logs

Added tracks are saved to:
```bash
logs/YYYY-MM-DD_sync.txt
```
---

## 💡 Example Usage

```bash
=== TIDAL Playlist Synchronizer ===

Logging in...
Login successful!

Enter the SOURCE playlist ID: abc123...
Enter the TARGET playlist ID: xyz456...

Loaded 248 tracks from source playlist: My Daily Mix
Loaded 215 tracks from target playlist: Shared Mix

Added 5 new track(s) to 'Shared Mix':
✓ Artist1 - Song1
✓ Artist2 - Song2
...

Do you want to sync another playlist? (y/n): n
Exiting...
```
---

## 📝 License

MIT – free to use, modify, and distribute.
