import tidalapi

def welcome():
    print("Welcome to my Playlist Synchronizer\n")
    authenticate()

def authenticate():
    print("Logging in:")
    session = tidalapi.Session()
    session.login_oauth_simple()

    if session.check_login():
        print("\nLogin successful\n")
        get_track_ids(session)
    else:
        print("Login failed")
        print("Please try logging in again")
        authenticate()

def get_track_ids(session):
    playlist_id_jann = "3962aa06-f821-4608-9862-ce97070e686a"
    playlist_id_nati = "c1f1620f-1809-4873-b79b-9ecdac5babd1"

    playlist_jann = session.playlist(playlist_id_jann)
    playlist_nati = session.playlist(playlist_id_nati)

    jann_count = playlist_jann.num_tracks
    nati_count = playlist_nati.num_tracks

    start_jann = max(0, jann_count - 1000)
    start_nati = max(0, nati_count - 1000)

    jann_tracks = playlist_jann.tracks(offset=start_jann, limit=1000)
    nati_tracks = playlist_nati.tracks(offset=start_nati, limit=1000)

    jann_missing = playlist_jann.tracks(offset=0, limit=start_jann)
    nati_missing = playlist_nati.tracks(offset=0, limit=start_nati)

    all_tracks_jann = jann_tracks + jann_missing
    all_tracks_nati = nati_tracks + nati_missing

    print(f"Successfully loaded {jann_count} tracks from {playlist_jann.name}")
    print(f"Successfully loaded {nati_count} tracks from {playlist_nati.name}\n")

    compare_playlists(all_tracks_jann, all_tracks_nati, playlist_nati)

def compare_playlists(tracks_jann, tracks_nati, target_playlist):
    jann_ids = [track.id for track in tracks_jann]
    nati_ids = [track.id for track in tracks_nati]

    missing_ids = [track_id for track_id in jann_ids if track_id not in nati_ids]

    missing_songs = [
        f"{track.name} - {track.artist.name}"
        for track in tracks_jann
        if track.id in missing_ids
    ]

    add_to_playlist(missing_ids, len(missing_ids), missing_songs, target_playlist)

def add_to_playlist(track_ids, count, songs, target_playlist):
    if count == 0:
        print("No tracks to add.\n")
    else:
        target_playlist.add(track_ids)
        print("Successfully added:\n")
        for song in songs:
            print(song)

if __name__ == "__main__":
    welcome()
