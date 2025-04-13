import pandas as pd
import os
from datetime import datetime

from interfaces.transformation import BaseTransformation
from Error_Handling.transformation_errors import log_transformation_error

def transform_fmp_data(validated_data: dict) -> pd.DataFrame:
    """
    Converts validated FMP data into a Pandas DataFrame.

    Returns:
        pd.DataFrame
    """
    try:
        dict_for_df = {
            ts: dp.dict() for ts, dp in validated_data.items()
        }
        df = pd.DataFrame.from_dict(dict_for_df, orient="index")
        df.reset_index(inplace=True)
        df.rename(columns={"index": "date"}, inplace=True)
        return df
    except Exception as e:
        log_transformation_error(str(e))
        raise ValueError("FMP Transformation failed") from e

class FMPTransformation(BaseTransformation):
    def __init__(self, config):
        self.output_dir = config.get("output_dir", "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def transform(self, validated_data):
        return transform_fmp_data(validated_data)

    def save(self, df: pd.DataFrame) -> str:
        filename = f"fmp_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path = os.path.join(self.output_dir, filename)
        df.to_csv(path, index=False)
        return path

