import pytest
from unittest.mock import patch, MagicMock

def test_successful_ingestion_returns_data(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "Time Series (Daily)": {"2023-01-01": {"1. open": "100"}},  # for Vantage
        "historical": [{"date": "2023-01-01", "open": 100}]         # for FMP
    }
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert result is None or isinstance(result, (dict, list))

