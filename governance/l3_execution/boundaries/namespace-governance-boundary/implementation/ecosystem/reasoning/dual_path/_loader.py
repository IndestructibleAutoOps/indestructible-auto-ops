"""Utility loader to reuse dual-path implementations with import-safe modules."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType


def load_impl(relative_path: str, module_name: str) -> ModuleType:
    """
    Load a module from the existing dual-path implementation directory.

    Args:
        relative_path: Path to the target file relative to dual-path/.
        module_name: A unique module name for importlib.

    Returns:
        Loaded module object.

    Raises:
        ImportError: If the module cannot be loaded.
    """
    impl_root = Path(__file__).resolve().parent.parent / "dual-path"
    target = impl_root / relative_path
    spec = spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to locate spec for {target}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
