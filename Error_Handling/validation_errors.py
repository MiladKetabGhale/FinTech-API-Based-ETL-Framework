import logging
import csv

def log_validation_errors(errors, error_log_path):
    """
    Logs a list of validation errors to CSV.
    """
    try:
        with open(error_log_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "field", "message", "type"])
            writer.writeheader()
            writer.writerows(errors)
            logging.error("Validation errors logged to %s", error_log_path)
    except Exception as e:
        logging.error("Failed to log validation errors: %s", str(e))

