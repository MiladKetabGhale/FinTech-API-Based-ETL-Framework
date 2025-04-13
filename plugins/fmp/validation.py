from pydantic import BaseModel, ValidationError
from typing import List, Tuple, Dict
from interfaces.validation import BaseValidation
from Error_Handling.validation_errors import log_validation_errors

class FMPDataPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

def validate_fmp_data(raw_data: List[dict], error_log_path="validation_errors_fmp.csv") -> Tuple[Dict[str, FMPDataPoint], List[dict]]:
    """
    Validates a list of FMP data points (dicts).

    Returns:
        (validated_data: dict, errors: list)
    """
    validated = {}
    errors = []

    for item in raw_data:
        try:
            dp = FMPDataPoint(**item)
            validated[dp.date] = dp
        except ValidationError as ve:
            errors.append({"error": str(ve), "data": item})

    log_validation_errors(errors, error_log_path)
    return validated, errors

class FMPValidation(BaseValidation):
    def __init__(self, config):
        self.config = config

    def validate(self, raw_data, error_log_path="validation_errors_fmp.csv"):
        return validate_fmp_data(raw_data, error_log_path)

