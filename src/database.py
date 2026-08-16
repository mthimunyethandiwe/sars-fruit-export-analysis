import sqlite3
from src.config import DATA_DIR
from src.config import RAW_DATA_DIR
import pandas as pd

DB_PATH = DATA_DIR / "exports.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    TradeType TEXT,
    CountryOfDestinationName TEXT,
    Tariff TEXT,
    YearMonth TEXT,
    ChapterAndDescription TEXT,
    StatisticalQuantity REAL,
    CustomsValue REAL
);
"""

CREATE_LOADED_FILES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS loaded_files (
    filename TEXT PRIMARY KEY,
    loaded_at TEXT
);
"""


def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    cursor.execute(CREATE_LOADED_FILES_TABLE_SQL)
    conn.commit()
    conn.close()


def load_csv_to_db(csv_path):
    df = pd.read_csv(csv_path)
    df["Tariff"] = df["Tariff"].astype(str).str.zfill(8)
    df["YearMonth"] = df["YearMonth"].astype(str)

    conn = create_connection()
    df.to_sql("raw_exports", conn, if_exists="append", index=False)
    conn.close()

    print(f"Loaded {len(df)} rows from {csv_path.name}")

def load_all_csvs():
    conn = create_connection()
    csv_files = RAW_DATA_DIR.glob("*.csv")

    for csv_path in csv_files:
        filename = csv_path.name

        if is_already_loaded(filename, conn):
            print(f"{filename} already loaded, skipping....")
            continue
        else:
            load_csv_to_db(csv_path)
            mark_as_loaded(filename, conn)

    conn.close()

def is_already_loaded(filename, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM loaded_files WHERE filename = ?", (filename,))
    result = cursor.fetchone()
    return result is not None


def mark_as_loaded(filename, conn):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO loaded_files (filename, loaded_at) VALUES (?, datetime('now'))",
        (filename,)
    )
    conn.commit()
    

if __name__ == "__main__":
    create_table()
    load_all_csvs()
            
    print("Table created and loaded successfully")