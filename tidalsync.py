import tidalapi
import datetime


def welcome():
    print("\n=== TIDAL Playlist Synchronizer ===\n")
    authenticate()


def authenticate():
    print("Logging in...")
    session = tidalapi.Session()
    session.login_oauth_simple()

    if session.check_login():
        print("Login successful!\n")
        while True:
            prompt_playlist_ids(session)
            choice = input("\nDo you want to sync another playlist? (y/n): ").lower()
            if choice != 'y':
                print("Exiting...")
                break
    else:
        print("Login failed. Please try again.\n")
        authenticate()


def prompt_playlist_ids(session):
    source_playlist_id = input("Enter the SOURCE playlist ID: ").strip()
    target_playlist_id = input("Enter the TARGET playlist ID: ").strip()
    sync_playlists(session, source_playlist_id, target_playlist_id)


def sync_playlists(session, source_id, target_id):
    try:
        source_playlist = session.playlist(source_id)
        target_playlist = session.playlist(target_id)
    except Exception as e:
        print(f"Error loading playlists: {e}")
        return

    source_count = source_playlist.num_tracks
    target_count = target_playlist.num_tracks

    source_tracks = get_all_tracks(source_playlist, source_count)
    target_tracks = get_all_tracks(target_playlist, target_count)

    print(f"Loaded {source_count} tracks from source playlist: {source_playlist.name}")
    print(f"Loaded {target_count} tracks from target playlist: {target_playlist.name}\n")

    compare_playlists(source_tracks, target_tracks, target_playlist)


def get_all_tracks(playlist, total_count):
    recent = playlist.tracks(offset=max(0, total_count - 1000), limit=1000)
    older = playlist.tracks(offset=0, limit=max(0, total_count - 1000))
    return recent + older


def compare_playlists(source_tracks, target_tracks, target_playlist):
    source_ids = [track.id for track in source_tracks]
    target_ids = [track.id for track in target_tracks]

    missing_ids = [track_id for track_id in source_ids if track_id not in target_ids]

    missing_songs = [
        f"{track.name} - {track.artist.name}"
        for track in source_tracks
        if track.id in missing_ids
    ]

    add_to_playlist(missing_ids, missing_songs, target_playlist)


def add_to_playlist(track_ids, songs, target_playlist):
    if not track_ids:
        print("\nNo new tracks to add.\n")
    else:
        target_playlist.add(track_ids)
        print("\nSuccessfully added the following tracks:\n")
        for song in songs:
            print(song)
        log_sync(target_playlist.name, songs)


def log_sync(playlist_name, songs):
    with open("sync_log.txt", "a", encoding="utf-8") as log:
        log.write(f"\n[{datetime.datetime.now()}] Synced to playlist: {playlist_name}\n")
        for song in songs:
            log.write(f"- {song}\n")


if __name__ == "__main__":
    welcome()
