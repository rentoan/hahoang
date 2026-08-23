from pathlib import Path
from src.pipeline import process_catalog

if __name__ == "__main__":
    result = process_catalog(
        catalog_file=Path("sample_input/supplier_catalog_messy.csv"),
        catalog_filename="supplier_catalog_messy.csv",
        template_file=Path("template/product_upload_template.xlsx"),
        completed_output=Path("output/completed_template.xlsx"),
        errors_output=Path("output/validation_errors.xlsx"),
    )
    print(result)
