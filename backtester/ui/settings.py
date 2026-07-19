"""Application settings (QSettings) — one place so tests can substitute it."""

from __future__ import annotations

from PySide6.QtCore import QSettings


def app_settings() -> QSettings:
    return QSettings("PythonBacktester", "PythonBacktester")


def cast_like(value, default):
    """Coerce a QSettings value (often a string) to the default's type."""
    if value is None:
        return default
    try:
        if isinstance(default, bool):
            return str(value).lower() in ("true", "1")
        if isinstance(default, int):
            return int(float(value))
        if isinstance(default, float):
            return float(value)
    except (TypeError, ValueError):
        return default
    return str(value)
