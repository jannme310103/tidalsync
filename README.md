# 🎵 TIDAL Playlist Synchronizer

Ein kleines, praktisches Python-Tool, das zwei TIDAL-Playlists miteinander vergleicht und fehlende Songs automatisch überträgt.

## 🚀 Funktionen

- Meldet sich per OAuth einfach bei TIDAL an  
- Vergleicht zwei Playlists (z. B. von dir und deiner Freundin 😉)  
- Identifiziert Titel, die in einer Playlist fehlen  
- Fügt diese automatisch in die Ziel-Playlist ein  
- Unterstützt bis zu 10.000 Titel je Playlist durch intelligentes Offset-Handling

## 🛠️ Voraussetzungen

- Python 3.7+
- [tidalapi](https://pypi.org/project/tidalapi/)

```bash
pip install tidalapi
```

## ⚙️ Nutzung

1. Starte das Skript
2. Folge den Anweisungen im Terminal zur Anmeldung.
3. Das Tool synchronisiert automatisch die fehlenden Titel in die Ziel-Playlist.

## 📂 Aufbau

| Funktion              | Beschreibung                                                    |
|-----------------------|------------------------------------------------------------------|
| `authenticate()`      | OAuth-Anmeldung bei TIDAL                                        |
| `get_track_ids()`     | Lädt alle Songs beider Playlists                                 |
| `compare_playlists()` | Ermittelt Unterschiede zwischen beiden Playlists                 |
| `add_to_playlist()`   | Fügt fehlende Titel in die zweite Playlist ein                  |

## 📝 Hinweis

Das Tool überschreibt **keine Songs** und löscht nichts – es fügt lediglich neue Songs hinzu, die in der Ziel-Playlist fehlen.
