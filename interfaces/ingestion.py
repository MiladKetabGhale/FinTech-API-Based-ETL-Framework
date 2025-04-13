from abc import ABC, abstractmethod

# defines an abstract base class BaseIngestion with:
    # a constructor storing configuration
    # an abstract ingest() method to be implemented by all concrete ingestion classes

class BaseIngestion(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def ingest(self):
        pass
