import pytest
from unittest.mock import patch
from requests.exceptions import Timeout

def test_timeout_error_returns_none(ingestion_instance):
    with patch("requests.get", side_effect=Timeout):
        result = ingestion_instance.ingest()
        assert result is None

