from pathlib import Path
import pandas as pd
import re

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "Sales_Report.xlsx"


def clean_text(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NA
    return str(value).strip()


def clean_date(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NaT

    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return pd.to_datetime(text, format=fmt)
        except ValueError:
            pass

    return pd.NaT


def clean_quantity(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NA
    try:
        number = float(str(value).strip())
        return int(number) if number.is_integer() else number
    except ValueError:
        return value


def clean_unit_price(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NA

    text = str(value).strip().replace("$", "")
    text = re.sub(r"(?i)\bUSD\b", "", text)
    text = text.replace(",", "").strip()

    try:
        return float(text)
    except ValueError:
        return value


def clean_discount(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NA

    text = str(value).strip()

    try:
        return float(text[:-1].strip()) / 100 if text.endswith("%") else float(text)
    except ValueError:
        return value


def clean_dataframe(df):
    text_columns = ["OrderID", "Branch", "CustomerID", "ProductID", "ProductName"]

    for col in text_columns:
        df[col] = df[col].apply(clean_text)

    df["Branch"] = df["Branch"].apply(
        lambda x: x.upper() if isinstance(x, str) else x
    )

    df["OrderDate"] = df["OrderDate"].apply(clean_date)
    df["Quantity"] = df["Quantity"].apply(clean_quantity)
    df["UnitPrice"] = df["UnitPrice"].apply(clean_unit_price)
    df["Discount"] = df["Discount"].apply(clean_discount)

    return df


def is_missing(value):
    return pd.isna(value) or (isinstance(value, str) and value.strip() == "")


def validate_row(row, duplicate_order_ids):
    errors = []

    required_fields = [
        "OrderID", "OrderDate", "Branch", "CustomerID",
        "ProductID", "ProductName", "Quantity",
        "UnitPrice", "Discount"
    ]

    for field in required_fields:
        if is_missing(row[field]):
            errors.append(f"{field} is missing")

    if not is_missing(row["OrderID"]) and row["OrderID"] in duplicate_order_ids:
        errors.append("OrderID is duplicated")

    if not is_missing(row["Quantity"]):
        try:
            q = float(row["Quantity"])
            if not q.is_integer():
                errors.append("Quantity must be an integer")
            elif q <= 0:
                errors.append("Quantity must be greater than 0")
        except (ValueError, TypeError):
            errors.append("Quantity is not numeric")

    if not is_missing(row["UnitPrice"]):
        try:
            if float(row["UnitPrice"]) <= 0:
                errors.append("UnitPrice must be greater than 0")
        except (ValueError, TypeError):
            errors.append("UnitPrice is not numeric")

    if not is_missing(row["Discount"]):
        try:
            d = float(row["Discount"])
            if d < 0 or d > 1:
                errors.append("Discount must be between 0 and 1")
        except (ValueError, TypeError):
            errors.append("Discount is not numeric")

    return errors


def main():
    csv_files = sorted(INPUT_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in input/.")
        return

    dataframes = []

    for file in csv_files:
        df = pd.read_csv(file)
        df["SourceFile"] = file.name
        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)
    df = clean_dataframe(df)

    duplicate_mask = df["OrderID"].duplicated(keep=False)
    duplicate_order_ids = set(
        df.loc[duplicate_mask, "OrderID"].dropna().tolist()
    )

    df["ErrorReason"] = df.apply(
        lambda row: "; ".join(validate_row(row, duplicate_order_ids)),
        axis=1
    )

    valid_df = df[df["ErrorReason"] == ""].copy()
    error_df = df[df["ErrorReason"] != ""].copy()

    valid_df["Quantity"] = valid_df["Quantity"].astype(int)
    valid_df["UnitPrice"] = valid_df["UnitPrice"].astype(float)
    valid_df["Discount"] = valid_df["Discount"].astype(float)

    valid_df["Revenue"] = (
        valid_df["Quantity"]
        * valid_df["UnitPrice"]
        * (1 - valid_df["Discount"])
    ).round(2)

    total_summary = pd.DataFrame({
        "KPI": ["Valid Orders", "Total Revenue"],
        "Value": [len(valid_df), valid_df["Revenue"].sum().round(2)]
    })

    branch_summary = (
        valid_df.groupby("Branch", as_index=False)
        .agg(
            Orders=("OrderID", "count"),
            Revenue=("Revenue", "sum")
        )
    )
    branch_summary["Revenue"] = branch_summary["Revenue"].round(2)

    OUTPUT_DIR.mkdir(exist_ok=True)

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        valid_columns = [
            "OrderID", "OrderDate", "Branch", "CustomerID",
            "ProductID", "ProductName", "Quantity",
            "UnitPrice", "Discount", "Revenue", "SourceFile"
        ]

        error_columns = [
            "OrderID", "OrderDate", "Branch", "CustomerID",
            "ProductID", "ProductName", "Quantity",
            "UnitPrice", "Discount", "SourceFile", "ErrorReason"
        ]

        valid_df[valid_columns].to_excel(
            writer, sheet_name="Clean_Data", index=False
        )

        error_df[error_columns].to_excel(
            writer, sheet_name="Errors", index=False
        )

        total_summary.to_excel(
            writer, sheet_name="Summary", index=False, startrow=0
        )

        branch_summary.to_excel(
            writer, sheet_name="Summary", index=False, startrow=5
        )

    print(f"Input records : {len(df)}")
    print(f"Valid records : {len(valid_df)}")
    print(f"Error records : {len(error_df)}")
    print(f"Report created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
