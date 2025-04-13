import pytest
from plugins.fmp.validation import validate_fmp_data

def test_validate_fmp_data_success():
    raw_data = [
        {
            "date": "2023-01-01",
            "open": 100.0,
            "high": 110.0,
            "low": 90.0,
            "close": 105.0,
            "volume": 1000000
        }
    ]
    validated, errors = validate_fmp_data(raw_data)
    assert len(validated) == 1
    assert not errors
    assert "2023-01-01" in validated

def test_validate_fmp_data_with_missing_field():
    raw_data = [
        {
            "date": "2023-01-01",
            "open": 100.0,
            "high": 110.0,
            "low": 90.0,
            "close": 105.0
            # missing "volume"
        }
    ]
    validated, errors = validate_fmp_data(raw_data)
    assert len(validated) == 0
    assert len(errors) == 1

