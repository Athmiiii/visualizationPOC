"""
csv_parser.py — Parses an uploaded CSV file using Pandas.
"""

import io
import pandas as pd
from fastapi import UploadFile


async def parse_csv(file: UploadFile) -> dict:
    """
    Read an uploaded CSV file into a Pandas DataFrame.

    Returns a dict containing:
      - 'dataframe'  : the raw DataFrame
      - 'schema'     : {column_name: dtype_as_string} mapping
      - 'sample_rows': last 10 rows serialised to a list of dicts
    """
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
    sample_rows = df.tail(10).to_dict(orient="records")

    return {
        "dataframe": df,
        "schema": schema,
        "sample_rows": sample_rows,
    }
