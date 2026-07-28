"""Named indicator sets, saved as files next to the app.

A template is just the list of indicators and their parameter values under a
name — the same shape the live selection is stored in, written to
``chart_templates/<name>.json`` so it can be backed up, edited, or handed to
someone else, the way MetaTrader's chart templates are files rather than
buried settings.

    {
      "format": 1,
      "name": "Trend setup",
      "saved": "2026-07-28T08:15:00",
      "indicators": [
        {"name": "SSL Channel", "params": {"period": 13, "nrtr": true}}
      ]
    }

Rebuilding is forgiving: an indicator that no longer exists, or whose
parameters have changed under the template, is skipped and reported rather
than taking the whole template down.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from backtester.indicators import loader
from backtester.indicators.base import Indicator

FORMAT = 1
SUFFIX = ".json"


def template_dir() -> Path:
    """``chart_templates/`` next to the app (or next to the .exe when frozen)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "chart_templates"
    return Path(__file__).resolve().parents[2] / "chart_templates"


# ------------------------------------------------------------ serialisation


def to_spec(indicators: list[Indicator]) -> list[dict]:
    return [{"name": i.display_name, "params": i.values()} for i in indicators]


def build(spec: list[dict]) -> tuple[list[Indicator], list[str]]:
    """Instantiate a saved spec; returns the indicators and what was skipped."""
    registry, _load_errors = loader.discover()
    built: list[Indicator] = []
    skipped: list[str] = []
    for entry in spec:
        name = entry.get("name", "")
        item = registry.get(name)
        if item is None:
            skipped.append(f"{name or '(unnamed)'}: no such indicator")
            continue
        try:
            built.append(item[0](**entry.get("params", {})))
        except (ValueError, TypeError) as exc:
            skipped.append(f"{name}: {exc}")
    return built, skipped


# ------------------------------------------------------------------- files


def _safe(name: str) -> str:
    cleaned = "".join(
        c if c.isalnum() or c in " -_." else "_" for c in name.strip()
    ).strip()
    return cleaned or "template"


def path_for(name: str) -> Path:
    return template_dir() / f"{_safe(name)}{SUFFIX}"


def list_templates() -> list[str]:
    """Saved template names, sorted, read from the files themselves."""
    directory = template_dir()
    if not directory.is_dir():
        return []
    names = []
    for file in directory.glob(f"*{SUFFIX}"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            names.append(str(data.get("name") or file.stem))
        except (OSError, ValueError):
            names.append(file.stem)   # unreadable, but still worth listing
    return sorted(set(names), key=str.lower)


def save_template(name: str, indicators: list[Indicator]) -> Path:
    directory = template_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = path_for(name)
    path.write_text(
        json.dumps(
            {
                "format": FORMAT,
                "name": name.strip() or path.stem,
                "saved": datetime.now().isoformat(timespec="seconds"),
                "indicators": to_spec(indicators),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def load_template(name: str) -> tuple[list[Indicator], list[str]]:
    path = path_for(name)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        return [], [f"{name}: template not found"]
    except ValueError as exc:
        return [], [f"{name}: not a readable template ({exc})"]
    spec = data.get("indicators")
    if not isinstance(spec, list):
        return [], [f"{name}: template has no indicator list"]
    return build(spec)


def delete_template(name: str) -> bool:
    try:
        path_for(name).unlink()
        return True
    except OSError:
        return False


def exists(name: str) -> bool:
    return path_for(name).is_file()
