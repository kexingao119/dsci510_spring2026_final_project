# Predicting the Popularity of Hip-Hop Songs Using Audio Features

#DSCI 510 — Spring 2026 | Kexin Gao

## Introduction

This project investigates what makes a hip-hop song a "hit" using data from the Spotify Web API. By collecting track metadata and audio features (danceability, energy, tempo, loudness, etc.) for hundreds of hip-hop songs, the project builds a machine learning classification model to predict whether a song will be popular (popularity score ≥ 50 on Spotify's 0–100 scale).

The goal is to identify which musical features are most strongly associated with commercial success in hip-hop, and to provide a reproducible data pipeline from raw API data to a trained classifier.

---

## Data Sources

| # | Name / Description | Source URL | Type | Fields | Format | Estimated Size              |
|---|-------------------|------------|------|--------|--------|-----------------------------|
| 1 | Spotify Track Search (Hip-Hop) | https://developer.spotify.com/documentation/web-api | API | track_id, track_name, artist, album, release_date, popularity, duration_ms, explicit | JSON → CSV | 200 tracks (API restricted) |
| 2 | Spotify Audio Features | https://developer.spotify.com/documentation/web-api | API | danceability, energy, tempo, loudness, speechiness, valence, acousticness | JSON → CSV | 200 tracks (API restricted) |
| 3 | Spotify Tracks Dataset (Kaggle) | https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset | File (CSV) | tempo, loudness, speechiness, acousticness, popularity | CSV | 1000–2000 tracks            |
| 4 | Billboard Hot 100 (Kaggle) | https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs | File (CSV) | song_name, artist, rank, date, weeks_on_chart | CSV | ~500 songs                  |
| 5 | Genius Song Lyrics Dataset (Kaggle) | https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information | File (CSV) | word_count, song_name, language, year | CSV | 500–1000 tracks             |

---

## Analysis

The project performs the following types of analysis:

1. **Exploratory Data Analysis (EDA)** — distributions of audio features, popularity scores, correlation heatmaps, and comparisons between hit vs. non-hit songs.
2. **Feature Selection** — identifying which audio features correlate most strongly with popularity.
3. **Classification Modeling** — training Logistic Regression and Decision Tree classifiers to predict the binary `is_hit` label (popularity ≥ 50). Models are evaluated using accuracy, precision, and recall.

---

## Summary of Results

The project trained two classification models on 1,000 hip-hop tracks from the Kaggle Spotify Tracks Dataset:

- **Decision Tree**: Accuracy 77.0%, Precision 0.821, Recall 0.763, F1 0.791
- **Logistic Regression**: Accuracy 68.5%, Precision 0.692, Recall 0.807, F1 0.745

The Decision Tree outperformed Logistic Regression and exceeded the 70% accuracy target. Feature importance analysis revealed that **explicit**, **danceability**, and **acousticness** are the strongest predictors of hit songs.

Note: Spotify API returned popularity = 0 for all collected tracks due to 2024–2026 policy restrictions. The Kaggle dataset was used as the primary data source for model training.

---
## How to Run

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd dsci510_spring2026_final_project
```

### 2. Set up a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### 3. Download the data

**Option A — To reproduce the analysis results in `results.ipynb` (recommended):**

Download `kaggledataset.csv` from Google Drive and place it in the `data/` folder:

https://drive.google.com/file/d/11wottgkPxLLOeUQywcIuqhcEiGpRejzi/view?usp=share_link

Then open and run `results.ipynb`:
```bash
jupyter notebook results.ipynb
```

**Option B — To run the full Spotify API data collection pipeline:**

1. Create a Spotify Developer account at https://developer.spotify.com/dashboard
2. Copy your Client ID and Client Secret
3. Set up your `.env` file:
```bash
cp .env.example .env
```
4. Run the pipeline:
```bash
python src/main.py
```
This will collect up to 200 hip-hop tracks and save them to `data/spotify_tracks.csv` and `data/hiphop_cleaned.csv`.

### 4. Run tests

```bash
python tests.py
```

## Data Availability Note
No data files are included in this repository (excluded via `.gitignore`). Please follow the instructions in the **How to Run** section above to download the required datasets.