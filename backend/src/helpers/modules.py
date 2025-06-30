import importlib
from pathlib import Path


def import_python_module(file_path: Path) -> object | None:
    """Imports a Python module from a given file path."""
    module_name = ".".join(file_path.with_suffix('').parts)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if not spec or not spec.loader:
        #logger.warning(f"Failed to load module spec for: {file_path}")
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod