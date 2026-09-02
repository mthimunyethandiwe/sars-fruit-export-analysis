# South African Fruit Export Analysis (SARS Data)

WTC-KGWBM47R



A small data engineering pipeline that loads South African fruit export
data (SARS Chapter 08 trade statistics, 2019–2026) into a SQLite database,
validates it, and analyzes trends using SQL.

**Research question:** has SA fruit export revenue growth come from
exporting *more* fruit (volume), or from earning *more per kilogram*
(price)?

## What this project demonstrates

- **ETL pipeline**: extract raw SARS export files, clean/type them
  correctly, load into a SQLite database
- **Idempotent loading**: the pipeline can be safely re-run without
  duplicating data — a `loaded_files` table tracks which source files
  have already been processed
- **Data validation**: checks for negative values, missing values, and
  duplicate rows before/while loading, with issues logged to
  `data/validation_log.txt`
- **SQL aggregation**: annual trend summary (total quantity, total value,
  implied price per kg) computed via a `GROUP BY` SQL query, not pandas
- **Tests**: automated tests covering the database, validation, and
  analysis modules

## How to run it

```bash
# 1. Set up a virtual environment
python -m venv venv
source venv/bin/activate      # For Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline
python main.py
```

This creates the SQLite database (`data/exports.db`), loads and validates
the raw SARS files in `data/raw/`, and prints an annual summary of export
quantity, value, and implied price per kg.

To run the tests:

```bash
pytest tests/ -v
```

## Project structure

```
├── data/
│   ├── raw/              # Raw SARS export files (.xls and converted .csv)
│   └── exports.db        # SQLite database (generated, not committed)
├── scripts/
│   └── convert_to_csv.py # One-off utility to convert .xls -> .csv
├── src/
│   ├── config.py         # Central file paths
│   ├── database.py       # Schema, connection, loading, idempotency
│   ├── validation.py     # Data quality checks
│   └── analysis.py       # SQL aggregation / trend analysis
├── tests/                # Automated tests for the modules above
└── main.py                # Runs the full pipeline end to end
```

## Data source

Raw data comes from SARS (South African Revenue Service) international
trade statistics, filtered to Chapter 08 (fruit and nuts). SARS limits
each download to a 2-year window, so the raw data is split across four
files covering 2019–2026.

## Known limitations

- Duplicate rows are logged, not automatically removed — the available
  columns don't include a shipment ID or exact date, so an exact-duplicate
  row could plausibly represent two genuinely separate shipments rather
  than a data entry error.
- 2026 is a partial year (data only through mid-year), so cumulative
  growth figures exclude it to avoid an unfair comparison against full
  years.
- This is a solo learning project, not a production pipeline — there's
  no scheduling/orchestration layer (e.g. Airflow), and validation
  currently logs issues rather than rejecting bad rows outright.