"""
openai_service.py — Calls the OpenAI API to recommend a chart type.
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a data visualization expert. Always respond in JSON. "
    "Return a JSON object with exactly these keys: "
    "chart_type (one of: line, bar, scatter, pie), "
    "x_axis (column name), "
    "y_axis (column name), "
    "group_by (column name or null), "
    "reason (short explanation)."
)


def get_chart_recommendation(schema: dict, sample_rows: list) -> dict:
    """
    Ask gpt-4o-mini which chart type best represents the given dataset.

    Args:
        schema      : {column_name: dtype_string} describing each column.
        sample_rows : Up to 10 rows of actual data as a list of dicts.

    Returns:
        Parsed JSON dict with keys: chart_type, x_axis, y_axis, group_by, reason.
    """
    user_message = (
        f"Dataset schema:\n{json.dumps(schema, indent=2)}\n\n"
        f"Sample rows (up to 10):\n{json.dumps(sample_rows, indent=2, default=str)}\n\n"
        "Which chart type best visualises this data? Respond only with valid JSON."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content
    return json.loads(raw_content)
