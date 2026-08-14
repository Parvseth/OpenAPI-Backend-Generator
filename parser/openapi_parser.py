import re
import yaml
import json
from typing import Dict, Any, List, Optional, Tuple
from parser.ir_models import (
    IRSpec, IRModel, IRField, IRParameter, IRRequestBody, IRResponse, IRRoute, IRRelationship
)
from parser.resolver import dereference_schema, resolve_ref

OPENAPI_TO_PYTHON_TYPES = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "List",
    "object": "Dict[str, Any]"
}

OPENAPI_TO_SQLALCHEMY_TYPES = {
    "string": "String",
    "integer": "Integer",
    "number": "Float",
    "boolean": "Boolean",
    "array": "JSON",
    "object": "JSON"
}

FORMAT_TO_PYTHON_TYPES = {
    "date-time": "datetime",
    "date": "date",
    "uuid": "UUID",
    "email": "str",
    "password": "str"
}

FORMAT_TO_SQLALCHEMY_TYPES = {
    "date-time": "DateTime",
    "date": "Date",
    "uuid": "String",
    "email": "String",
    "password": "String"
}

def to_camel_case(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]", " ", text)
    return "".join(word.capitalize() for word in s.split())

def to_snake_case(text: str) -> str:
    text = text.replace("-", "_").replace(" ", "_")
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().strip("_")

def map_openapi_type(prop_name: str, prop_schema: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Returns (python_type, pydantic_type, sqlalchemy_type) for a given OpenAPI property schema.
    """
    oa_type = prop_schema.get("type", "string")
    fmt = prop_schema.get("format")

    if fmt in FORMAT_TO_PYTHON_TYPES:
        py_type = FORMAT_TO_PYTHON_TYPES[fmt]
        sq_type = FORMAT_TO_SQLALCHEMY_TYPES[fmt]
        return py_type, py_type, sq_type

    if oa_type == "array":
        items = prop_schema.get("items", {})
        item_type = items.get("type", "str")
        py_item = OPENAPI_TO_PYTHON_TYPES.get(item_type, "str")
        return f"List[{py_item}]", f"List[{py_item}]", "JSON"

    py_type = OPENAPI_TO_PYTHON_TYPES.get(oa_type, "str")
    sq_type = OPENAPI_TO_SQLALCHEMY_TYPES.get(oa_type, "String")
    return py_type, py_type, sq_type

def parse_schema_to_model(model_name: str, schema: Dict[str, Any], full_spec: Dict[str, Any]) -> IRModel:
    schema = dereference_schema(schema, full_spec)
    description = schema.get("description", f"{model_name} model")
    table_name = to_snake_case(model_name) + "s"

    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    fields: List[IRField] = []
    has_pk = False

    for prop_name, prop_schema in properties.items():
        is_req = prop_name in required_fields
        py_type, pyd_type, sq_type = map_openapi_type(prop_name, prop_schema)

        is_pk = (prop_name == "id")
        if is_pk:
            has_pk = True

        field = IRField(
            name=prop_name,
            openapi_type=prop_schema.get("type", "string"),
            python_type=py_type,
            pydantic_type=pyd_type,
            sqlalchemy_type=sq_type,
            required=is_req,
            nullable=not is_req and not is_pk,
            description=prop_schema.get("description"),
            default=prop_schema.get("default"),
            format=prop_schema.get("format"),
            min_length=prop_schema.get("minLength"),
            max_length=prop_schema.get("maxLength"),
            pattern=prop_schema.get("pattern"),
            is_primary_key=is_pk,
            enum_values=prop_schema.get("enum")
        )
        fields.append(field)

    # Auto-add primary key 'id' if missing
    if not has_pk:
        fields.insert(0, IRField(
            name="id",
            openapi_type="integer",
            python_type="int",
            pydantic_type="int",
            sqlalchemy_type="Integer",
            required=True,
            nullable=False,
            is_primary_key=True,
            description="Auto-generated primary key"
        ))

    return IRModel(
        name=to_camel_case(model_name),
        table_name=table_name,
        description=description,
        fields=fields
    )

def parse_openapi_spec(spec_dict: Dict[str, Any]) -> IRSpec:
    title = spec_dict.get("info", {}).get("title", "Generated API Backend")
    version = spec_dict.get("info", {}).get("version", "1.0.0")
    description = spec_dict.get("info", {}).get("description", "")

    # Parse Models from components.schemas
    models: List[IRModel] = []
    schemas_dict = spec_dict.get("components", {}).get("schemas", {})
    if not schemas_dict:
        schemas_dict = spec_dict.get("schemas", {})

    for model_name, schema in schemas_dict.items():
        ir_model = parse_schema_to_model(model_name, schema, spec_dict)
        models.append(ir_model)

    # Parse Routes from paths
    routes: List[IRRoute] = []
    paths = spec_dict.get("paths", {})

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue

        for method, operation in path_item.items():
            if method.lower() not in ["get", "post", "put", "patch", "delete"]:
                continue

            summary = operation.get("summary", f"{method.upper()} {path}")
            op_id = operation.get("operationId")
            if not op_id:
                clean_path = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
                op_id = f"{method.lower()}_{clean_path or 'root'}"

            tags = operation.get("tags", ["default"])
            
            # Target model heuristic
            target_model = None
            if tags:
                matching_models = [m.name for m in models if m.name.lower() in tags[0].lower() or tags[0].lower() in m.name.lower()]
                if matching_models:
                    target_model = matching_models[0]
            if not target_model and models:
                target_model = models[0].name

            # Parameters
            params: List[IRParameter] = []
            for p in operation.get("parameters", []):
                if "$ref" in p:
                    p = resolve_ref(p["$ref"], spec_dict)
                p_name = p.get("name", "param")
                p_loc = p.get("in", "query")
                p_req = p.get("required", False)
                p_schema = p.get("schema", {})
                py_t, _, _ = map_openapi_type(p_name, p_schema)
                params.append(IRParameter(
                    name=p_name,
                    location=p_loc,
                    python_type=py_t,
                    required=p_req or (p_loc == "path"),
                    description=p.get("description")
                ))

            # Request Body
            request_body = None
            if "requestBody" in operation:
                rb_data = operation["requestBody"]
                if "$ref" in rb_data:
                    rb_data = resolve_ref(rb_data["$ref"], spec_dict)
                content = rb_data.get("content", {}).get("application/json", {})
                rb_schema = content.get("schema", {})
                ref_str = rb_schema.get("$ref", "")
                rb_model = ref_str.split("/")[-1] if ref_str else target_model

                request_body = IRRequestBody(
                    required=rb_data.get("required", False),
                    model_name=rb_model
                )

            # Responses
            responses: List[IRResponse] = []
            for status_code, resp_data in operation.get("responses", {}).items():
                try:
                    sc = int(status_code)
                except ValueError:
                    sc = 200

                if "$ref" in resp_data:
                    resp_data = resolve_ref(resp_data["$ref"], spec_dict)

                resp_desc = resp_data.get("description", "Response")
                resp_schema = resp_data.get("content", {}).get("application/json", {}).get("schema", {})

                resp_model = None
                is_list = False
                if "$ref" in resp_schema:
                    resp_model = resp_schema["$ref"].split("/")[-1]
                elif resp_schema.get("type") == "array":
                    is_list = True
                    items = resp_schema.get("items", {})
                    if "$ref" in items:
                        resp_model = items["$ref"].split("/")[-1]
                    else:
                        resp_model = target_model
                else:
                    resp_model = target_model

                responses.append(IRResponse(
                    status_code=sc,
                    description=resp_desc,
                    model_name=resp_model,
                    is_list=is_list
                ))

            routes.append(IRRoute(
                path=path,
                method=method.upper(),
                operation_id=to_snake_case(op_id),
                summary=summary,
                description=operation.get("description"),
                tags=tags,
                parameters=params,
                request_body=request_body,
                responses=responses,
                target_model=target_model,
                service_method_name=to_snake_case(op_id)
            ))

    return IRSpec(
        title=title,
        version=version,
        description=description,
        models=models,
        routes=routes
    )
