from src.mapper import resolve_columns

def test_alias_mapping():
    mapping = {
        "sku":["SKU","Item No"],
        "brand":["Brand","MFG Brand"]
    }
    result = resolve_columns(
        ["Item No","MFG Brand","Something Else"],
        mapping
    )
    assert result["Item No"] == "sku"
    assert result["MFG Brand"] == "brand"
