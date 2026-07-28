"""Text drawn on a chart at a fixed pixel size: corner readouts and line labels.

Both items paint with the world transform reset, the way ``SeparatorLines``
labels its day boundaries, so text stays legible at any zoom instead of being
scaled by the data-space transform.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QFont, QFontMetrics

#: Large enough that Qt never culls an item whose paint covers the viewport.
_EVERYWHERE = QRectF(-1e7, -1e7, 2e7, 2e7)

CORNERS = {
    "top-left": "Top left",
    "top-right": "Top right",
    "bottom-left": "Bottom left",
    "bottom-right": "Bottom right",
}


class CornerTextItem(pg.GraphicsObject):
    """A single line of text pinned to a corner of the view."""

    def __init__(self, corner: str = "bottom-left", offset: tuple[int, int] = (12, 12),
                 font_size: int = 12):
        super().__init__()
        self._text = ""
        self._color = QColor("#9598a1")
        self._corner = corner if corner in CORNERS else "bottom-left"
        self._offset = offset
        self._font = QFont("Consolas")
        self._font.setPointSize(font_size)
        self._font.setBold(True)

    def set_text(self, text: str, color=None) -> None:
        self._text = text or ""
        if color is not None:
            self._color = QColor(color)
        self.update()

    def boundingRect(self) -> QRectF:
        return _EVERYWHERE

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        return (None, None)      # never influence auto-range

    def pixelPadding(self) -> float:
        return 0.0

    def paint(self, painter, option, widget=None) -> None:
        if not self._text:
            return
        view = self.getViewBox()
        if view is None:
            return
        (x0, x1), (y0, y1) = view.viewRange()

        transform = painter.transform()
        left = transform.map(QPointF(x0, y0)).x()
        right = transform.map(QPointF(x1, y0)).x()
        bottom = transform.map(QPointF(x0, y0)).y()
        top = transform.map(QPointF(x0, y1)).y()

        painter.save()
        painter.resetTransform()
        painter.setFont(self._font)
        painter.setPen(self._color)
        width = QFontMetrics(self._font).horizontalAdvance(self._text)
        height = QFontMetrics(self._font).height()
        dx, dy = self._offset

        if self._corner.endswith("left"):
            x = left + dx
        else:
            x = right - dx - width
        if self._corner.startswith("top"):
            y = top + dy + height
        else:
            y = bottom - dy
        painter.drawText(QPointF(x, y), self._text)
        painter.restore()


class SegmentLabelItem(pg.GraphicsObject):
    """Labels each unbroken run of a series — one per day for a stepped level.

    Only the runs inside the current view are drawn, so a year of daily levels
    costs nothing to pan across.
    """

    def __init__(self, text: str, color="#9598a1", font_size: int = 8):
        super().__init__()
        self._text = text
        self._color = QColor(color)
        self._x = np.empty(0)
        self._y = np.empty(0)
        self._font = QFont()
        self._font.setPointSize(font_size)

    def set_series(self, values: np.ndarray) -> None:
        """Anchor a label at the first bar of every finite run in ``values``."""
        values = np.asarray(values, dtype=float)
        finite = np.isfinite(values)
        if not finite.any():
            self._x, self._y = np.empty(0), np.empty(0)
        else:
            starts = finite & ~np.roll(finite, 1)
            starts[0] = finite[0]
            index = np.nonzero(starts)[0]
            self._x = index.astype(float)
            self._y = values[index]
        self.prepareGeometryChange()
        self.update()

    def boundingRect(self) -> QRectF:
        return _EVERYWHERE

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        return (None, None)

    def paint(self, painter, option, widget=None) -> None:
        if len(self._x) == 0 or not self._text:
            return
        view = self.getViewBox()
        if view is None:
            return
        (x0, x1), _y_range = view.viewRange()
        lo = int(np.searchsorted(self._x, x0, "left"))
        hi = int(np.searchsorted(self._x, x1, "right"))
        if lo >= hi:
            return

        transform = painter.transform()
        painter.save()
        painter.resetTransform()
        painter.setFont(self._font)
        painter.setPen(self._color)
        for i in range(lo, hi):
            point = transform.map(QPointF(float(self._x[i]), float(self._y[i])))
            painter.drawText(point + QPointF(4.0, -3.0), self._text)
        painter.restore()
