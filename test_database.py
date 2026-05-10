# test_database.py
# Run this to test that data saves correctly to MySQL

from spotify.client import (
    create_spotify_client,
    get_current_user,
    fetch_recently_played,
    fetch_audio_features
)
from database.db_handler import (
    save_user,
    save_tracks,
    save_listening_history
)

def main():
    print("=" * 50)
    print("   Stage 4 — Saving Data to MySQL")
    print("=" * 50)

    # Step 1 — Connect to Spotify
    client = create_spotify_client()

    # Step 2 — Get your profile and save to users table
    user = get_current_user(client)
    save_user(user)

    # Step 3 — Fetch your tracks
    tracks = fetch_recently_played(client)
    tracks = fetch_audio_features(client, tracks)

    # Step 4 — Save tracks and history to MySQL
    save_tracks(tracks)
    save_listening_history(user["user_id"], tracks)

    print("=" * 50)
    print(" All data saved! Go check MySQL Workbench.")
    print("=" * 50)

if __name__ == "__main__":
    main()