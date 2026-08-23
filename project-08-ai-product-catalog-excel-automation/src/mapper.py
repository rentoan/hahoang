import json
from pathlib import Path

def load_mapping(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_alias_lookup(mapping):
    lookup = {}
    for canonical, aliases in mapping.items():
        for alias in aliases:
            lookup[alias.strip().lower()] = canonical
    return lookup

def resolve_columns(source_columns, mapping):
    alias_lookup = build_alias_lookup(mapping)
    resolved = {}
    for column in source_columns:
        canonical = alias_lookup.get(str(column).strip().lower())
        if canonical:
            resolved[column] = canonical
    return resolved
