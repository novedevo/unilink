from typing import Optional

import requests as rq

def is_valid_rym_link(url: str) -> bool:
    return rq.get(url).status_code == 200

def naive_parse(artist:str, album: Optional[str] = None) -> str:
    artist = artist.lower().replace(" ", "-")
    url = "https://rateyourmusic.com/"
    if album:
        album = album.lower().replace(" ", "-")
        url += f"release/album/{artist}/{album}"
    else:
        url += f"artist/{artist}"
    return url

def fallback_url(artist:str, album: Optional[str] = None) -> str:
    artist = artist.lower().replace(" ", "-")
    url = f"https://rateyourmusic.com/search?searchterm={artist}"
    if album:
        album = album.lower().replace(" ", "-")
        url += " album&searchtype=album"
    else:
        url += "&searchtype=artist"
    return url