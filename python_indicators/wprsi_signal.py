"""WPRSI signal — converted from ``wprsisignal.mq5`` (Trading signals module
based on WPRSIsignal).

A buy arrow when Williams %R crosses up through −20 with RSI above 50, provided
%R had not been above −20 in the ``filter_up`` bars before the cross; a sell
arrow for the cross down through −80 with RSI below 50. Both use one period.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class WprsiSignal(Indicator):
    name = "WPRSI Signal"
    pane = Pane.PRICE
    params = {"period": 27, "filter_up": 10, "filter_down": 10}
    plots = [
        Plot("sell", "WPRSI signal Sell", style=DrawStyle.ARROW, color="#ff00ff",
             symbol="arrow_down", size=12),
        Plot("buy", "WPRSI signal Buy", style=DrawStyle.ARROW, color="#00ff00",
             symbol="arrow_up", size=12),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        f_up = max(int(self.p.filter_up), 0)
        f_dn = max(int(self.p.filter_down), 0)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        wpr = mql5.wpr(h, l, c, period)
        rsi = mql5.rsi(c, period)
        sell = self.empty(n)
        buy = self.empty(n)
        start = period + 2 + max(f_up, f_dn)
        half = (h - l) / 2.0
        for i in range(start, n):
            if wpr[i] > -20 and wpr[i - 1] < -20 and rsi[i] > 50:
                if not np.any(wpr[i - f_up - 2: i - 1] > -20):
                    buy[i] = l[i] - half[i]
            if wpr[i - 1] > -80 and wpr[i] < -80 and rsi[i] < 50:
                if not np.any(wpr[i - f_dn - 2: i - 1] < -80):
                    sell[i] = h[i] + half[i]
        return {"sell": sell, "buy": buy}
