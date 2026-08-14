import os
import re
import subprocess
import shutil
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from parser.ir_models import IRSpec
from ai_engine.generator import generate_ai_service_logic
from ai_engine.formatter import format_python_code
from ai_engine.self_healing import run_self_healing_loop
from logger import logger

# Template loader from templates/clean_arch
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "clean_arch")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def extract_custom_logic(service_path: str) -> Optional[str]:
    """
    Safely extract user's manual business logic from an existing service file
    by looking between the AST protected block markers.
    """
    if not os.path.exists(service_path):
        return None

    try:
        with open(service_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex matches everything between the start and end markers
        pattern = r"# === USER CODE START: custom_business_logic ===.*?# Hand-written integrations, external calls, or overrides\s*(.*?)\s*# === USER CODE END ==="
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            extracted = match.group(1).strip()
            # Only return if the user actually added logic (more than just AI generated stuff)
            # If the block only contains standard boilerplate, we could return None, 
            # but for safety we'll return exactly what's there if it's not empty
            if extracted:
                return extracted
                
    except Exception as e:
        print(f"Warning: Failed to extract custom logic from {service_path}: {e}")
        
    return None

def render_and_write(template_name: str, context: dict, target_file_path: str, format_py: bool = False):
    template = env.get_template(template_name)
    rendered = template.render(**context)

    if format_py and target_file_path.endswith(".py"):
        rendered = format_python_code(rendered)

    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(rendered)

def generate_clean_backend(ir_spec: IRSpec, output_dir: str, use_ai: bool = True, test_driven_healing: bool = True, spec_file_path: Optional[str] = None, generate_sdk: bool = True, git_pr: bool = False):
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize Git branching if requested
    if git_pr:
        logger.info("🌿 [PR Automation] Checking Git repository...")
        if not os.path.exists(os.path.join(output_dir, ".git")):
            subprocess.run(["git", "init"], cwd=output_dir, check=True)
            logger.info("🌿 [PR Automation] Initialized new Git repository.")
        
        branch_name = f"auto-update-{int(os.path.getctime(output_dir) if os.path.exists(output_dir) else 0)}"
        logger.info(f"🌿 [PR Automation] Creating branch {branch_name}")
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=output_dir, capture_output=True)

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
        
    # Optional Automated SDK Generation
    if generate_sdk and spec_file_path:
        logger.info(f"📦 Generating TypeScript SDK using openapi-typescript-codegen...")
        # Copy the spec file into the output dir for the generator
        dest_spec_path = os.path.join(output_dir, "openapi_spec" + os.path.splitext(spec_file_path)[1])
        shutil.copyfile(spec_file_path, dest_spec_path)
        
        sdk_dir = os.path.join(output_dir, "sdk", "typescript")
        os.makedirs(sdk_dir, exist_ok=True)
        try:
            subprocess.run(
                ["npx", "-y", "openapi-typescript-codegen", "--input", dest_spec_path, "--output", sdk_dir, "--client", "axios"],
                check=True,
                capture_output=True
            )
            logger.info("✅ SDK Generated successfully.")
        except Exception as e:
            logger.warning(f"⚠️ Failed to generate SDK (is Node/npx installed?): {e}")

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

    # 3. Services (with AI logic generation option & Safe Code Merging)
    import asyncio

    async def generate_single_service(model, sem):
        async with sem:
            service_file = os.path.join(services_dir, f"{model.name.lower()}_service.py")
            custom_logic = extract_custom_logic(service_file)
            ai_create_logic = None
            
            if use_ai and not custom_logic:
                try:
                    raw_ai = await generate_ai_service_logic(
                        route_summary=f"Create a new {model.name}",
                        method="POST",
                        path=f"/{model.table_name}",
                        model=model,
                        operation_id=f"create_{model.name.lower()}"
                    )
                    ai_create_logic = "\n".join([f"        {line}" for line in raw_ai.splitlines() if line.strip()])
                except Exception as e:
                    logger.warning(f"AI Service logic failed for {model.name}: {e}")

            render_and_write("service_layer.j2", {
                "model": model, 
                "ai_create_logic": ai_create_logic,
                "custom_logic": custom_logic
            }, service_file, format_py=True)

    async def generate_services_concurrently():
        sem = asyncio.Semaphore(20)  # Tiered Batching (Concurrency limit)
        tasks = [generate_single_service(model, sem) for model in ir_spec.models]
        await asyncio.gather(*tasks)

    asyncio.run(generate_services_concurrently())

    # 4. FastAPI Routers
    for model in ir_spec.models:
        router_file = os.path.join(api_dir, f"{model.name.lower()}_router.py")
        render_and_write("fastapi_router.j2", {"model": model}, router_file, format_py=True)

    # 5. Main FastAPI Application
    render_and_write("main_app.j2", {"models": ir_spec.models, "title": ir_spec.title, "version": ir_spec.version}, os.path.join(app_dir, "main.py"), format_py=True)

    # 6. Pytest Suites & Conftest
    conftest_content = """import os
import pytest
from fastapi.testclient import TestClient

# Force tests to use an in-memory SQLite database
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

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
    render_and_write("sonar_properties.j2", {}, os.path.join(output_dir, "sonar-project.properties"))
    
    # 8. TS React Query SDK
    if generate_sdk:
        context = {"ir_spec": ir_spec, "models": ir_spec.models}
        sdk_dir = os.path.join(output_dir, "sdk", "frontend")
        os.makedirs(sdk_dir, exist_ok=True)
        render_and_write("sdk/typescript/types.ts.j2", context, os.path.join(sdk_dir, "types.ts"))
        render_and_write("sdk/typescript/api.ts.j2", context, os.path.join(sdk_dir, "api.ts"))
        render_and_write("sdk/typescript/hooks.ts.j2", context, os.path.join(sdk_dir, "hooks.ts"))
        logger.info("📦 Generated React Query/TypeScript SDK in 'sdk/frontend'")
        
    render_and_write("readme.j2", {"title": ir_spec.title, "version": ir_spec.version}, os.path.join(output_dir, "README.md"))

    # Requirements for generated app
    app_reqs = """fastapi>=0.100.0
uvicorn>=0.22.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
pytest>=7.4.0
httpx>=0.24.0
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-instrumentation-fastapi>=0.41b0
"""
    with open(os.path.join(output_dir, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(app_reqs)

    # .env.example
    with open(os.path.join(output_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write("DATABASE_URL=sqlite:///./backend.db\nSECRET_KEY=super-secret-key-change-me\n")

    logger.info(f"✨ Successfully generated clean backend at '{output_dir}'")
    
    if use_ai and test_driven_healing:
        from ai_engine.self_healing import run_self_healing_loop
        run_self_healing_loop(output_dir)

    if git_pr:
        logger.info("🌿 [PR Automation] Committing generated changes...")
        subprocess.run(["git", "add", "."], cwd=output_dir)
        subprocess.run(["git", "commit", "-m", "Auto-generated backend updates"], cwd=output_dir, capture_output=True)
        
        # Generate pr_summary.md
        diff_result = subprocess.run(["git", "show", "--stat"], cwd=output_dir, capture_output=True, text=True)
        diff_content = diff_result.stdout if diff_result.returncode == 0 else "No changes detected."
        
        pr_summary_path = os.path.join(output_dir, "..", "pr_summary.md")
        with open(pr_summary_path, "w", encoding="utf-8") as f:
            f.write("# Pull Request Summary\n\n")
            f.write("## Automated Generation Report\n\n")
            f.write("The AI Codegen Engine successfully rebuilt the backend architecture. Below is the generated diff summary:\n\n")
            f.write("```diff\n")
            f.write(diff_content)
            f.write("\n```\n")
            f.write("\n> *Please review the AST-protected custom business logic blocks to ensure no spec drift occurred.*\n")
        logger.info(f"🌿 [PR Automation] PR Summary generated at {os.path.abspath(pr_summary_path)}")
