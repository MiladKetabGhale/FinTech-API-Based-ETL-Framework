import argparse
import os
from dotenv import load_dotenv
from core.pipeline_runner import load_config, run_pipeline
from Error_Handling.logging_config import configure_logging

def load_config_with_env(path):
    """Load a YAML config file and interpolate environment variables like ${VAR}."""
    import yaml
    with open(path, "r") as f:
        raw = f.read()
    interpolated = os.path.expandvars(raw)
    return yaml.safe_load(interpolated)

if __name__ == "__main__":
    # Load .env file into os.environ
    load_dotenv()

    # CLI arguments
    parser = argparse.ArgumentParser(description="Run the DataOps pipeline.")
    parser.add_argument("--config", type=str, default="config.yaml", help="YAML config file path.")
    parser.add_argument("--logfile", type=str, default="mastering_etl.log", help="Log file name.")
    args = parser.parse_args()

    configure_logging(args.logfile)  # Logs to Error_Handling/logs/
    config = load_config_with_env(args.config)
    run_pipeline(config)

