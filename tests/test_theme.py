"""Application theme: applying, persisting, and the View > Theme menu."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication, QMenu

from backtester.ui import theme


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def ini(tmp_path, monkeypatch):
    settings = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    monkeypatch.setattr("backtester.ui.theme.app_settings", lambda: settings)
    return settings


def window_lightness(app):
    return app.palette().color(QPalette.ColorRole.Window).lightness()


def test_apply_dark_and_light(qapp):
    theme.apply_theme(qapp, "dark")
    assert qapp.style().name().lower() == "fusion"
    assert window_lightness(qapp) < 80
    theme.apply_theme(qapp, "light")
    assert window_lightness(qapp) > 200
    theme.apply_theme(qapp, "system")


def test_theme_persists(ini):
    assert theme.load_theme() == "system"
    theme.save_theme("dark")
    assert theme.load_theme() == "dark"
    ini.setValue("ui/theme", "bogus")
    assert theme.load_theme() == "system"


def test_menu_switches_and_saves_theme(qapp, ini):
    menu = QMenu()
    actions = theme.populate_theme_menu(menu)
    try:
        assert list(actions) == ["system", "light", "dark"]
        assert actions["system"].isChecked()
        actions["dark"].trigger()
        assert theme.load_theme() == "dark"
        assert window_lightness(qapp) < 80
        assert actions["dark"].isChecked() and not actions["system"].isChecked()
    finally:
        theme.apply_theme(qapp, "system")
