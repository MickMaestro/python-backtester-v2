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

from .candlestick_item import CandlestickItem
from .chart_text import CornerTextItem, SegmentLabelItem


def _pen(plot: Plot) -> pg.mkPen:
    style = Qt.PenStyle.DashLine if plot.dash else Qt.PenStyle.SolidLine
    return pg.mkPen(plot.color, width=plot.width, style=style)


def zigzag_points(highs: np.ndarray, lows: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Vertices of an MT5 DRAW_ZIGZAG through two pivot buffers.

    A bar holding both a high and a low contributes both, ordered so the line
    alternates: after a low it goes to the high first, after a high the low.
    """
    xs: list[float] = []
    ys: list[float] = []
    last_was_high: bool | None = None
    n = min(len(highs), len(lows))
    for i in np.nonzero(np.isfinite(highs[:n]) | np.isfinite(lows[:n]))[0]:
        hi, lo = highs[i], lows[i]
        if np.isfinite(hi) and np.isfinite(lo):
            pair = [(lo, False), (hi, True)] if last_was_high else [(hi, True), (lo, False)]
        elif np.isfinite(hi):
            pair = [(hi, True)]
        else:
            pair = [(lo, False)]
        for value, is_high in pair:
            xs.append(float(i))
            ys.append(float(value))
            last_was_high = is_high
    return np.asarray(xs), np.asarray(ys)


def _graphics(item) -> tuple:
    """The drawable objects behind one plot (a fill owns three)."""
    return item if isinstance(item, tuple) else (item,)


class RepaintSource:
    """What a repainting indicator showed with only the revealed bars.

    The full-history result is right for settled bars, but a zigzag's newest
    swing is provisional until price turns: with hindsight it may never have
    been a swing at all, and leaving it out would hint at what comes next.
    So for the newest bars the indicator is recomputed on the revealed tail
    (``repaint_window`` bars) and its second half spliced over the full
    result — far enough in for the tail run to have settled.
    """

    def __init__(self, indicator: Indicator, df, full: dict[str, np.ndarray]):
        self.indicator = indicator
        self.df = df
        self.full = {key: np.asarray(v, dtype=float) for key, v in full.items()}
        self.window = int(indicator.repaint_window)
        # Series holding bar indices, which must be shifted from tail-relative.
        self.index_keys = {
            name for plot in indicator.plots
            for name in (plot.known_at, plot.expires_at) if name
        }
        self._k: int | None = None
        self._merged = self.full

    def values_at(self, k: int | None) -> dict[str, np.ndarray]:
        if k is None or self.window <= 0 or k >= len(self.df):
            return self.full
        if k == self._k:
            return self._merged
        start = max(0, k - self.window)
        boundary = start + self.window // 2 if start > 0 else 0
        merged = {key: values.copy() for key, values in self.full.items()}
        if k > 0:
            try:
                tail = self.indicator.calculate(self.df.iloc[start:k].reset_index(drop=True))
            except Exception:
                tail = None
            for key, values in (tail or {}).items():
                if key not in merged:
                    continue
                part = np.asarray(values, dtype=float)[boundary - start:]
                if key in self.index_keys:
                    part = part + start
                merged[key][boundary:k] = part
        self._k, self._merged = k, merged
        return merged


class IndicatorLayer:
    """The drawable items for a single indicator on a single pane."""

    def __init__(self, plot_item: pg.PlotItem, candles=None):
        self._plot = plot_item
        self._candles = candles
        self._items: list[tuple[Plot, object]] = []
        self._series: dict[str, np.ndarray] = {}
        self._plots: list[Plot] = []
        self._limit: int | None = None
        self._owns_candle_color = False
        self._source: RepaintSource | None = None

    def set_repaint_source(self, source: RepaintSource | None) -> None:
        self._source = source

    # ---------------------------------------------------------------- data

    def set_plots(self, plots: list[Plot], values: dict[str, np.ndarray]) -> None:
        self.clear()
        self._plots = [
            p for p in plots
            if p.key in values
            or (p.style is DrawStyle.CANDLES and f"{p.key}_close" in values)
        ]
        self._series = {
            key: np.asarray(series, dtype=float) for key, series in values.items()
        }
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
            elif plot.style is DrawStyle.HISTOGRAM2:
                self._add_histogram2(plot)
            elif plot.style is DrawStyle.CORNER_TEXT:
                self._add_corner_text(plot)
            elif plot.style is DrawStyle.CANDLES:
                self._add_candles(plot)
            else:
                self._add_line(plot)
        self._refresh()

    def set_visible_length(self, k: int | None) -> None:
        self._limit = k
        if self._source is not None:
            self._series = self._source.values_at(k)
        self._refresh()

    def clear(self) -> None:
        # Each entry is (plot, graphics), and a fill's graphics is itself a
        # tuple — handing the pair straight to removeItem silently does
        # nothing, which used to leave indicators on the chart after removal.
        for _plot, item in self._items:
            for graphic in _graphics(item):
                self._plot.removeItem(graphic)
        self._items.clear()
        self._plots = []
        self._series = {}
        if self._owns_candle_color and self._candles is not None:
            self._candles.set_color_index(None, ())
        self._owns_candle_color = False

    @property
    def items(self) -> list:
        """Every graphics object this layer put on the plot."""
        return [g for _plot, item in self._items for g in _graphics(item)]

    # ----------------------------------------------------------- internals

    def _clipped(
        self, key: str, known_at: str = "", expires_at: str = ""
    ) -> tuple[np.ndarray, np.ndarray]:
        values = self._series.get(key)
        if values is None:
            return np.empty(0), np.empty(0)
        n = len(values) if self._limit is None else max(0, min(self._limit, len(values)))
        clipped = values[:n]
        known = self._series.get(known_at) if known_at else None
        if known is not None and self._limit is not None:
            # A back-painted value stays hidden until its confirming bar shows.
            clipped = np.where(known[:n] < n, clipped, np.nan)
        expires = self._series.get(expires_at) if expires_at else None
        if expires is not None:
            # A superseded value disappears once a bar past its expiry shows.
            clipped = np.where(expires[:n] >= n - 1, clipped, np.nan)
        return np.arange(n, dtype=float), clipped

    def _add_line(self, plot: Plot) -> None:
        item = pg.PlotDataItem(pen=_pen(plot), connect="finite")
        self._plot.addItem(item, ignoreBounds=not plot.autoscale)
        if plot.text:
            labels = SegmentLabelItem(plot.text, color=plot.color)
            self._plot.addItem(labels, ignoreBounds=True)
            self._items.append((plot, (item, labels)))
        else:
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

    def _add_histogram2(self, plot: Plot) -> None:
        item = pg.BarGraphItem(x=[], y0=[], y1=[], width=0.7, brush=plot.color, pen=None)
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

    def _add_corner_text(self, plot: Plot) -> None:
        item = CornerTextItem(corner=plot.corner)
        self._plot.addItem(item, ignoreBounds=True)
        self._items.append((plot, item))

    def _add_candles(self, plot: Plot) -> None:
        item = CandlestickItem()
        if len(plot.colors) >= 2:
            item.set_colors(plot.colors[0], plot.colors[1])
        self._plot.addItem(item, ignoreBounds=True)
        self._items.append((plot, item))

    def _refresh_candles(self, plot: Plot, item: CandlestickItem) -> None:
        o, h, l, c = (
            self._clipped(f"{plot.key}_{part}", plot.known_at, plot.expires_at)[1]
            for part in ("open", "high", "low", "close")
        )
        item.set_data(o, h, l, c)
        if plot.color_key and plot.colors:
            item.set_color_index(self._clipped(plot.color_key)[1], plot.colors)

    def _refresh(self) -> None:
        for plot, item in self._items:
            x, y = self._clipped(plot.key, plot.known_at, plot.expires_at)
            if plot.style is DrawStyle.FILL:
                upper, lower, _fill = item
                _, other = self._clipped(plot.fill_with, plot.known_at, plot.expires_at)
                upper.setData(x=x, y=y)
                lower.setData(x=x[: len(other)], y=other[: len(x)])
            elif plot.style in (DrawStyle.ARROW, DrawStyle.SECTION):
                mask = np.isfinite(y)
                item.setData(x=x[mask], y=y[mask])
            elif plot.style is DrawStyle.ZIGZAG:
                _, lows = self._clipped(plot.fill_with, plot.known_at, plot.expires_at)
                zx, zy = zigzag_points(y, lows)
                item.setData(x=zx, y=zy)
            elif plot.style is DrawStyle.HISTOGRAM:
                mask = np.isfinite(y)
                item.setOpts(x=x[mask], height=y[mask], width=0.7)
            elif plot.style is DrawStyle.HISTOGRAM2:
                _, other = self._clipped(plot.fill_with, plot.known_at, plot.expires_at)
                m = min(len(y), len(other))
                mask = np.isfinite(y[:m]) & np.isfinite(other[:m])
                item.setOpts(x=x[:m][mask], y0=other[:m][mask], y1=y[:m][mask], width=0.7)
            elif plot.style is DrawStyle.CORNER_TEXT:
                self._refresh_corner_text(plot, item, y)
            elif plot.style is DrawStyle.CANDLES:
                self._refresh_candles(plot, item)
            elif isinstance(item, tuple):        # a line with segment labels
                line, labels = item
                line.setData(x=x, y=y)
                labels.set_series(y)
            else:
                item.setData(x=x, y=y)
        self._refresh_candle_colors()

    def _refresh_corner_text(self, plot: Plot, item: CornerTextItem, y) -> None:
        """Show the most recent revealed value, formatted by the plot's text."""
        finite = np.nonzero(np.isfinite(y))[0]
        if len(finite) == 0:
            item.set_text("")
            return
        last = int(finite[-1])
        value = float(y[last])
        template = plot.text or "{value:.2f}"
        colour = plot.color
        if plot.colors and plot.color_key:
            slots = self._series.get(plot.color_key)
            if slots is not None and last < len(slots) and np.isfinite(slots[last]):
                slot = int(slots[last])
                if 0 <= slot < len(plot.colors):
                    colour = plot.colors[slot]
        item.set_text(template.format(value=value), colour)

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
        (an oscillator that also marks the candles)."""
        seen: dict[int, Indicator] = {}
        for indicator, _layer in self._layers:
            seen.setdefault(id(indicator), indicator)
        return list(seen.values())
