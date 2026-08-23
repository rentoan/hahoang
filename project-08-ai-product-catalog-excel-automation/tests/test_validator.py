from src.validator import validate_record

def test_valid_record():
    seen = set()
    record, errors = validate_record({
        "sku":"A-1",
        "brand":"Acme",
        "name":"Test Product",
        "price":"10.50",
        "category":"Safety",
        "description":"Test",
        "upc":"081234567890",
        "active":"Y",
    }, seen)
    assert errors == []
    assert record["price"] == 10.50

def test_duplicate_sku():
    seen = {"A-1"}
    _, errors = validate_record({
        "sku":"A-1",
        "brand":"Acme",
        "name":"Test Product",
        "price":"10",
        "category":"Safety",
        "upc":"",
        "active":"Y",
    }, seen)
    assert "Duplicate SKU" in errors
