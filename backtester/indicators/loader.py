"""Discovers Indicator subclasses from the ``indicators/`` folder.

Same contract as ``strategy/loader.py``: user files live next to the app (next
to the .exe in a packaged build), source is recompiled on every discovery so
edits are picked up without restarting, and load errors are collected rather
than raised.
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from types import ModuleType

from .base import Indicator


def _user_indicator_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "indicators"
    return Path(__file__).resolve().parents[2] / "indicators"


USER_INDICATOR_DIR = _user_indicator_dir()

#: (class, ("file", path, class_name)) — the spec re-imports the class later.
IndicatorEntry = tuple[type, tuple]


def load_indicators_from_file(path: Path | str) -> dict[str, type]:
    """Execute a .py file and return the Indicator subclasses it defines."""
    path = Path(path)
    module_name = f"user_indicator_{path.stem}"
    source = path.read_text(encoding="utf-8")
    code = compile(source, str(path), "exec")
    module = ModuleType(module_name)
    module.__file__ = str(path)
    sys.modules[module_name] = module
    exec(code, module.__dict__)
    return {
        name: obj
        for name, obj in vars(module).items()
        if inspect.isclass(obj)
        and issubclass(obj, Indicator)
        and obj is not Indicator
        and obj.__module__ == module_name
    }


def discover(
    directory: Path | str | None = None,
) -> tuple[dict[str, IndicatorEntry], list[str]]:
    """All available indicators keyed by display name, plus load errors."""
    registry: dict[str, IndicatorEntry] = {}
    errors: list[str] = []

    directory = Path(directory) if directory is not None else USER_INDICATOR_DIR
    if not directory.is_dir():
        return registry, errors

    for file in sorted(directory.glob("*.py")):
        if file.name.startswith("_"):
            continue
        try:
            for class_name, cls in load_indicators_from_file(file).items():
                name = cls.name or class_name
                # Two files claiming one name would silently shadow each other.
                if name in registry:
                    name = f"{name} ({file.stem})"
                registry[name] = (cls, ("file", str(file), class_name))
        except Exception as exc:
            errors.append(f"{file.name}: {type(exc).__name__}: {exc}")
    return registry, errors
