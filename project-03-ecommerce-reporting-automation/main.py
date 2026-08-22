from pathlib import Path
from datetime import datetime
import pandas as pd

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "Ecommerce_Performance_Report.xlsx"

ORDERS_FILE = INPUT_DIR / "orders.csv"
PRODUCTS_FILE = INPUT_DIR / "products.csv"
REFUNDS_FILE = INPUT_DIR / "refunds.csv"

def load_data():
    orders = pd.read_csv(ORDERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    refunds = pd.read_csv(REFUNDS_FILE)
    return orders, products, refunds

def validate_inputs(orders, products, refunds):
    required_orders = {"OrderID","OrderDate","Store","SKU","Quantity","UnitPrice"}
    required_products = {"SKU","ProductName","Category","UnitCost","CurrentStock","ReorderLevel"}
    required_refunds = {"RefundID","OrderID","RefundAmount","Reason"}

    if not required_orders.issubset(orders.columns):
        raise ValueError("orders.csv is missing required columns.")
    if not required_products.issubset(products.columns):
        raise ValueError("products.csv is missing required columns.")
    if not required_refunds.issubset(refunds.columns):
        raise ValueError("refunds.csv is missing required columns.")

def build_report_data(orders, products, refunds):
    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"], errors="coerce")
    orders["Quantity"] = pd.to_numeric(orders["Quantity"], errors="coerce")
    orders["UnitPrice"] = pd.to_numeric(orders["UnitPrice"], errors="coerce")
    products["UnitCost"] = pd.to_numeric(products["UnitCost"], errors="coerce")
    refunds["RefundAmount"] = pd.to_numeric(refunds["RefundAmount"], errors="coerce").fillna(0)

    refund_summary = (
        refunds.groupby("OrderID", as_index=False)["RefundAmount"]
        .sum()
    )

    df = orders.merge(products, on="SKU", how="left")
    df = df.merge(refund_summary, on="OrderID", how="left")
    df["RefundAmount"] = df["RefundAmount"].fillna(0)

    df["GrossSales"] = df["Quantity"] * df["UnitPrice"]
    df["NetSales"] = df["GrossSales"] - df["RefundAmount"]
    df["COGS"] = df["Quantity"] * df["UnitCost"]
    df["Profit"] = df["NetSales"] - df["COGS"]

    product_perf = (
        df.groupby(["SKU","ProductName","Category"], as_index=False)
        .agg(
            Units_Sold=("Quantity","sum"),
            Net_Sales=("NetSales","sum"),
            Refunds=("RefundAmount","sum"),
            Profit=("Profit","sum")
        )
    )

    inventory = products[[
        "SKU","ProductName","CurrentStock","ReorderLevel"
    ]].copy()
    inventory["Status"] = inventory.apply(
        lambda r: "REORDER"
        if r["CurrentStock"] <= r["ReorderLevel"]
        else "OK",
        axis=1
    )

    store_summary = (
        df.groupby("Store", as_index=False)
        .agg(
            Orders=("OrderID","count"),
            Net_Sales=("NetSales","sum"),
            Profit=("Profit","sum")
        )
    )

    return df, product_perf, inventory, store_summary

def export_excel(df, product_perf, inventory, store_summary):
    OUTPUT_DIR.mkdir(exist_ok=True)

    kpi = pd.DataFrame({
        "KPI": ["Orders","Gross Sales","Refunds","Net Sales","Gross Profit"],
        "Value": [
            len(df),
            df["GrossSales"].sum(),
            df["RefundAmount"].sum(),
            df["NetSales"].sum(),
            df["Profit"].sum()
        ]
    })

    run_log = pd.DataFrame([{
        "Run Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Status": "SUCCESS",
        "Orders": len(df),
        "Message": "Orders, products and refunds consolidated successfully."
    }])

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        kpi.to_excel(writer, sheet_name="Dashboard", index=False, startrow=0)
        store_summary.to_excel(writer, sheet_name="Dashboard", index=False, startrow=8)
        df.to_excel(writer, sheet_name="Orders_Enriched", index=False)
        product_perf.to_excel(writer, sheet_name="Product_Performance", index=False)
        inventory.to_excel(writer, sheet_name="Inventory_Alerts", index=False)
        run_log.to_excel(writer, sheet_name="Run_Log", index=False)

def main():
    try:
        orders, products, refunds = load_data()
        validate_inputs(orders, products, refunds)
        df, product_perf, inventory, store_summary = build_report_data(
            orders, products, refunds
        )
        export_excel(df, product_perf, inventory, store_summary)
    except Exception as e:
        print(f"FAILED: {e}")
        return

    print(f"Orders processed: {len(df)}")
    print(f"Report created: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
