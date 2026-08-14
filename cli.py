import sys
import os
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from parse_openapi import load_openapi_spec
from parser.openapi_parser import parse_openapi_spec
from codegen.engine import generate_clean_backend

app = typer.Typer(help="OpenAPI Enterprise Backend Generator CLI")
console = Console(legacy_windows=False)

@app.command()
def generate(
    input: str = typer.Option(..., "--input", "-i", help="Path to OpenAPI spec (YAML or JSON)"),
    output: str = typer.Option("./generated_backend", "--output", "-o", help="Target output directory"),
    use_ai: bool = typer.Option(True, "--use-ai/--no-ai", help="Enable Groq/GPT-4 AI logic generation"),
    sdk: bool = typer.Option(True, "--sdk/--no-sdk", help="Generate TypeScript SDK using openapi-typescript-codegen"),
    git_pr: bool = typer.Option(False, "--git-pr", help="Automate PR workflow: branch, commit, and generate markdown diff")
):
    """
    Generate a production-ready FastAPI backend with Clean Architecture, Docker, and Pytest.
    """
    console.print(Panel.fit("[bold green]OpenAPI Backend Generator CLI[/bold green]\n[dim]Enterprise Codegen Engine[/dim]"))
    
    if not os.path.exists(input):
        console.print(f"[bold red]Error:[/bold red] Input spec file '{input}' not found!")
        raise typer.Exit(code=1)

    start_time = time.time()
    
    # 1. Parse Spec
    with console.status("[bold blue]Parsing OpenAPI Spec & Building Intermediate Representation (IR)...[/bold blue]"):
        raw_spec = load_openapi_spec(input)
        ir_spec = parse_openapi_spec(raw_spec)

    console.print(f"Spec parsed: [bold cyan]{ir_spec.title}[/bold cyan] v{ir_spec.version}")
    console.print(f"Detected [green]{len(ir_spec.models)}[/green] Models, [green]{len(ir_spec.routes)}[/green] Routes")

    # 2. Codegen Engine
    with console.status("[bold blue]Rendering Clean Architecture Templates & AI Business Logic...[/bold blue]"):
        generate_clean_backend(ir_spec, output, use_ai=use_ai, spec_file_path=input, generate_sdk=sdk, git_pr=git_pr)

    elapsed = round(time.time() - start_time, 2)
    console.print(Panel(
        f"[bold green]Backend successfully generated in {elapsed}s![/bold green]\n\n"
        f"Output Directory: [cyan]{os.path.abspath(output)}[/cyan]\n"
        f"Quick Run:\n"
        f"   [yellow]cd {output}[/yellow]\n"
        f"   [yellow]docker compose up --build[/yellow]",
        title="Generation Complete",
        border_style="green"
    ))

@app.command()
def inspect(
    input: str = typer.Option(..., "--input", "-i", help="Path to OpenAPI spec (YAML or JSON)")
):
    """
    Inspect the Intermediate Representation (IR) extracted from an OpenAPI spec.
    """
    if not os.path.exists(input):
        console.print(f"[bold red]Error:[/bold red] Spec file '{input}' not found!")
        raise typer.Exit(code=1)

    raw_spec = load_openapi_spec(input)
    ir_spec = parse_openapi_spec(raw_spec)

    console.print(f"\n[bold]Spec Overview:[/bold] {ir_spec.title} (v{ir_spec.version})")

    # Models Table
    model_table = Table(title="Detected Data Models (ORM / Pydantic)")
    model_table.add_column("Model Name", style="cyan")
    model_table.add_column("Table Name", style="magenta")
    model_table.add_column("Fields Count", style="green")
    model_table.add_column("Field Names", style="white")

    for m in ir_spec.models:
        f_names = ", ".join([f.name for f in m.fields[:5]]) + ("..." if len(m.fields) > 5 else "")
        model_table.add_row(m.name, m.table_name, str(len(m.fields)), f_names)

    console.print(model_table)

    # Routes Table
    route_table = Table(title="Detected API Routes")
    route_table.add_column("Method", style="bold yellow")
    route_table.add_column("Path", style="cyan")
    route_table.add_column("Operation ID", style="magenta")
    route_table.add_column("Target Model", style="green")

    for r in ir_spec.routes[:10]:
        route_table.add_row(r.method, r.path, r.operation_id, r.target_model or "-")

    if len(ir_spec.routes) > 10:
        console.print(f"\n[dim]...and {len(ir_spec.routes) - 10} more routes[/dim]")

    console.print(route_table)

if __name__ == "__main__":
    app()
