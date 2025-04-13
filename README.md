# FinStack: A Modular, Scalable API-Based ETL Framework for Market Data

Welcome to **FinStack**, a production-oriented DataOps pipeline that automates **ingestion, validation, transformation, and saving** of financial market data from multiple external APIs. Built with a plugin-based design, FinStack makes it easy to add new data providers or adapt existing ones—so you can focus on using reliable, clean market data for analytics, dashboards, and machine learning models.

---

## Table of Contents
1. [Why FinStack?](#why-finstack)  
2. [Key Components](#key-components)  
   - [Core](#core)  
   - [Error Handling](#error-handling)  
   - [Interfaces](#interfaces)  
   - [Plugins](#plugins)  
   - [Tests](#tests)  
3. [Typical Workflow](#typical-workflow)  
4. [Project Structure](#project-structure)  
5. [Usage](#usage)  
6. [How to Extend](#how-to-extend)  
7. [Future Directions](#future-directions)  
8. [License](#license)  

---

## Why FinStack?

Financial data can be messy, inconsistent, and prone to transient API errors. **FinStack** addresses these common challenges by:

- **Centralizing DataOps**: Ingest data from *multiple* APIs (e.g., Alpha Vantage, Finnhub, FMP) into a unified workflow.  
- **Ensuring Data Reliability**: Validations and transformations guarantee standardized schemas, consistent datatypes, and high-quality data.  
- **Simplifying Integrations**: The plugin-based architecture allows you to easily add new sources or extend validations without rewriting the entire pipeline.  
- **Supporting Downstream ML & Analytics**: Once ingested and cleaned, data can be pushed to your warehouse, fed into ML models, or served to BI dashboards.

Whether you’re building daily reporting systems, feeding real-time dashboards, or training forecasting models, **FinStack** provides a robust foundation for managing financial market data at scale.

---

## Key Components

### Core

#### `pipeline_runner.py`
- **Orchestrates the entire pipeline**: from ingestion → validation → transformation → saving.  
- Loads your YAML configuration to determine which plugins to run, and in which order.  
- Handles early exit if no data arrives from the API.

#### `plugin_registry.py`
- Stores references to each available plugin’s ingestion, validation, and transformation classes.  
- Facilitates a clean **“register + run”** approach for newly added APIs.

---

### Error Handling

#### `logging_config.py`
- Centralizes logging. Messages can be routed to console, files, or external logging frameworks.

#### `api_error_handler.py`, `validation_errors.py`, `transformation_errors.py`, `retry_mechanism.py`
- **API Errors**: Gracefully handle HTTP 404/500, rate limits, or malformed responses.  
- **Validation Failures**: Identify incomplete data, wrong datatypes, unexpected columns.  
- **Retry & Backoff**: Automatically retry on transient network or rate-limit errors, logging every attempt.

> **Example**: If Finnhub responds with a 503, FinStack retries a few times before logging a warning and skipping ingestion.

---

### Interfaces

- **`ingestion.py`, `validation.py`, `transformation.py`**  
  Define base classes that each plugin must implement (e.g., `IngestionBase`, `ValidationBase`, `TransformationBase`).  
  They ensure a **consistent contract**: every plugin can ingest, validate, and transform data in a predictable way.

---

### Plugins

- **`vantage/`, `fmp/`, `finnhub/`**  
  Each folder contains three files implementing ingestion, validation, and transformation logic specific to that data source.  
  - **`ingestion.py`**: Calls the API, parses JSON, handles authentication.  
  - **`validation.py`**: Checks for required fields, correct types, or suspicious anomalies.  
  - **`transformation.py`**: Reshapes data (e.g., pivot, rename columns), merges related data, and saves final output.

Use the plugins as-is or customize them for advanced or vendor-specific logic. 

---

### Tests

- **`tests/`**  
  - Thorough unit tests cover ingestion, validation, and transformation stages for each plugin.  
  - Includes edge-case checks such as missing/extra JSON keys, rate limit error messages, partial data ingestion, etc.  
  - Organized by plugin and function type to maintain clarity and coverage.

---

## Usage

1. **Clone the repository** (or copy it to your local environment).

2. **Install dependencies**.  
   - If you have a `requirements.txt`, run:
     ```
     pip install -r requirements.txt
     ```
   - Otherwise, ensure you have libraries like `requests`, `PyYAML`, and `pytest` installed.

3. **Set environment variables**.  
   - The config files (`example_config_finnhub.yaml`, `example_config_vantage.yaml`, etc.) may reference environment variables (e.g., `${VANTAGE_API_KEY}`).  
   - You can create a `.env` file or export them directly:
     ```bash
     export VANTAGE_API_KEY=YOUR_ACTUAL_KEY
     export FINNHUB_API_KEY=YOUR_ACTUAL_KEY
     # etc.
     ```

4. **Run the pipeline** using a specified config:
   ```bash
   python main.py --config example_config_vantage.yaml

---
## Project Structure

Below is a high-level overview of the repository:

```bash
LLM_Assisted_DataOps_Pipeline/
├── Error_Handling/
│   ├── api_error_handler.py
│   ├── logging_config.py
│   ├── retry_mechanism.py
│   ├── transformation_errors.py
│   └── validation_errors.py
├── README.md
├── core/
│   ├── pipeline_runner.py
│   └── plugin_registry.py
├── example_config.yaml
├── interfaces/
│   ├── ingestion.py
│   ├── transformation.py
│   └── validation.py
├── logs/
│   ├── vantage/
│   ├── fmp/
│   └── finnhub/
├── main.py
├── output/
│   ├── vantage/
│   ├── fmp/
│   └── finnhub/
├── plugins/
│   ├── vantage/
│   │   ├── ingestion.py
│   │   ├── transformation.py
│   │   └── validation.py
│   ├── fmp/
│   │   ├── ingestion.py
│   │   ├── transformation.py
│   │   └── validation.py
│   └── finnhub/
│       ├── ingestion.py
│       ├── transformation.py
│       └── validation.py
├── tests/
│   ├── ingestion/
│   │   ├── test_404_error_returns_none.py
│   │   ├── test_500_error_returns_none.py
│   │   ├── test_invalid_symbol_returns_none.py
│   │   ├── test_logging_on_failure.py
│   │   ├── test_malformed_json_returns_none.py
│   │   ├── test_missing_required_key_in_json_returns_none.py
│   │   ├── test_rate_limit_note_returns_none.py
│   │   ├── test_retry_on_failure_with_backoff.py
│   │   ├── test_returns_none_on_completely_malformed_response.py
│   │   ├── test_successful_ingestion_returns_data.py
│   │   ├── test_timeout_error_returns_none.py
│   │   └── test_ingestion_respects_config_structure.py
│   ├── test_plugins/
│   │   ├── test_ingestion.py
│   │   ├── fmp/
│   │   │   ├── test_fmp_validation.py
│   │   │   └── test_fmp_transformation.py
│   │   └── finnhub/
│   │       ├── test_finnhub_validation.py
│   │       └── test_finnhub_transformation.py
│   ├── transformation/
│   ├── validation/
│   └── shared/

```
---
## How to Extend

### 1. Create a New Plugin

- Create a folder in `plugins/` with the name of your data source.  
  Example:

- Implement the following classes within that folder:

- `ingestion.py`  
  Define a class `MyDataSourceIngestion` that implements your data fetching logic.

- `validation.py`  
  Define a class `MyDataSourceValidation` that verifies the structure and quality of the fetched data.

- `transformation.py`  
  Define a class `MyDataSourceTransformation` that shapes the data into the desired format and saves it.

- Register your plugin by editing `core/plugin_registry.py`:

```python
from plugins.mydatasource.ingestion import MyDataSourceIngestion
from plugins.mydatasource.validation import MyDataSourceValidation
from plugins.mydatasource.transformation import MyDataSourceTransformation

PLUGINS = {
    "vantage": {...},
    "finnhub": {...},
    "fmp": {...},
    "mydatasource": {
        "ingestion": MyDataSourceIngestion,
        "validation": MyDataSourceValidation,
        "transformation": MyDataSourceTransformation
    }
}
```
### Update Your Config File to Use the New Plugin

```yaml
source: mydatasource
api_key: ${MYDATASOURCE_API_KEY}
output_dir: output/mydatasource
error_log_dir: logs/mydatasource
# any other plugin-specific parameters...
```
### 2. Modify or Enhance Existing Plugins

You can extend or override methods in `ingestion.py`, `validation.py`, or `transformation.py` of an existing plugin to support additional logic, such as:

- Fetching from new API endpoints  
- Adding complex validation rules  
- Introducing new transformation techniques

### 3. Adjust Pipeline Behavior

To customize the overall pipeline logic (e.g., post-processing, analytics, automated reporting), modify the following file to reflect your desired control flow:
```bash
core/pipeline_runner.py
```
## Future Directions

### Dockerization (April)
- Containerize this pipeline for easier deployment and environment consistency.  
- A `Dockerfile` and usage instructions will be added.

### Airflow Integration (April)
- Orchestrate and schedule these pipelines using **Apache Airflow**.  
- Enables automatic data pulls at regular intervals and improved observability of pipeline runs.

---

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).  
You are free to use, modify, and distribute the code, provided proper attribution is given.
The software is provided "as is," without warranties or guarantees of any kind.
