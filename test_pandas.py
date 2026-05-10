# test_pandas.py — Stages 5 through 9 combined

import pandas as pd
from database.db_handler         import get_all_tracks, get_user
from analysis.analyzer           import analyze
from analysis.color_identity     import get_color_identity
from analysis.animal_personality import get_animal_personality
from visualization.plotter       import plot_energy_curves

def main():
    print("=" * 55)
    print("   Stage 5 — Loading Data into Pandas")
    print("=" * 55)

    user = get_user()
    print(f"\n User: {user['username']}")

    df = get_all_tracks()

    df["played_at"] = pd.to_datetime(df["played_at"])
    df["played_at"] = df["played_at"] + pd.Timedelta(hours=5, minutes=30)
    df["hour"]      = df["played_at"].dt.hour
    df["weekday"]   = df["played_at"].dt.day_name()
    df["month"]     = df["played_at"].dt.month_name()

    print(f"\n Total rows loaded : {len(df)}")
    print(f" Unique tracks     : {df['track_id'].nunique()}")

    print("\n Sample of your tracks:")
    print("-" * 55)
    print(df[["track_name", "artist", "energy", "valence"]].drop_duplicates(subset="track_name").head())
    print("-" * 55)

    # Stage 6 — Analyze
    metrics = analyze(df)

    # Stage 7 — Color Identity
    color_result = get_color_identity(metrics)

    # Stage 8 — Animal Personality
    animal_result = get_animal_personality(metrics)

    # Stage 9 — Visualization
    print("\n Generating your energy curve graphs...")
    plot_energy_curves(df, color_result["color"])

    return df, metrics, color_result, animal_result

if __name__ == "__main__":
    main()