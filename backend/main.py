"""
main.py — FastAPI entry point for the AI-Powered Data Visualizer.

Exposes a single POST /upload-csv endpoint that orchestrates:
  csv_parser -> data_cleaner -> openai_service -> chart_generator
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.csv_parser import parse_csv
from services.data_cleaner import clean_data
from services.openai_service import get_chart_recommendation
from services.chart_generator import generate_chart

app = FastAPI(
    title="AI-Powered Data Visualizer",
    description="Upload a CSV, let AI recommend a chart, and get a rendered visualization.",
    version="0.1.0",
)

# Allow the Vite dev server to call the API without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Accept a CSV upload, clean the data, ask OpenAI for a chart recommendation,
    generate the chart, and return both the chart image and a cleaning report.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted.")

    # Step 1 — Parse the uploaded CSV into a DataFrame
    parsed = await parse_csv(file)
    df = parsed["dataframe"]
    schema = parsed["schema"]          # {column_name: dtype_string}
    sample_rows = parsed["sample_rows"]  # last 10 rows as list of dicts

    # Step 2 — Clean the data and collect a report of changes
    df_clean, cleaning_report = clean_data(df)

    # Step 3 — Ask OpenAI which chart to render
    chart_decision = get_chart_recommendation(schema, sample_rows)

    # Step 4 — Generate the chart and encode it as base64
    chart_image_b64 = generate_chart(df_clean, chart_decision)

    return {
        "chart_image": chart_image_b64,
        "cleaning_report": cleaning_report,
        "chart_decision": chart_decision,
    }
