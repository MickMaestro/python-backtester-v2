"""A sub-window under the candles for a separate-pane indicator (RSI, …).

X-linked to the price chart the same way the backtest tab's equity curve is,
so panning and zooming move every pane together.
"""

from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from backtester.indicators.base import Indicator

PANE_HEIGHT = 140


class IndicatorPane(QWidget):
    def __init__(self, indicator: Indicator, main_plot: pg.PlotItem, parent=None):
        super().__init__(parent)
        self.indicator = indicator

        self.plot = pg.PlotWidget()
        self.plot.setFixedHeight(PANE_HEIGHT)
        self.plot.getPlotItem().setXLink(main_plot)
        self.plot.getPlotItem().hideAxis("bottom")
        self.plot.getPlotItem().getViewBox().setMouseEnabled(x=True, y=False)

        self.title = QLabel(indicator.label)
        self.title.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 11px; color: #9598a1;"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title)
        layout.addWidget(self.plot)

        for level in indicator.levels:
            style = Qt.PenStyle.DashLine if level.dash else Qt.PenStyle.SolidLine
            line = pg.InfiniteLine(
                pos=level.value, angle=0, movable=False,
                pen=pg.mkPen(level.color, width=1, style=style),
            )
            self.plot.addItem(line, ignoreBounds=True)

        if indicator.y_range is not None:
            low, high = indicator.y_range
            self.plot.setYRange(low, high, padding=0.02)
        else:
            view = self.plot.getPlotItem().getViewBox()
            view.enableAutoRange(y=True)
            view.setAutoVisible(y=True)

    def apply_display_settings(self, settings) -> None:
        self.plot.setBackground(settings.background)
        alpha = 0.3 if settings.grid_visible else 0.0
        self.plot.showGrid(x=settings.grid_visible, y=settings.grid_visible, alpha=alpha)
        axis_color = settings.grid_color if settings.grid_visible else "#787b86"
        for name in ("left", "bottom"):
            axis = self.plot.getAxis(name)
            axis.setPen(pg.mkPen(axis_color))
            axis.setTextPen(pg.mkPen("#9598a1"))

    @property
    def plot_item(self) -> pg.PlotItem:
        return self.plot.getPlotItem()
