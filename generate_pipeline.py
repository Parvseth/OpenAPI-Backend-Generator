import argparse
from parse_openapi import load_openapi_spec
from parser.openapi_parser import parse_openapi_spec
from codegen.engine import generate_clean_backend
from logger import logger

def generate_backend_from_spec(spec_path: str, output_dir: str, use_ai: bool = True):
    logger.info("Starting enterprise backend generation pipeline...")
    raw_spec = load_openapi_spec(spec_path)
    ir_spec = parse_openapi_spec(raw_spec)
    generate_clean_backend(ir_spec, output_dir, use_ai=use_ai)
    logger.info("Backend generation pipeline completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate enterprise FastAPI backend from OpenAPI spec")
    parser.add_argument("--input", type=str, required=True, help="Path to OpenAPI YAML/JSON file")
    parser.add_argument("--output", type=str, default="./generated_backend", help="Output directory for generated project")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI logic generation")
    args = parser.parse_args()

    generate_backend_from_spec(args.input, args.output, use_ai=not args.no_ai)
