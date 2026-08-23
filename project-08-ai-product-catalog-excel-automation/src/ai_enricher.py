import json
from .config import AI_MODE, OPENAI_MODEL

def mock_enrich(record):
    name = " ".join(record["name"].split())
    brand = record["brand"]
    category = record["category"]
    description = " ".join(record.get("description","").split())

    title = (
        name if name.lower().startswith(brand.lower())
        else f"{brand} {name}"
    )[:80]

    if description and not description.endswith("."):
        description += "."

    return {
        "product_title": title,
        "description": description,
        "features": [
            f"Category: {category}",
            "Standardized for catalog consistency",
            "Portfolio mock AI enrichment",
        ],
    }

def openai_enrich(record):
    from openai import OpenAI

    client = OpenAI()

    prompt = f"""
Standardize this industrial product catalog record.

Return JSON with exactly:
product_title: concise title, max 80 characters
description: factual product description, no invented specifications
features: array of exactly 3 short factual features

Input:
Brand: {record['brand']}
Name: {record['name']}
Category: {record['category']}
Description: {record.get('description','')}

Do not invent dimensions, certifications, materials, performance values,
or other facts that are not present in the input.
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        text={"format": {"type": "json_object"}},
    )

    data = json.loads(response.output_text)

    if not isinstance(data.get("features"), list):
        raise RuntimeError("AI response does not contain a features list.")

    data["features"] = (data["features"] + ["","",""])[:3]
    data["product_title"] = str(data["product_title"])[:80]

    return data

def enrich(record):
    if AI_MODE == "openai":
        return openai_enrich(record)
    return mock_enrich(record)
