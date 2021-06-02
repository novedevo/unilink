from spotipy import SpotifyClientCredentials, Spotify
from typing import Optional, Tuple, Union
from secret_list import *
from spotify import *


prefs = {}

# store dict prefs and their order

# make api requests to spotify, youtube music, apple music, rym, etc

# conversion service from spotify, etc sharing links

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

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