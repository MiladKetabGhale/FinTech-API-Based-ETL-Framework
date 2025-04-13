import requests
import logging

from interfaces.ingestion import BaseIngestion
from Error_Handling.retry_mechanism import retry_request
from Error_Handling.api_error_handler import handle_api_error

def fetch_fmp_stock_data(symbol, api_key):
    """
    Fetch historical stock data from FMP API.

    Returns:
        list | None
    """
    logging.info("Fetching FMP data for %s...", symbol)
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}"

    try:
        response = retry_request(
            requests.get,
            max_retries=3,
            backoff_factor=1,
            url=url,
            timeout=10
        )
        response.raise_for_status()
        if not handle_api_error(response, required_key="historical", context_info=symbol):
            return None
        return response.json().get("historical", None)
    except Exception as e:
        logging.error("FMP ingestion failed for %s. Error: %s", symbol, str(e))
        return None

class FMPIngestion(BaseIngestion):
    def __init__(self, config):
        self.api_key = config.get("api_key")
        self.symbol = config.get("symbol")

    def ingest(self):
        return fetch_fmp_stock_data(self.symbol, self.api_key)

