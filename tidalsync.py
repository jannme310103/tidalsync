import tidalapi


def welcome():
    print("Willkommen zu meinem Playlist Synchronisierer", "\n")
    authenticate()


def authenticate():
    print("Anmeldung:")
    session = tidalapi.Session()
    session.login_oauth_simple()

    if session.check_login():
        print("")
        print("Anmeldung erfolgreich", "\n")
        get_track_ids(session)
    else:
        print("Anmeldung fehlgeschlagen")
        print("Bitte erneut einloggen")
        authenticate()


def get_track_ids(session):
    playlist_id_jann = "3962aa06-f821-4608-9862-ce97070e686a"
    playlist_id_nati = "c1f1620f-1809-4873-b79b-9ecdac5babd1"

    playlist_jann = session.playlist(playlist_id_jann)
    playlist_nati = session.playlist(playlist_id_nati)

    playlist_jann_count = playlist_jann.num_tracks
    playlist_nati_count = playlist_nati.num_tracks

    start_index_jann = max(0, playlist_jann_count - 1000)
    start_index_nati = max(0, playlist_nati_count - 1000)

    first_1000_tracks_jann = playlist_jann.tracks(offset=start_index_jann, limit=1000)
    first_1000_tracks_nati = playlist_nati.tracks(offset=start_index_nati, limit=1000)

    missing_tracks_jann = playlist_jann.tracks(offset=0, limit=start_index_jann)
    missing_tracks_nati = playlist_nati.tracks(offset=0, limit=start_index_nati)

    all_tracks_jann = first_1000_tracks_jann + missing_tracks_jann
    all_tracks_nati = first_1000_tracks_nati + missing_tracks_nati

    print(
        "Erfolgreich geladene Titel aus ",
        playlist_jann.name,
        ": ",
        str(playlist_jann_count),
    )
    print(
        "Erfolgreich geladene Titel aus ",
        playlist_nati.name,
        ": ",
        str(playlist_nati_count),
        "\n",
        "\n",
    )

    compare_playlists(all_tracks_jann, all_tracks_nati, playlist_nati)


def compare_playlists(all_tracks_jann, all_tracks_nati, playlist_nati):
    tracks_jann_ids = [track.id for track in all_tracks_jann]
    tracks_nati_ids = [track.id for track in all_tracks_nati]

    differend_ids = [
        track_id for track_id in tracks_jann_ids if track_id not in tracks_nati_ids
    ]

    differend_songs = [
        (x.name + " - " + x.artist.name)
        for x in all_tracks_jann
        if x.id in differend_ids
    ]

    add_to_playlist(differend_ids, len(differend_ids), differend_songs, playlist_nati)


def add_to_playlist(differend_ids, count_ids, differend_songs, playlist_nati):
    if count_ids == 0:
        print("Keine Titel zum Hinzufügen", "\n")
    else:
        playlist_nati.add(differend_ids)
        print("Erfolgreich hinzugefügt:", "\n")
        for differend_song in differend_songs:
            print(differend_song)


if __name__ == "__main__":
    welcome()
