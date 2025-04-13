from pydantic import BaseModel, ValidationError, Field
from typing import Dict
import csv
import json
import os

from interfaces.validation import BaseValidation
from Error_Handling.validation_errors import log_validation_errors

class StockDataPoint(BaseModel):
    open: float = Field(..., alias="1. open")
    high: float = Field(..., alias="2. high")
    low: float = Field(..., alias="3. low")
    close: float = Field(..., alias="4. close")
    volume: int  = Field(..., alias="5. volume")

class TimeSeries(BaseModel):
    data: Dict[str, StockDataPoint]

def validate_stock_data(raw_data, error_log_path="validation_errors.csv"):
    """
    Validates the structure of the stock data fetched from the Alpha Vantage API.

    Args:
        raw_data (dict): Raw JSON data containing the time series.
        error_log_path (str): Path to save the error log file.

    Returns:
        (dict, list): Validated stock data (only valid entries), and a list of errors.
    """
    valid_data = {}
    errors = []

    for timestamp, entry in raw_data.items():
        try:
            stock_data_point = StockDataPoint(**entry)
            valid_data[timestamp] = stock_data_point
        except ValidationError as e:
            for err in e.errors():
                errors.append({
                    "timestamp": timestamp,
                    "field": err["loc"][0],
                    "message": err["msg"],
                    "type": err["type"],
                })

    # Write errors to a CSV file if any
    if errors:
        log_validation_errors(errors, error_log_path)

    return valid_data, errors

def log_errors_to_csv(error_log_path: str, csv_log_path: str = "validation_errors.csv") -> None:
    """
    Converts a JSON error log file to CSV format.
    """
    try:
        with open(error_log_path, "r") as json_file:
            errors = json.load(json_file)

        with open(csv_log_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "field", "message", "type"])
            writer.writeheader()
            writer.writerows(errors)

        print(f"Validation errors converted and saved to {csv_log_path}")
    except FileNotFoundError:
        print(f"Error log file not found: {error_log_path}")
    except Exception as e:
        print(f"An error occurred while converting errors to CSV: {e}")

class VantageValidation(BaseValidation):
    def validate(self, raw_data):
        error_log_dir = self.config.get("error_log_dir", "logs")
        os.makedirs(error_log_dir, exist_ok=True)
        error_log_path = os.path.join(error_log_dir, "validation_errors.csv")
        return validate_stock_data(raw_data, error_log_path)

