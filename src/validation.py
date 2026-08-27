from datetime import datetime
from src.config import DATA_DIR

LOG_PATH = DATA_DIR / "validation_log.txt"


def log_issue(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def check_negative_values(df):
    negative_quantity = df[df["StatisticalQuantity"] < 0]
    negative_value = df[df["CustomsValue"] < 0]

    if len(negative_quantity) > 0:
        print(f"Found {len(negative_quantity)} rows with negative StatisticalQuantity")

    if len(negative_value) > 0:
        print(f"Found {len(negative_value)} rows with negative CustomsValue")

    return negative_quantity, negative_value


def check_missing_values(df, required_columns):
    missing_report = {}

    for col in required_columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            missing_report[col] = missing_count
            print(f"Found {missing_count} missing values in {col}")

    return missing_report


def check_duplicate_rows(df, source_filename=""):
    duplicates = df[df.duplicated()]

    if len(duplicates) > 0:
        message = f"Found {len(duplicates)} duplicate rows in {source_filename}"
        print(message)
        log_issue(message)

    return duplicates