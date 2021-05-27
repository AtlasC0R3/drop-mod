"""
Simple-to-use set of functions/commands that don't have a specific goal,
but still are great commands that every bot should have.
"""
import random

import lyricsgenius
from requests.exceptions import HTTPError

from . import ext
from .types import Search

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
    engines = (lambda: ext.duckducksearch(to_search), lambda: ext.qwant_search(to_search))
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
    GENIUS = lyricsgenius.Genius(token, verbose=False, remove_section_headers=True,
                                 skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])


# noinspection PyUnresolvedReferences
def get_lyrics(artist, title):
    """
    Obtains lyrics for a song using lyricsgenius.
    NOTE: requires init_genius() to have been used! or... how do i explain things.
    """
    if GENIUS:
        try:
            song = GENIUS.search_song(title=title, artist=artist)
            # Fun fact: that's how I discovered that GHOST by Camellia
            # (the song every beat saber player hates the most) has lyrics, and that they lead to
            # youtu.be/DkrzV5GIQXQ! how the actual fuck did i get here
            # I am now in shock and terrified. If anyone's into ARGs and reading this,
            # well here you go. It appears to be in Japanese though.
        except HTTPError:
            song = None
            print("FIXME: Genius API token probably not working")
        if song:
            return song
    # no genius, woopsies
    return None


# noinspection PyUnresolvedReferences
def get_artist(artist):
    """
    Obtains an artist's most popular songs using lyricsgenius.
    NOTE: requires init_genius() to have been used!
    """
    if GENIUS:
        try:
            songs = GENIUS.search_artist(artist, max_songs=5, sort='popularity').songs
        except HTTPError:
            songs = None
            print("FIXME: Genius API token probably not working")
        except AttributeError:
            songs = None
        if songs:
            lyrics = []
            for song in songs:
                lyric = song.lyrics.split('\n')
                lyrics.append([song.title, lyric[:5], song.url])
            artist_name = songs[0].artist
            return ['Genius', [artist_name, lyrics]]
    return ['nothing', []]
