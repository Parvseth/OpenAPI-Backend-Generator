import argparse
from parse_openapi import load_openapi_spec
from generate_models import generate_models
from generate_routes import generate_routes
from generate_tests import generate_tests
from logger import logger

def generate_backend_from_spec(spec: dict, output_dir: str):
    logger.info("Starting backend generation pipeline...")

    # Generate models
    if "components" in spec and "schemas" in spec["components"]:
        generate_models(spec["components"]["schemas"], output_dir)
    else:
        logger.warning("No components.schemas found in the spec.")

    # Generate routes
    if "paths" in spec:
        generate_routes(spec["paths"], output_dir)
    else:
        logger.warning("No paths found in the spec.")

    # Generate tests
    if "paths" in spec:
        generate_tests(spec["paths"], output_dir)
    else:
        logger.warning("No paths found for tests in the spec.")

    logger.info("Backend generation completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate backend from OpenAPI spec")
    parser.add_argument("--input", type=str, required=True, help="Path to OpenAPI YAML/JSON file")
    parser.add_argument("--output", type=str, default="./generated_backend", help="Output directory for generated files")
    args = parser.parse_args()

    spec = load_openapi_spec(args.input)
    generate_backend_from_spec(spec, args.output)
