import pytest
from parser.openapi_parser import parse_openapi_spec

SAMPLE_SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "Test E-Commerce API", "version": "2.0.0"},
    "components": {
        "schemas": {
            "Product": {
                "type": "object",
                "required": ["name", "price"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "price": {"type": "number"},
                    "is_active": {"type": "boolean", "default": True}
                }
            }
        }
    },
    "paths": {
        "/products": {
            "get": {
                "summary": "List all products",
                "operationId": "list_products",
                "responses": {
                    "200": {
                        "description": "A list of products",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Product"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

def test_parse_openapi_spec():
    ir_spec = parse_openapi_spec(SAMPLE_SPEC)
    assert ir_spec.title == "Test E-Commerce API"
    assert ir_spec.version == "2.0.0"
    assert len(ir_spec.models) == 1
    
    product_model = ir_spec.models[0]
    assert product_model.name == "Product"
    assert product_model.table_name == "products"
    assert len(product_model.fields) == 4

    assert len(ir_spec.routes) == 1
    route = ir_spec.routes[0]
    assert route.path == "/products"
    assert route.method == "GET"
    assert route.operation_id == "list_products"
