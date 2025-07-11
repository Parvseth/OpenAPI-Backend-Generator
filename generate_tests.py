import os
from jinja2 import Environment, FileSystemLoader
from logger import logger

env = Environment(loader=FileSystemLoader("templates"))

def generate_tests(paths: dict, output_dir: str):
    template = env.get_template("test_template.j2")
    tests_path = os.path.join(output_dir, "tests")
    os.makedirs(tests_path, exist_ok=True)

    for path, methods in paths.items():
        test_name = path.strip("/").replace("/", "_").replace("{", "").replace("}", "") or "root"
        test_cases = []

        for method, details in methods.items():
            operation_id = details.get("operationId", f"{method}_{test_name}")
            test_cases.append({
                "method": method.upper(),
                "path": path,
                "operationId": operation_id
            })

        rendered = template.render(tests=test_cases)
        with open(os.path.join(tests_path, f"test_{test_name}.py"), "w", encoding="utf-8") as f:
            f.write(rendered)
            logger.info(f"✅ Generated test file: test_{test_name}.py")
