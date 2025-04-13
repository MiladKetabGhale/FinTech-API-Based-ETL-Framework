from abc import ABC, abstractmethod

# abstract class BaseTransformation defines two expected behaviors:
    # transform: to apply transformations to already validated data.
    # save: to persist the transformed data.
# each method is expected to be implemented by subclasses tailored to a specific data source.
# it also initializes with a config.

class BaseTransformation(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def transform(self, validated_data):
        pass

    @abstractmethod
    def save(self, transformed_data):
        pass
