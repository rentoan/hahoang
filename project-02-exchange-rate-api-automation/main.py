from pathlib import Path
from datetime import datetime
import requests
import pandas as pd

API_URL = "https://api.frankfurter.dev/v2/rates"
BASE = "USD"
QUOTES = ["EUR", "GBP", "JPY", "VND"]
DATE_FROM = "2026-08-01"
DATE_TO = "2026-08-15"

OUTPUT_DIR = Path("output")
CSV_FILE = OUTPUT_DIR / "exchange_rates.csv"
EXCEL_FILE = OUTPUT_DIR / "Exchange_Rate_Report.xlsx"

def fetch_rates():
    params = {"base": BASE, "quotes": ",".join(QUOTES), "from": DATE_FROM, "to": DATE_TO}
    try:
        response = requests.get(API_URL, params=params, timeout=20)
        response.raise_for_status()
    except requests.Timeout as e:
        raise RuntimeError("API request timed out.") from e
    except requests.ConnectionError as e:
        raise RuntimeError("Could not connect to the exchange-rate API.") from e
    except requests.HTTPError as e:
        message = ""
        try:
            message = response.json().get("message", "")
        except Exception:
            pass
        raise RuntimeError(f"API returned HTTP {response.status_code}. {message}".strip()) from e

    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError("API returned invalid JSON.") from e

    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response structure.")
    return data

def validate_and_transform(data):
    required = {"date", "base", "quote", "rate"}
    clean_rows = []

    for i, row in enumerate(data, start=1):
        if not isinstance(row, dict) or not required.issubset(row):
            raise RuntimeError(f"Invalid API record at position {i}.")
        try:
            date = pd.to_datetime(row["date"], format="%Y-%m-%d")
            rate = float(row["rate"])
        except (ValueError, TypeError) as e:
            raise RuntimeError(f"Invalid data at API record {i}.") from e
        if rate <= 0:
            raise RuntimeError(f"Non-positive rate at API record {i}.")
        clean_rows.append({
            "Date": date,
            "Base": str(row["base"]).upper(),
            "Quote": str(row["quote"]).upper(),
            "Rate": rate,
        })

    df = pd.DataFrame(clean_rows)
    if df.empty:
        raise RuntimeError("API returned no rate data.")
    return df.sort_values(["Date", "Quote"]).reset_index(drop=True)

def build_summary(df):
    stats = (
        df.groupby("Quote")["Rate"]
        .agg(["min", "max", "mean"])
        .reset_index()
        .rename(columns={"Quote":"Currency","min":"Min Rate","max":"Max Rate","mean":"Average Rate"})
    )
    kpi = pd.DataFrame({
        "KPI":["Observations","First Date","Last Date"],
        "Value":[len(df),df["Date"].min().date().isoformat(),df["Date"].max().date().isoformat()]
    })
    return kpi, stats

def export_outputs(df, status, message):
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(CSV_FILE, index=False)
    kpi, stats = build_summary(df)
    run_log = pd.DataFrame([{
        "Run Time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Status":status,"Records":len(df),"Message":message
    }])
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Rates", index=False)
        kpi.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
        stats.to_excel(writer, sheet_name="Summary", index=False, startrow=6)
        run_log.to_excel(writer, sheet_name="Run_Log", index=False)

def main():
    print("Fetching exchange-rate data...")
    try:
        data = fetch_rates()
        df = validate_and_transform(data)
        export_outputs(df, "SUCCESS", "Data downloaded successfully.")
    except Exception as e:
        print(f"FAILED: {e}")
        return
    print(f"Records: {len(df)}")
    print(f"CSV:   {CSV_FILE}")
    print(f"Excel: {EXCEL_FILE}")

if __name__ == "__main__":
    main()
