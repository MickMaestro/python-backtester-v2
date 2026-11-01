"""Draggable entry / take-profit / stop-loss lines for manual trading.

Three horizontal lines the user positions to define (and then manage) a trade.
Each can be shown or hidden independently — a trade needs neither a TP nor an
SL. ``moved`` fires while a line is dragged so the panel can refresh its
preview and, when a position is open, push the new level to the broker.
Until then, moving the entry line carries TP and SL with it.
"""

from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtCore import QObject, Qt, Signal

ENTRY_COLOR = "#c0c0c0"  # silver
TP_COLOR = "#26a69a"
SL_COLOR = "#ef5350"

ENTRY = "entry"
TP = "tp"
SL = "sl"

_SPECS = (
    (ENTRY, ENTRY_COLOR, "Entry"),
    (TP, TP_COLOR, "TP"),
    (SL, SL_COLOR, "SL"),
)


class OrderLines(QObject):
    moved = Signal(str)           # live during a drag — refresh previews
    move_finished = Signal(str)   # on release — safe point to hit the broker

    def __init__(self, plot_item: pg.PlotItem, parent: QObject | None = None):
        super().__init__(parent)
        self._plot = plot_item
        self._lines: dict[str, pg.InfiniteLine] = {}
        # While setting up a trade, TP/SL ride along with the entry line at a
        # fixed distance so they can't be stranded far off-screen. The owner
        # turns this off once the levels belong to a live position or order.
        self.brackets_follow_entry = True
        self._entry_pos = 0.0
        for key, color, text in _SPECS:
            line = pg.InfiniteLine(
                angle=0,
                movable=True,
                pen=pg.mkPen(color, width=1, style=Qt.PenStyle.DashLine),
                hoverPen=pg.mkPen(color, width=2),
                label=text,
                labelOpts={"position": 0.06, "color": color},
            )
            line.setVisible(False)
            if key == ENTRY:
                line.sigPositionChanged.connect(self._on_entry_dragged)
            else:
                line.sigPositionChanged.connect(
                    lambda _line, k=key: self.moved.emit(k)
                )
            line.sigPositionChangeFinished.connect(
                lambda _line, k=key: self.move_finished.emit(k)
            )
            plot_item.addItem(line, ignoreBounds=True)
            self._lines[key] = line

    # ----------------------------------------------------------- visibility

    def set_visible(self, key: str, visible: bool) -> None:
        self._lines[key].setVisible(visible)

    def is_visible(self, key: str) -> bool:
        return self._lines[key].isVisible()

    def hide_all(self) -> None:
        for line in self._lines.values():
            line.setVisible(False)

    # ---------------------------------------------------------------- price

    def price(self, key: str) -> float:
        return float(self._lines[key].value())

    def visible_price(self, key: str) -> float | None:
        """Price if the line is in use, else None (i.e. 'no TP' / 'no SL')."""
        return self.price(key) if self.is_visible(key) else None

    def set_price(self, key: str, price: float | None) -> None:
        """Move a line without emitting ``moved`` (programmatic sync)."""
        if price is None:
            return
        line = self._lines[key]
        line.blockSignals(True)
        line.setPos(float(price))
        line.blockSignals(False)
        if key == ENTRY:
            self._entry_pos = float(price)

    def move_entry(self, price: float) -> None:
        """Move the entry line programmatically, carrying TP/SL if following."""
        self._shift_brackets(float(price) - self._entry_pos)
        self.set_price(ENTRY, price)

    def _on_entry_dragged(self, _line) -> None:
        new = self.price(ENTRY)
        self._shift_brackets(new - self._entry_pos)
        self._entry_pos = new
        self.moved.emit(ENTRY)

    def _shift_brackets(self, delta: float) -> None:
        if not self.brackets_follow_entry or delta == 0.0:
            return
        for key in (TP, SL):
            self.set_price(key, self.price(key) + delta)

    def seed_around(self, price: float, offset: float) -> None:
        """Place the lines sensibly around a price the first time they're shown."""
        self.set_price(ENTRY, price)
        self.set_price(TP, price + offset)
        self.set_price(SL, price - offset)
