"""Karacatica — converted from ``karacatica.mq5`` (Trading signals module based
on Karacatica).

A buy arrow when close is above the close ``period`` bars ago and +DI leads
−DI; a sell arrow for the reverse. Arrows alternate: after a buy, the next
signal must be a sell, and vice versa. Arrows sit 0.75 × ATR(period) from
the bar.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class Karacatica(Indicator):
    name = "Karacatica"
    pane = Pane.PRICE
    params = {"period": 70}
    plots = [
        Plot("sell", "Karacatica Sell", style=DrawStyle.ARROW, color="#ff00ff",
             symbol="arrow_down", size=12),
        Plot("buy", "Karacatica Buy", style=DrawStyle.ARROW, color="#00ff00",
             symbol="arrow_up", size=12),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        atr = mql5.atr(h, l, c, period)
        _adx, pdi, mdi = mql5.adx(h, l, c, period)
        offset = 1.5 / 2.0
        sell = self.empty(n)
        buy = self.empty(n)
        last = 0                       # 1 = last arrow was a buy, 2 = a sell
        for i in range(period, n):
            if np.isfinite(buy[i - 1]):
                last = 1
            if np.isfinite(sell[i - 1]):
                last = 2
            if c[i] > c[i - period] and pdi[i] > mdi[i] and last != 1:
                buy[i] = l[i] - atr[i] * offset
            if c[i] < c[i - period] and pdi[i] < mdi[i] and last != 2:
                sell[i] = h[i] + atr[i] * offset
        return {"sell": sell, "buy": buy}
