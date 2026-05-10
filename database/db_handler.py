# database/db_handler.py
# This file handles everything related to saving and reading from MySQL

import mysql.connector
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from datetime import datetime   


def get_connection():
    """Opens a connection to your MySQL database."""
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection


def save_user(user):
    """
    Saves your Spotify profile to the users table.
    If you already exist in the table, it skips — no duplicates.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT IGNORE INTO users (user_id, username)
        VALUES (%s, %s)
    """
    cursor.execute(query, (user["user_id"], user["username"]))

    conn.commit()
    cursor.close()
    conn.close()
    print(f" User '{user['username']}' saved to database.")


def save_tracks(tracks):
    """
    Saves each unique track to the tracks table.
    If a track already exists, it skips — no duplicates.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT IGNORE INTO tracks (track_id, track_name, artist, energy, valence)
        VALUES (%s, %s, %s, %s, %s)
    """

    for track in tracks:
        cursor.execute(query, (
            track["track_id"],
            track["track_name"],
            track["artist"],
            track["energy"],
            track["valence"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f" {len(tracks)} tracks saved to database.")


def save_listening_history(user_id, tracks):
    """
    Saves every play event to listening_history.
    Converts Spotify's timestamp format to MySQL's format first.
    Same song played 5 times = 5 rows saved.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO listening_history (user_id, track_id, played_at)
        VALUES (%s, %s, %s)
    """

    for track in tracks:
        # Convert '2026-05-08T15:10:11.930Z' → '2026-05-08 15:10:11'
        raw_time    = track["played_at"]
        clean_time  = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%S.%fZ")

        cursor.execute(query, (
            user_id,
            track["track_id"],
            clean_time
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f" {len(tracks)} listening events saved to history.")


def get_all_tracks(user_id=None):
    """
    Fetches tracks from MySQL for a specific user.
    If no user_id given, fetches all tracks.
    """
    import pandas as pd

    conn  = get_connection()

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
            WHERE lh.user_id = %s
        """
        df = pd.read_sql(query, conn, params=(user_id,))
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
        df = pd.read_sql(query, conn)

    conn.close()
    return df


def get_user():
    """Fetches your user info from the users table."""
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user