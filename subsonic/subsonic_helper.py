import os
import sys
import time
import spotipy
from subsonic import Subsonic
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

baseUrl = os.getenv("SUBSONIC_API_HOST")
apiKey = os.getenv("SUBSONIC_API_TOKEN")
port = int(os.getenv("SUBSONIC_API_PORT"))
apiVersion = os.getenv("SUBSONIC_API_VERSION")
appName = os.getenv("SUBSONIC_API_APP_NAME")
serverPath = (os.getenv("SUBSONIC_API_BASE_URL_DEFAULT_VALUE")+"/rest").strip('/')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    ))
username = os.getenv("SPOTIFY_USERNAME")

subsonic = Subsonic(baseUrl, apiKey, port, apiVersion, appName, serverPath)


def create_playlist(name, songs):
    """Create a playlist in Subsonic."""
    song_ids = []
    for song in songs:
        search_results = subsonic.search(song)["searchResult2"]
        if search_results["song"]:
            song_ids.append(search_results["song"][0]['id'])

    return subsonic.createPlaylist(name=name, songIds=song_ids)


def get_playlist_songs(playlist_url):
    """Fetch all songs from a Spotify playlist."""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    playlist = sp.user_playlist_tracks(username, playlist_id)
    playlist_name = sp.playlist(playlist_id)['name']

    tracks = playlist['items']
    while playlist['next']:
        playlist = sp.next(playlist)
        tracks.extend(playlist['items'])

    songs = []
    for item in tracks:
        songs.append(item['track']['name'])

    create_playlist(playlist_name, songs)


if subsonic.ping():
    # print(subsonic.getPlaylists())
    # print(subsonic.getPlaylist("1"))
    # print(subsonic.deletePlaylist("3"))
    # print(subsonic.createPlaylist(name="test", songIds=["track-1547", "track-1543"]))
    # print(subsonic.search("Te comes por dentro"))
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            subsonic.startScan()
            get_playlist_songs(sys.argv[1])
        else:
            print("Debes proporcionar un enlace.")
else:
    print("Failed to connect to Subsonic server")
