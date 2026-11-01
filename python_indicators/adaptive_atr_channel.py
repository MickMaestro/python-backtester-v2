"""Adaptive ATR Channel — converted from ``adaptiveatrchannelmt5indicator.mq5``
(mladen; Smooth Algorithms - Corrected_Modified library).

An EMA whose period adapts between period/2 and period with Kaufman's
efficiency ratio, wrapped in bands ± ``multiplier`` × an equally adaptive ATR.
The centre line is green while rising, orange while falling.
"""

import math

import numpy as np
import pandas as pd

from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


def efficiency_ratio(values: np.ndarray, period: int) -> np.ndarray:
    """mladen's ``iEr``: 0 until more than ``period`` bars exist."""
    n = len(values)
    diff = np.r_[0.0, np.abs(np.diff(values))]
    noise = pd.Series(diff).rolling(period, min_periods=1).sum().to_numpy()
    move = np.abs(values - mql5.shift_forward(values, period))
    with np.errstate(divide="ignore", invalid="ignore"):
        er = np.where((noise != 0) & (np.arange(n) > period), move / noise, 0.0)
    return np.nan_to_num(er)


class AdaptiveAtrChannel(Indicator):
    name = "Adaptive ATR Channel"
    pane = Pane.PRICE
    params = {"period": 20, "price": price_choice(), "multiplier": 1.0}
    plots = [
        Plot("flat", "Adaptive EMA", color="#c0c0c0", width=2),
        Plot("up", "Adaptive EMA rising", color="#3cb371", width=2),
        Plot("down", "Adaptive EMA falling", color="#ff8c00", width=2),
        Plot("upper", "Upper band", color="#808080", width=1),
        Plot("lower", "Lower band", color="#808080", width=1),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        mult = float(self.p.multiplier)
        min_p = max(period / 2.0, 1.0)
        max_p = min_p * 2.0
        price = mql5.applied_price(df, self.p.price)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(price)
        prev_close = np.r_[c[0], c[:-1]]
        tr = np.maximum(h, prev_close) - np.minimum(l, prev_close)
        tr[0] = h[0] - l[0]
        csum = np.r_[0.0, np.cumsum(tr)]
        er = efficiency_ratio(price, period)

        val = np.empty(n)
        atr = np.empty(n)
        slot = np.zeros(n)
        for i in range(n):
            avg_period = er[i] * (max_p - min_p) + min_p
            alpha = 2.0 / (1.0 + avg_period)
            terms = min(math.ceil(avg_period), i + 1)
            window_atr = (csum[i + 1] - csum[i + 1 - terms]) / terms
            if i == 0:
                atr[i], val[i] = window_atr, price[i]
                continue
            atr[i] = atr[i - 1] + alpha * (window_atr - atr[i - 1])
            val[i] = val[i - 1] + alpha * (price[i] - val[i - 1])
            slot[i] = 1 if val[i] > val[i - 1] else 2 if val[i] < val[i - 1] else slot[i - 1]

        return {
            "flat": mql5.segments(val, slot == 0),
            "up": mql5.segments(val, slot == 1),
            "down": mql5.segments(val, slot == 2),
            "upper": val + mult * atr,
            "lower": val - mult * atr,
        }
