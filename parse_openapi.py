import yaml
import json

def load_openapi_spec(filepath: str) -> dict:
    if filepath.endswith(".yaml") or filepath.endswith(".yml"):
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif filepath.endswith(".json"):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format for OpenAPI spec.")
