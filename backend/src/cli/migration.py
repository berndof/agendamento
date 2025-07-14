import logging
import os
import subprocess
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from helpers.logs import setup_logs

console = Console(soft_wrap=True)
app = typer.Typer(name="migration", help="Chimera migrations")

@app.callback()
def env_callback(
    env_file: Annotated[str, typer.Option(
        "--env-file", help="Path to .env file"
    )] = None
):

    if env_file:
        console.print(f"🔧 Carregando variáveis de ambiente de '{env_file}'", style="yellow")
        from dotenv import load_dotenv
        if not os.path.exists(env_file):
            console.print(f"❌ Arquivo {env_file} não encontrado.", style="bold red")
            raise typer.Exit(code=1)
        load_dotenv(env_file)

@app.command("new")
def new_migration(
    name: str = typer.Argument(..., help="Name of the migration"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Create a new Alembic migration revision"""
    if verbose:
        os.environ["ALEMBIC_LOGS"] = "true"
        setup_logs(level=logging.DEBUG)

    console.print(f"📦 Generating migration: '{name}'", style="bold cyan")

    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", name],
        stdout=subprocess.PIPE if verbose else subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        text=True,
        cwd="./src/"
    )

    if verbose:
        console.print(result.stdout)

    console.print("✅ Migration created!", style="bold green")

@app.command("apply")
def apply_migration(verbose: bool = typer.Option(False, "--verbose", "-v")):
    """Apply all pending Alembic migrations"""
    console.print("🔄 Running Alembic migrations...", style="bold cyan")

    if verbose:
        setup_logs(level=logging.DEBUG)  # 🔍 Ativa logs detalhados
        os.environ["ALEMBIC_LOGS"] = "true"
        
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd="./src/"
        )
        console.print(result.stdout)
    else:
        
        with console.status("Applying migrations...", spinner="dots"):
            subprocess.run(
                ["alembic", "upgrade", "head"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                cwd="./src/"
            )

    console.print("✅ Migrations applied!", style="bold green")

@app.command("clean")
def clean_migrations():
    """Delete all migrations"""
    console.print("🗑️ Cleaning migrations...", style="bold cyan")

    versions_path = Path("./src/migrations") / "versions"

    if not versions_path.exists():
        console.print("⚠️ [yellow]No 'migrations/versions' directory found.[/yellow]")
        raise typer.Exit()

    with console.status("Deleting migration files...", spinner="dots"):
        for file in versions_path.glob("*.py"):
            try:
                file.unlink()
            except Exception as e:
                console.print(f"❌ [red]Failed to delete {file.name}: {e}[/red]")

    console.print("✅ Migrations cleaned, please clean your database tables!", style="bold green")
