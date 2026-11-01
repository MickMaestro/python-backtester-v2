"""Delta ZigZag — converted from ``deltazigzag.mq5`` (Trading Signals / Trailing
Stop modules based on Delta ZigZag).

A zigzag that reverses after a fixed move (``reversal_points``) or a percentage
of price. It also tracks the last ``levels`` swing highs and lows: breaking
above the highest of the swing highs turns the trend up, below the lowest
swing low turns it down. The zigzag is blue in an uptrend, red in a downtrend,
and dots mark the level whose break would reverse the trend.

The zigzag paints back to each turning point; on the replay the newest leg
is drawn to the swing as it stood at each bar. The source's special handling
of the still-forming last bar (for live ticks) is not needed on history.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class DeltaZigZag(Indicator):
    name = "Delta ZigZag"
    pane = Pane.PRICE
    params = {
        "applied_price": Choice({"high_low": "High/Low", "close": "Close"}, default="high_low"),
        "reversal_mode": Choice({"points": "Points", "percent": "Percent"}, default="points"),
        "reversal_points": 500,
        "reversal_percent": 0.5,
        "levels": 1,
    }
    plots = [
        Plot("zz_up", "ZigZag (uptrend)", color="#0000ff", width=2, known_at="known"),
        Plot("zz_down", "ZigZag (downtrend)", color="#ff0000", width=2, known_at="known"),
        Plot("reverse_down", "Reverse-down level", style=DrawStyle.ARROW,
             color="#ff6347", size=3),
        Plot("reverse_up", "Reverse-up level", style=DrawStyle.ARROW,
             color="#1e90ff", size=3),
    ]

    repaint_window = 3000

    def calculate(self, df):
        c = self.series(df, "close")
        if self.p.applied_price == "high_low":
            hi, lo = self.series(df, "high"), self.series(df, "low")
        else:
            hi = lo = c
        n = len(c)
        levels = max(int(self.p.levels), 1)
        digits = mql5.digits(df)
        fixed = int(self.p.reversal_points) * mql5.point(df)

        def reversal(price):
            if self.p.reversal_mode == "points":
                return fixed
            return round(price / 100.0 * float(self.p.reversal_percent), digits)

        empty = {key: self.empty(n) for key in
                 ("zz_up", "zz_down", "reverse_down", "reverse_up")}
        empty["known"] = np.full(n, np.inf)
        if n < 2:
            return empty

        top = np.zeros(n)
        bottom = np.zeros(n)
        slots = np.zeros(n)
        rev_down = self.empty(n)
        rev_up = self.empty(n)

        first_rev = reversal(c[0])
        start = 1
        while start < n and abs(c[start] - c[0]) - first_rev <= 0.00001:
            start += 1
        if start >= n:
            return empty
        if c[start] > c[0]:
            up = up_trend = True
            high_bar, high_val = start, c[start]
            low_bar, low_val = 0, c[0]
            top[start] = c[start]
            bottom[0] = c[0]
        else:
            up = up_trend = False
            high_bar, high_val = 0, c[0]
            low_bar, low_val = start, c[start]
            top[0] = c[0]
            bottom[start] = c[start]
        min_levels = [low_val] * levels
        max_levels = [high_val] * levels

        def push(array, value):
            array.insert(0, value)
            del array[levels:]

        for i in range(start, n):
            if up:
                rev = reversal(high_val)
                if hi[i] > high_val:
                    top[high_bar] = 0.0
                    top[i] = hi[i]
                    bottom[i] = 0.0
                    high_bar, high_val = i, hi[i]
                elif lo[i] < high_val - rev:
                    bottom[i] = lo[i]
                    low_bar, low_val = i, lo[i]
                    top[i] = 0.0
                    up = False
                    if max_levels[0] != high_val:
                        push(max_levels, high_val)
                else:
                    top[i] = bottom[i] = 0.0
            else:
                rev = reversal(low_val)
                if lo[i] < low_val:
                    bottom[low_bar] = 0.0
                    bottom[i] = lo[i]
                    top[i] = 0.0
                    low_bar, low_val = i, lo[i]
                elif hi[i] > low_val + rev:
                    top[i] = hi[i]
                    high_bar, high_val = i, hi[i]
                    bottom[i] = 0.0
                    up = True
                    if min_levels[0] != low_val:
                        push(min_levels, low_val)
                else:
                    top[i] = bottom[i] = 0.0

            if not up_trend and high_val > max(max_levels):
                up_trend = True
            elif up_trend and low_val < min(min_levels):
                up_trend = False
            if up_trend:
                rev_down[i] = min(min_levels)
                slots[i] = 1
            else:
                rev_up[i] = max(max_levels)
                slots[i] = 0

        pivots = np.where(top != 0, top, np.where(bottom != 0, bottom, np.nan))
        line, known = mql5.pivot_line(pivots)
        colour = mql5.leg_colors(pivots, slots)
        return {
            "zz_up": mql5.segments(line, colour == 1),
            "zz_down": mql5.segments(line, colour == 0),
            "reverse_down": rev_down,
            "reverse_up": rev_up,
            "known": known,
        }
