import tidalapi

def welcome():
    print("Welcome to the Playlist Synchronizer\n")
    authenticate()

def authenticate():
    print("Logging in:")
    session = tidalapi.Session()
    session.login_oauth_simple()

    if session.check_login():
        print("\nLogin successful\n")
        prompt_playlist_ids(session)
    else:
        print("Login failed")
        print("Please try logging in again\n")
        authenticate()

def prompt_playlist_ids(session):
    source_playlist_id = input("Enter the source playlist ID: ").strip()
    target_playlist_id = input("Enter the target playlist ID: ").strip()

    sync_playlists(session, source_playlist_id, target_playlist_id)

def sync_playlists(session, source_id, target_id):
    source_playlist = session.playlist(source_id)
    target_playlist = session.playlist(target_id)

    source_count = source_playlist.num_tracks
    target_count = target_playlist.num_tracks

    source_start = max(0, source_count - 1000)
    target_start = max(0, target_count - 1000)

    source_tracks = source_playlist.tracks(offset=source_start, limit=1000)
    target_tracks = target_playlist.tracks(offset=target_start, limit=1000)

    source_missing = source_playlist.tracks(offset=0, limit=source_start)
    target_missing = target_playlist.tracks(offset=0, limit=target_start)

    all_source_tracks = source_tracks + source_missing
    all_target_tracks = target_tracks + target_missing

    print(f"Loaded {source_count} tracks from source playlist: {source_playlist.name}")
    print(f"Loaded {target_count} tracks from target playlist: {target_playlist.name}\n")

    compare_playlists(all_source_tracks, all_target_tracks, target_playlist)

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
        print("No new tracks to add.\n")
    else:
        target_playlist.add(track_ids)
        print("Successfully added the following tracks:\n")
        for song in songs:
            print(song)

if __name__ == "__main__":
    welcome()
