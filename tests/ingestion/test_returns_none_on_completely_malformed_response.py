import pytest
from unittest.mock import patch, MagicMock

def test_returns_none_on_completely_malformed_response(ingestion_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.side_effect = Exception("completely malformed")
    with patch("requests.get", return_value=mock_resp):
        result = ingestion_instance.ingest()
        assert result is None

