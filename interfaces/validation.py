from abc import ABC, abstractmethod

# defines BaseValidation abstract class with:
    # a constructor storing configuration.
    # an abstract validate method that takes raw_data and is expected to return validated data or raise an error.
# To be implemented by each plugin (e.g., Vantage, FMP, Finnhub).

class BaseValidation(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def validate(self, raw_data):
        pass
