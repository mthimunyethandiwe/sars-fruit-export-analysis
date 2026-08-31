import pandas as pd
from src.database import create_table, load_all_csvs
from src.analysis import get_annual_summary
from src.validation import check_negative_values, check_missing_values, check_duplicate_rows
from src.config import RAW_DATA_DIR


def run_validation():
    required_columns = [
        "TradeType",
        "CountryOfDestinationName",
        "Tariff",
        "YearMonth",
        "StatisticalQuantity",
        "CustomsValue",
    ]

    for csv_path in RAW_DATA_DIR.glob("*.csv"):
        df = pd.read_csv(csv_path)
        check_negative_values(df)
        check_missing_values(df, required_columns)
        check_duplicate_rows(df, source_filename=csv_path.name)


def main():
    print("Step 1: creating database tables...")
    create_table()

    print("\nStep 2: validating raw data...")
    run_validation()

    print("\nStep 3: loading raw data into the database...")
    load_all_csvs()

    print("\nStep 4: running annual summary aggregation...")
    summary = get_annual_summary()
    for year, quantity, value, price in summary:
        print(f"{year}: quantity={quantity:.2f}, value={value:.2f}, implied_price_per_kg={price:.2f}")


if __name__ == "__main__":
    main()