from pydantic import BaseModel, ValidationError, Field
from typing import List
import csv
import json
import os

from interfaces.validation import BaseValidation
from Error_Handling.validation_errors import log_validation_errors

class FinnhubCandle(BaseModel):
    c: List[float]  # close prices
    h: List[float]  # high prices
    l: List[float]  # low prices
    o: List[float]  # open prices
    v: List[int]    # volume
    t: List[int]    # timestamps
    s: str          # status

def validate_finnhub_data(raw_data, error_log_path="finnhub_validation_errors.csv"):
    valid_data = None
    errors = []
    try:
        candle = FinnhubCandle(**raw_data)
        if candle.s != "ok":
            raise ValueError("Status not OK in Finnhub data.")
        valid_data = candle
    except (ValidationError, ValueError) as e:
        errors.append({"message": str(e)})

    if errors:
        log_validation_errors(errors, error_log_path)

    return valid_data, errors

class FinnhubValidation(BaseValidation):
    def validate(self, raw_data):
        error_log_dir = self.config.get("error_log_dir", "logs")
        os.makedirs(error_log_dir, exist_ok=True)
        error_log_path = os.path.join(error_log_dir, "finnhub_validation_errors.csv")
        return validate_finnhub_data(raw_data, error_log_path)

