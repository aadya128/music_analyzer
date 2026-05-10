# database/db_handler.py
# Now using SQLite instead of MySQL
# SQLite stores everything in a single file — no server needed!

import sqlite3
import os
import pandas as pd

# Database file will be created automatically in the project root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music_analyzer.db")


def get_connection():
    """Opens a connection to the SQLite database file."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates all tables if they don't exist yet.
    This runs automatically every time the app starts.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id  TEXT PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id   TEXT PRIMARY KEY,
            track_name TEXT NOT NULL,
            artist     TEXT NOT NULL,
            energy     REAL,
            valence    REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listening_history (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id   TEXT,
            track_id  TEXT,
            played_at TEXT,
            FOREIGN KEY (user_id)  REFERENCES users(user_id),
            FOREIGN KEY (track_id) REFERENCES tracks(track_id)
        )
    """)

    conn.commit()
    conn.close()
    print(" Database initialized!")


def save_user(user):
    """Saves user to database. Skips if already exists."""
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username)
        VALUES (?, ?)
    """, (user["user_id"], user["username"]))

    conn.commit()
    conn.close()
    print(f" User '{user['username']}' saved.")


def save_tracks(tracks):
    """Saves unique tracks. Skips duplicates."""
    conn   = get_connection()
    cursor = conn.cursor()

    for track in tracks:
        cursor.execute("""
            INSERT OR IGNORE INTO tracks (track_id, track_name, artist, energy, valence)
            VALUES (?, ?, ?, ?, ?)
        """, (
            track["track_id"],
            track["track_name"],
            track["artist"],
            track["energy"],
            track["valence"]
        ))

    conn.commit()
    conn.close()
    print(f" {len(tracks)} tracks saved.")


def save_listening_history(user_id, tracks):
    """Saves every play event with timestamp."""
    from datetime import datetime

    conn   = get_connection()
    cursor = conn.cursor()

    for track in tracks:
        raw_time   = track["played_at"]
        clean_time = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%S.%fZ")

        cursor.execute("""
            INSERT INTO listening_history (user_id, track_id, played_at)
            VALUES (?, ?, ?)
        """, (user_id, track["track_id"], clean_time.strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    print(f" {len(tracks)} listening events saved.")


def get_all_tracks(user_id=None):
    """Loads tracks from database into a pandas DataFrame."""
    conn = get_connection()

    if user_id:
        query = """
            SELECT
                t.track_id,
                t.track_name,
                t.artist,
                t.energy,
                t.valence,
                lh.played_at
            FROM tracks t
            JOIN listening_history lh ON t.track_id = lh.track_id
            WHERE lh.user_id = ?
        """
        df = pd.read_sql_query(query, conn, params=(user_id,))
    else:
        query = """
            SELECT
                t.track_id,
                t.track_name,
                t.artist,
                t.energy,
                t.valence,
                lh.played_at
            FROM tracks t
            JOIN listening_history lh ON t.track_id = lh.track_id
        """
        df = pd.read_sql_query(query, conn)

    conn.close()
    return df


def get_user():
    """Gets the first user from the database."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"user_id": row["user_id"], "username": row["username"]}
    return None