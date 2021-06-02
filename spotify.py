from spotipy import Spotify
from typing import Optional, Tuple, Union

def spotify_url_to_uri(sp: Spotify, url:str) -> Optional[str]:
    try:
        return url.split("?")[0].split("/")[-1]
    except:
        return None

def parse_spotify_track(sp: Spotify, uri: str) -> Optional[Tuple[str, str, str]]:
    try:
        track = sp.track(track_id=uri)
        return (track['name'], track['album']['name'], track['artists'][0]['name'])
    except:
        return None

def parse_spotify_album(sp: Spotify, uri: str) -> Optional[Tuple[str, str]]:
    try:
        album = sp.album(album_id=uri)
        return (album['name'], album['artists'][0]['name'])
    except:
        return None

def parse_spotify_artist(sp: Spotify, uri: str) -> Optional[str]:
    try:
        artist = sp.artist(artist_id=uri)
        return artist['name']
    except:
        return None

def get_spotify_track(sp: Spotify, track_name: str, album_name: str, artist_name: str) -> Optional[str]:
    query = " ".join([track_name, album_name, artist_name])
    try:
        tracks = sp.search(q=query, limit=10, type="track")['tracks']['items']
        mapped_tracks = map(lambda item: item["external_urls"]["spotify"], tracks)
        return mapped_tracks.__next__()
    except:
        return None

def get_spotify_album(sp: Spotify, album_name: str, artist_name: str) -> Optional[str]:
    query = " ".join([album_name, artist_name])
    try:
        albums = sp.search(q=query, limit=10, type="album")['albums']['items']
        mapped_albums = map(lambda item: item["external_urls"]["spotify"], albums)
        return mapped_albums.__next__()
    except:
        return None

def get_spotify_artist(sp: Spotify, artist_name: str) -> Optional[str]:
    query = artist_name
    try:
        artists = sp.search(q=query, limit=10, type="artist")['artists']['items']
        mapped_artists = map(lambda item: item["external_urls"]["spotify"], artists)
        return mapped_artists.__next__()
    except:
        return None
