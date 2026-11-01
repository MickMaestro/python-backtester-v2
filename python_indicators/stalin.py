"""Stalin — converted from ``stalin.mq5`` (Trading signals module based on
Stalin).

Arrows on fast/slow moving-average crosses, filtered by RSI on the same side of
50. With ``confirm`` set, a cross only arms the signal: the arrow comes once
price runs ``confirm`` beyond the crossing bar. ``flat`` suppresses an arrow
that lands within that distance of the previous one on the same side.

``confirm`` and ``flat`` are in pips: points, or 10 points on 3/5-digit
symbols, as the source scales them; 0 disables each. One deliberate fix: on
3/5-digit symbols the source sets the confirm distance to 10 points whatever
``Confirm`` says, which switches confirmation on even at 0. Here ``confirm``
is honoured.
"""

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class Stalin(Indicator):
    name = "Stalin"
    pane = Pane.PRICE
    params = {
        "ma_method": Choice(list(mql5.MA_METHODS), default="ema"),
        "ma_shift": 0, "fast": 14, "slow": 21, "rsi": 17,
        "confirm": 0, "flat": 0,
    }
    plots = [
        Plot("sell", "Stalin Sell", style=DrawStyle.ARROW, color="#ffb6c1",
             symbol="arrow_down", size=12),
        Plot("buy", "Stalin Buy", style=DrawStyle.ARROW, color="#87cefa",
             symbol="arrow_up", size=12),
    ]

    def calculate(self, df):
        c = self.series(df, "close")
        o = self.series(df, "open")
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(c)
        shift = int(self.p.ma_shift)
        slow = mql5.shift_forward(mql5.ma(c, int(self.p.slow), self.p.ma_method), shift)
        fast = mql5.shift_forward(mql5.ma(c, int(self.p.fast), self.p.ma_method), shift)
        rsi_period = int(self.p.rsi)
        rsi = mql5.rsi(c, rsi_period) if rsi_period > 0 else None
        pip = mql5.point(df) * (10 if mql5.digits(df) in (3, 5) else 1)
        confirm = float(self.p.confirm) * pip
        flat = float(self.p.flat) * pip

        sell = self.empty(n)
        buy = self.empty(n)
        last_buy = last_sell = 0.0
        armed_up = armed_dn = 0.0

        def place_buy(i):
            nonlocal last_buy
            if l[i] >= last_buy + flat or l[i] <= last_buy - flat:
                buy[i] = last_buy = l[i]

        def place_sell(i):
            nonlocal last_sell
            if h[i] >= last_sell + flat or h[i] <= last_sell - flat:
                sell[i] = last_sell = h[i]

        start = max(rsi_period, int(self.p.slow), int(self.p.fast))
        for i in range(max(start - 1, 1), n):
            rsi_up = rsi is None or rsi[i] > 50
            rsi_dn = rsi is None or rsi[i] < 50
            if fast[i - 1] < slow[i - 1] and fast[i] > slow[i] and rsi_up:
                if not confirm:
                    place_buy(i)
                else:
                    armed_up, armed_dn = l[i], 0.0
            if fast[i - 1] > slow[i - 1] and fast[i] < slow[i] and rsi_dn:
                if not confirm:
                    place_sell(i)
                else:
                    armed_dn, armed_up = h[i], 0.0
            if armed_up and h[i] - armed_up >= confirm and c[i] <= h[i]:
                place_buy(i)
                armed_up = 0.0
            if armed_dn and armed_dn - l[i] >= confirm and o[i] >= c[i]:
                place_sell(i)
                armed_dn = 0.0
        return {"sell": sell, "buy": buy}
