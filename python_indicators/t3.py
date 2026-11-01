"""T3 — converted from ``t3.mq5`` (Module of Trade Signals based on T3).

Tillson's T3: six chained EMAs blended so the result lags less than any one of
them. ``b`` is the volume factor × 100 (0.7 is the classic value).
"""

from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators import smoothing as sm


class T3(Indicator):
    name = "T3"
    pane = Pane.PRICE
    params = {"period": 14, "b": 70.0, "price": sm.price_choice(), "shift": 0, "price_shift": 0}
    plots = [Plot("t3", "T3", color="#ff0000", width=1)]

    def calculate(self, df):
        price = sm.price_series(df, self.p.price)
        line = sm.t3(price, max(int(self.p.period), 1), float(self.p.b))
        line = line + int(self.p.price_shift) * mql5.point(df)
        return {"t3": mql5.shift_forward(line, int(self.p.shift))}
