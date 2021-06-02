# oh no

from typing import Optional, Tuple, Union
from ytmusicapi import YTMusic
from pprint import pprint

def get_youtube_artist(yt: YTMusic, artist: str) -> Optional[str]:
    try:
        return "https://music.youtube.com/channel/" + yt.search(artist, "artists", 1)[0]['browseId']
    except:
        return None

def get_youtube_album(yt: YTMusic, artist: str, album: str) -> Optional[str]:
    try:
        return "https://music.youtube.com/browse/" + yt.search(album + " " + artist, "albums", 1)[0]['browseId']
    except:
        return None

def get_youtube_track(yt: YTMusic, artist: str, album: str, track: str) -> Optional[str]:
    try:
        return "https://music.youtube.com/watch?v=" + yt.search(track + album + " " + artist, "songs", 1)[0]['videoId']
    except:
        return None

def get_youtube_fallback(query: str) -> str:
    return "https://music.youtube.com/search?q=" + query

def parse_youtube_url(yt: YTMusic, url: str) -> Optional[Union[Tuple[str, str, str], Tuple[str, str], str]]:
    if "channel" in url:
        split = url.split("/channel/")[1].split("&")[0]
        return yt.get_artist(split)["name"]
    elif "playlist" in url:
        split = url.split("?list=")[1].split("&")[0]
        album = yt.get_album(yt.get_album_browse_id(split))
        return (album['artist']['name'], album['title'])
    elif "watch" in url:
        split = url.split("?v=")[1].split("&")[0]
        track = yt.get_song(split)['videoDetails']
        return (track['author'].replace(" - Topic", ""), "", track['title'])
