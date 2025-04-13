import pytest
from unittest.mock import MagicMock
from plugins.vantage.ingestion import VantageIngestion
from plugins.fmp.ingestion import FMPIngestion

@pytest.fixture
def ingestion_module():
    config = {
        "symbol": "AAPL",
        "api_key": "DUMMY_KEY",  # you can mock requests later
    }
    return VantageIngestion(config)

@pytest.fixture
def valid_response():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "Time Series (Daily)": {
            "2023-10-01": {
                "1. open": "100.0",
                "2. high": "102.0",
                "3. low": "98.0",
                "4. close": "101.0",
                "5. volume": "1000000"
            }
        }
    }
    return mock_resp

@pytest.fixture
def vantage_ingestion_instance():
    config = {"symbol": "AAPL", "api_key": "DUMMY_KEY"}
    return VantageIngestion(config)

@pytest.fixture
def fmp_ingestion_instance():
    config = {"symbol": "AAPL", "api_key": "DUMMY_KEY"}
    return FMPIngestion(config)

@pytest.fixture(params=["vantage", "fmp"])
def ingestion_instance(request, vantage_ingestion_instance, fmp_ingestion_instance):
    if request.param == "vantage":
        return vantage_ingestion_instance
    elif request.param == "fmp":
        return fmp_ingestion_instance

