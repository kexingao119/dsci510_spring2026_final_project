import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from spotify_api import get_spotify_token, search_tracks, collect_tracks
from data_cleaning import clean_tracks, add_hit_label


def test_get_spotify_token():
    print("[TEST] test_get_spotify_token ...")
    token = get_spotify_token()
    assert isinstance(token, str) and len(token) > 0
    print("  PASSED")
    return token


def test_search_tracks(token):
    print("[TEST] test_search_tracks ...")
    items = search_tracks(query="hip hop", token=token, limit=1, offset=0)
    assert isinstance(items, list) and len(items) > 0
    print(f"  PASSED — {len(items)} item returned")
    return items


def test_track_fields(items):
    print("[TEST] test_track_fields ...")
    required = ["id", "name", "artists", "duration_ms", "explicit"]
    for key in required:
        assert key in items[0], f"Missing field: {key}"
    print("  PASSED (note: popularity field restricted by Spotify API 2024-2026 policy)")



def test_clean_tracks():

    print("[TEST] test_clean_tracks ...")
    sample = pd.DataFrame({
        "track_id": ["a", "b", "a", "c"],
        "track_name": ["Song A", "Song B", "Song A", None],
        "artist": ["Artist A", "Artist B", "Artist A", "Artist C"],
        "popularity": [80, 30, 80, 50],
        "duration_ms": [200000, 180000, 200000, 210000],
        "explicit": [True, False, True, False],
        "album": ["Album A", "Album B", "Album A", "Album C"],
        "release_date": ["2021-01-01", "2020-05", "2021-01-01", "2019"],
    })
    cleaned = clean_tracks(sample)
    assert "release_year" in cleaned.columns
    assert "duration_sec" in cleaned.columns
    assert len(cleaned) == 2
    print("  PASSED")


def test_add_hit_label():

    print("[TEST] test_add_hit_label ...")
    sample = pd.DataFrame({"popularity": [20, 50, 80, 49, 51]})
    result = add_hit_label(sample, threshold=50)
    assert list(result["is_hit"]) == [0, 1, 1, 0, 1]
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 50)
    print("  Running tests — Hip-Hop Popularity Project")
    print("=" * 50 + "\n")

    token = test_get_spotify_token()
    items = test_search_tracks(token)
    test_track_fields(items)
    test_clean_tracks()
    test_add_hit_label()

    print("\n" + "=" * 50)
    print("  All tests passed! ✓")
    print("=" * 50)