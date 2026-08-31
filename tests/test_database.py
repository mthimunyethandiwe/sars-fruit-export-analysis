import sqlite3
from src.database import CREATE_TABLE_SQL, CREATE_LOADED_FILES_TABLE_SQL
from src.database import is_already_loaded, mark_as_loaded


def test_create_table_creates_raw_exports(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    cursor.execute(CREATE_LOADED_FILES_TABLE_SQL)
    conn.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]

    assert "raw_exports" in table_names
    assert "loaded_files" in table_names

    conn.close()

def test_idempotency_tracking(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(CREATE_LOADED_FILES_TABLE_SQL)
    conn.commit()

    assert is_already_loaded("fake_file.csv", conn) == False

    mark_as_loaded("fake_file.csv", conn)

    assert is_already_loaded("fake_file.csv", conn) == True

    conn.close()    