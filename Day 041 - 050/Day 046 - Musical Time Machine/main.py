# --- Imports --- #
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
from generic_functions import cls
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

# --- Global Variables/Objects --- #
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

# --- Functions --- #
def authenticate_spotify() -> spotipy.Spotify:
    """Authentication flow to sign in to spotify using spotipy"""
    spotify_auth=SpotifyOAuth(
        client_id= os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret= os.environ.get("SPOTIPY_CLIENT_SECRET"),
        redirect_uri= "http://example.com",
        scope= "playlist-modify-private",
        show_dialog= True,
        username=os.environ.get("SPOTIPY_USERNAME")
    )
    spotify = spotipy.Spotify(auth_manager= spotify_auth)
    return spotify

def get_date(text:str) -> datetime:
    """Check input and return a date tuple[str] with format (year,month,day)."""
    while True:
        try:
            date = input(text)
            date = datetime.strptime(date,"%Y-%m-%d")
            today = datetime.today()
            if date > today:
                raise TypeError
            return date
        except ValueError:
            print("Wrong input. Please try again.")
        except TypeError:
            print("You cannot type a future date. Please try again.")

def get_songs(date:datetime):
    """Return a list of songs from a given day."""
    request = requests.get(f"{BILLBOARD_URL}{date.strftime('%Y-%m-%d')}/")
    request.raise_for_status()
    website = BeautifulSoup(request.text,"html.parser")
    def get_text(song):
        title = song.getText()
        return title.strip()
    song_list = website.select("li ul li h3")
    song_list = [get_text(song) for song in song_list]
    
    author_list = website.select("div ul li ul li .a-truncate-ellipsis-2line")
    author_list = [get_text(author) for author in author_list]
    
    songs = []
    for i in range(len(song_list)):
        songs.append({
            "track":song_list[i],
            "author":author_list[i]
        })
    return songs
    
# --- Program --- #
cls()
date = get_date("Which date do you want to travel to? (YYYY-MM-DD)\n")
songs = get_songs(date)
spotify = authenticate_spotify()
# Search URI
tracks_uri = []
for i in range(len(songs)):
    try:
        track = spotify.search(
            q=f"{songs[i]['track']} {songs[i]['author']}",
            limit=1,
            type='track')
        uri = track['tracks']['items'][0]['uri']
        tracks_uri.append(uri)
    except:
        pass

# Create the playlist
user_id = spotify.current_user()["id"]
playlist=spotify.user_playlist_create(
    user=user_id,
    name=f"Top 100 songs on {date.strftime('%Y-%m-%d')}",
    public=False,
)

# Add songs to playlist
spotify.user_playlist_add_tracks(
    user=user_id,
    playlist_id=playlist['id'],
    tracks=tracks_uri,
)