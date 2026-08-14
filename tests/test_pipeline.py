import os
import tempfile
import pytest
from parse_openapi import load_openapi_spec
from parser.openapi_parser import parse_openapi_spec
from codegen.engine import generate_clean_backend

def test_pipeline_end_to_end():
    spec_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "openapi3.yaml")
    if not os.path.exists(spec_path):
        pytest.skip("openapi3.yaml not found")

    raw_spec = load_openapi_spec(spec_path)
    ir_spec = parse_openapi_spec(raw_spec)

    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = os.path.join(tmp_dir, "backend")
        generate_clean_backend(ir_spec, out_dir, use_ai=False)

        assert os.path.exists(os.path.join(out_dir, "app", "main.py"))
        assert os.path.exists(os.path.join(out_dir, "app", "models", "models.py"))
        assert os.path.exists(os.path.join(out_dir, "app", "schemas", "schemas.py"))
        assert os.path.exists(os.path.join(out_dir, "Dockerfile"))
        assert os.path.exists(os.path.join(out_dir, "docker-compose.yml"))
        assert os.path.exists(os.path.join(out_dir, "requirements.txt"))
