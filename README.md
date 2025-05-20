# TIDAL Playlist Synchronizer

A Python-based CLI tool to synchronize songs from one TIDAL playlist to another.  

## 🚀 Features

- 🔐 OAuth login using the official TIDAL API
- 🎵 Manual input of source and target playlist IDs
- 🔁 Detects and adds only missing songs
- 📋 Supports playlists with up to over 1000 tracks
- 🧾 Logging: Saves added tracks to `sync_log.txt`
- 🔄 Repeat syncs in one session without restarting the script

## 📦 Requirements

- Python 3.8+
- `tidalapi` Python package
- A valid TIDAL account (HiFi or HiFi Plus)

## 🛠 Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/tidalsync.git
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

## 💡 Example Usage

```bash
=== TIDAL Playlist Synchronizer ===

Logging in...
Login successful!

Enter the SOURCE playlist ID: abc123...
Enter the TARGET playlist ID: xyz456...

Loaded 248 tracks from source playlist: My Daily Mix
Loaded 215 tracks from target playlist: Shared Mix

Successfully added the following tracks:
Artist1 - Song1
Artist2 - Song2

Do you want to sync another playlist? (y/n):
```

All added tracks are logged with timestamps in `sync_log.txt`.

## 📝 License

MIT – free to use, modify, and share.
