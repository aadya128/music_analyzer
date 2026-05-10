import os
from dotenv import load_dotenv

# This line tells the program to go look at your secret .env diary
load_dotenv()

# --- Spotify Credentials ---
SPOTIPY_CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI  = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIFY_SCOPE = "user-read-recently-played"
# --- MySQL Credentials ---
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME     = os.getenv("DB_NAME", "music_analyzer")

# --- Analysis Constants ---
TRACKS_TO_FETCH   = 50
ENERGY_THRESHOLD  = 0.5
VALENCE_THRESHOLD = 0.5