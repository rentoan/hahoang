# Public Record Lead Qualification Pipeline

> **Portfolio Project – Simulated Client Requirement**

A Python data pipeline that qualifies foreclosure-surplus leads using information extracted from deed documents.

## Business Rule

A lead is qualified only when:

```text
Final Sale Price - Foreclosure Debt >= $35,000
AND
Purchaser is a Third Party
```

Banks, mortgage lenders, mortgage servicers, and creditors do not qualify as third-party purchasers.

## Workflow

```text
Lead CSV
   |
   v
Deed Document
   |
   v
Rule-Based Extraction
   |
   +--> Sale Price
   +--> Debt Amount
   +--> Purchaser
   |
   v
Purchaser Classification
   |
   +--> Third Party
   +--> Lender / Creditor
   +--> Manual Review
   |
   v
Surplus Calculation
   |
   v
Qualified / Not Qualified
   |
   +--> qualified_leads.csv
   +--> all_results.csv
   +--> review_queue.csv
```

## Why a Review Queue Matters

The system does not guess when document extraction or purchaser classification is uncertain.

Ambiguous cases are routed to manual review.

That design is important for workflows involving legal/public-record documents where false positives can be expensive.

## Document Extraction

The sample deed documents intentionally use different wording.

For example, sale price may appear as:

- `true consideration ... is $194,000.00`
- `purchase price paid by grantee: $194,000.00`
- `final bid and sale amount: $194,000.00`
- `sold for the sum of $194,000.00`

The extraction logic therefore supports multiple patterns instead of relying on one exact phrase.

## Sample Output

The repository includes:

- `all_results.csv`
- `qualified_leads.csv`
- `review_queue.csv`
- `Public_Record_Lead_Qualification_Report.xlsx`

## Excel Report

The workbook contains:

- `Summary`
- `All_Results`
- `Qualified_Leads`
- `Review_Queue`
- `Run_Log`

## Technologies

- Python
- CSV processing
- regular expressions
- document text extraction
- rule-based entity classification
- business-rule automation
- Excel reporting

## Run

```bash
python main.py
```

Place:

```text
input/
├── leads.csv
└── documents/
```

and the script creates CSV outputs in `output/`.

## Portfolio Scope

This portfolio version deliberately uses synthetic text documents.

It does **not** claim to implement:

- live county website crawling
- OCR of scanned deed images
- CAPTCHA bypassing
- authentication automation
- 70,000-record production crawling
- legal determination of entitlement

Those would be separate production engineering phases.

## Portfolio Note

All names, addresses, documents and transaction values in this repository are synthetic.
No real foreclosure or personal data is included.
