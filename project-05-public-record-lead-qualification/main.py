from pathlib import Path
import csv
import re

INPUT_DIR = Path("input")
DOCUMENT_DIR = INPUT_DIR / "documents"
LEADS_FILE = INPUT_DIR / "leads.csv"
OUTPUT_DIR = Path("output")

SURPLUS_THRESHOLD = 35000.0

LENDER_KEYWORDS = [
    "bank",
    "mortgage",
    "servicer",
    "financial",
    "credit union",
]

SALE_PATTERNS = [
    r"true consideration.*?\$([\d,]+\.\d{2})",
    r"purchase price paid by grantee:\s*\$([\d,]+\.\d{2})",
    r"final bid and sale amount:\s*\$([\d,]+\.\d{2})",
    r"sold for the sum of\s*\$([\d,]+\.\d{2})",
]

DEBT_PATTERNS = [
    r"amount due.*?is\s*\$([\d,]+\.\d{2})",
    r"satisfaction of the sum of\s*\$([\d,]+\.\d{2})",
    r"foreclosure judgment amount.*?:\s*\$([\d,]+\.\d{2})",
    r"advances to be satisfied total\s*\$([\d,]+\.\d{2})",
]

PURCHASER_PATTERNS = [
    r"purchaser at sheriff sale is\s+(.+)",
    r"grantee / winning bidder:\s*(.+)",
    r"new owner / purchaser:\s*(.+)",
    r"buyer:\s*(.+)",
]


def extract_money(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def extract_text(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return match.group(1).strip()
    return None


def classify_purchaser(name):
    if not name:
        return "Manual Review"

    lower = name.lower()

    if any(keyword in lower for keyword in LENDER_KEYWORDS):
        return "Lender/Creditor"

    # In production, ambiguous entities should be reviewed rather than guessed.
    if "loan" in lower or "capital" in lower:
        return "Manual Review"

    return "Third Party"


def process_lead(lead):
    document_path = DOCUMENT_DIR / lead["DocumentFile"]

    if not document_path.exists():
        return {
            **lead,
            "ReviewStatus": "Manual Review",
            "ReviewReason": "Document file not found",
        }

    text = document_path.read_text(encoding="utf-8")

    sale_price = extract_money(text, SALE_PATTERNS)
    debt = extract_money(text, DEBT_PATTERNS)
    purchaser = extract_text(text, PURCHASER_PATTERNS)

    missing = []
    if sale_price is None:
        missing.append("sale price")
    if debt is None:
        missing.append("debt")
    if purchaser is None:
        missing.append("purchaser")

    if missing:
        return {
            **lead,
            "ReviewStatus": "Manual Review",
            "ReviewReason": "Could not reliably extract: " + ", ".join(missing),
        }

    purchaser_type = classify_purchaser(purchaser)

    if purchaser_type == "Manual Review":
        return {
            **lead,
            "FinalSalePrice": sale_price,
            "DebtAmount": debt,
            "CalculatedDifference": round(sale_price - debt, 2),
            "Purchaser": purchaser,
            "PurchaserType": purchaser_type,
            "ReviewStatus": "Manual Review",
            "ReviewReason": "Purchaser classification is ambiguous",
        }

    difference = round(sale_price - debt, 2)
    third_party = purchaser_type == "Third Party"
    qualified = difference >= SURPLUS_THRESHOLD and third_party

    return {
        **lead,
        "FinalSalePrice": sale_price,
        "DebtAmount": debt,
        "CalculatedDifference": difference,
        "Purchaser": purchaser,
        "PurchaserType": purchaser_type,
        "ThirdPartyBuyer": "Yes" if third_party else "No",
        "Qualified": "Yes" if qualified else "No",
        "ReviewStatus": "Automated",
        "ReviewReason": "",
    }


def write_csv(path, rows):
    if not rows:
        return

    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with LEADS_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        leads = list(csv.DictReader(f))

    results = [process_lead(lead) for lead in leads]

    automated = [
        r for r in results
        if r.get("ReviewStatus") == "Automated"
    ]

    qualified = [
        r for r in automated
        if r.get("Qualified") == "Yes"
    ]

    review_queue = [
        r for r in results
        if r.get("ReviewStatus") == "Manual Review"
    ]

    write_csv(OUTPUT_DIR / "all_results.csv", results)
    write_csv(OUTPUT_DIR / "qualified_leads.csv", qualified)
    write_csv(OUTPUT_DIR / "review_queue.csv", review_queue)

    print(f"Records processed: {len(results)}")
    print(f"Qualified leads: {len(qualified)}")
    print(f"Manual review: {len(review_queue)}")


if __name__ == "__main__":
    main()
