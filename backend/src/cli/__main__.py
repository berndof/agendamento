import asyncio
import logging
import subprocess
import sys
from typing import Annotated

import typer
from rich.console import Console

from cli import migration

console = Console()
app = typer.Typer(name="chimera")
app.add_typer(migration.app)

CONTAINER_NAME = "chimera_backend"
#CLI_PATH_IN_CONTAINER = "/backend/src/main.py"  # ajuste conforme caminho real no container



@app.callback()
def remote_callback(
    remote: Annotated[bool, typer.Option(
        "--remote",
        is_eager=True,
        help="Run command remotely in container"
    )] = False
):
    if remote:
        args = [arg for arg in sys.argv[1:] if arg != "--remote"]
        docker_cmd = ["docker", "exec","--workdir", "/backend/src", "-it", CONTAINER_NAME, "chimera"] + args
        console.print(f"🚀 Executando remotamente: {' '.join(docker_cmd)}", style="bold magenta")
        result = subprocess.run(
            docker_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
            
        raise typer.Exit(code=result.returncode)


def main():
    app()


if __name__ == "__main__":
    typer.run(main)


