import pandas as pd
import os
from datetime import datetime

from interfaces.transformation import BaseTransformation
from Error_Handling.transformation_errors import log_transformation_error

def transform_finnhub_data(validated_data):
    try:
        df = pd.DataFrame({
            "date": pd.to_datetime(validated_data.t, unit="s"),
            "open": validated_data.o,
            "high": validated_data.h,
            "low": validated_data.l,
            "close": validated_data.c,
            "volume": validated_data.v
        })

        df.sort_values(by="date", inplace=True)
        df["daily_return"] = df["close"].pct_change() * 100
        df["ma_5"] = df["close"].rolling(window=5).mean()
        df["volatility"] = df["daily_return"].rolling(window=10).std()
        return df

    except Exception as e:
        log_transformation_error("Failed to transform Finnhub data", e)
        raise ValueError("Transformation process failed") from e

def save_transformed_data(transformed_data, stock_symbol, output_dir="output"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"data_finnhub_{stock_symbol}_{timestamp}.csv"
        file_path = os.path.join(output_dir, file_name)
        transformed_data.to_csv(file_path, index=False)
        return file_path

    except Exception as e:
        log_transformation_error("Failed to save transformed data", e)
        raise IOError("Failed to save transformed data") from e

class FinnhubTransformation(BaseTransformation):
    def transform(self, validated_data):
        return transform_finnhub_data(validated_data)

    def save(self, transformed_data):
        stock_symbol = self.config.get("symbol")
        output_dir = self.config.get("output_dir", "output")
        print(f"[DEBUG] Saving Finnhub data to output_dir: {output_dir}")
        return save_transformed_data(transformed_data, stock_symbol, output_dir)

