from src.analysis import get_annual_summary


def test_get_annual_summary_returns_results():
    results = get_annual_summary()
    assert len(results) > 0


def test_get_annual_summary_has_four_columns():
    results = get_annual_summary()
    first_row = results[0]
    assert len(first_row) == 4


def test_implied_price_is_positive():
    results = get_annual_summary()
    for year, quantity, value, price in results:
        assert price > 0