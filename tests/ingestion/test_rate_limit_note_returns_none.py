import pytest
from unittest.mock import patch, MagicMock

def test_rate_limit_note_returns_none(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"Note": "API call frequency exceeded"}
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert result is None

