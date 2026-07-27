"""Period separators: vertical lines at calendar boundaries, MT5-style.

For intraday data the boundaries are day changes, labelled with the weekday
(Friday, Tuesday, …); for daily+ data they are months, then years, labelled
accordingly. Only the separators inside the current view are drawn, and labels
are painted at a fixed pixel size at the bottom of the chart.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPen

LABEL_COLOR = "#9598a1"
_DAY = 86_400


def compute_separators(df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    """Bar indices that start a new period, and each one's label.

    The period is chosen from the bar spacing: intraday → day boundaries
    (weekday name), up to ~monthly → months (Mon YYYY), coarser → years.
    """
    if len(df) < 2:
        return np.empty(0, dtype=int), []
    times = pd.to_datetime(df["time"])
    median_s = float(np.median(np.diff(times.to_numpy()).astype("timedelta64[s]").astype(float)))

    if median_s < _DAY:
        key = times.dt.floor("D")
        label_of = lambda t: t.strftime("%A")              # noqa: E731  Friday
    elif median_s < 20 * _DAY:
        key = times.dt.to_period("M").dt.start_time
        label_of = lambda t: t.strftime("%b %Y")           # noqa: E731  Jan 2024
    else:
        key = times.dt.to_period("Y").dt.start_time
        label_of = lambda t: t.strftime("%Y")              # noqa: E731  2024

    change = key.ne(key.shift(1)).to_numpy().copy()
    change[0] = False  # the first bar doesn't start a separator
    idx = np.nonzero(change)[0]
    labels = [label_of(times.iloc[int(i)]) for i in idx]
    return idx.astype(int), labels


class SeparatorLines(pg.GraphicsObject):
    def __init__(self):
        super().__init__()
        self._x = np.empty(0)
        self._labels: list[str] = []
        self._color = QColor("#3a4a5a")
        self._label_color = QColor(LABEL_COLOR)
        self._visible = True
        self._limit: int | None = None  # revealed-bar clip during replay
        self._font = QFont()
        self._font.setPointSize(8)

    # ------------------------------------------------------------- data

    def set_separators(self, x: np.ndarray, labels: list[str]) -> None:
        self._x = np.asarray(x, dtype=float)
        self._labels = list(labels)
        self._limit = None
        self.prepareGeometryChange()
        self.update()

    def set_style(self, visible: bool, color) -> None:
        self._visible = visible
        self._color = QColor(color)
        self.update()

    def set_visible_length(self, k: int | None) -> None:
        self._limit = k
        self.update()

    # -------------------------------------------------- pyqtgraph plumbing

    def boundingRect(self) -> QRectF:
        if len(self._x) == 0:
            return QRectF()
        lo, hi = float(self._x.min()), float(self._x.max())
        return QRectF(lo - 1.0, -1e7, (hi - lo) + 2.0, 2e7)

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        return (None, None)  # never influence auto-range

    def paint(self, painter, option, widget=None) -> None:
        if not self._visible or len(self._x) == 0:
            return
        vb = self.getViewBox()
        if vb is None:
            return
        (x0, x1), (y0, y1) = vb.viewRange()
        limit = len(self._x) if self._limit is None else self._limit

        lo = int(np.searchsorted(self._x, x0 - 1, "left"))
        hi = int(np.searchsorted(self._x, x1 + 1, "right"))

        pen = QPen(self._color)
        pen.setCosmetic(True)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)

        shown = []
        for i in range(lo, hi):
            x = self._x[i]
            if x >= limit:  # not yet revealed during replay
                continue
            painter.drawLine(QPointF(float(x), y0), QPointF(float(x), y1))
            shown.append(i)

        if not shown:
            return
        # Labels at a fixed pixel size along the bottom (reset the world
        # transform so text isn't scaled by the data-space zoom).
        transform = painter.transform()
        painter.save()
        painter.resetTransform()
        painter.setPen(QPen(self._label_color))
        painter.setFont(self._font)
        for i in shown:
            device = transform.map(QPointF(float(self._x[i]), y0))
            painter.drawText(device + QPointF(3.0, -3.0), self._labels[i])
        painter.restore()
