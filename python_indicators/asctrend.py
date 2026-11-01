"""ASCtrend — converted from ``asctrend.mq5`` (Trading signals module based on
ASCtrendSignal).

Williams %R, read as 0..100, with the period picked per bar by volatility:
a bar whose open gapped twice the average range from the previous close, or
a 4.6× average-range move over three bars, switches to a shorter %R. A buy
dot appears when %R is overbought and, looking back past the neutral zone,
was last oversold; a sell dot mirrors it.

``risk`` widens the overbought/oversold bands (67+risk / 33−risk) and
lengthens the slow %R period (3 + 2·risk).
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class AscTrend(Indicator):
    name = "ASCtrend"
    pane = Pane.PRICE
    params = {"risk": 4}
    plots = [
        Plot("sell", "ASCtrend Sell", style=DrawStyle.ARROW, color="#ff00ff", size=8),
        Plot("buy", "ASCtrend Buy", style=DrawStyle.ARROW, color="#0000ff", size=8),
    ]

    def calculate(self, df):
        risk = int(self.p.risk)
        o = self.series(df, "open")
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        x1 = 67 + risk
        x2 = 33 - risk
        # The three %R handles; the source indexes them 0, 1, 2.
        wprs = [
            100.0 - np.abs(mql5.wpr(h, l, c, period))
            for period in (3, 4, max(3 + risk * 2, 1))
        ]
        sell = self.empty(n)
        buy = self.empty(n)
        start = max(int(max(3 + risk * 2, 4) + 1) - 1, 12)
        vel = 0.0
        for i in range(start, n):
            rng = float(np.sum(np.abs(h[i - 9: i + 1] - l[i - 9: i + 1]))) / 10.0
            # MRO1 (gap vs previous close) is computed by the source but then
            # overwritten — only MRO2 decides the %R period.
            mro2 = any(abs(c[i - k - 3] - c[i - k]) >= rng * 4.6 for k in range(6))
            series = wprs[1 if mro2 else 2]
            value = series[i]
            if not np.isfinite(value):
                continue
            if value < x2 or value > x1:
                j = 1
                while i - j >= 0:
                    vel = series[i - j]
                    if x2 <= vel <= x1:
                        j += 1
                    else:
                        break
            if value < x2 and vel > x1:
                sell[i] = h[i] + rng * 0.5
            if value > x1 and vel < x2:
                buy[i] = l[i] - rng * 0.5
        return {"sell": sell, "buy": buy}
