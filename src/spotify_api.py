import os
import time
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SPOTIFY_TRACKS_FILE = DATA_DIR / "spotify_tracks.csv"


def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError("Missing Spotify credentials in .env")
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=30
    )
    if r.status_code != 200:
        raise RuntimeError(f"Token failed: {r.status_code} {r.text}")
    return r.json()["access_token"]


def search_tracks(query, token, limit=1, offset=0):
    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": "Bearer " + token},
        params={"q": query, "type": "track", "limit": limit, "offset": offset},
        timeout=30
    )
    if r.status_code == 429:
        print("[WARN] Rate limited, waiting 10 seconds...")
        time.sleep(10)
        return search_tracks(query, token, limit, offset)
    if r.status_code != 200:
        print(f"[WARN] Search failed at offset={offset}: {r.status_code}")
        return []
    return r.json().get("tracks", {}).get("items", [])


def collect_tracks(query, token, total_limit=200):
    all_tracks = []
    seen_ids = set()
    offset = 0

    while len(all_tracks) < total_limit and offset < 1000:
        items = search_tracks(query=query, token=token, limit=1, offset=offset)

        if not items:
            offset += 1
            continue

        item = items[0]
        track_id = item.get("id")

        if track_id and track_id not in seen_ids:
            seen_ids.add(track_id)
            artists = item.get("artists", [])
            album = item.get("album", {})

            # popularity is directly in the track object
            popularity = item.get("popularity")

            all_tracks.append({
                "track_id": track_id,
                "track_name": item.get("name"),
                "artist": artists[0].get("name") if artists else None,
                "album": album.get("name"),
                "release_date": album.get("release_date"),
                "popularity": popularity,
                "duration_ms": item.get("duration_ms"),
                "explicit": item.get("explicit")
            })

        offset += 1
        time.sleep(0.3)

        if len(all_tracks) % 10 == 0 and len(all_tracks) > 0:
            print(f"[INFO] Collected {len(all_tracks)}/{total_limit} tracks...")

    df = pd.DataFrame(all_tracks)
    if not df.empty:
        df = df.drop_duplicates(subset=["track_id"]).reset_index(drop=True)
    return df


def save_tracks_to_csv(df, output_path=None):
    if output_path is None:
        output_path = SPOTIFY_TRACKS_FILE
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Saved {len(df)} rows to {output_path}")
    # Show popularity stats to confirm data is correct
    if "popularity" in df.columns:
        print(f"[INFO] Popularity — mean: {df['popularity'].mean():.1f}, nulls: {df['popularity'].isnull().sum()}")


if __name__ == "__main__":
    print("[INFO] Getting Spotify token...")
    token = get_spotify_token()
    print("[INFO] Token OK. Collecting tracks...")
    df = collect_tracks("hip hop", token, total_limit=200)
    if df.empty:
        print("[WARNING] No tracks collected.")
    else:
        save_tracks_to_csv(df)
        print(f"[INFO] Done! {len(df)} tracks saved.")
        print(df[["track_name", "artist", "popularity"]].head(10))