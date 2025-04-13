import pytest
from unittest.mock import patch, MagicMock

def test_missing_required_key_in_json_returns_none(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {}  # Missing "Time Series (Daily)" or "historical"
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert result is None

