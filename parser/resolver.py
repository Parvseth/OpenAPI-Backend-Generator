from typing import Any, Dict

def resolve_ref(ref_path: str, full_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolves JSON Pointer refs within an OpenAPI spec dictionary.
    Example: "#/components/schemas/User" -> returns the User schema dict.
    """
    if not ref_path.startswith("#/"):
        # Local ref only supported for now; external refs fall back to empty dict
        return {}
    
    parts = ref_path.lstrip("#/").split("/")
    current = full_spec
    for part in parts:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return {}
    return current if isinstance(current, dict) else {}

def dereference_schema(schema: Dict[str, Any], full_spec: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
    """
    Recursively dereferences $ref keys in a schema object up to depth limit.
    """
    if depth > 10 or not isinstance(schema, dict):
        return schema

    if "$ref" in schema:
        ref_target = resolve_ref(schema["$ref"], full_spec)
        # Merge properties if any alongside $ref
        merged = {k: v for k, v in schema.items() if k != "$ref"}
        merged.update(dereference_schema(ref_target, full_spec, depth + 1))
        return merged

    result = {}
    for key, value in schema.items():
        if isinstance(value, dict):
            result[key] = dereference_schema(value, full_spec, depth + 1)
        elif isinstance(value, list):
            result[key] = [
                dereference_schema(item, full_spec, depth + 1) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
            
    return result
