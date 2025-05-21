import tidalapi
import datetime
import os
import time
from colorama import init, Fore
from typing import List
from jinja2 import Template

init(autoreset=True)

def authenticate_custom(label=""):
    print(Fore.CYAN + f"\nLogin for {label} Playlist:")
    session = tidalapi.Session()
    session.login_oauth_simple()
    if session.check_login():
        print(Fore.GREEN + f"{label} login successful!\n")
        return session
    else:
        raise Exception(f"{label} login failed.")

def run_sync(default_session):
    while True:
        print("\nWhat do you want to do?")
        print("1. Sync playlists")
        print("2. Undo last sync")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            use_dual_login = input("Use two different TIDAL accounts? (y/n): ").strip().lower() == 'y'
            source_session = authenticate_custom("SOURCE") if use_dual_login else default_session
            target_session = authenticate_custom("TARGET") if use_dual_login else default_session

            source_playlist = select_playlist_by_name(source_session, "SOURCE")
            target_playlist = select_playlist_by_name(target_session, "TARGET")

            dry_run = input("Enable Dry-Run mode? (y/n): ").strip().lower() == 'y'
            mirror_mode = input("Enable Mirror Mode (remove missing songs)? (y/n): ").strip().lower() == 'y'

            try:
                sync_playlists(source_session, target_session, source_playlist, target_playlist, dry_run, mirror_mode)
            except Exception as e:
                print(Fore.RED + f"\nError during sync: {e}")
                print(Fore.YELLOW + "Running Auto-Dry-Run for diagnostics...\n")
                sync_playlists(source_session, target_session, source_playlist, target_playlist, dry_run=True, mirror_mode=mirror_mode)

        elif choice == '2':
            try:
                undo_last_sync(default_session)
            except Exception as e:
                print(Fore.RED + f"Undo failed: {e}")

        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2 or 3.")

def select_playlist_by_name(session, label):
    user_playlists = retry_request(lambda: session.user.playlists())
    print(f"\nAvailable Playlists for {label}:")
    for idx, pl in enumerate(user_playlists):
        print(f"{idx + 1}. {pl.name} ({pl.num_tracks} Tracks)")
    choice = int(input(f"\nSelect {label} playlist by number: ")) - 1
    return user_playlists[choice]

def retry_request(func, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            print(Fore.RED + f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("Maximum retries reached.")

def sync_playlists(source_session, target_session, source_playlist, target_playlist, dry_run=False, mirror_mode=False):
    source_tracks = get_all_tracks(source_playlist)
    target_tracks = get_all_tracks(target_playlist)

    print(f"\nLoaded {len(source_tracks)} tracks from source: {source_playlist.name}")
    print(f"Loaded {len(target_tracks)} tracks from target: {target_playlist.name}")

    source_ids = [t.id for t in source_tracks]
    target_ids = [t.id for t in target_tracks]

    to_add = [t for t in source_tracks if t.id not in target_ids]
    to_remove = [t for t in target_tracks if t.id not in source_ids] if mirror_mode else []

    print(Fore.BLUE + f"\nTracks to ADD: {len(to_add)}")
    print(Fore.MAGENTA + f"Tracks to REMOVE: {len(to_remove)}" if mirror_mode else "")

    if to_add:
        print(Fore.GREEN + "\nTracks to be added:")
        for t in to_add:
            print(f"- {t.name} - {t.artist.name}")

    if not dry_run:
        if to_add:
            retry_request(lambda: target_playlist.add([t.id for t in to_add]))
        if to_remove:
            retry_request(lambda: target_playlist.remove([t.id for t in to_remove]))

    log_sync(target_playlist.name, to_add, to_remove, dry_run)
    create_report(target_playlist.name, to_add, to_remove, dry_run)

def get_all_tracks(playlist) -> List:
    tracks = []
    offset = 0
    limit = 100
    while True:
        chunk = playlist.tracks(offset=offset, limit=limit)
        if not chunk:
            break
        tracks.extend(chunk)
        offset += limit
    return tracks

def log_sync(playlist_name, added, removed, dry_run):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"logs/{timestamp}_log.csv"
    with open(filename, "w", encoding="utf-8") as log:
        log.write("Timestamp,Playlist,Track,Artist,Action,DryRun\n")
        for track in added:
            log.write(f"{timestamp},{playlist_name},{track.name},{track.artist.name},added,{dry_run}\n")
        for track in removed:
            log.write(f"{timestamp},{playlist_name},{track.name},{track.artist.name},removed,{dry_run}\n")

def create_report(playlist_name, added, removed, dry_run):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"logs/{timestamp}_report.html"
    html_template = """<html><head><title>Sync Report</title></head><body>
    <h2>Playlist Sync Report - {{ playlist_name }}</h2>
    <p><strong>Dry Run:</strong> {{ dry_run }}</p>
    <h3>Added Tracks ({{ added | length }})</h3>
    <ul>{% for t in added %}<li>{{ t.name }} - {{ t.artist.name }}</li>{% endfor %}</ul>
    <h3>Removed Tracks ({{ removed | length }})</h3>
    <ul>{% for t in removed %}<li>{{ t.name }} - {{ t.artist.name }}</li>{% endfor %}</ul>
    </body></html>"""
    template = Template(html_template)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(template.render(
            playlist_name=playlist_name,
            added=added,
            removed=removed,
            dry_run=dry_run
        ))

def undo_last_sync(session):
    from csv import DictReader

    print(Fore.YELLOW + "\nAttempting to undo last sync...")

    log_dir = "logs"
    files = [f for f in os.listdir(log_dir) if f.endswith("_log.csv")]
    if not files:
        raise Exception("No log files found.")

    latest_log = max(files, key=lambda f: os.path.getmtime(os.path.join(log_dir, f)))
    path = os.path.join(log_dir, latest_log)

    with open(path, "r", encoding="utf-8") as file:
        reader = list(DictReader(file))
        if not reader:
            raise Exception("Log file is empty.")
        if reader[0]["DryRun"].lower() == "true":
            raise Exception("Last sync was a dry-run. Nothing to undo.")

        playlist_name = reader[0]["Playlist"]
        print(f"Restoring playlist: {playlist_name} from log: {latest_log}")

        user_playlists = retry_request(lambda: session.user.playlists())
        target_playlist = next((pl for pl in user_playlists if pl.name == playlist_name), None)
        if not target_playlist:
            raise Exception(f"Playlist '{playlist_name}' not found.")

        to_remove = [row["Track"] for row in reader if row["Action"] == "added"]
        to_add = [row["Track"] for row in reader if row["Action"] == "removed"]

        all_tracks = []
        for pl in user_playlists:
            all_tracks.extend(get_all_tracks(pl))

        name_to_track = {f"{t.name} - {t.artist.name}": t for t in all_tracks}
        remove_ids = [name_to_track[t].id for t in to_remove if t in name_to_track]
        add_ids = [name_to_track[t].id for t in to_add if t in name_to_track]

        if remove_ids:
            print(Fore.MAGENTA + f"Removing {len(remove_ids)} previously added tracks...")
            retry_request(lambda: target_playlist.remove(remove_ids))

        if add_ids:
            print(Fore.GREEN + f"Restoring {len(add_ids)} previously removed tracks...")
            retry_request(lambda: target_playlist.add(add_ids))

        print(Fore.GREEN + "Undo completed.\n")

if __name__ == "__main__":
    print(Fore.CYAN + "\n=== TIDAL Playlist Synchronizer v1.3.0 ===\n")
    run_sync(None)