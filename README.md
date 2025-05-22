# TIDAL Playlist Synchronizer

A command-line tool written in Python that lets you synchronize songs from one TIDAL playlist to another

---

## 🚀 Features

- 🔐 **OAuth Login** – Official TIDAL API
- 🔁 **Two Account Login** - Synchronization between two different TIDAL accounts possible
- 🎧 **Playlist Selection by Name** – Choose source and target by name (track count shown)
- 🔄 **Sync with Optional Mirror Mode** – Keep your target playlist in sync with the source
- ✅ **Dry-Run Mode** – Preview changes before they happen
- 🧹 **Mirror Mode** – Optionally remove songs from target that are missing in source
- 🧾 **CSV Logging** – Sync actions logged in `logs/` as timestamped CSV
- 📄 **HTML Report** – Generates a readable sync report
- ♻️ **Undo Mode** – Revert the most recent real (non-dry-run) sync based on logs
- 🧠 **Auto-Dry-Run on Error** – Shows a diagnostic dry-run if syncing fails
- 💡 **Interactive Main Menu** – Select actions: Sync / Undo / Exit
- 🎨 **Colorful CLI** – Terminal output with color for better clarity
- 🔁 **Retry Mechanism** – Handles API hiccups automatically
- 🧠 **Handles large playlists** – Supports syncing with more then 1000 tracks
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
python tidalsync.py
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

CC BY-NC-SA 4.0

---

## 🤝 Contributing

Pull requests and feature ideas are welcome. Potential improvements:

- Scheduled jobs (e.g., via cron)
- GUI frontend
