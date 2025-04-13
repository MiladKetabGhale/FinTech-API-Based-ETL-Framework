import pandas as pd
from plugins.fmp.transformation import transform_fmp_data
from plugins.fmp.validation import FMPDataPoint

def test_transform_fmp_data_valid_input():
    validated_data = {
        "2023-01-01": FMPDataPoint(
            date="2023-01-01",
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0,
            volume=1000000
        )
    }
    df = transform_fmp_data(validated_data)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert set(["date", "open", "high", "low", "close", "volume"]).issubset(df.columns)

def test_transform_fmp_data_empty_dict():
    df = transform_fmp_data({})
    assert isinstance(df, pd.DataFrame)
    assert df.empty

