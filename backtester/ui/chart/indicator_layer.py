"""Draws one indicator's plots onto a pyqtgraph plot item.

Every item is redrawn from a **clipped** copy of its series: during a replay
the chart reveals bars one at a time, and an indicator drawn to the end of the
array would run ahead of the candles — showing values computed from bars the
run has not reached yet.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from backtester.indicators.base import DrawStyle, Indicator, Plot


def _pen(plot: Plot) -> pg.mkPen:
    style = Qt.PenStyle.DashLine if plot.dash else Qt.PenStyle.SolidLine
    return pg.mkPen(plot.color, width=plot.width, style=style)


class IndicatorLayer:
    """The drawable items for a single indicator on a single pane."""

    def __init__(self, plot_item: pg.PlotItem, candles=None):
        self._plot = plot_item
        self._candles = candles
        self._items: list = []
        self._series: dict[str, np.ndarray] = {}
        self._plots: list[Plot] = []
        self._limit: int | None = None
        self._owns_candle_color = False

    # ---------------------------------------------------------------- data

    def set_plots(self, plots: list[Plot], values: dict[str, np.ndarray]) -> None:
        self.clear()
        self._plots = [p for p in plots if p.key in values]
        self._series = {p.key: np.asarray(values[p.key], dtype=float) for p in self._plots}
        for plot in self._plots:
            if plot.style is DrawStyle.NONE:
                continue
            if plot.style is DrawStyle.CANDLE_COLOR:
                self._owns_candle_color = True
                continue
            if plot.style is DrawStyle.FILL:
                self._add_fill(plot)
            elif plot.style is DrawStyle.ARROW:
                self._add_scatter(plot)
            elif plot.style is DrawStyle.HISTOGRAM:
                self._add_histogram(plot)
            else:
                self._add_line(plot)
        self._refresh()

    def set_visible_length(self, k: int | None) -> None:
        self._limit = k
        self._refresh()

    def clear(self) -> None:
        for item in self._items:
            self._plot.removeItem(item)
        self._items.clear()
        self._plots = []
        self._series = {}
        if self._owns_candle_color and self._candles is not None:
            self._candles.set_color_index(None, ())
        self._owns_candle_color = False

    # ----------------------------------------------------------- internals

    def _clipped(self, key: str) -> tuple[np.ndarray, np.ndarray]:
        values = self._series.get(key)
        if values is None:
            return np.empty(0), np.empty(0)
        n = len(values) if self._limit is None else max(0, min(self._limit, len(values)))
        return np.arange(n, dtype=float), values[:n]

    def _add_line(self, plot: Plot) -> None:
        item = pg.PlotDataItem(pen=_pen(plot), connect="finite")
        self._plot.addItem(item, ignoreBounds=False)
        self._items.append((plot, item))

    def _add_scatter(self, plot: Plot) -> None:
        item = pg.ScatterPlotItem(
            symbol=plot.symbol, size=plot.size,
            brush=pg.mkBrush(plot.color), pen=None,
        )
        self._plot.addItem(item, ignoreBounds=True)
        self._items.append((plot, item))

    def _add_histogram(self, plot: Plot) -> None:
        item = pg.BarGraphItem(x=[], height=[], width=0.7, brush=plot.color, pen=None)
        self._plot.addItem(item, ignoreBounds=True)
        self._items.append((plot, item))

    def _add_fill(self, plot: Plot) -> None:
        upper = pg.PlotDataItem(pen=pg.mkPen(None), connect="finite")
        lower = pg.PlotDataItem(pen=pg.mkPen(None), connect="finite")
        colour = QColor(plot.color)
        colour.setAlpha(70)
        fill = pg.FillBetweenItem(upper, lower, brush=pg.mkBrush(colour))
        for item in (upper, lower, fill):
            self._plot.addItem(item, ignoreBounds=True)
        self._items.append((plot, (upper, lower, fill)))

    def _refresh(self) -> None:
        for plot, item in self._items:
            x, y = self._clipped(plot.key)
            if plot.style is DrawStyle.FILL:
                upper, lower, _fill = item
                _, other = self._clipped(plot.fill_with)
                upper.setData(x=x, y=y)
                lower.setData(x=x[: len(other)], y=other[: len(x)])
            elif plot.style is DrawStyle.ARROW:
                mask = np.isfinite(y)
                item.setData(x=x[mask], y=y[mask])
            elif plot.style is DrawStyle.HISTOGRAM:
                mask = np.isfinite(y)
                item.setOpts(x=x[mask], height=y[mask], width=0.7)
            else:
                item.setData(x=x, y=y)
        self._refresh_candle_colors()

    def _refresh_candle_colors(self) -> None:
        if not self._owns_candle_color or self._candles is None:
            return
        for plot in self._plots:
            if plot.style is not DrawStyle.CANDLE_COLOR:
                continue
            _x, values = self._clipped(plot.key)
            self._candles.set_color_index(values, plot.colors)
            return


class IndicatorSet:
    """All indicators attached to one chart, across its panes."""

    def __init__(self):
        self._layers: list[tuple[Indicator, IndicatorLayer]] = []

    def add(self, indicator: Indicator, layer: IndicatorLayer) -> None:
        self._layers.append((indicator, layer))

    def set_visible_length(self, k: int | None) -> None:
        for _indicator, layer in self._layers:
            layer.set_visible_length(k)

    def clear(self) -> None:
        for _indicator, layer in self._layers:
            layer.clear()
        self._layers.clear()

    def __len__(self) -> int:
        return len(self._layers)

    @property
    def indicators(self) -> list[Indicator]:
        """The attached indicators, once each — one can own several layers
        (RSI MA Arrows draws an oscillator *and* arrows on the candles)."""
        seen: dict[int, Indicator] = {}
        for indicator, _layer in self._layers:
            seen.setdefault(id(indicator), indicator)
        return list(seen.values())
