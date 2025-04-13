from plugins.finnhub.transformation import FinnhubTransformation
from plugins.finnhub.validation import FinnhubCandle

def test_finnhub_transformation_runs():
    mock_validated = FinnhubCandle(
        c=[100.0, 101.0],
        h=[102.0, 103.0],
        l=[99.0, 98.5],
        o=[100.0, 100.5],
        v=[1000, 1100],
        t=[1609459200, 1609545600],
        s="ok"
    )
    config = {"symbol": "AAPL", "output_dir": "output/finnhub"}
    transformer = FinnhubTransformation(config)
    df = transformer.transform(mock_validated)

    assert df.shape[0] == 2
    assert "daily_return" in df.columns
    assert "ma_5" in df.columns
    assert "volatility" in df.columns
    assert df["date"].dtype.name.startswith("datetime")

