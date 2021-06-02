from spotipy import SpotifyClientCredentials, Spotify
from typing import AnyStr, Optional, Tuple, Union
from secret_list import *

prefs = {}

# store dict prefs and their order

# make api requests to spotify, youtube music, apple music, rym, etc

# conversion service from spotify, etc sharing links

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def spotify_url_to_uri(url:str) -> Optional[str]:
    try:
        return url.split("?")[0].split("/")[-1]
    except:
        return None

def parse_spotify_track(uri: str) -> Optional[Tuple[str, str, str]]:
    try:
        track = sp.track(track_id=uri)
        return (track['name'], track['album']['name'], track['artists'][0]['name'])
    except:
        return None

def parse_spotify_album(uri: str) -> Optional[Tuple[str, str]]:
    try:
        album = sp.album(album_id=uri)
        return (album['name'], album['artists'][0]['name'])
    except:
        return None

def parse_spotify_artist(uri: str) -> Optional[str]:
    try:
        artist = sp.artist(artist_id=uri)
        return artist['name']
    except:
        return None

def parse_unilink(unilink: str) -> Optional[Union[str, Tuple[str, str], Tuple[str, str, str]]]:
    try:
        params = map(lambda param: param.split("="), unilink.split("?")[1].split("&"))
        dictionary = {}
        for param in params:
            dictionary[param[0]] = param[1]
        if len(dictionary) == 0:
            return None
        elif len(dictionary) == 1:
            return dictionary['artist']
        elif len(dictionary) == 2:
            return (dictionary['album'], dictionary['artist'])
        else:
            return (dictionary['track'], dictionary['album'], dictionary['artist'])
    except:
        return None

def generate_unilink(artist_name: str, album_name: Optional[str] = None, track_name: Optional[str] = None) -> str:
    url = f"https://unilink.nove.dev?artist={artist_name}"
    if album_name:
        url += f"&album={album_name}"
        if track_name:
            url += f"&track={track_name}"
    return url

def get_spotify_track(track_name: str, album_name: str, artist_name: str) -> Optional[str]:
    query = "track:" + " ".join([track_name, album_name, artist_name])
    try:
        tracks = sp.search(q=query, limit=10, type="track")['tracks']['items']
        mapped_tracks = map(lambda item: item["external_urls"]["spotify"], tracks)
        return mapped_tracks.__next__()
    except:
        return None
