from src.database import create_connection


def get_annual_summary():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SUBSTR(YearMonth, 1, 4) AS year,
            SUM(StatisticalQuantity) AS total_quantity,
            SUM(CustomsValue) AS total_value,
            SUM(CustomsValue) / SUM(StatisticalQuantity) AS implied_price_per_kg
        FROM raw_exports
        GROUP BY year
        ORDER BY year;
    """)

    results = cursor.fetchall()
    conn.close()

    return results


if __name__ == "__main__":
    summary = get_annual_summary()
    for row in summary:
        print(row)