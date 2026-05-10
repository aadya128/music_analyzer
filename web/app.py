# web/app.py

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, redirect, request, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd


from config.settings import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIFY_SCOPE
)
from spotify.client              import fetch_recently_played, fetch_audio_features
from database.db_handler         import save_user, save_tracks, save_listening_history, get_all_tracks
from analysis.analyzer           import analyze
from analysis.color_identity     import get_color_identity
from analysis.animal_personality import get_animal_personality
from visualization.plotter       import plot_energy_curves
# Initialize database tables when app starts
from database.db_handler import save_user, save_tracks, save_listening_history, get_all_tracks, init_db
init_db()

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Strong secret key so sessions don't leak between users
app.secret_key = "music_analyzer_2026_fixed"
from datetime import timedelta
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

REDIRECT_URI = "https://h899vxh4-5000.inc1.devtunnels.ms/callback"

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        cache_path=None,
        show_dialog=True
    )


@app.route("/")
def index():
    session.clear()  # Clear any previous user's session
    return render_template("index.html")


@app.route("/login")
def login():
    # Always clear session before new login
    session.clear()
    oauth    = get_spotify_oauth()
    auth_url = oauth.get_authorize_url()
    auth_url += "&show_dialog=true"
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(url_for("index"))

    # Always clear session first
    session.clear()

    oauth      = get_spotify_oauth()
    token_info = oauth.get_access_token(code)

    # Get fresh user info directly from Spotify
    sp        = spotipy.Spotify(auth=token_info["access_token"])
    user_data = sp.current_user()

    # Print to CMD so we can verify
    print(f"\n NEW LOGIN: {user_data['display_name']} — {user_data['id']}\n")

    # Save to session
    session["token"]    = token_info["access_token"]
    session["username"] = user_data["display_name"]
    session["user_id"]  = user_data["id"]

    return render_template("loading.html", username=user_data["display_name"])


@app.route("/analyze")
def analyze_route():
    # Read directly from session
    token    = session.get("token")
    username = session.get("username")
    user_id  = session.get("user_id")

    print(f"\n ANALYZING FOR: {username} — {user_id}\n")

    if not token:
        return redirect(url_for("index"))

    sp = spotipy.Spotify(auth=token)

    user = {
        "user_id" : user_id,
        "username": username
    }

    # Fetch and save tracks
    tracks = fetch_recently_played(sp)
    tracks = fetch_audio_features(sp, tracks)

    save_user(user)
    save_tracks(tracks)
    save_listening_history(user["user_id"], tracks)

    # Load from database for this user only
    df = get_all_tracks(user["user_id"])
    df["played_at"] = pd.to_datetime(df["played_at"])
    df["played_at"] = df["played_at"] + pd.Timedelta(hours=5, minutes=30)
    df["hour"]      = df["played_at"].dt.hour
    df["weekday"]   = df["played_at"].dt.day_name()
    df["month"]     = df["played_at"].dt.month_name()

    # Run analysis
    metrics       = analyze(df)
    color_result  = get_color_identity(metrics)
    animal_result = get_animal_personality(metrics)

    # Save graph
    graphs_folder = os.path.join(os.path.dirname(__file__), "static", "graphs")
    os.makedirs(graphs_folder, exist_ok=True)
    graph_path = os.path.join(graphs_folder, f"{user_id}_energy.png")
    plot_energy_curves(df, color_result["color"], save_path=graph_path)
    graph_url = f"/static/graphs/{user_id}_energy.png?v={int(time.time())}"

    return render_template("profile.html",
        username      = username,
        color         = color_result["color"],
        color_emoji   = color_result["emoji"],
        color_meaning = color_result["meaning"],
        animal        = animal_result["animal"],
        animal_emoji  = animal_result["emoji"],
        animal_meaning= animal_result["meaning"],
        avg_energy    = round(metrics["avg_energy"], 2),
        avg_valence   = round(metrics["avg_valence"], 2),
        peak_hour     = metrics["peak_hour"],
        peak_day      = metrics["peak_day"],
        total_plays   = metrics["total_plays"],
        unique_tracks = metrics["unique_tracks"],
        unique_artists= metrics["unique_artists"],
        replay_ratio  = round(metrics["replay_ratio"], 2),
        exploration   = round(metrics["exploration_score"], 2),
        graph_url     = graph_url
    )


@app.route("/test")
def test():
    return "<h1>Flask is working!</h1>"


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000, host="0.0.0.0")