import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout

# ingestion_module fixture must be defined in plugin-specific tests

@pytest.fixture
def valid_response():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "Time Series (Daily)": {
            "2024-03-27": {
                "1. open": "100", "2. high": "105",
                "3. low": "95", "4. close": "102", "5. volume": "100000"
            }
        }
    }
    return mock_resp
