import sqlite3
from src.config import DATA_DIR

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

def creat_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    conn = creat_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Table created successfully")    