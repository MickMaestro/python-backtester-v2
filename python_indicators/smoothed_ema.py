"""EMA (SmoothAlgorithms) — converted from ``EMA.mq5`` (SmoothAlgorithms; the
identical ``emak10.mq5`` in Smooth Algorithms - Corrected_Modified).

The library's ``CMoving_Average::EMASeries``: an EMA seeded with the first
bar's price that accepts a fractional period (12.75 by default), on the
library's extended applied-price set.
"""

import numpy as np

from backtester.indicators import smoothing as sm
from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5


class SmoothedEma(Indicator):
    name = "EMA (SmoothAlgorithms)"
    pane = Pane.PRICE
    params = {"length": 12.75, "price": sm.price_choice(), "shift": 0, "price_shift": 0}
    plots = [Plot("ema", "EMA", color="#7b68ee", width=1)]

    def calculate(self, df):
        line = sm.ema(sm.price_series(df, self.p.price), float(self.p.length))
        line = line + int(self.p.price_shift) * mql5.point(df)
        line[:2] = np.nan                          # PLOT_DRAW_BEGIN
        return {"ema": mql5.shift_forward(line, int(self.p.shift))}
