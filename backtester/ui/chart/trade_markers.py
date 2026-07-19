"""Draws live trade activity on the chart during a replay.

Visuals:
- entry arrows: ▲ (buy, teal) / ▼ (sell, red) at the fill bar and price
- exit crosses colored by the trade's net result
- dashed entry→exit connector per closed trade (teal = win, red = loss)
- for each open position, dashed horizontal SL/TP lines that move when the
  strategy modifies them (trailing stops visibly trail)
"""

from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtCore import Qt

from backtester.engine.events import (
    PositionClosed,
    PositionModified,
    PositionOpened,
)

WIN_COLOR = "#26a69a"
LOSS_COLOR = "#ef5350"
SL_COLOR = "#ef5350"
TP_COLOR = "#26a69a"


class TradeLayer:
    def __init__(self, plot_item: pg.PlotItem):
        self._plot = plot_item

        self._buy_entries = pg.ScatterPlotItem(
            symbol="t1", size=12, brush=pg.mkBrush(WIN_COLOR), pen=None
        )
        self._sell_entries = pg.ScatterPlotItem(
            symbol="t", size=12, brush=pg.mkBrush(LOSS_COLOR), pen=None
        )
        self._win_exits = pg.ScatterPlotItem(
            symbol="x", size=10, brush=pg.mkBrush(WIN_COLOR), pen=None
        )
        self._loss_exits = pg.ScatterPlotItem(
            symbol="x", size=10, brush=pg.mkBrush(LOSS_COLOR), pen=None
        )
        self._win_links = pg.PlotDataItem(
            connect="pairs",
            pen=pg.mkPen(WIN_COLOR, width=1, style=Qt.PenStyle.DashLine),
        )
        self._loss_links = pg.PlotDataItem(
            connect="pairs",
            pen=pg.mkPen(LOSS_COLOR, width=1, style=Qt.PenStyle.DashLine),
        )
        for item in (
            self._win_links, self._loss_links,
            self._buy_entries, self._sell_entries,
            self._win_exits, self._loss_exits,
        ):
            plot_item.addItem(item, ignoreBounds=True)

        self._buy_points: list[tuple[float, float]] = []
        self._sell_points: list[tuple[float, float]] = []
        self._win_exit_points: list[tuple[float, float]] = []
        self._loss_exit_points: list[tuple[float, float]] = []
        self._win_link_points: list[tuple[float, float]] = []
        self._loss_link_points: list[tuple[float, float]] = []
        #: position id -> {"sl": InfiniteLine | None, "tp": InfiniteLine | None}
        self._open_lines: dict[int, dict[str, pg.InfiniteLine | None]] = {}

    # -------------------------------------------------------------- events

    def handle(self, event) -> None:
        if isinstance(event, PositionOpened):
            self._on_opened(event)
        elif isinstance(event, PositionModified):
            self._on_modified(event)
        elif isinstance(event, PositionClosed):
            self._on_closed(event)

    def clear(self) -> None:
        self._buy_points.clear()
        self._sell_points.clear()
        self._win_exit_points.clear()
        self._loss_exit_points.clear()
        self._win_link_points.clear()
        self._loss_link_points.clear()
        for lines in self._open_lines.values():
            self._remove_lines(lines)
        self._open_lines.clear()
        self._push_scatters()
        self._push_links()

    @property
    def open_count(self) -> int:
        return len(self._open_lines)

    @property
    def closed_count(self) -> int:
        return len(self._win_exit_points) + len(self._loss_exit_points)

    # ----------------------------------------------------------- internals

    def _on_opened(self, event: PositionOpened) -> None:
        position = event.position
        point = (float(event.index), float(position.entry_price))
        if position.is_long:
            self._buy_points.append(point)
        else:
            self._sell_points.append(point)
        self._push_scatters()

        self._open_lines[position.id] = {
            "sl": self._make_level(position.sl, SL_COLOR, "SL"),
            "tp": self._make_level(position.tp, TP_COLOR, "TP"),
        }

    def _on_modified(self, event: PositionModified) -> None:
        lines = self._open_lines.get(event.position.id)
        if lines is None:
            return
        lines["sl"] = self._sync_level(lines["sl"], event.position.sl, SL_COLOR, "SL")
        lines["tp"] = self._sync_level(lines["tp"], event.position.tp, TP_COLOR, "TP")

    def _on_closed(self, event: PositionClosed) -> None:
        trade = event.trade
        lines = self._open_lines.pop(trade.id, None)
        if lines is not None:
            self._remove_lines(lines)
        self._record_closed(trade)
        self._push_scatters()
        self._push_links()

    def load_trades(self, trades: list) -> None:
        """Draw a finished run's trades in one shot (fast-run mode)."""
        self.clear()
        for trade in trades:
            entry_point = (float(trade.entry_index), float(trade.entry_price))
            if trade.direction > 0:
                self._buy_points.append(entry_point)
            else:
                self._sell_points.append(entry_point)
            self._record_closed(trade)
        self._push_scatters()
        self._push_links()

    def _record_closed(self, trade) -> None:
        exit_point = (float(trade.exit_index), float(trade.exit_price))
        entry_point = (float(trade.entry_index), float(trade.entry_price))
        if trade.net > 0:
            self._win_exit_points.append(exit_point)
            self._win_link_points.extend([entry_point, exit_point])
        else:
            self._loss_exit_points.append(exit_point)
            self._loss_link_points.extend([entry_point, exit_point])

    def _make_level(
        self, price: float | None, color: str, text: str
    ) -> pg.InfiniteLine | None:
        if price is None:
            return None
        line = pg.InfiniteLine(
            pos=price, angle=0, movable=False,
            pen=pg.mkPen(color, width=1, style=Qt.PenStyle.DashLine),
            label=text, labelOpts={"position": 0.02, "color": color},
        )
        self._plot.addItem(line, ignoreBounds=True)
        return line

    def _sync_level(self, line, price, color, text):
        if price is None:
            if line is not None:
                self._plot.removeItem(line)
            return None
        if line is None:
            return self._make_level(price, color, text)
        line.setPos(price)
        return line

    def _remove_lines(self, lines: dict) -> None:
        for line in lines.values():
            if line is not None:
                self._plot.removeItem(line)

    def _push_scatters(self) -> None:
        for item, points in (
            (self._buy_entries, self._buy_points),
            (self._sell_entries, self._sell_points),
            (self._win_exits, self._win_exit_points),
            (self._loss_exits, self._loss_exit_points),
        ):
            item.setData(
                x=[p[0] for p in points], y=[p[1] for p in points]
            )

    def _push_links(self) -> None:
        for item, points in (
            (self._win_links, self._win_link_points),
            (self._loss_links, self._loss_link_points),
        ):
            item.setData(
                x=[p[0] for p in points], y=[p[1] for p in points]
            )
