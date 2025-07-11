import os
import re
import textwrap
from jinja2 import Environment, FileSystemLoader
from logger import logger
from ai_logic_generator import generate_route_logic

env = Environment(loader=FileSystemLoader("templates"))

def sanitize_logic(text: str) -> str:
    """
    Cleans Groq AI output:
    - Removes code fences
    - Removes explanations
    - Strips excess whitespace
    """
    cleaned_lines = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            continue
        if "explain" in line.lower() or "note that" in line.lower():
            continue
        cleaned_lines.append(line.rstrip())

    cleaned = "\n".join(cleaned_lines).strip()
    return cleaned

def generate_routes(paths: dict, output_dir: str):
    template = env.get_template("route_template.j2")
    routes_path = os.path.join(output_dir, "routes")
    os.makedirs(routes_path, exist_ok=True)

    for path, methods in paths.items():
        route_name = path.strip("/").replace("/", "_").replace("{", "").replace("}", "") or "root"
        endpoints = []

        for method, details in methods.items():
            summary = details.get("summary", f"{method.upper()} {path}")
            operation_id = details.get("operationId", f"{method}_{route_name}")

            # ✅ Refined Prompt
            logic_prompt = f"""
Write only the correctly indented Python body for a FastAPI route using SQLAlchemy ORM, without explanations or code fences.

Requirements:
- All lines must be consistently indented with 4 spaces (use spaces, not tabs).
- Do not include the function definition; only the body inside the function.
- Assume the function signature already includes 'db: Session = Depends(get_db)' and any required path parameters.
- Assume SQLAlchemy models like Customer, Product, Order are already imported.
- Use `db.query(Model).all()` and similar ORM idioms where applicable.
- If JSON request data is needed, use `request: Request` injected, and parse with `data = await request.json()` if async or `data = request.json()` if sync.
- Return properly structured JSON responses, matching fields of the model.
- Ensure the code is ready to paste inside a FastAPI route without indentation errors or further adjustments.

Method: {method.upper()}
Path: {path}
Operation ID: {operation_id}
Summary: {summary}
"""

            try:
                raw_logic = generate_route_logic(logic_prompt)
                logger.info(f"[AI LOGIC] {method.upper()} {path}:\n{raw_logic}\n")
                logic = sanitize_logic(raw_logic).lstrip()

                # Force consistent 4-space indentation if Groq returns unindented code
                if logic and not logic.startswith("    "):
                    logic = textwrap.indent(logic, "    ")

            except Exception as e:
                logger.warning(f"AI generation failed for {method.upper()} {path}: {e}")
                logic = '    return {"message": "Placeholder logic for ' + operation_id + '"}'

            # Extract path parameters like {customer_id}
            param_matches = re.findall(r"{(.*?)}", path)
            param_list = ", ".join(param_matches) if param_matches else ""
            function_signature = param_list + (", " if param_list else "") + "db: Session = Depends(get_db)"

            endpoints.append({
                "method": method.upper(),
                "summary": summary,
                "path": path,
                "operationId": operation_id,
                "logic": logic,
                "params": function_signature
            })

        rendered = template.render(endpoints=endpoints)
        with open(os.path.join(routes_path, f"{route_name}.py"), "w", encoding="utf-8") as f:
            f.write(rendered)
            logger.info(f"✅ Generated route file: {route_name}.py")
