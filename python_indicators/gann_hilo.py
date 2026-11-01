"""Gann HiLo — converted from ``hilo.mq5`` (MQL5 Wizard - GANN HiLo Signal).

Moving averages of the highs and of the lows (SMMA by default). Closing above
the previous high-average turns the trend up and the line follows the
low-average (blue); closing below the previous low-average turns it down and
the line follows the high-average (orange-red).
"""

import numpy as np

from backtester.indicators.base import Choice, Indicator, Pane, Plot
from backtester.indicators import mql5


class GannHiLo(Indicator):
    name = "Gann HiLo"
    pane = Pane.PRICE
    params = {"period": 13, "method": Choice(list(mql5.MA_METHODS), default="smma")}
    plots = [
        Plot("up", "Gann HiLo (up)", color="#1e90ff", width=2),
        Plot("down", "Gann HiLo (down)", color="#ff4500", width=2),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 2)
        c = self.series(df, "close")
        ma_high = mql5.ma(self.series(df, "high"), period, self.p.method)
        ma_low = mql5.ma(self.series(df, "low"), period, self.p.method)
        digits = mql5.digits(df)
        close_r = np.round(c, digits)
        high_r = np.round(ma_high, digits)
        low_r = np.round(ma_low, digits)
        n = len(c)
        line = self.empty(n)
        trend = np.zeros(n)
        for i in range(period, n):
            trend[i] = trend[i - 1]
            if close_r[i] > high_r[i - 1]:
                trend[i] = 1
            if close_r[i] < low_r[i - 1]:
                trend[i] = -1
            if trend[i] < 0:
                line[i] = ma_high[i]
            elif trend[i] > 0:
                line[i] = ma_low[i]
        return {
            "up": mql5.segments(line, trend > 0),
            "down": mql5.segments(line, trend < 0),
        }
