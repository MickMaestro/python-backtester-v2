"""Chandelier Exit — converted from ``ChandelierExit.mq5`` (mladen).

Two trailing stops at once: the highest high of the look-back minus a multiple
of ATR while the trend is up, the lowest low plus that multiple while it is
down, each ratcheting so it never gives ground. Two multipliers run in
parallel, so you see a tight and a wide stop together, with a dot where each
line starts.

The ATR here is the source's own: a plain mean of gap-aware true range over the
bars *before* the current one, not Wilder's smoothing.

One deliberate difference: the original's ``ArrayMaximum(high, start, period)``
reads a full look-back window even on the first bars, which reaches past the
current bar into data the chart has not reached yet. Here the window is clipped
to the bars up to the previous one, so the first values are computed from less
data instead of from the future.
"""

import numpy as np
import pandas as pd

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class ChandelierExit(Indicator):
    name = "Chandelier Exit"
    pane = Pane.PRICE
    params = {
        "atr_period": 22,
        "atr_multiplier_1": 3.0,
        "atr_multiplier_2": 4.5,
        "lookback_period": 22,
    }
    plots = [
        Plot("up1", "Upper 1", color="#00bfff", width=1.5, dash=True),
        Plot("down1", "Lower 1", color="#db7093", width=1.5, dash=True),
        Plot("up2", "Upper 2", color="#00bfff", width=1.5),
        Plot("down2", "Lower 2", color="#db7093", width=1.5),
        Plot("up1_dot", "Upper 1 start", style=DrawStyle.ARROW, color="#00bfff", size=7),
        Plot("down1_dot", "Lower 1 start", style=DrawStyle.ARROW, color="#db7093", size=7),
        Plot("up2_dot", "Upper 2 start", style=DrawStyle.ARROW, color="#00bfff", size=9),
        Plot("down2_dot", "Lower 2 start", style=DrawStyle.ARROW, color="#db7093", size=9),
    ]

    def calculate(self, df):
        atr_period = max(int(self.p.atr_period), 1)
        lookback = max(int(self.p.lookback_period), 1)
        mult1 = float(self.p.atr_multiplier_1)
        mult2 = float(self.p.atr_multiplier_2)

        high = self.series(df, "high")
        low = self.series(df, "low")
        close = self.series(df, "close")
        n = len(df)

        # True range of each bar against the previous close, averaged over the
        # bars before the current one (hence the shift).
        prev_close = mql5.shift_forward(close, 1)
        true_range = np.maximum(high, prev_close) - np.minimum(low, prev_close)
        true_range[0] = 0.0
        rolled = pd.Series(true_range).rolling(atr_period, min_periods=1).sum()
        atr = mql5.shift_forward(rolled.to_numpy() / atr_period, 1)

        highest = mql5.shift_forward(mql5.highest(high, lookback), 1)
        lowest = mql5.shift_forward(mql5.lowest(low, lookback), 1)

        hi1 = highest - mult1 * atr
        lo1 = lowest + mult1 * atr
        hi2 = highest - mult2 * atr
        lo2 = lowest + mult2 * atr

        out = {key: self.empty(n) for key in (
            "up1", "down1", "up2", "down2",
            "up1_dot", "down1_dot", "up2_dot", "down2_dot",
        )}
        trend1 = trend2 = 0.0

        for i in range(1, n):
            if close[i] > lo1[i - 1]:
                trend1 = 1
            if close[i] < hi1[i - 1]:
                trend1 = -1
            if close[i] > lo2[i - 1]:
                trend2 = 1
            if close[i] < hi2[i - 1]:
                trend2 = -1

            for mult, trend, hi, lo, up_key, down_key in (
                (mult1, trend1, hi1, lo1, "up1", "down1"),
                (mult2, trend2, hi2, lo2, "up2", "down2"),
            ):
                if mult <= 0:
                    continue
                if trend == 1:
                    if hi[i] < hi[i - 1]:
                        hi[i] = hi[i - 1]      # the stop never steps back down
                    out[up_key][i] = hi[i]
                    if np.isnan(out[up_key][i - 1]):
                        out[f"{up_key}_dot"][i] = hi[i]
                elif trend == -1:
                    if lo[i] > lo[i - 1]:
                        lo[i] = lo[i - 1]
                    out[down_key][i] = lo[i]
                    if np.isnan(out[down_key][i - 1]):
                        out[f"{down_key}_dot"][i] = lo[i]

        return out
