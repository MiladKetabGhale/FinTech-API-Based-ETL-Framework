import requests
import logging

from interfaces.ingestion import BaseIngestion
from Error_Handling.retry_mechanism import retry_request
from Error_Handling.api_error_handler import handle_api_error

def fetch_daily_stock_data(symbol, api_key):
    """
    Fetch daily stock data from the Alpha Vantage API.

    Args:
        symbol (str): Stock symbol.
        api_key (str): Alpha Vantage API key.

    Returns:
        dict: Parsed JSON response or None if the request fails.
    """
    logging.info("Fetching data for %s...", symbol)
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    try:
        response = retry_request(
            requests.get,
            max_retries=3,
            backoff_factor=1,
            url=url,
            timeout=10
        )
        response.raise_for_status()
        # Pass symbol to context_info and also check for "Time Series (Daily)" as required key
        if handle_api_error(response, required_key='Time Series (Daily)', context_info=symbol):
            return response.json().get('Time Series (Daily)', None)
    except requests.exceptions.Timeout:
        logging.error("Request timed out for symbol %s.", symbol)
    except requests.exceptions.RequestException as e:
        logging.error("Request error for symbol %s: %s", symbol, str(e))
    return None

class VantageIngestion(BaseIngestion):
    def ingest(self):
        symbol = self.config.get("symbol")
        api_key = self.config.get("api_key")
        return fetch_daily_stock_data(symbol, api_key)

