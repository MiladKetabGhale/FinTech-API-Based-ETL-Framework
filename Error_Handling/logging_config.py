import logging
import os

def configure_logging(log_file="etl_pipeline.log", level=logging.INFO):
    """
    configure the logging system to write logs to a file in the logs directory.
    parameters:
        log_file : str
            name of the log file to write to
        level : int
            logging level (e.g., logging.INFO, logging.DEBUG)
    returns:
        None
    """
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        filename=log_path,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

