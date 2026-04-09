"""
main.py - Hip-Hop Popularity Prediction Data Pipeline
Run from src/ directory: python main.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import DATA_DIR, RESULTS_DIR, SEARCH_QUERY, TOTAL_TRACKS_LIMIT
from spotify_api import get_spotify_token, collect_tracks, save_tracks_to_csv
from data_cleaning import clean_tracks, add_hit_label, save_cleaned_data

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 55)
    print("  Hip-Hop Popularity Prediction — Data Pipeline")
    print("=" * 55)

    print("\n[Step 1] Authenticating with Spotify API...")
    token = get_spotify_token()
    print("[INFO] Token obtained.")

    print(f"\n[Step 2] Collecting {TOTAL_TRACKS_LIMIT} tracks for '{SEARCH_QUERY}'...")
    df_raw = collect_tracks(query=SEARCH_QUERY, token=token, total_limit=TOTAL_TRACKS_LIMIT)

    if df_raw.empty:
        print("[WARNING] No tracks collected.")
        sys.exit(1)

    print(f"\n[Step 3] Saving raw data...")
    save_tracks_to_csv(df_raw)

    print(f"\n[Step 4] Cleaning data and adding hit label...")
    df_clean = clean_tracks(df_raw)
    df_clean = add_hit_label(df_clean)
    save_cleaned_data(df_clean)

    print("\n" + "=" * 55)
    print(f"  Done! {len(df_raw)} raw / {len(df_clean)} cleaned tracks")
    print("=" * 55)
