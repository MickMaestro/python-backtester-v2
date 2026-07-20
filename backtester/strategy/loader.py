"""Discovers Strategy subclasses: built-ins plus user .py files.

User strategies live in the ``strategies/`` folder next to the app. Files
are re-executed on every discovery, so editing a file and clicking Reload
in the GUI picks up changes without restarting (hot reload).
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from types import ModuleType

from backtester.strategy.base import Strategy


def _user_strategy_dir() -> Path:
    # Frozen (PyInstaller): a strategies/ folder next to the executable, so
    # users can drop in .py files without rebuilding. Source checkout: the
    # strategies/ folder at the project root.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "strategies"
    return Path(__file__).resolve().parents[2] / "strategies"


USER_STRATEGY_DIR = _user_strategy_dir()

#: spec tuples are picklable handles the optimizer's worker processes use
#: to re-import the class (see engine/optimizer.py).
StrategyEntry = tuple[type, tuple]  # (class, spec)


def load_strategies_from_file(path: Path | str) -> dict[str, type]:
    """Execute a .py file and return the Strategy subclasses it defines.

    Source is read and compiled fresh on every call (no bytecode cache), so
    editing a file and re-discovering always picks up the change — even if the
    edit keeps the same file size within one filesystem timestamp tick, which
    would fool ``SourceFileLoader``'s mtime/size cache check.
    """
    path = Path(path)
    module_name = f"user_strategy_{path.stem}"
    source = path.read_text(encoding="utf-8")
    code = compile(source, str(path), "exec")
    module = ModuleType(module_name)
    module.__file__ = str(path)
    sys.modules[module_name] = module  # so the module can self-reference
    exec(code, module.__dict__)
    return {
        name: obj
        for name, obj in vars(module).items()
        if inspect.isclass(obj)
        and issubclass(obj, Strategy)
        and obj is not Strategy
        and obj.__module__ == module_name
    }


def load_strategy_class(path: str, class_name: str) -> type:
    return load_strategies_from_file(path)[class_name]


def discover(
    directory: Path | str | None = None,
) -> tuple[dict[str, StrategyEntry], list[str]]:
    """All available strategies keyed by display name, plus load errors.

    Built-ins keep their short names; file strategies are named
    ``<filename>.<ClassName>``.
    """
    from backtester.strategy.examples import STRATEGIES

    registry: dict[str, StrategyEntry] = {
        name: (cls, ("builtin", name)) for name, cls in STRATEGIES.items()
    }
    errors: list[str] = []

    directory = Path(directory) if directory is not None else USER_STRATEGY_DIR
    if directory.is_dir():
        for file in sorted(directory.glob("*.py")):
            if file.name.startswith("_"):
                continue
            try:
                for class_name, cls in load_strategies_from_file(file).items():
                    registry[f"{file.stem}.{class_name}"] = (
                        cls,
                        ("file", str(file), class_name),
                    )
            except Exception as exc:
                errors.append(f"{file.name}: {type(exc).__name__}: {exc}")
    return registry, errors
