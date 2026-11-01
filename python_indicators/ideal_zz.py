"""IdealZZ and IdealZZP — converted from ``idealzz.mq5`` / ``idealzzp.mq5``
(TheXpert; Convenient use of indicators).

A zigzag that walks each bar's high and low in the order they most likely
traded (high first on a down candle, low first on an up candle) and reverses
once price comes back ``channel_points`` points (IdealZZ) or
``channel_percent`` percent (IdealZZP) from the running extreme.

The source leaves out the still-forming bar; on history every bar is closed,
so all are included.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5

UP, DOWN = 1, -1


def ideal_zigzag(o, h, l, c, reversed_down, reversed_up):
    """The shared state machine. ``reversed_down(price, high)`` says whether
    ``price`` is far enough below the running high to turn; ``reversed_up``
    likewise for lows. Returns (highs, lows) pivot buffers."""
    n = len(c)
    maxs = np.full(n, np.nan)
    mins = np.full(n, np.nan)
    max_at = np.zeros(n, dtype=int)
    min_at = np.zeros(n, dtype=int)
    direction = np.zeros(n, dtype=int)
    inited = False

    for j in range(n):
        if j > 0:
            max_at[j], min_at[j], direction[j] = max_at[j - 1], min_at[j - 1], direction[j - 1]
        for p in ((h[j], l[j]) if c[j] < o[j] else (l[j], h[j])):
            if not inited:
                max_at[j] = min_at[j] = j
                maxs[j] = mins[j] = p
                direction[j] = UP
                inited = True
            elif direction[j] == UP:
                last = max_at[j]
                if np.isnan(maxs[last]):
                    maxs[last] = h[last]
                if p > maxs[last]:
                    maxs[last] = np.nan
                    maxs[j] = p
                    max_at[j] = last = j
                if reversed_down(p, maxs[last]):
                    direction[j] = DOWN
                    mins[j] = p
                    min_at[j] = j
            elif direction[j] == DOWN:
                last = min_at[j]
                if np.isnan(mins[last]):
                    mins[last] = l[last]
                if p < mins[last]:
                    mins[last] = np.nan
                    mins[j] = p
                    min_at[j] = last = j
                if reversed_up(p, mins[last]):
                    direction[j] = UP
                    maxs[j] = p
                    max_at[j] = j
    return maxs, mins


class _IdealZZMixin:
    """Shared calculate(); not an Indicator itself, so the loader skips it."""

    repaint_window = 3000

    def calculate(self, df):
        down, up = self._tests(df)
        highs, lows = ideal_zigzag(
            self.series(df, "open"), self.series(df, "high"),
            self.series(df, "low"), self.series(df, "close"), down, up,
        )
        return {"highs": highs, "lows": lows}


class IdealZZ(_IdealZZMixin, Indicator):
    name = "IdealZZ"
    pane = Pane.PRICE
    params = {"channel_points": 100}
    plots = [Plot("highs", "IdealZZ", style=DrawStyle.ZIGZAG, color="#808080",
                  width=1, fill_with="lows")]

    def _tests(self, df):
        gap = int(self.p.channel_points) * mql5.point(df)
        return (lambda p, top: p + gap < top), (lambda p, bottom: p - gap > bottom)


class IdealZZP(_IdealZZMixin, Indicator):
    name = "IdealZZP"
    pane = Pane.PRICE
    params = {"channel_percent": 0.1}
    plots = [Plot("highs", "IdealZZP", style=DrawStyle.ZIGZAG, color="#808080",
                  width=1, fill_with="lows")]

    def _tests(self, df):
        k = 1.0 + float(self.p.channel_percent) / 100.0
        return (lambda p, top: top / p > k), (lambda p, bottom: p / bottom > k)
