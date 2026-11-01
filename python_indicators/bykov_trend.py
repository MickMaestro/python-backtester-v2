"""BykovTrend — converted from ``bykovtrend.mq5`` (Trading signals module based
on BykovTrend).

Williams %R crossing out of a band sets the trend: above −(33−risk) is up,
below −100+(33−risk) is down. An arrow marks each change of trend, offset from
the bar by 3/8 of ATR(15).
"""

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class BykovTrend(Indicator):
    name = "BykovTrend"
    pane = Pane.PRICE
    params = {"risk": 3, "ssp": 9}
    plots = [
        Plot("sell", "BykovTrend Sell", style=DrawStyle.ARROW, color="#ff00ff",
             symbol="arrow_down", size=12),
        Plot("buy", "BykovTrend Buy", style=DrawStyle.ARROW, color="#00ff00",
             symbol="arrow_up", size=12),
    ]

    def calculate(self, df):
        k = 33 - int(self.p.risk)
        ssp = max(int(self.p.ssp), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        wpr = mql5.wpr(h, l, c, ssp)
        atr = mql5.atr(h, l, c, 15)
        sell = self.empty(n)
        buy = self.empty(n)
        uptrend = old = False
        for i in range(max(ssp, 15), n):
            rng = atr[i] * 3.0 / 8.0
            if wpr[i] < -100 + k:
                uptrend = False
            if wpr[i] > -k:
                uptrend = True
            if not old and uptrend:
                buy[i] = l[i] - rng
            if old and not uptrend:
                sell[i] = h[i] + rng
            old = uptrend
        return {"sell": sell, "buy": buy}
