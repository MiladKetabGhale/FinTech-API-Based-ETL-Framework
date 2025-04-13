import pytest
from unittest.mock import patch, MagicMock

def test_logging_on_failure(ingestion_instance, caplog):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.json.return_value = {}
    with patch("requests.get", return_value=mock_resp):
        ingestion_instance.ingest()
        assert any("Error" in record.message or "error" in record.message for record in caplog.records)

