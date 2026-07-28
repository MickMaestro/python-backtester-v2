"""Bid Ratio — converted from ``Bid Ratio.mq5``.

Where the day is closing within its own range: 100% means the close is at the
day's high with an up day, 0% at the low. Above 80 is a strong close, below 20
a weak one.

The original prints a single number in the chart corner for *today*. There is
no corner to print in on a historical chart, and a single number would waste
the history, so the conversion plots the ratio bar by bar in its own pane —
each bar showing the ratio as it stood at that point of its day, computed from
the day so far, never from how the day ended.
"""

import numpy as np

from backtester.indicators.base import Indicator, Level, Pane, Plot
from backtester.indicators import mql5


class BidRatio(Indicator):
    name = "Bid Ratio"
    pane = Pane.SEPARATE
    params = {"strong": 80.0, "weak": 20.0}
    plots = [
        Plot("ratio", "D1 Bid Ratio %", color="#9598a1", width=1.5),
        Plot("strong", "Strong close", color="#1e90ff", width=2),
        Plot("weak", "Weak close", color="#ff1493", width=2),
    ]
    y_range = (0.0, 100.0)

    def setup(self):
        self.levels = [
            Level(float(self.p.strong), color="#1e90ff"),
            Level(50.0, color="#5a5f6a"),
            Level(float(self.p.weak), color="#ff1493"),
        ]

    def calculate(self, df):
        day = mql5.running_daily(df)
        day_open, day_high = day["open"], day["high"]
        day_low, day_close = day["low"], day["close"]

        day_range = day_high - day_low
        with np.errstate(divide="ignore", invalid="ignore"):
            up_day = (day_close - day_low) * 100.0 / day_range
            down_day = (day_range + day_close - day_high) * 100.0 / day_range
        ratio = np.where(day_close >= day_open, up_day, down_day)
        ratio = np.where(day_range > 0, ratio, np.nan)

        return {
            "ratio": ratio,
            "strong": mql5.segments(ratio, ratio >= float(self.p.strong)),
            "weak": mql5.segments(ratio, ratio <= float(self.p.weak)),
        }
