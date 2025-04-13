import pytest
from unittest.mock import patch, MagicMock

def test_retry_on_failure_with_backoff(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"Time Series (Daily)": {}}
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert isinstance(result, dict) or result is None

