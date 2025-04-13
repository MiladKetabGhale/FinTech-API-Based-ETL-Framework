import requests
import logging

from interfaces.ingestion import BaseIngestion
from Error_Handling.retry_mechanism import retry_request
from Error_Handling.api_error_handler import handle_api_error

def fetch_candle_data(symbol, api_key, from_unix, to_unix, resolution="D"):
    logging.info("Fetching Finnhub data for %s...", symbol)
    url = (
        f"https://finnhub.io/api/v1/stock/candle"
        f"?symbol={symbol}&resolution={resolution}&from={from_unix}&to={to_unix}&token={api_key}"
    )
    try:
        response = retry_request(
            requests.get,
            max_retries=3,
            backoff_factor=1,
            url=url,
            timeout=10
        )
        response.raise_for_status()
        if handle_api_error(response, required_key='c', context_info=symbol):  # 'c' is the closing price array
            return response.json()
    except requests.exceptions.Timeout:
        logging.error("Request timed out for symbol %s.", symbol)
    except requests.exceptions.RequestException as e:
        logging.error("Request error for symbol %s: %s", symbol, str(e))
    return None

class FinnhubIngestion(BaseIngestion):
    def ingest(self):
        symbol = self.config.get("symbol")
        api_key = self.config.get("api_key")
        from_unix = self.config.get("from")
        to_unix = self.config.get("to")
        resolution = self.config.get("resolution", "D")
        return fetch_candle_data(symbol, api_key, from_unix, to_unix, resolution)

