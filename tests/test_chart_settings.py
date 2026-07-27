"""Chart display settings: model, separators, and applying to the chart."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pandas as pd
import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from backtester.ui.chart.chart_settings import ChartSettings, ChartSettingsDialog
from backtester.ui.chart.chart_widget import ChartWidget
from backtester.ui.chart.separators import compute_separators


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def intraday_df(n=400, freq="1h"):
    return pd.DataFrame(
        {
            "time": pd.date_range("2024-01-01", periods=n, freq=freq),
            "open": 1.10, "high": 1.101, "low": 1.099, "close": 1.1005,
            "tick_volume": 5,
        }
    )


# ------------------------------------------------------------- model

def test_defaults_grid_off_separators_on():
    d = ChartSettings()
    assert d.grid_visible is False
    assert d.separators_visible is True


def test_settings_roundtrip(qapp, tmp_path, monkeypatch):
    ini = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    monkeypatch.setattr("backtester.ui.chart.chart_settings.app_settings", lambda: ini)

    ChartSettings(
        up_color="#010203", down_color="#040506", background="#070809",
        grid_visible=True, grid_color="#0a0b0c",
        separators_visible=False, separator_color="#0d0e0f",
    ).save()
    loaded = ChartSettings.load()
    assert loaded.up_color == "#010203"
    assert loaded.grid_visible is True
    assert loaded.separators_visible is False
    assert loaded.separator_color == "#0d0e0f"


# ------------------------------------------------------------- separators

def test_compute_separators_intraday_weekdays():
    idx, labels = compute_separators(intraday_df(240, "1h"))  # 10 days
    assert len(idx) == 9                       # 9 day changes over 10 days
    assert labels[0] in {
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    }
    assert idx[0] == 24                          # first new day is 24 hours in


def test_compute_separators_daily_months():
    df = pd.DataFrame(
        {"time": pd.date_range("2024-01-01", periods=120, freq="1D"),
         "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}
    )
    idx, labels = compute_separators(df)
    assert labels[0] == "Feb 2024"
    assert len(idx) >= 3


def test_compute_separators_short_frame():
    idx, labels = compute_separators(intraday_df(1))
    assert len(idx) == 0 and labels == []


# ------------------------------------------------------------- chart widget

def test_chart_applies_settings(qapp):
    chart = ChartWidget()
    chart.set_data(intraday_df(), "T")
    s = ChartSettings(
        up_color="#00ff00", down_color="#ff0000", background="#000000",
        grid_visible=True, grid_color="#333333",
        separators_visible=True, separator_color="#8080ff",
    )
    chart.apply_display_settings(s)
    assert chart.settings is s
    assert chart.candles._up_color.name() == "#00ff00"
    assert chart.separators._visible is True
    chart.resize(800, 500)
    assert not chart.grab().isNull()


def test_separators_hidden_when_disabled(qapp):
    chart = ChartWidget()
    chart.set_data(intraday_df(), "T")
    chart.apply_display_settings(ChartSettings(separators_visible=False))
    assert chart.separators._visible is False
    assert not chart.grab().isNull()


def test_separators_clip_to_revealed_bars(qapp):
    chart = ChartWidget()
    chart.set_data(intraday_df(240), "T")
    chart.reveal_to(30)                          # only ~1 day revealed
    assert chart.separators._limit == 30
    assert not chart.grab().isNull()


def test_dialog_result_reflects_edits(qapp):
    dialog = ChartSettingsDialog(ChartSettings())
    dialog.up_btn.setColor("#123456")
    dialog.grid_check.setChecked(True)
    dialog.sep_check.setChecked(False)
    out = dialog.result_settings()
    assert out.up_color == "#123456"
    assert out.grid_visible is True
    assert out.separators_visible is False


def test_dialog_restore_defaults(qapp):
    dialog = ChartSettingsDialog(
        ChartSettings(grid_visible=True, separators_visible=False)
    )
    dialog._restore_defaults()
    out = dialog.result_settings()
    assert out.grid_visible is False
    assert out.separators_visible is True
