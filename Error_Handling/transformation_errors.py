import logging

def log_transformation_error(message, exception=None):
    if exception:
        logging.error("%s: %s", message, str(exception), exc_info=True)
    else:
        logging.error(message)

