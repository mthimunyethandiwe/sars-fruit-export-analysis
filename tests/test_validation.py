import pandas as pd
from src.validation import check_negative_values, check_missing_values, check_duplicate_rows


def make_sample_df():
    return pd.DataFrame({
        "TradeType": ["Exports", "Exports", "Exports", "Exports"],
        "CountryOfDestinationName": ["Zambia", "Kenya", "Zambia", "Zambia"],
        "Tariff": ["08011000", "08021000", "08011000", "08011000"],
        "YearMonth": ["202001", "202001", "202001", "202001"],
        "StatisticalQuantity": [100.0, -50.0, 100.0, 100.0],
        "CustomsValue": [1000.0, 500.0, 1000.0, 1000.0],
    })

def test_check_negative_values_finds_negative_row():
    df = make_sample_df()
    negative_qty, negative_val = check_negative_values(df)
    assert len(negative_qty) == 1
    assert len(negative_val) == 0