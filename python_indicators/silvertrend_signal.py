"""SilverTrend Signal — converted from ``silvertrend_signal.mq5`` (Trading
signals module based on SilverTrend_Signal).

Over the last ``ssp`` bars, a band is cut ``33−risk`` percent in from each end
of the high–low range. Closing above the upper cut sets the trend up, below
the lower cut sets it down; a dot marks each change, offset by half the
average bar range. (The source's alert pop-ups are left out.)
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class SilverTrendSignal(Indicator):
    name = "SilverTrend Signal"
    pane = Pane.PRICE
    params = {"ssp": 9, "risk": 3}
    plots = [
        Plot("sell", "Silver Sell", style=DrawStyle.ARROW, color="#ff0000", size=8),
        Plot("buy", "Silver Buy", style=DrawStyle.ARROW, color="#00ff00", size=8),
    ]

    def calculate(self, df):
        ssp = max(int(self.p.ssp), 1)
        k = 33 - int(self.p.risk)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        avg_range = (
            np.convolve(np.abs(h - l), np.ones(ssp + 1), mode="full")[:n] / (ssp + 1)
        )
        # The source seeds the max with the bar's low and the min with its
        # close before scanning the window, so both are clamped by them.
        ss_max = np.maximum(mql5.highest(h, ssp), l)
        ss_min = np.minimum(mql5.lowest(l, ssp), c)
        smin = ss_min + (ss_max - ss_min) * k / 100.0
        smax = ss_max - (ss_max - ss_min) * k / 100.0

        sell = self.empty(n)
        buy = self.empty(n)
        uptrend = old = False
        for i in range(ssp, n):
            if c[i] < smin[i]:
                uptrend = False
            if c[i] > smax[i]:
                uptrend = True
            if uptrend != old:
                if uptrend:
                    buy[i] = l[i] - avg_range[i] * 0.5
                else:
                    sell[i] = h[i] + avg_range[i] * 0.5
            old = uptrend
        return {"sell": sell, "buy": buy}
