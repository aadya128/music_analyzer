 
# main.py
# ─────────────────────────────────────────────────────
# Temporal Music Identity & Listening Pattern Analyzer
# Final Script — runs everything from start to finish
# ─────────────────────────────────────────────────────

import pandas as pd

from spotify.client              import create_spotify_client, get_current_user
from spotify.client              import fetch_recently_played, fetch_audio_features
from database.db_handler         import save_user, save_tracks, save_listening_history
from database.db_handler         import get_all_tracks, get_user
from analysis.analyzer           import analyze
from analysis.color_identity     import get_color_identity
from analysis.animal_personality import get_animal_personality
from visualization.plotter       import plot_energy_curves


def print_profile(user, color_result, animal_result, metrics):
    """Prints the final Music Identity Profile in a clean format."""

    width = 55
    print("\n")
    print("═" * width)
    print("   🎵  MUSIC IDENTITY PROFILE")
    print("═" * width)
    print(f"   Listener : {user['username']}")
    print(f"   Tracks   : {metrics['total_plays']} plays · {metrics['unique_tracks']} unique songs")
    print(f"   Artists  : {metrics['unique_artists']} different artists")
    print("─" * width)

    print(f"\n   {color_result['emoji']}  COLOR IDENTITY  →  {color_result['color'].upper()}")
    print(f"   {color_result['meaning']}")

    print(f"\n   {animal_result['emoji']}  ANIMAL PERSONALITY  →  {animal_result['animal'].upper()}")

    # Print animal meaning wrapped neatly
    words = animal_result["meaning"].split()
    line  = "   "
    for word in words:
        if len(line) + len(word) > 53:
            print(line)
            line = "   " + word + " "
        else:
            line += word + " "
    print(line)

    print(f"\n   ⚡  ENERGY PROFILE")
    print(f"   Average Energy  : {metrics['avg_energy']:.3f}  ({'High' if metrics['avg_energy'] >= 0.5 else 'Low'})")
    print(f"   Average Valence : {metrics['avg_valence']:.3f}  ({'Happy' if metrics['avg_valence'] >= 0.5 else 'Moody'})")
    print(f"   Peak Hour       : {metrics['peak_hour']}:00 IST")
    print(f"   Peak Day        : {metrics['peak_day']}")

    print(f"\n   📊  LISTENING ENERGY CURVE")
    print(f"   Replay Ratio    : {metrics['replay_ratio']:.2f}  (you repeat songs quite a bit)")
    print(f"   Exploration     : {metrics['exploration_score']:.2f}  (you explore lots of artists)")

    print("\n" + "═" * width)
    print("   Graphs saved to → energy_curves.png")
    print("═" * width)
    print()


def main():
    print("\n" + "═" * 55)
    print("   🎵  Temporal Music Identity Analyzer")
    print("   Starting full analysis...")
    print("═" * 55)

    # ── Step 1: Connect to Spotify ───────────────────────────
    print("\n [1/6] Connecting to Spotify...")
    client = create_spotify_client()
    user   = get_current_user(client)
    print(f"       Logged in as: {user['username']}")

    # ── Step 2: Fetch tracks ─────────────────────────────────
    print("\n [2/6] Fetching your recently played tracks...")
    tracks = fetch_recently_played(client)
    tracks = fetch_audio_features(client, tracks)

    # ── Step 3: Save to MySQL ────────────────────────────────
    print("\n [3/6] Saving data to MySQL...")
    save_user(user)
    save_tracks(tracks)
    save_listening_history(user["user_id"], tracks)

    # ── Step 4: Load from MySQL into pandas ──────────────────
    print("\n [4/6] Loading data from MySQL...")
    df = get_all_tracks()

    df["played_at"] = pd.to_datetime(df["played_at"])
    df["played_at"] = df["played_at"] + pd.Timedelta(hours=5, minutes=30)
    df["hour"]      = df["played_at"].dt.hour
    df["weekday"]   = df["played_at"].dt.day_name()
    df["month"]     = df["played_at"].dt.month_name()

    # ── Step 5: Analyze ──────────────────────────────────────
    print("\n [5/6] Analyzing your listening patterns...")
    metrics       = analyze(df)
    color_result  = get_color_identity(metrics)
    animal_result = get_animal_personality(metrics)

    # ── Step 6: Visualize ────────────────────────────────────
    print("\n [6/6] Generating energy curve graphs...")
    plot_energy_curves(df, color_result["color"])

    # ── Final Output ─────────────────────────────────────────
    print_profile(user, color_result, animal_result, metrics)


if __name__ == "__main__":
    main()