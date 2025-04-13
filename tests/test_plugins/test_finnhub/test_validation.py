import pytest
from plugins.finnhub.validation import FinnhubValidation

@pytest.fixture
def dummy_config():
    return {"error_log_dir": "logs/finnhub"}

def test_valid_finnhub_data_passes(dummy_config):
    raw_data = {
        "c": [100.0, 101.0],
        "h": [102.0, 103.0],
        "l": [99.0, 98.5],
        "o": [100.0, 100.5],
        "v": [1000, 1100],
        "t": [1609459200, 1609545600],
        "s": "ok"
    }
    validator = FinnhubValidation(dummy_config)
    validated, errors = validator.validate(raw_data)
    assert errors == []
    assert validated is not None

def test_invalid_finnhub_data_fails(dummy_config):
    raw_data = {
        "c": [100.0],
        "h": [102.0],
        "l": [99.0],
        "o": ["BAD"],  # string instead of float
        "v": [1000],
        "t": [1609459200],
        "s": "ok"
    }
    validator = FinnhubValidation(dummy_config)
    validated, errors = validator.validate(raw_data)
    assert validated is None or len(errors) > 0

