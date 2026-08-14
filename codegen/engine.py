import os
from jinja2 import Environment, FileSystemLoader
from parser.ir_models import IRSpec
from ai_engine.generator import generate_ai_service_logic
from ai_engine.formatter import format_python_code
from logger import logger

# Template loader from templates/clean_arch
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "clean_arch")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render_and_write(template_name: str, context: dict, target_file_path: str, format_py: bool = False):
    template = env.get_template(template_name)
    rendered = template.render(**context)

    if format_py and target_file_path.endswith(".py"):
        rendered = format_python_code(rendered)

    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(rendered)

def generate_clean_backend(ir_spec: IRSpec, output_dir: str, use_ai: bool = True):
    logger.info(f"🚀 Starting Codegen Engine for spec: {ir_spec.title} ({len(ir_spec.models)} models, {len(ir_spec.routes)} routes)")

    # Root directories
    app_dir = os.path.join(output_dir, "app")
    api_dir = os.path.join(app_dir, "api")
    core_dir = os.path.join(app_dir, "core")
    db_dir = os.path.join(app_dir, "db")
    models_dir = os.path.join(app_dir, "models")
    schemas_dir = os.path.join(app_dir, "schemas")
    services_dir = os.path.join(app_dir, "services")
    tests_dir = os.path.join(output_dir, "tests")
    github_dir = os.path.join(output_dir, ".github", "workflows")

    for d in [app_dir, api_dir, core_dir, db_dir, models_dir, schemas_dir, services_dir, tests_dir, github_dir]:
        os.makedirs(d, exist_ok=True)

    # Write __init__.py files
    for init_path in [
        os.path.join(app_dir, "__init__.py"),
        os.path.join(api_dir, "__init__.py"),
        os.path.join(core_dir, "__init__.py"),
        os.path.join(db_dir, "__init__.py"),
        os.path.join(models_dir, "__init__.py"),
        os.path.join(schemas_dir, "__init__.py"),
        os.path.join(services_dir, "__init__.py"),
        os.path.join(tests_dir, "__init__.py")
    ]:
        with open(init_path, "w", encoding="utf-8") as f:
            f.write("# Package marker\n")

    # 1. Config & Database
    render_and_write("config.j2", {"title": ir_spec.title, "version": ir_spec.version}, os.path.join(core_dir, "config.py"), format_py=True)
    render_and_write("database.j2", {}, os.path.join(db_dir, "database.py"), format_py=True)

    # 2. Pydantic Schemas & SQLAlchemy Models
    render_and_write("pydantic_schema.j2", {"models": ir_spec.models}, os.path.join(schemas_dir, "schemas.py"), format_py=True)
    render_and_write("sqlalchemy_model.j2", {"models": ir_spec.models}, os.path.join(models_dir, "models.py"), format_py=True)

    # 3. Services (with AI logic generation option)
    for model in ir_spec.models:
        ai_create_logic = None
        if use_ai:
            try:
                raw_ai = generate_ai_service_logic(
                    route_summary=f"Create a new {model.name}",
                    method="POST",
                    path=f"/{model.table_name}",
                    model_name=model.name,
                    operation_id=f"create_{model.name.lower()}"
                )
                ai_create_logic = "\n".join([f"        {line}" for line in raw_ai.splitlines() if line.strip()])
            except Exception as e:
                logger.warning(f"AI Service logic failed for {model.name}: {e}")

        service_file = os.path.join(services_dir, f"{model.name.lower()}_service.py")
        render_and_write("service_layer.j2", {"model": model, "ai_create_logic": ai_create_logic}, service_file, format_py=True)

    # 4. FastAPI Routers
    for model in ir_spec.models:
        router_file = os.path.join(api_dir, f"{model.name.lower()}_router.py")
        render_and_write("fastapi_router.j2", {"model": model}, router_file, format_py=True)

    # 5. Main FastAPI Application
    render_and_write("main_app.j2", {"models": ir_spec.models, "title": ir_spec.title, "version": ir_spec.version}, os.path.join(app_dir, "main.py"), format_py=True)

    # 6. Pytest Suites & Conftest
    conftest_content = """import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
"""
    with open(os.path.join(tests_dir, "conftest.py"), "w", encoding="utf-8") as f:
        f.write(conftest_content)

    for model in ir_spec.models:
        test_file = os.path.join(tests_dir, f"test_{model.name.lower()}.py")
        render_and_write("pytest_suite.j2", {"model": model}, test_file, format_py=True)

    # 7. DevOps Files
    render_and_write("dockerfile.j2", {}, os.path.join(output_dir, "Dockerfile"))
    render_and_write("docker_compose.j2", {}, os.path.join(output_dir, "docker-compose.yml"))
    render_and_write("ci_cd_github.j2", {}, os.path.join(github_dir, "ci.yml"))
    render_and_write("readme.j2", {"title": ir_spec.title, "version": ir_spec.version}, os.path.join(output_dir, "README.md"))

    # Requirements for generated app
    app_reqs = """fastapi>=0.100.0
uvicorn>=0.22.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
pytest>=7.4.0
httpx>=0.24.0
"""
    with open(os.path.join(output_dir, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(app_reqs)

    # .env.example
    with open(os.path.join(output_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write("DATABASE_URL=sqlite:///./backend.db\nSECRET_KEY=super-secret-key-change-me\n")

    logger.info(f"✨ Successfully generated clean backend at '{output_dir}'")
