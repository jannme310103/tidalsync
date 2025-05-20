import tidalapi
import datetime
import os
import re
import time
from colorama import init, Fore, Style
from typing import List
from jinja2 import Template

init(autoreset=True)

def welcome():
    print(Fore.CYAN + "\n=== TIDAL Playlist Synchronizer v1.2.0 ===\n")
    authenticate()

def authenticate():
    print("Logging in...")
    session = tidalapi.Session()
    session.login_oauth_simple()
    if session.check_login():
        print(Fore.GREEN + "Login successful!\n")
        while True:
            run_sync(session)
            choice = input("\nDo you want to sync another playlist? (y/n): ").lower()
            if choice != 'y':
                print("Exiting...")
                break
    else:
        print(Fore.RED + "Login failed. Please try again.\n")
        authenticate()

def run_sync(session):
    source_playlist = select_playlist_by_name(session, "SOURCE")
    target_playlist = select_playlist_by_name(session, "TARGET")

    dry_run = input("Enable Dry-Run mode? (y/n): ").strip().lower() == 'y'
    mirror_mode = input("Enable Mirror Mode (remove missing songs)? (y/n): ").strip().lower() == 'y'

    sync_playlists(session, source_playlist, target_playlist, dry_run, mirror_mode)

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

def sync_playlists(session, source_playlist, target_playlist, dry_run=False, mirror_mode=False):
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
        print(Fore.GREEN + "\nFolgende Songs werden hinzugefügt:")
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

if __name__ == "__main__":
    welcome()
