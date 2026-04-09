"""
data_cleaning.py — cleans raw Spotify track data for the Hip-Hop Popularity project.

Functions:
    load_raw_data(path)       — load the raw CSV from spotify_api.py
    clean_tracks(df)          — remove duplicates, nulls, fix types
    add_hit_label(df)         — add binary 'is_hit' column based on popularity
    save_cleaned_data(df)     — save cleaned DataFrame to CSV
"""

import pandas as pd
from config import SPOTIFY_TRACKS_FILE, CLEANED_DATA_FILE, POPULARITY_THRESHOLD


def load_raw_data(path=None):
    """
    Load raw Spotify tracks CSV into a DataFrame.

    :param path: path to CSV file (defaults to config.SPOTIFY_TRACKS_FILE)
    :return: pandas DataFrame
    """
    if path is None:
        path = SPOTIFY_TRACKS_FILE

    print(f"[INFO] Loading raw data from {path} ...")
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} rows, {len(df.columns)} columns.")
    return df


def clean_tracks(df):
    """
    Clean the raw tracks DataFrame:
      - Drop rows missing critical fields (track_id, track_name, artist, popularity)
      - Remove duplicate track_ids
      - Convert release_date to datetime (year only)
      - Convert duration from ms to seconds
      - Reset index

    :param df: raw DataFrame from load_raw_data()
    :return: cleaned DataFrame
    """
    print("[INFO] Cleaning data ...")
    original_len = len(df)

    # Drop rows missing critical fields
    df = df.dropna(subset=["track_id", "track_name", "artist", "popularity"])

    # Remove duplicates
    df = df.drop_duplicates(subset=["track_id"]).reset_index(drop=True)

    # Extract release year from release_date (handles "2023", "2023-04", "2023-04-01")
    df["release_year"] = pd.to_datetime(
        df["release_date"], errors="coerce"
    ).dt.year

    # Convert duration from ms to seconds (easier to read)
    df["duration_sec"] = (df["duration_ms"] / 1000).round(1)
    df = df.drop(columns=["duration_ms"])

    # Ensure correct types
    df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
    df["explicit"] = df["explicit"].astype(bool)

    # Drop rows where popularity is still null after conversion
    df = df.dropna(subset=["popularity"]).reset_index(drop=True)

    print(f"[INFO] Cleaned: {original_len} → {len(df)} rows.")
    return df


def add_hit_label(df, threshold=None):
    """
    Add a binary 'is_hit' column: 1 if popularity >= threshold, else 0.

    :param df: cleaned DataFrame
    :param threshold: popularity cutoff (defaults to config.POPULARITY_THRESHOLD)
    :return: DataFrame with new 'is_hit' column
    """
    if threshold is None:
        threshold = POPULARITY_THRESHOLD

    df["is_hit"] = (df["popularity"] >= threshold).astype(int)
    hit_count = df["is_hit"].sum()
    print(f"[INFO] Hit label added (threshold={threshold}): "
          f"{hit_count} hits / {len(df) - hit_count} non-hits.")
    return df


def save_cleaned_data(df, output_path=None):
    """
    Save the cleaned DataFrame to CSV.

    :param df: cleaned DataFrame
    :param output_path: file path (defaults to config.CLEANED_DATA_FILE)
    """
    if output_path is None:
        output_path = CLEANED_DATA_FILE

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Saved cleaned data ({len(df)} rows) to {output_path}")


if __name__ == "__main__":
    df_raw = load_raw_data()
    df_clean = clean_tracks(df_raw)
    df_clean = add_hit_label(df_clean)
    save_cleaned_data(df_clean)
    print(df_clean.head())
    print(df_clean.dtypes)