import pytest
from unittest.mock import patch, MagicMock

def test_invalid_symbol_returns_none(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"Error Message": "Invalid symbol"}
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert result is None

