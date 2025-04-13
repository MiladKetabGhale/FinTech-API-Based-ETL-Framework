import time
import logging
import requests

def retry_request(request_func, max_retries=3, backoff_factor=1, *args, **kwargs):
    """
    retry a request-based function with exponential backoff.

    parameters:
        request_func : callable
            the request function to retry (e.g., requests.get)
        max_retries : int
            maximum number of retry attempts
        backoff_factor : int or float
            factor for calculating backoff delay (in seconds)
        *args : tuple
            positional arguments to pass to the request function
        **kwargs : dict
            keyword arguments to pass to the request function

    returns:
    any
        the response returned by the request function if successful

    raises:
        requests.exceptions.RequestException if all retries fail
    """
    retries = 0
    while retries <= max_retries:
        try:
            logging.info("Attempt %d for request.", retries + 1)
            return request_func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries > max_retries:
                logging.error("All retries failed: %s", str(e))
                raise e
            wait_time = backoff_factor * (2 ** retries)
            logging.warning("Retry %d failed. Retrying in %d seconds.", retries, wait_time)
            time.sleep(wait_time)

