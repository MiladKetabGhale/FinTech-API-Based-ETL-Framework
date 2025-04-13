import pandas as pd
import os
from datetime import datetime

from interfaces.transformation import BaseTransformation
from Error_Handling.transformation_errors import log_transformation_error

def transform_stock_data(validated_data):
    """
    Perform transformations on validated stock data.

    Args:
        validated_data (dict): Validated stock data in dictionary format.

    Returns:
        pd.DataFrame: Transformed stock data.

    Raises:
        ValueError: If transformation fails due to invalid data.
    """
    try:
        # Convert each timestamp -> StockDataPoint into a dict so DataFrame can read it
        dict_for_df = {
            ts: data.dict(by_alias=True)  # Get original keys if needed
            for ts, data in validated_data.items()
        }

        df = pd.DataFrame.from_dict(dict_for_df, orient="index")
        df.reset_index(inplace=True)
        df.rename(columns={"index": "date"}, inplace=True)

        # If your Pydantic model used aliases, the columns might already be
        # "1. open", "2. high", etc. This rename will unify them:
        column_mapping = {
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        }
        df.rename(columns=column_mapping, inplace=True)

        # Convert date to datetime and sort
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values(by="date", inplace=True)

        # Add calculated fields
        df["daily_return"] = df["close"].pct_change() * 100
        df["ma_5"] = df["close"].rolling(window=5).mean()
        df["volatility"] = df["daily_return"].rolling(window=10).std()

        return df

    except Exception as e:
        log_transformation_error("Failed to transform stock data", e)
        raise ValueError("Transformation process failed") from e

def save_transformed_data(transformed_data, stock_symbol, output_dir="output"):
    """
    Save the transformed stock data to a CSV file.

    Args:
        transformed_data (pd.DataFrame): Transformed stock data.
        stock_symbol (str): Stock symbol for dynamic file naming.
        output_dir (str): Directory to save the transformed data file.

    Returns:
        str: Path to the saved file.

    Raises:
        IOError: If file saving fails.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"data_{stock_symbol}_{timestamp}.csv"
        file_path = os.path.join(output_dir, file_name)
        transformed_data.to_csv(file_path, index=False)
        return file_path

    except Exception as e:
        log_transformation_error("Failed to save transformed data", e)
        raise IOError("Failed to save transformed data") from e

class VantageTransformation(BaseTransformation):
    def transform(self, validated_data):
        return transform_stock_data(validated_data)

    def save(self, transformed_data):
        stock_symbol = self.config.get("symbol")
        output_dir = self.config.get("output_dir", "output")
        return save_transformed_data(transformed_data, stock_symbol, output_dir)

