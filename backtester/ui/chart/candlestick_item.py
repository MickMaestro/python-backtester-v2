"""Candlestick graphics item with viewport-windowed rendering.

X coordinates are **bar indices** (0..n-1), not timestamps — this removes
weekend/session gaps and is what the replay clock will drive in Phase 4.

Performance model: only the visible index window (plus one screen of padding
each side) is painted into a cached QPicture, which is rebuilt when the view
leaves the padded window or the zoom changes materially. When more bars are
visible than ``max_candles`` the item draws a decimated close-price polyline
instead, so zooming all the way out over 100k+ bars stays fluid.
"""

from __future__ import annotations

import math

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen, QPicture

UP_COLOR = QColor("#26a69a")
DOWN_COLOR = QColor("#ef5350")
LINE_COLOR = QColor("#5c7cfa")


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, max_candles: int = 4000, body_width: float = 0.7):
        super().__init__()
        self._max_candles = max_candles
        self._body_width = body_width
        self._o = self._h = self._l = self._c = np.empty(0)
        self._picture: QPicture | None = None
        self._built: tuple[int, int] | None = None  # index window in the cache
        self._visible: int | None = None  # replay reveal limit; None = all
        self._up_color = QColor(UP_COLOR)
        self._down_color = QColor(DOWN_COLOR)

    def set_colors(self, up, down) -> None:
        self._up_color = QColor(up)
        self._down_color = QColor(down)
        self._picture = None
        self._built = None
        self.update()

    # ------------------------------------------------------------- data

    def set_data(
        self, o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray
    ) -> None:
        self._o, self._h, self._l, self._c = (
            np.asarray(o, float), np.asarray(h, float),
            np.asarray(l, float), np.asarray(c, float),
        )
        self._picture = None
        self._built = None
        self._visible = None
        self.prepareGeometryChange()
        self.update()

    def __len__(self) -> int:
        return len(self._c)

    def set_visible_length(self, k: int | None) -> None:
        """Limit drawing to the first ``k`` bars (replay reveal); None = all."""
        self._visible = None if k is None else max(0, min(int(k), len(self._c)))
        self._picture = None
        self._built = None
        self.prepareGeometryChange()
        self.update()

    @property
    def visible_length(self) -> int:
        return len(self._c) if self._visible is None else self._visible

    # -------------------------------------------------- pyqtgraph plumbing

    def boundingRect(self) -> QRectF:
        n = self.visible_length
        if n == 0:
            return QRectF()
        lo, hi = float(self._l[:n].min()), float(self._h[:n].max())
        return QRectF(-1.0, lo, n + 1.0, max(hi - lo, 1e-12))

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        """Lets the ViewBox auto-fit Y to the *visible* X window."""
        n = self.visible_length
        if n == 0:
            return (None, None)
        if ax == 0:
            return (0.0, float(n - 1))
        if orthoRange is not None:
            i0 = max(0, int(math.floor(orthoRange[0])))
            i1 = min(n, int(math.ceil(orthoRange[1])) + 1)
            if i0 >= i1:
                return (None, None)
        else:
            i0, i1 = 0, n
        return (float(self._l[i0:i1].min()), float(self._h[i0:i1].max()))

    def pixelPadding(self) -> float:
        return 2.0

    def paint(self, painter: QPainter, option, widget=None) -> None:
        n = self.visible_length
        if n == 0:
            return
        vb = self.getViewBox()
        if vb is not None:
            (x0, x1), _ = vb.viewRange()
        else:
            x0, x1 = 0.0, float(n)
        i0 = max(0, int(math.floor(x0)) - 1)
        i1 = min(n, int(math.ceil(x1)) + 2)
        if i0 >= i1:
            return

        if not self._cache_covers(i0, i1):
            span = i1 - i0
            b0 = max(0, i0 - span)          # one screenful of padding per side
            b1 = min(n, i1 + span)
            self._picture = self._build_picture(b0, b1, span)
            self._built = (b0, b1)
        self._picture.play(painter)

    # ----------------------------------------------------------- internals

    def _cache_covers(self, i0: int, i1: int) -> bool:
        if self._picture is None or self._built is None:
            return False
        b0, b1 = self._built
        if i0 < b0 or i1 > b1:
            return False
        # Rebuild when zoomed out far beyond what the cache was built for,
        # so we don't keep playing a picture 3x wider than needed.
        return (b1 - b0) <= 3 * max(i1 - i0, 1)

    def _build_picture(self, i0: int, i1: int, visible_span: int) -> QPicture:
        picture = QPicture()
        painter = QPainter(picture)
        try:
            if visible_span > self._max_candles:
                self._draw_polyline(painter, i0, i1)
            else:
                self._draw_candles(painter, i0, i1)
        finally:
            painter.end()
        return picture

    def _draw_candles(self, painter: QPainter, i0: int, i1: int) -> None:
        half = self._body_width / 2
        up_pen = QPen(self._up_color)
        up_pen.setCosmetic(True)
        down_pen = QPen(self._down_color)
        down_pen.setCosmetic(True)
        up_brush, down_brush = QBrush(self._up_color), QBrush(self._down_color)

        o, h, l, c = self._o, self._h, self._l, self._c
        for i in range(i0, i1):
            rising = c[i] >= o[i]
            painter.setPen(up_pen if rising else down_pen)
            if h[i] > l[i]:
                painter.drawLine(QPointF(i, l[i]), QPointF(i, h[i]))
            top, bottom = (c[i], o[i]) if rising else (o[i], c[i])
            if top == bottom:  # doji: flat body
                painter.drawLine(QPointF(i - half, top), QPointF(i + half, top))
            else:
                painter.setBrush(up_brush if rising else down_brush)
                painter.drawRect(QRectF(i - half, bottom, self._body_width, top - bottom))

    def _draw_polyline(self, painter: QPainter, i0: int, i1: int) -> None:
        stride = max(1, (i1 - i0) // 20_000)
        xs = np.arange(i0, i1, stride)
        ys = self._c[i0:i1:stride]
        path = QPainterPath()
        path.moveTo(float(xs[0]), float(ys[0]))
        for x, y in zip(xs[1:], ys[1:]):
            path.lineTo(float(x), float(y))
        pen = QPen(LINE_COLOR)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
