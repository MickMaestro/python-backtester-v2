"""LeManSignal — converted from ``lemansignal.mq5`` (Trading signals module
based on LeManSignal).

Compares the highest high (lowest low) of the last ``period`` bars with the
``period`` before that, one bar apart: a buy dot when the newer window's high
just broke above the older one's after not doing so a bar earlier, a sell dot
for the mirror on lows. The dot sits one point beyond the previous bar's
high (low).
"""

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class LeManSignal(Indicator):
    name = "LeManSignal"
    pane = Pane.PRICE
    params = {"period": 12}
    plots = [
        Plot("sell", "LeManSell", style=DrawStyle.ARROW, color="#ff00ff", size=8),
        Plot("buy", "LeManBuy", style=DrawStyle.ARROW, color="#00ff00", size=8),
    ]

    def calculate(self, df):
        p = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(h)
        hmax = mql5.highest(h, p)              # window ending at each bar
        lmin = mql5.lowest(l, p)
        h1 = mql5.shift_forward(hmax, 1)       # bars i-p   .. i-1
        h2 = mql5.shift_forward(hmax, p + 1)   # bars i-2p  .. i-p-1
        h3 = mql5.shift_forward(hmax, 2)       # bars i-p-1 .. i-2
        h4 = mql5.shift_forward(hmax, p + 2)   # bars i-2p-1.. i-p-2
        l1 = mql5.shift_forward(lmin, 1)
        l2 = mql5.shift_forward(lmin, p + 1)
        l3 = mql5.shift_forward(lmin, 2)
        l4 = mql5.shift_forward(lmin, p + 2)
        prev_high = mql5.previous(h)
        prev_low = mql5.previous(l)

        sell = self.empty(n)
        buy = self.empty(n)
        start = 2 * p + 3
        if start < n:
            idx = slice(start, n)
            buy_on = (h3[idx] <= h4[idx]) & (h1[idx] > h2[idx])
            sell_on = (l3[idx] >= l4[idx]) & (l1[idx] < l2[idx])
            point = mql5.point(df)
            buy[idx][buy_on] = prev_high[idx][buy_on] + point
            sell[idx][sell_on] = prev_low[idx][sell_on] - point
        return {"sell": sell, "buy": buy}
