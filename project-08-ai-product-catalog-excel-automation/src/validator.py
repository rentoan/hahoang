from .config import ALLOWED_CATEGORIES, MAX_TITLE_LENGTH

def normalize_active(value):
    text = str(value or "Y").strip().upper()
    mapping = {
        "YES":"Y", "TRUE":"Y", "1":"Y", "ACTIVE":"Y",
        "NO":"N", "FALSE":"N", "0":"N", "INACTIVE":"N",
    }
    return mapping.get(text, text)

def parse_price(value):
    text = str(value or "").replace("$","").replace(",","").strip()
    return float(text)

def validate_record(record, seen_skus):
    errors = []

    sku = str(record.get("sku","") or "").strip()
    brand = str(record.get("brand","") or "").strip()
    name = str(record.get("name","") or "").strip()
    category = str(record.get("category","") or "").strip()
    upc = str(record.get("upc","") or "").strip()
    active = normalize_active(record.get("active","Y"))

    if not sku:
        errors.append("SKU is required")
    elif sku in seen_skus:
        errors.append("Duplicate SKU")
    else:
        seen_skus.add(sku)

    if not brand:
        errors.append("Brand is required")

    if not name:
        errors.append("Product name is required")
    elif len(name) > MAX_TITLE_LENGTH:
        errors.append(
            f"Product name exceeds {MAX_TITLE_LENGTH} characters"
        )

    try:
        price = parse_price(record.get("price"))
        if price <= 0:
            errors.append("Price must be greater than 0")
    except Exception:
        price = None
        errors.append("Price is not numeric")

    if category not in ALLOWED_CATEGORIES:
        errors.append("Category is not allowed")

    if upc and (not upc.isdigit() or len(upc) != 12):
        errors.append("UPC must contain exactly 12 digits")

    if active not in {"Y","N"}:
        errors.append("Active must be Y or N")

    normalized = dict(record)
    normalized.update({
        "sku":sku,
        "brand":brand,
        "name":name,
        "category":category,
        "upc":upc,
        "active":active,
        "price":price,
        "description":str(record.get("description","") or "").strip(),
    })

    return normalized, errors
