import pandas as pd
import pytest
from plugins.vantage.transformation import transform_stock_data

class DummyDataPoint:
    def __init__(self, open_, high, low, close, volume):
        self.data = {
            "1. open": open_,
            "2. high": high,
            "3. low": low,
            "4. close": close,
            "5. volume": volume,
        }

    def dict(self, by_alias=True):
        return self.data

def test_transformation_structure():
    sample_input = {
        "2024-01-01": DummyDataPoint(100, 110, 90, 105, 1000),
        "2024-01-02": DummyDataPoint(105, 115, 95, 110, 1200)
    }
    df = transform_stock_data(sample_input)
    expected_columns = {"date", "open", "high", "low", "close", "volume", "daily_return", "ma_5", "volatility"}
    assert expected_columns.issubset(df.columns)
    assert len(df) == 2

def test_daily_return_calculation():
    sample_input = {
        "2024-01-01": DummyDataPoint(100, 110, 90, 100, 1000),
        "2024-01-02": DummyDataPoint(100, 110, 90, 110, 1200)
    }
    df = transform_stock_data(sample_input)
    assert round(df["daily_return"].iloc[1], 2) == 10.0

def test_sorting_and_datetime_conversion():
    sample_input = {
        "2024-01-02": DummyDataPoint(100, 110, 90, 110, 1200),
        "2024-01-01": DummyDataPoint(100, 110, 90, 100, 1000)
    }
    df = transform_stock_data(sample_input)
    assert df["date"].is_monotonic_increasing
    assert isinstance(df["date"].iloc[0], pd.Timestamp)

