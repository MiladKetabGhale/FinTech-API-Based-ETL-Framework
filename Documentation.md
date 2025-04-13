# Documentation: Inner Workings of FinStack

This document provides a deeper look at **FinStack**’s internal architecture, focusing on the **control flow, error handling, and interactions** among pipeline components. It’s intended for contributors, maintainers, or anyone who needs to customize FinStack beyond the basic usage documented in the main README.

---

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Pipeline Flow Details](#pipeline-flow-details)
   - [Configuration & Plugin Registry](#configuration--plugin-registry)
   - [Ingestion Stage](#ingestion-stage)
   - [Validation Stage](#validation-stage)
   - [Transformation Stage](#transformation-stage)
   - [Saving to Output](#saving-to-output)
3. [Error Handling & Logging](#error-handling--logging)
   - [Severity: Soft vs. Hard Errors](#severity-soft-vs-hard-errors)
   - [Automatic Retries & Backoff](#automatic-retries--backoff)
   - [Logging Levels & Error Reporting](#logging-levels--error-reporting)
4. [Partial Data vs. Early Exit Logic](#partial-data-vs-early-exit-logic)
5. [Advanced Extensions](#advanced-extensions)
6. [FAQ](#faq)

---

## High-Level Architecture

FinStack coordinates **data ingestion** from external APIs, **validation** to ensure data quality, **transformation** to unify structure, and finally **saving** the results for downstream use (machine learning, analytics, dashboards, etc.).

Key architectural elements:

- **Core**  
  - `pipeline_runner.py` orchestrates the overall data flow.  
  - `plugin_registry.py` holds references to all registered plugins.  

- **Error Handling**  
  - Modules in `Error_Handling/` (e.g., `api_error_handler.py`, `validation_errors.py`, `transformation_errors.py`, `retry_mechanism.py`) centralize how failures are detected and handled.  

- **Plugins**  
  - Each plugin folder (`vantage`, `finnhub`, `fmp`, etc.) implements logic for ingestion, validation, and transformation.

- **Tests**  
  - Unit tests (`tests/`) verify correct functionality and handle many edge cases (rate limits, incomplete JSON data, timeouts, etc.).

---

## Pipeline Flow Details

### Configuration & Plugin Registry

1. **Configuration (YAML)**  
   - A user-specified YAML config points FinStack to the desired plugin, API keys, logging locations, and output paths.  
   - Example: `example_config_vantage.yaml` might look like:

     ```yaml
     source: vantage
     api_key: ${VANTAGE_API_KEY}
     output_dir: output/vantage
     error_log_dir: logs/vantage
     ...
     ```

2. **Plugin Registry**  
   - `plugin_registry.py` maps plugin names (e.g., `"vantage"`) to their ingestion, validation, and transformation classes:

     ```python
     PLUGINS = {
       "vantage": {
         "ingestion": VantageIngestion,
         "validation": VantageValidation,
         "transformation": VantageTransformation
       },
       ...
     }
     ```
   - `pipeline_runner.py` references this registry to dynamically load the correct plugin classes.

### Ingestion Stage

1. **API Request**  
   - The chosen plugin’s `ingestion.py` is called. For instance, `VantageIngestion` might:
     - Construct URLs with query params (symbol, function=TIME_SERIES_DAILY, etc.).
     - Handle authentication (API keys).
     - Use `requests` to fetch data.

2. **Error Intercept**  
   - If HTTP status codes (4xx, 5xx) or malformed JSON occur, `api_error_handler.py` and `retry_mechanism.py` come into play:
     - **Retries** for certain errors (e.g., 503) a set number of times before giving up.  
     - Logs each attempt in `logs/vantage/`.

3. **Output**  
   - Returns a Python object (dict, list of dicts, or `None` on total failure) to `pipeline_runner.py`.

### Validation Stage

1. **Schema & Integrity Checks**  
   - `validation.py` ensures the required columns/fields are present (e.g., “symbol”, “timestamp”, “open”, “close”).  
   - Checks data types, missing or null values, suspicious anomalies (e.g., negative prices).

2. **Validation Errors**  
   - `validation_errors.py` logs any anomalies, deciding whether it’s a “soft” or “hard” error (see [Error Handling & Logging](#error-handling--logging)).

3. **Output**  
   - Produces a “validated_data” structure. If a critical error occurs, the pipeline can stop early. Otherwise, warnings or partial fixes might be applied.

### Transformation Stage

1. **Data Reshaping**  
   - `transformation.py` merges or pivots data, converts numeric types, renames columns, etc.
   - For example, daily time-series might be standardized to an internal column format like `["Date", "Open", "High", "Low", "Close", "Volume"]`.

2. **Transformation Errors**  
   - If transformations fail (e.g., unexpected data type, date parse errors), `transformation_errors.py` is triggered.

3. **Output**  
   - The final in-memory structure is returned for the “saving” phase.

### Saving to Output

- **pipeline_runner.py** calls the plugin’s saving logic or uses a shared method to write data to CSV, Parquet, or your desired format in the `output/` folder.
- On partial or non-fatal errors, you might still get some usable data—depending on whether the error-handling logic deems it safe to do so.

---

## Error Handling & Logging

FinStack’s **Error_Handling** modules centralize how failures are detected, logged, and either retried or escalated. The system aims to continue running where possible (“soft fail”) but will halt on truly blocking issues (“hard fail”).

### Severity: Soft vs. Hard Errors

- **Soft Error**  
  - Non-critical anomalies that can be logged and possibly recovered.  
  - Examples:
    - Minor missing fields that can be defaulted or dropped.
    - Intermittent network hiccups that succeed upon retry.
  - **Outcome**: Pipeline logs a warning, attempts to clean or partially fix the data, and continues.

- **Hard Error**  
  - Fatal issues where continuing could lead to invalid results or major data corruption.  
  - Examples:
    - Complete API failure (no data returned).
    - Critical schema mismatch (missing core columns, e.g., “Date” or “Close”).
    - Invalid transformations that can’t be patched.
  - **Outcome**: Pipeline logs an error message, raises an exception, and terminates ingestion or validation at that stage.

### Automatic Retries & Backoff

- **`retry_mechanism.py`** detects transient errors like timeouts or 5xx responses.  
- Applies a configurable backoff strategy (e.g., exponential or fixed intervals).  
- If repeated attempts fail, it logs a hard error and returns `None` for that data fetch.

### Logging Levels & Error Reporting

- **`logging_config.py`** sets up various logging handlers (console, file, etc.).  
- Each stage uses `logger.warning(...)` or `logger.error(...)` to categorize severity.  
- Logs are stored under `logs/<plugin_name>/` for easy debugging:
  - `error.log` might capture all serious errors.
  - `info.log` might capture general pipeline messages.

---

## Partial Data vs. Early Exit Logic

Because each plugin or stage can label errors as soft or hard, FinStack’s runner can handle scenarios like:

1. **Partial Data**  
   - If an API returns some valid data but is missing a few optional fields, the pipeline may skip those fields (soft error) and continue.

2. **Early Exit**  
   - If the entire validation fails (missing essential columns) or the API is entirely down (no data returned), FinStack will log a hard error and exit.

This approach prevents the pipeline from silently failing while still allowing you to salvage data in borderline cases.

---

## Advanced Extensions

- **Analytics Hooks**: You could add post-transformation analytics or summary statistics (e.g., daily volatility metrics) before saving.  
- **Batch vs. Streaming**: FinStack is primarily batch-oriented right now, but plugins or runner logic could be adapted for streaming ingestion (e.g., websocket feed).  
- **Parallelization**: You can spawn multiple ingestion tasks in parallel for different symbols or data sources if your system needs to process large volumes quickly.

---

## FAQ

1. **How do I skip validation?**  
   - By default, you need all three steps (ingestion→validation→transformation). You could create a “no-op” validation plugin if you truly want to bypass checks.

2. **Where do the logs go?**  
   - Each plugin writes logs to `logs/<plugin_name>/` by default. Check your config or logging setup for alternate paths.

3. **How do I add custom error severity?**  
   - Create additional classes or codes in `validation_errors.py`, `api_error_handler.py`, etc., and update `pipeline_runner.py` to interpret them as soft/hard.

---

**End of Documentation**  
For additional details, consult the code in `Error_Handling/` or open an issue in this repository if you have questions. Feel free to modify the pipeline runner or plugin design to fit your specific use case. Happy DataOps!

