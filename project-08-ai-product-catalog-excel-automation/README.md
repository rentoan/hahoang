# AI Product Catalog → Excel Template Automation

> **Portfolio Project – Simulated Client Requirement**

A reusable business automation workflow for converting inconsistent supplier catalogs into a strict Excel product-upload template.

## Business Problem

Suppliers send product data using different CSV/XLSX column names and inconsistent text formats.

The client needs to transform those catalogs into a controlled Excel template without manually copying and reformatting hundreds or thousands of rows.

## Workflow

```text
Supplier CSV / XLSX
        |
        v
Column Mapping
        |
        v
Normalize + Validate
       / \
      /   \
 Valid     Errors
   |         |
   v         v
AI Content  Validation Report
Enrichment
   |
   v
Excel Template Writer
   |
   v
Completed Multi-Sheet Workbook
```

## What the Project Demonstrates

- CSV / XLSX ingestion
- schema and column mapping
- data normalization
- validation and error reporting
- duplicate detection
- product-catalog business rules
- OpenAI API integration
- deterministic mock AI mode
- Excel template preservation
- multi-sheet workbook output
- Streamlit upload / process / download workflow

## Sample Dataset

The synthetic catalog contains **16 source rows**:

- **10 valid products**
- **6 validation-error rows**

The invalid rows intentionally include:

- missing SKU
- invalid price
- duplicate SKU
- over-length title
- invalid UPC
- unsupported category

## AI Modes

### Mock Mode

Default:

```text
AI_MODE=mock
```

This makes the repository fully runnable without an API key.

### OpenAI Mode

```text
AI_MODE=openai
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.5
```

The implementation uses the OpenAI Python SDK `responses.create(...)` flow and expects structured JSON output.

The AI prompt explicitly instructs the model **not to invent product specifications** that are absent from the source catalog.

## Excel Template Preservation

The application writes only to the `Product_Upload` data area.

The design preserves:

- sheet names
- unrelated sheets
- template headers
- lookup sheets
- formulas outside the populated data area

The repository contains a synthetic multi-sheet template:

```text
Instructions
Product_Upload
Category_Lookup
Summary
```

## Streamlit UI

Run:

```bash
streamlit run app.py
```

Workflow:

```text
Upload supplier catalog
        ↓
Upload Excel template
        ↓
Process Catalog
        ↓
KPIs
        ↓
Download completed template
Download validation errors
```

## CLI Demo

```bash
python main.py
```

## Project Structure

```text
project-08-ai-product-catalog-excel-automation/
├── README.md
├── customer_requirements.txt
├── .env.example
├── requirements.txt
├── mapping_config.json
├── app.py
├── main.py
├── src/
│   ├── config.py
│   ├── mapper.py
│   ├── validator.py
│   ├── ai_enricher.py
│   ├── excel_writer.py
│   └── pipeline.py
├── sample_input/
│   └── supplier_catalog_messy.csv
├── template/
│   └── product_upload_template.xlsx
├── sample_output/
│   ├── completed_template.xlsx
│   ├── validation_errors.xlsx
│   └── processing_summary.csv
├── tests/
└── screenshots/
```

## Production Extensions

A real client project could add:

- supplier-specific saved mappings
- fuzzy/interactive column mapping
- large-file batching
- background processing queue
- database job history
- per-field confidence / manual approval
- category taxonomy mapping
- `.xlsm` / VBA preservation testing
- Shopify / ERP / PIM API integrations
- product image processing
- cloud deployment and authentication

## Portfolio Integrity

All data is synthetic.

This project demonstrates the engineering workflow and does not claim access to any client's private ERP, marketplace, or product catalog.
