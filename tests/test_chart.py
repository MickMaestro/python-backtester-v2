"""Offscreen tests for the chart widgets (no display needed)."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pandas as pd
import pytest
from PySide6.QtWidgets import QApplication

from backtester.ui.chart.candlestick_item import CandlestickItem
from backtester.ui.chart.chart_widget import ChartWidget, format_bar
from backtester.ui.chart.time_axis import TimeAxisItem


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def make_df(n: int = 500, freq: str = "1h") -> pd.DataFrame:
    rng = np.random.default_rng(7)
    closes = 1.10 + np.cumsum(rng.normal(0, 0.0008, n))
    opens = np.roll(closes, 1)
    opens[0] = closes[0]
    highs = np.maximum(opens, closes) + 0.0004
    lows = np.minimum(opens, closes) - 0.0004
    return pd.DataFrame(
        {
            "time": pd.date_range("2024-01-01", periods=n, freq=freq),
            "open": opens, "high": highs, "low": lows, "close": closes,
            "tick_volume": rng.integers(100, 5000, n),
        }
    )


def test_set_data_shows_recent_window(qapp):
    chart = ChartWidget()
    chart.set_data(make_df(1000), "TEST H1")
    assert chart.bar_count == 1000
    (x0, x1), _ = chart.plot.getPlotItem().getViewBox().viewRange()
    assert x1 >= 999            # latest bar in view
    assert x1 - x0 < 400        # ~INITIAL_BARS window, not the whole series


def test_databounds_fit_visible_window(qapp):
    df = make_df(300)
    item = CandlestickItem()
    item.set_data(
        df["open"].to_numpy(), df["high"].to_numpy(),
        df["low"].to_numpy(), df["close"].to_numpy(),
    )
    lo, hi = item.dataBounds(1, orthoRange=(100, 200))
    window = df.iloc[100:201]
    assert lo == pytest.approx(window["low"].min())
    assert hi == pytest.approx(window["high"].max())
    assert item.dataBounds(0) == (0.0, 299.0)


def test_100k_bars_render_via_grab(qapp):
    chart = ChartWidget()
    chart.set_data(make_df(100_000, freq="1min"), "BIG M1")
    chart.resize(1000, 600)
    assert not chart.grab().isNull()          # zoomed-in initial window
    chart.plot.setXRange(0, 100_000)          # fully zoomed out: polyline path
    assert not chart.grab().isNull()


def test_overlay_add_replace_clear(qapp):
    chart = ChartWidget()
    df = make_df(200)
    chart.set_data(df, "TEST")
    values = df["close"].rolling(20).mean().to_numpy()
    chart.add_overlay("SMA(20)", values)
    chart.add_overlay("SMA(20)", values)      # replace, not duplicate
    chart.add_overlay("EMA(50)", values)
    assert sorted(chart.overlay_names) == ["EMA(50)", "SMA(20)"]
    chart.clear_overlays()
    assert chart.overlay_names == []


def test_time_axis_formats(qapp):
    hourly = TimeAxisItem()
    hourly.set_times(pd.date_range("2024-01-01", periods=100, freq="1h").to_numpy())
    assert ":" in hourly.tickStrings([50], scale=1, spacing=10)[0]

    daily = TimeAxisItem()
    daily.set_times(pd.date_range("2024-01-01", periods=100, freq="1D").to_numpy())
    label = daily.tickStrings([50], scale=1, spacing=10)[0]
    assert ":" not in label and label.startswith("2024")

    assert hourly.tickStrings([-5, 1_000_000], scale=1, spacing=10) == ["", ""]


def test_format_bar_readout():
    df = make_df(10)
    text = format_bar(df, 5, "EURUSD H1")
    assert "EURUSD H1" in text
    assert "O " in text and "Vol" in text
