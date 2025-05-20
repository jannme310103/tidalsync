# TIDAL Playlist Synchronizer

A Python-based tool to synchronize songs from one TIDAL playlist to another.  
Useful for maintaining shared playlists, backups, or updating secondary accounts.

## 🔧 Features

- Authenticates with your TIDAL account using OAuth
- Prompts for a source and a target playlist ID
- Compares the playlists and identifies missing tracks
- Automatically adds missing songs from source to target
- Handles playlists with over 1000 tracks by using pagination

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A TIDAL account (HiFi or HiFi Plus for API access)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/tidal-playlist-sync.git
    cd tidal-playlist-sync
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:
    ```bash
    python sync.py
    ```

4. When prompted, paste:
    - The **source playlist ID** (songs will be copied from here)
    - The **target playlist ID** (songs will be added here)

## 🧪 Example

Welcome to the Playlist Synchronizer

Logging in:
Login successful

Enter the source playlist ID: 1234abcd...
Enter the target playlist ID: 5678efgh...

Loaded 248 songs from source playlist: My Daily Mix
Loaded 215 songs from target playlist: Shared Mix

Successfully added the following tracks:
Artist1 - Song1
Artist2 - Song2


## 📝 License

MIT – use it freely, modify it, and share it!
