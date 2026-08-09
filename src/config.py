from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
IMAGES_DIR = ROOT_DIR / "images"

for folder in(RAW_DATA_DIR, PROCESSED_DATA_DIR, IMAGES_DIR):
    folder.mkdir(parents=True, exist_ok=True)