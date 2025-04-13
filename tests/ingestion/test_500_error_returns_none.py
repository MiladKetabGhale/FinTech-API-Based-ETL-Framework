import pytest
from unittest.mock import patch, MagicMock

def test_500_error_returns_none(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.json.return_value = {}
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert result is None

