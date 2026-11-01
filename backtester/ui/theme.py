"""Application colour theme — System, Light, or Dark.

Light and Dark use the Fusion style with an explicit palette so they look the
same on every platform; System falls back to the platform's native style.
The choice is persisted in QSettings. Charts keep their own display colours
(see chart_settings).
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QColor, QPalette
from PySide6.QtWidgets import QApplication, QMenu

from backtester.ui.settings import app_settings

THEMES = ("system", "light", "dark")
DEFAULT_THEME = "system"

_native_style: str | None = None


def load_theme() -> str:
    name = str(app_settings().value("ui/theme", DEFAULT_THEME))
    return name if name in THEMES else DEFAULT_THEME


def save_theme(name: str) -> None:
    app_settings().setValue("ui/theme", name)


def _palette(colors: dict[str, str], disabled: str) -> QPalette:
    pal = QPalette()
    roles = {
        "window": QPalette.ColorRole.Window,
        "window_text": QPalette.ColorRole.WindowText,
        "base": QPalette.ColorRole.Base,
        "alt_base": QPalette.ColorRole.AlternateBase,
        "text": QPalette.ColorRole.Text,
        "button": QPalette.ColorRole.Button,
        "button_text": QPalette.ColorRole.ButtonText,
        "highlight": QPalette.ColorRole.Highlight,
        "highlighted_text": QPalette.ColorRole.HighlightedText,
        "tooltip_base": QPalette.ColorRole.ToolTipBase,
        "tooltip_text": QPalette.ColorRole.ToolTipText,
        "placeholder": QPalette.ColorRole.PlaceholderText,
        "link": QPalette.ColorRole.Link,
        "bright_text": QPalette.ColorRole.BrightText,
        "light": QPalette.ColorRole.Light,
        "midlight": QPalette.ColorRole.Midlight,
        "mid": QPalette.ColorRole.Mid,
        "dark": QPalette.ColorRole.Dark,
        "shadow": QPalette.ColorRole.Shadow,
    }
    for key, role in roles.items():
        pal.setColor(role, QColor(colors[key]))
    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        pal.setColor(QPalette.ColorGroup.Disabled, role, QColor(disabled))
    return pal


def dark_palette() -> QPalette:
    return _palette(
        {
            "window": "#1e222d",
            "window_text": "#d1d4dc",
            "base": "#131722",
            "alt_base": "#1a1e29",
            "text": "#d1d4dc",
            "button": "#2a2e39",
            "button_text": "#d1d4dc",
            "highlight": "#2962ff",
            "highlighted_text": "#ffffff",
            "tooltip_base": "#2a2e39",
            "tooltip_text": "#d1d4dc",
            "placeholder": "#787b86",
            "link": "#42a5f5",
            "bright_text": "#ffffff",
            "light": "#3a3f4b",
            "midlight": "#30343f",
            "mid": "#24283b",
            "dark": "#101320",
            "shadow": "#000000",
        },
        disabled="#5d606b",
    )


def light_palette() -> QPalette:
    return _palette(
        {
            "window": "#f0f3fa",
            "window_text": "#131722",
            "base": "#ffffff",
            "alt_base": "#f5f7fb",
            "text": "#131722",
            "button": "#e8ebf2",
            "button_text": "#131722",
            "highlight": "#2962ff",
            "highlighted_text": "#ffffff",
            "tooltip_base": "#ffffff",
            "tooltip_text": "#131722",
            "placeholder": "#787b86",
            "link": "#1565c0",
            "bright_text": "#ffffff",
            "light": "#ffffff",
            "midlight": "#e0e3eb",
            "mid": "#b2b5be",
            "dark": "#9598a1",
            "shadow": "#5d606b",
        },
        disabled="#a3a6af",
    )


def apply_theme(app: QApplication, name: str) -> None:
    """Restyle the whole application. Safe to call repeatedly at runtime."""
    global _native_style
    if _native_style is None:
        _native_style = app.style().name()

    if name == "dark":
        scheme, style, palette = Qt.ColorScheme.Dark, "Fusion", dark_palette()
    elif name == "light":
        scheme, style, palette = Qt.ColorScheme.Light, "Fusion", light_palette()
    else:
        scheme, style, palette = Qt.ColorScheme.Unknown, _native_style, None

    hints = app.styleHints()
    if hasattr(hints, "setColorScheme"):  # Qt >= 6.8
        hints.setColorScheme(scheme)
    app.setStyle(style)
    app.setPalette(palette if palette is not None else app.style().standardPalette())


def populate_theme_menu(menu: QMenu) -> dict[str, QAction]:
    """Add exclusive System/Light/Dark actions that apply and save the theme."""
    group = QActionGroup(menu)
    current = load_theme()
    actions: dict[str, QAction] = {}
    for name in THEMES:
        action = QAction(name.capitalize(), menu, checkable=True)
        action.setChecked(name == current)
        action.triggered.connect(lambda _=False, n=name: _choose(n))
        group.addAction(action)
        menu.addAction(action)
        actions[name] = action
    return actions


def _choose(name: str) -> None:
    apply_theme(QApplication.instance(), name)
    save_theme(name)
