import pandas as pd
from config import SPOTIFY_TRACKS_FILE, CLEANED_DATA_FILE, POPULARITY_THRESHOLD


def load_raw_data(path=None):
    if path is None:
        path = SPOTIFY_TRACKS_FILE

    print(f"[INFO] Loading raw data from {path} ...")
    df = pd.read_csv(path)
    print(f"[INFO] Loaded {len(df)} rows, {len(df.columns)} columns.")
    return df


def clean_tracks(df):
    print("[INFO] Cleaning data ...")
    original_len = len(df)


    df = df.dropna(subset=["track_id", "track_name", "artist", "popularity"])


    df = df.drop_duplicates(subset=["track_id"]).reset_index(drop=True)


    df["release_year"] = pd.to_datetime(
        df["release_date"], errors="coerce"
    ).dt.year


    df["duration_sec"] = (df["duration_ms"] / 1000).round(1)
    df = df.drop(columns=["duration_ms"])


    df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
    df["explicit"] = df["explicit"].astype(bool)


    df = df.dropna(subset=["popularity"]).reset_index(drop=True)

    print(f"[INFO] Cleaned: {original_len} → {len(df)} rows.")
    return df


def add_hit_label(df, threshold=None):

    if threshold is None:
        threshold = POPULARITY_THRESHOLD

    df["is_hit"] = (df["popularity"] >= threshold).astype(int)
    hit_count = df["is_hit"].sum()
    print(f"[INFO] Hit label added (threshold={threshold}): "
          f"{hit_count} hits / {len(df) - hit_count} non-hits.")
    return df


def save_cleaned_data(df, output_path=None):

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