"""
Simple-to-use set of functions/commands that don't have a specific goal,
but still are great commands that every bot should have.
"""
import random

from . import ext
from .types import Search, Lyrics
import aiohttp

GENIUS = None


def owofy(string: str):
    """
    Applies an "owospeak" filter over a passed string. God I hate myself.
    """
    for old, new in ext.owofy_letters.items():
        string = string.replace(old, new)
    while '!' in string:
        string = string.replace('!', random.choice(ext.owofy_exclamations), 1)
    return string


def search(to_search: str):
    """
    Does a DuckDuckPy query. NOTE: does not return search results, only returns queries.
    I don't know how I can really explain this.
    """
    engines = [lambda: ext.duckducksearch(to_search), lambda: ext.qwant_search(to_search)]
    result = None
    for engine in engines:
        result = engine()
        if result:
            break
    if not result:
        return None
    return Search().from_dict(result) if isinstance(result, dict) else result


def init_genius(token):
    """
    Initializes Genius' lyrics command (such as get_lyrics() or get_artist()).
    """
    global GENIUS
    GENIUS = token


async def lyrics(query: str):
    """
    Does a Genius search.
    """
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {GENIUS}'}) as session:
        async with session.get(f"https://api.genius.com/search?q={query}") as r:
            if r.status == 400:
                print("Genius API token probably not working")
            results = (await r.json())['response']['hits']
            try:
                song_result = results[0]['result']
            except IndexError:
                return None
    song_path = f"https://genius.com{song_result['path']}"

    song = Lyrics()

    song.lyrics = await ext.genius_get_lyrics(song_path)
    song.title = song_result["title"]
    song.artist = song_result["primary_artist"]["name"]
    song.url = song_path
    song.thumbnail = song_result["song_art_image_url"]
    song.set_source('Genius', "http://images.genius.com/8ed669cadd956443e29c70361ec4f372"
                              ".1000x1000x1.png")
    return song
