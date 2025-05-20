# TIDAL Playlist Synchronizer

A command-line tool written in Python that lets you synchronize songs from one TIDAL playlist to another

---

## 🚀 Features

- 🔐 **OAuth login** - official TIDAL API
- 🎧 **Playlist Name Selection** – Choose source and target playlists by name (with track count)
- ⚠️ **Detection** - Handles empty source playlists gracefully
- 📋 **Support** - Support playlists with up to over 1000 tracks
- 🧾 **CSV Logging** - Detailed log of changes with timestamps inside `logs/YYYY-MM-DD_H-M-S_log.csv`
- 🎨 **CLI** - Color-coded terminal output for better clarity
- 🔢 **Viusalisation** - Summary of added tracks after each sync
- 🔄 **Repetition** - Repeat syncs without restarting the script
- ✅ **Dry-Run Mode** - Preview which tracks would be added/removed without making changes
- 🔁 **Retry Mechanism** - Automatic retries on TIDAL API failures
- 🧹 **Mirror Mode** - Optionally remove tracks from target that are missing in source
- 📄 **HTML Report** - Generates human-readable summary of changes
---

## 📦 Installation

### Requirements

- Python 3.8+
- A valid TIDAL account (HiFi or HiFi Plus)
- `tidalapi`, `colorama`, `jinja2` Python packages

### Clone this repository:

```bash
git clone https://github.com/jannme310103/tidalsync.git
cd tidalsync
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python main.py
```
---

## ✅ Process:

1. Log in via OAuth (opens your browser)
2. Select source and target playlists by number
3. Enable dry-run and/or mirror mode (optional)
4. Review the track changes
5. Sync starts if not in dry-run mode

---

## 📁 Logs & Reports

Every sync generates:

- A CSV log in the `logs/` folder
- An HTML report with a track list (added/removed)

---

## ⚠️ Notes

- This tool modifies playlists. Use dry-run to test before applying.
- Playlist names must be unique. Duplicates might cause issues.

---

## 📝 License

MIT – free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests and feature ideas are welcome. Potential improvements:

- Multi-source playlist sync
- Scheduled jobs (e.g., via cron)
- GUI frontend
