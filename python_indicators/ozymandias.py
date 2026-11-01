"""Ozymandias Lite — converted from ``ozymandias_lite.mq5`` (Ozymandias Signal
Module).

A HalfTrend-style stop line: while up, it trails the highest of the recent
lows; it flips down once the high-average drops below that level and price
closes under the previous low, then trails the lowest recent high. Blue in an
uptrend, pink in a downtrend.
"""

import numpy as np

from backtester.indicators.base import Choice, Indicator, Pane, Plot
from backtester.indicators import mql5


class OzymandiasLite(Indicator):
    name = "Ozymandias Lite"
    pane = Pane.PRICE
    params = {"length": 2, "ma_method": Choice(list(mql5.MA_METHODS), default="sma"),
              "shift": 0}
    plots = [
        Plot("up", "Ozymandias (up)", color="#1e90ff", width=2),
        Plot("down", "Ozymandias (down)", color="#ff1493", width=2),
    ]

    def calculate(self, df):
        length = max(int(self.p.length), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        hma = mql5.ma(h, length, self.p.ma_method)
        lma = mql5.ma(l, length, self.p.ma_method)
        hh = mql5.highest(h, length)
        ll = mql5.lowest(l, length)
        n = len(c)

        # The source keeps 0 as "empty" in its line buffer.
        line = np.zeros(n)
        slot = np.full(n, -1)
        trend = next_trend = 0
        max_low, min_high = 0.0, 9999999.0
        for i in range(max(length, 1), n):
            trend_now = trend
            if next_trend == 1:
                max_low = max(ll[i], max_low)
                if hma[i] < max_low and c[i] < l[i - 1]:
                    trend_now, next_trend, min_high = 1, 0, hh[i]
            if next_trend == 0:
                min_high = min(hh[i], min_high)
                if lma[i] > min_high and c[i] > h[i - 1]:
                    trend_now, next_trend, max_low = 0, 1, ll[i]
            if trend_now == 0:
                line[i] = line[i - 1] if trend != 0 else max(max_low, line[i - 1])
                slot[i] = 1
            else:
                line[i] = line[i - 1] if trend != 1 else min(min_high, line[i - 1])
                slot[i] = 0
            trend = trend_now

        line = np.where(line != 0, line, np.nan)
        shift = int(self.p.shift)
        return {
            "up": mql5.shift_forward(mql5.segments(line, slot == 1), shift),
            "down": mql5.shift_forward(mql5.segments(line, slot == 0), shift),
        }
