import logging
import os

from rich.console import Console
from rich.logging import RichHandler

console = Console(soft_wrap=True)

console_handler = RichHandler(
    console=console,
    markup=True,
    show_path=True,
    rich_tracebacks=True,
    show_time=True,
    show_level=True,
)

formatter = logging.Formatter(
    "%(name)s | %(message)s",
    datefmt="[%X]"
)

console_handler.setFormatter(formatter)

access_handler = RichHandler(
    console=console,
    markup=True,
    show_path=False,
    rich_tracebacks=False,
    show_time=True,
    show_level=False,
)
access_formatter = logging.Formatter("%(message)s")
access_handler.setFormatter(access_formatter)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logs(level: int | None = None) -> None:
    """
    Configura o logger para a aplicação.
    """
    if level is None:
        level = getattr(logging, log_level)

    console_handler.setLevel(level)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler],
    # force=True  # Garante que sobrescreva handlers anteriores
    )

    app_logger = logging.getLogger("app")
    app_logger.setLevel(level)

    # Logger de acesso com handler separado
    access_logger = logging.getLogger("app.access")
    access_logger.handlers.clear()  # Remove handlers existentes
    access_logger.propagate = False  # Evita duplicação no root
    access_logger.setLevel(level)
    access_logger.addHandler(access_handler)
    