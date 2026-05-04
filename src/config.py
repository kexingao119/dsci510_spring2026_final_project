from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

# Collection settings
SEARCH_QUERY = "hip hop"
TOTAL_TRACKS_LIMIT = 500
POPULARITY_THRESHOLD = 50

# File paths
SPOTIFY_TRACKS_FILE = DATA_DIR / "spotify_tracks.csv"
CLEANED_DATA_FILE = DATA_DIR / "hiphop_cleaned.csv"
KAGGLE_DATA_FILE = DATA_DIR / "kaggledataset.csv"