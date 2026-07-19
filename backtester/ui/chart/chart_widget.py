"""Candlestick chart widget: crosshair, OHLC readout, indicator overlays.

Pan with left-drag / mouse wheel (X only); Y auto-fits the visible window.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .candlestick_item import CandlestickItem
from .time_axis import TimeAxisItem

BACKGROUND = "#131722"
CROSSHAIR_PEN = pg.mkPen("#787b86", width=1, style=Qt.PenStyle.DashLine)
OVERLAY_COLORS = ["#f0a732", "#42a5f5", "#ab47bc", "#26c6da", "#ec407a", "#d4e157"]
INITIAL_BARS = 300


class ChartWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._df: pd.DataFrame | None = None
        self._title = ""
        self._overlays: dict[str, pg.PlotDataItem] = {}
        self._color_cycle = 0

        self.info_label = QLabel(" ")
        self.info_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 2px;"
        )

        self.time_axis = TimeAxisItem()
        self.plot = pg.PlotWidget(axisItems={"bottom": self.time_axis})
        self.plot.setBackground(BACKGROUND)
        self.plot.showGrid(x=True, y=True, alpha=0.12)

        self.candles = CandlestickItem()
        self.plot.addItem(self.candles)

        view_box = self.plot.getPlotItem().getViewBox()
        view_box.setMouseEnabled(x=True, y=False)
        view_box.enableAutoRange(y=True)
        view_box.setAutoVisible(y=True)
        self._view_box = view_box

        self._vline = pg.InfiniteLine(angle=90, pen=CROSSHAIR_PEN, movable=False)
        self._hline = pg.InfiniteLine(angle=0, pen=CROSSHAIR_PEN, movable=False)
        for line in (self._vline, self._hline):
            line.setVisible(False)
            self.plot.addItem(line, ignoreBounds=True)
        self._mouse_proxy = pg.SignalProxy(
            self.plot.scene().sigMouseMoved, rateLimit=60, slot=self._on_mouse_moved
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.info_label)
        layout.addWidget(self.plot)

    # ---------------------------------------------------------------- data

    def set_data(self, df: pd.DataFrame, title: str = "") -> None:
        """Load a bar frame (canonical schema) and show the most recent bars."""
        self._df = df
        self._title = title
        self.clear_overlays()

        n = len(df)
        self.candles.set_data(
            df["open"].to_numpy(float), df["high"].to_numpy(float),
            df["low"].to_numpy(float), df["close"].to_numpy(float),
        )
        self.time_axis.set_times(df["time"].to_numpy())

        self._view_box.setLimits(
            xMin=-10, xMax=n + 10, minXRange=8, maxXRange=max(n * 1.1, 20)
        )
        start = max(0, n - INITIAL_BARS)
        self.plot.setXRange(start, n, padding=0.02)
        self._update_info(n - 1)

    @property
    def bar_count(self) -> int:
        return len(self.candles)

    @property
    def df(self) -> pd.DataFrame | None:
        return self._df

    # ------------------------------------------------------------ overlays

    def add_overlay(self, name: str, values: np.ndarray) -> str:
        """Draw (or replace) a named indicator line; returns its color."""
        self.remove_overlay(name)
        color = OVERLAY_COLORS[self._color_cycle % len(OVERLAY_COLORS)]
        self._color_cycle += 1
        item = pg.PlotDataItem(
            x=np.arange(len(values)), y=values,
            pen=pg.mkPen(color, width=1.5), connect="finite",
        )
        self.plot.addItem(item)
        self._overlays[name] = item
        return color

    def remove_overlay(self, name: str) -> None:
        item = self._overlays.pop(name, None)
        if item is not None:
            self.plot.removeItem(item)

    def clear_overlays(self) -> None:
        for name in list(self._overlays):
            self.remove_overlay(name)
        self._color_cycle = 0

    @property
    def overlay_names(self) -> list[str]:
        return list(self._overlays)

    # ----------------------------------------------------------- crosshair

    def _on_mouse_moved(self, args) -> None:
        if self._df is None:
            return
        pos = args[0]
        if not self.plot.sceneBoundingRect().contains(pos):
            self._vline.setVisible(False)
            self._hline.setVisible(False)
            return
        point = self._view_box.mapSceneToView(pos)
        i = int(round(point.x()))
        if 0 <= i < len(self._df):
            self._vline.setPos(i)
            self._hline.setPos(point.y())
            self._vline.setVisible(True)
            self._hline.setVisible(True)
            self._update_info(i)

    def _update_info(self, i: int) -> None:
        if self._df is None or not (0 <= i < len(self._df)):
            return
        self.info_label.setText(format_bar(self._df, i, self._title))


def format_bar(df: pd.DataFrame, i: int, title: str = "") -> str:
    row = df.iloc[i]
    o, h, l, c = row["open"], row["high"], row["low"], row["close"]
    change = (c - o) / o * 100 if o else 0.0
    text = (
        f"{title}   {pd.Timestamp(row['time']):%Y-%m-%d %H:%M}   "
        f"O {o:g}  H {h:g}  L {l:g}  C {c:g}  ({change:+.2f}%)"
    )
    if "tick_volume" in df.columns:
        text += f"  Vol {int(row['tick_volume']):,}"
    return text
