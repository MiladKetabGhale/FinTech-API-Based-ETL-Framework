import logging
import yaml
from core.plugin_registry import PLUGINS

def load_config(path="config.yaml"):
    """
    load the pipeline configuration from a YAML file.

    parameters:
        path : str
            path to the YAML configuration file.

    returns:
        dict
            Parsed configuration as a dictionary.
    """
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def run_pipeline(config):
    """
    execute the full data pipeline using the specified plugin.

    the pipeline includes ingestion, validation, transformation, 
    and saving of the transformed data. If ingestion returns no data, 
    the pipeline logs an error and exits early.

    parameters:
        config : dict
            dictionary containing pipeline configuration, including the data source plugin, API key, and symbol.
    """
    source = config["source"]
    api_key = config.get("api_key")
    symbol = config.get("symbol")

    plugin = PLUGINS[source]

    ingestion = plugin["ingestion"](config)
    raw_data = ingestion.ingest()

    # Guard if no data is returned
    if not raw_data:
        logging.error("No data was ingested. Pipeline will exit.")
        return

    validation = plugin["validation"](config)
    validated_data, errors = validation.validate(raw_data)

    transformation = plugin["transformation"](config)
    transformed_data = transformation.transform(validated_data)
    path = transformation.save(transformed_data)
    print(f"Data saved to {path}")

