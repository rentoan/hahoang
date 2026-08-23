from pathlib import Path
import tempfile

import streamlit as st

from src.pipeline import process_catalog

st.set_page_config(
    page_title="AI Catalog → Excel Automation",
    layout="wide",
)

st.title("AI Product Catalog → Excel Template Automation")
st.caption(
    "Upload a supplier catalog and an Excel template. "
    "The app maps columns, validates records, enriches product content, "
    "and produces a completed workbook."
)

with st.sidebar:
    st.subheader("AI Mode")
    st.write(
        "Default repository mode is MOCK. "
        "Set AI_MODE=openai and OPENAI_API_KEY in the environment "
        "to use the OpenAI API."
    )

catalog = st.file_uploader(
    "Supplier catalog",
    type=["csv","xlsx","xlsm"]
)

template = st.file_uploader(
    "Excel template",
    type=["xlsx","xlsm"]
)

if st.button("Process Catalog", type="primary"):
    if not catalog or not template:
        st.error("Please upload both a catalog and a template.")
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)

            template_path = temp_dir / template.name
            template_path.write_bytes(template.getvalue())

            completed_path = temp_dir / (
                "completed_template" + template_path.suffix
            )
            errors_path = temp_dir / "validation_errors.xlsx"

            try:
                result = process_catalog(
                    catalog,
                    catalog.name,
                    template_path,
                    completed_path,
                    errors_path,
                )
            except Exception as e:
                st.exception(e)
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("Source Rows", result["source_rows"])
                c2.metric("Valid Products", result["valid_products"])
                c3.metric(
                    "Validation Errors",
                    result["validation_errors"]
                )

                st.success("Processing complete.")

                st.download_button(
                    "Download Completed Template",
                    data=completed_path.read_bytes(),
                    file_name=completed_path.name,
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                )

                st.download_button(
                    "Download Validation Errors",
                    data=errors_path.read_bytes(),
                    file_name=errors_path.name,
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                )
