 
# analysis/analyzer.py
# Stage 6 — Analyze listening patterns and compute key metrics

def analyze(df):
    """
    Takes the pandas DataFrame and computes all the metrics
    we need for Color Identity and Animal Personality.
    """
    print("\n" + "=" * 55)
    print("   Stage 6 — Analyzing Your Listening Patterns")
    print("=" * 55)

    # ── Basic Audio Metrics ──────────────────────────────────
    avg_energy  = df["energy"].mean()
    avg_valence = df["valence"].mean()

    # ── Replay Ratio ─────────────────────────────────────────
    # How repetitive are you?
    # 100 plays / 17 unique tracks = 5.88 plays per song on average
    # We normalize it to a 0.0 - 1.0 scale
    total_plays   = len(df)
    unique_tracks = df["track_id"].nunique()
    raw_ratio     = total_plays / unique_tracks  # e.g. 5.88
    # Cap at 10 plays per song maximum for the scale
    replay_ratio  = min(raw_ratio / 10.0, 1.0)

    # ── Exploration Score ────────────────────────────────────
    # How many different artists do you listen to?
    # More artists = more exploratory listener
    unique_artists   = df["artist"].nunique()
    # Normalize: 10+ artists = fully exploratory
    exploration_score = min(unique_artists / 10.0, 1.0)

    # ── Peak Listening Hour ──────────────────────────────────
    # Which hour of the day do you listen to most music?
    peak_hour = df["hour"].mode()[0]  # mode = most common value

    # ── Peak Listening Day ───────────────────────────────────
    peak_day = df["weekday"].mode()[0]

    # ── Print Results ────────────────────────────────────────
    print(f"\n  Audio Profile:")
    print(f"   Average Energy      : {avg_energy:.3f}  (0=calm, 1=intense)")
    print(f"   Average Valence     : {avg_valence:.3f}  (0=moody, 1=happy)")

    print(f"\n  Listening Behavior:")
    print(f"   Total Plays         : {total_plays}")
    print(f"   Unique Tracks       : {unique_tracks}")
    print(f"   Plays Per Track     : {raw_ratio:.1f}")
    print(f"   Replay Ratio        : {replay_ratio:.2f}  (0=explorer, 1=repeater)")
    print(f"   Unique Artists      : {unique_artists}")
    print(f"   Exploration Score   : {exploration_score:.2f}  (0=focused, 1=exploratory)")

    print(f"\n  Time Patterns:")
    print(f"   Peak Listening Hour : {peak_hour}:00")
    print(f"   Peak Listening Day  : {peak_day}")

    print("\n" + "=" * 55)

    # Return all metrics as a dictionary for use in later stages
    return {
        "avg_energy"        : avg_energy,
        "avg_valence"       : avg_valence,
        "replay_ratio"      : replay_ratio,
        "exploration_score" : exploration_score,
        "peak_hour"         : peak_hour,
        "peak_day"          : peak_day,
        "unique_tracks"     : unique_tracks,
        "unique_artists"    : unique_artists,
        "total_plays"       : total_plays
    }