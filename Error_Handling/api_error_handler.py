import logging

def handle_api_error(response, required_key=None, context_info=""):
    """
    handles common HTTP and API-level errors.

    args:
        response (requests.Response): The HTTP response object.
        required_key (str, optional): A key expected in the JSON payload.
        context_info (str, optional): Identifier for logging context (e.g., symbol).

    returns:
        bool: True if no error, False otherwise.
    """
    if response.status_code == 404:
        logging.error("404 Error: Resource not found. Context: %s", context_info)
        return False
    elif response.status_code == 500:
        logging.error("500 Error: Internal server error. Context: %s", context_info)
        return False
    elif response.status_code >= 400:
        logging.error("HTTP Error %d. Context: %s", response.status_code, context_info)
        return False

    try:
        data = response.json()
        if 'Note' in data:
            logging.warning("Rate limit note: %s | Context: %s", data['Note'], context_info)
            return False
        if 'Error Message' in data:
            logging.error("API Error Message: %s | Context: %s", data['Error Message'], context_info)
            return False
        if required_key and required_key not in data:
            logging.error("Expected key '%s' missing in API response. Context: %s", required_key, context_info)
            return False
    except Exception as e:
        logging.error("Failed to parse JSON response. Context: %s | Error: %s", context_info, str(e))
        return False

    return True

