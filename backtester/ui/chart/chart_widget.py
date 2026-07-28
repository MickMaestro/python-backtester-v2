"""Candlestick chart widget: crosshair, OHLC readout, indicator plugins.

Pan with left-drag / mouse wheel (X only); Y auto-fits the visible window.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from backtester.indicators.base import Indicator, Pane

from .candlestick_item import CandlestickItem
from .chart_settings import ChartSettings, ChartSettingsDialog
from .indicator_layer import IndicatorLayer, IndicatorSet
from .indicator_pane import IndicatorPane
from .separators import SeparatorLines, compute_separators
from .time_axis import TimeAxisItem

BACKGROUND = "#131722"
CROSSHAIR_PEN = pg.mkPen("#787b86", width=1, style=Qt.PenStyle.DashLine)
INITIAL_BARS = 300
#: Small gap kept to the right of the newest candle when following (bars).
RIGHT_PAD_BARS = 2.0
#: Blank space to the right of the newest candle when "chart shift" is on,
#: as a fraction of the visible width (MT5-style shift).
SHIFT_FRACTION = 0.2


class ChartWidget(QWidget):
    #: Emitted when auto-follow turns off because the user panned/zoomed.
    follow_changed = Signal(bool)
    #: Emitted with the new ChartSettings when the user edits display settings.
    display_settings_changed = Signal(object)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._df: pd.DataFrame | None = None
        self._title = ""
        self._follow = True
        self._shift = False
        self._settings = ChartSettings.load()

        self.info_label = QLabel(" ")
        self.info_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 2px;"
        )
        self.display_button = QPushButton("Display…")
        self.display_button.setToolTip("Chart colours, grid, and period separators")
        self.display_button.clicked.connect(self._open_display_settings)
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.addWidget(self.info_label, stretch=1)
        top.addWidget(self.display_button)

        self.time_axis = TimeAxisItem()
        self.plot = pg.PlotWidget(axisItems={"bottom": self.time_axis})

        self.candles = CandlestickItem()
        self.plot.addItem(self.candles)
        self.separators = SeparatorLines()
        self.plot.addItem(self.separators, ignoreBounds=True)

        view_box = self.plot.getPlotItem().getViewBox()
        view_box.setMouseEnabled(x=True, y=False)
        view_box.enableAutoRange(y=True)
        view_box.setAutoVisible(y=True)
        view_box.sigRangeChangedManually.connect(self._on_manual_range)
        self._view_box = view_box

        self._vline = pg.InfiniteLine(angle=90, pen=CROSSHAIR_PEN, movable=False)
        self._hline = pg.InfiniteLine(angle=0, pen=CROSSHAIR_PEN, movable=False)
        for line in (self._vline, self._hline):
            line.setVisible(False)
            self.plot.addItem(line, ignoreBounds=True)
        self._mouse_proxy = pg.SignalProxy(
            self.plot.scene().sigMouseMoved, rateLimit=60, slot=self._on_mouse_moved
        )

        self._indicators = IndicatorSet()
        self._panes: list[IndicatorPane] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(top)
        layout.addWidget(self.plot, stretch=1)
        self._layout = layout

        self.apply_display_settings(self._settings)

    # ---------------------------------------------------------------- data

    def set_data(self, df: pd.DataFrame, title: str = "") -> None:
        """Load a bar frame (canonical schema) and show the most recent bars."""
        self._df = df
        self._title = title
        # Indicators are computed against a specific frame; the caller
        # re-attaches them for the new one.
        self.clear_indicators()

        n = len(df)
        self.candles.set_data(
            df["open"].to_numpy(float), df["high"].to_numpy(float),
            df["low"].to_numpy(float), df["close"].to_numpy(float),
        )
        self.time_axis.set_times(df["time"].to_numpy())
        self.separators.set_separators(*compute_separators(df))

        # Allow room past the last bar so "chart shift" can hold blank space
        # on the right without the range limit fighting it.
        self._view_box.setLimits(
            xMin=-10, xMax=n + INITIAL_BARS, minXRange=8, maxXRange=max(n * 1.1, 20)
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

    # -------------------------------------------------------------- replay

    def reveal_to(self, k: int) -> None:
        """Show only the first ``k`` bars; when following, scroll the window
        (keeping its width) so the newest candle stays in view."""
        self.candles.set_visible_length(k)
        self.separators.set_visible_length(k)
        self._indicators.set_visible_length(k)
        if k <= 0:
            return
        if self._follow:
            self._follow_scroll(k)
        self._update_info(k - 1)

    def reveal_all(self) -> None:
        self.candles.set_visible_length(None)
        self.separators.set_visible_length(None)
        self._indicators.set_visible_length(None)

    def set_follow(self, on: bool) -> None:
        self._follow = on
        if on:
            k = self.candles.visible_length
            if k > 0:
                self._follow_scroll(k, force=True)

    def set_shift(self, on: bool) -> None:
        """Toggle blank space to the right of the newest candle (MT5 shift)."""
        self._shift = on
        if self._follow:
            k = self.candles.visible_length
            if k > 0:
                self._follow_scroll(k, force=True)

    @property
    def follow(self) -> bool:
        return self._follow

    @property
    def shift(self) -> bool:
        return self._shift

    # ------------------------------------------------------ display settings

    @property
    def settings(self) -> ChartSettings:
        return self._settings

    def apply_display_settings(self, settings: ChartSettings) -> None:
        self._settings = settings
        self.plot.setBackground(settings.background)
        self.candles.set_colors(settings.up_color, settings.down_color)

        alpha = 0.3 if settings.grid_visible else 0.0
        self.plot.showGrid(x=settings.grid_visible, y=settings.grid_visible, alpha=alpha)
        axis_color = settings.grid_color if settings.grid_visible else "#787b86"
        for name in ("left", "bottom"):
            axis = self.plot.getAxis(name)
            axis.setPen(pg.mkPen(axis_color))
            axis.setTextPen(pg.mkPen("#9598a1"))

        self.separators.set_style(settings.separators_visible, settings.separator_color)
        for pane in self._panes:
            pane.apply_display_settings(settings)

    def _open_display_settings(self) -> None:
        result = ChartSettingsDialog.edit(self, self._settings)
        if result is None:
            return
        result.save()
        self.apply_display_settings(result)
        self.display_settings_changed.emit(result)

    def _follow_scroll(self, k: int, force: bool = False) -> None:
        """Slide the view so the newest bar sits at its anchor, **preserving
        the current width** (no squeezing)."""
        (x0, x1), _ = self._view_box.viewRange()
        width = max(x1 - x0, 10.0)
        newest = k - 1
        blank_right = width * SHIFT_FRACTION if self._shift else RIGHT_PAD_BARS
        right = newest + blank_right
        # Until the newest bar reaches the anchor, let candles fill from the
        # left (no empty gap); once it does, keep it pinned there.
        if force or right > x1:
            self.plot.setXRange(right - width, right, padding=0)

    def _on_manual_range(self, *_args) -> None:
        if self._follow:
            self._follow = False
            self.follow_changed.emit(False)

    # ---------------------------------------------------------- indicators

    def set_indicators(self, indicators: list[Indicator]) -> list[str]:
        """Attach (replacing any existing) indicator plugins to this chart.

        Each is computed against the loaded bar frame; one that raises is
        skipped and reported rather than taking the whole chart down with it.
        Returns the errors, so the caller can show them.
        """
        self.clear_indicators()
        if self._df is None:
            return []

        errors: list[str] = []
        for indicator in indicators:
            try:
                values = indicator.calculate(self._df)
            except Exception as exc:
                errors.append(f"{indicator.label}: {type(exc).__name__}: {exc}")
                continue
            self._attach(indicator, values)

        # Newly built panes start at the reveal limit the chart is already at.
        self._indicators.set_visible_length(self.candles.visible_length)
        return errors

    def _attach(self, indicator: Indicator, values: dict) -> None:
        price_plots = [
            plot for plot in indicator.plots
            if (plot.pane or indicator.pane) is Pane.PRICE
        ]
        pane_plots = [
            plot for plot in indicator.plots
            if (plot.pane or indicator.pane) is Pane.SEPARATE
        ]
        if price_plots:
            layer = IndicatorLayer(self.plot.getPlotItem(), candles=self.candles)
            layer.set_plots(price_plots, values)
            self._indicators.add(indicator, layer)
        if pane_plots:
            pane = IndicatorPane(indicator, self.plot.getPlotItem(), parent=self)
            pane.apply_display_settings(self._settings)
            self._layout.addWidget(pane)
            self._panes.append(pane)
            layer = IndicatorLayer(pane.plot_item)
            layer.set_plots(pane_plots, values)
            self._indicators.add(indicator, layer)

    def clear_indicators(self) -> None:
        self._indicators.clear()
        for pane in self._panes:
            self._layout.removeWidget(pane)
            pane.setParent(None)
            pane.deleteLater()
        self._panes.clear()

    @property
    def indicators(self) -> list[Indicator]:
        return self._indicators.indicators

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
        # Clamp to revealed bars so the readout can't leak future data mid-replay.
        if 0 <= i < self.candles.visible_length:
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
