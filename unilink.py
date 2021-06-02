from spotipy import SpotifyClientCredentials, Spotify
from typing import AnyStr, Optional, Tuple, Union
from secret_list import *
from spotify import *


prefs = {}

# store dict prefs and their order

# make api requests to spotify, youtube music, apple music, rym, etc

# conversion service from spotify, etc sharing links

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
