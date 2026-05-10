import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from spotify.client import create_spotify_client, get_current_user, fetch_recently_played

def main():
    print("=" * 50)
    print("   Spotify Premium Connection Test")
    print("=" * 50)

    try:
        client = create_spotify_client()
        user = get_current_user(client)
        display_name = user.get('display_name', 'Music Explorer')
        
        print(f"✅ Successfully logged in!")
        print(f"👤 User: {display_name}")
        print("-" * 50)

        print("🎵 Fetching your recently played tracks...")
        tracks = fetch_recently_played(client)

        if not tracks:
            print("❌ No tracks found. Go listen to some music on Spotify first!")
            return

        print(f"✅ Found {len(tracks)} tracks. Here are the top 5:")
        print("-" * 50)
        
        for i in range(min(5, len(tracks))):
            track = tracks[i]['track']
            name = track['name']
            artist = track['artists'][0]['name']
            print(f"{i+1}. {name} by {artist}")

        print("-" * 50)

    except Exception as e:
        print(f"❌ Oops! Something went wrong:")
        print(f"   {e}")

if __name__ == "__main__":
    main()