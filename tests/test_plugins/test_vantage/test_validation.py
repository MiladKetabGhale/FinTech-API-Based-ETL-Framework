import pytest
from plugins.vantage.validation import validate_stock_data

def test_valid_stock_data_passes():
    raw_data = {
        "2024-01-01": {
            "1. open": 100, "2. high": 110, "3. low": 90,
            "4. close": 105, "5. volume": 1000
        }
    }
    valid_data, errors = validate_stock_data(raw_data)
    assert "2024-01-01" in valid_data
    assert errors == []

def test_missing_field_fails_validation():
    raw_data = {
        "2024-01-01": {
            "1. open": 100, "2. high": 110,
            "4. close": 105, "5. volume": 1000
        }  # Missing "3. low"
    }
    valid_data, errors = validate_stock_data(raw_data)
    assert "2024-01-01" not in valid_data
    assert len(errors) == 1
    assert errors[0]["field"] == "3. low"

def test_multiple_errors_logged():
    raw_data = {
        "2024-01-01": {
            "1. open": "BAD",  # Not a float
            "2. high": 110,
            "3. low": 90,
            "4. close": None,  # Invalid
            "5. volume": "BAD"  # Not an int
        }
    }
    valid_data, errors = validate_stock_data(raw_data)
    assert "2024-01-01" not in valid_data
    assert any(err["field"] == "1. open" for err in errors)
    assert any(err["field"] == "4. close" for err in errors)
    assert any(err["field"] == "5. volume" for err in errors)

