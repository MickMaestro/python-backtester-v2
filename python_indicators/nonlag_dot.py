"""NonLagDot — converted from ``nonlagdot.mq5`` (Trading signals module based
on NonLagDot).

Igorad's NonLagMA drawn as dots: a moving average is re-smoothed with a
damped-cosine kernel over ``5·length − 1`` bars, which cancels most of its lag.
Dots are green while it rises, magenta while it falls, grey before the first
move.

``filter`` (in points) holds the line still on moves smaller than that. The
source compares against the *next* bar for this, which has not been computed
yet; here it compares against the previous bar.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


def nonlag_weights(length: int) -> np.ndarray:
    """The kernel the source rebuilds on every bar (it never changes)."""
    cycle = 4.0
    phase = length - 1
    span = int(length * cycle + phase)
    coeff = 3.0 * np.pi
    dt1 = (2.0 * cycle - 1.0) / (cycle * length - 1.0)
    dt2 = 1.0 / (phase - 1.0) if phase > 1 else 1.0
    weights = np.empty(span)
    t = 0.0
    for k in range(span):
        g = 1.0 if t <= 0.5 else 1.0 / (coeff * t + 1.0)
        weights[k] = g * np.cos(np.pi * t)
        if t < 1:
            t += dt2
        elif t < span - 1:
            t += dt1
    return weights


class NonLagDot(Indicator):
    name = "NonLagDot"
    pane = Pane.PRICE
    params = {
        "price": price_choice(),
        "method": Choice(list(mql5.MA_METHODS), default="sma"),
        "length": 10, "filter": 0, "deviation": 0.0, "shift": 0,
    }
    plots = [
        Plot("flat", "NonLagDot", style=DrawStyle.ARROW, color="#808080", size=5),
        Plot("down", "NonLagDot down", style=DrawStyle.ARROW, color="#ff00ff", size=5),
        Plot("up", "NonLagDot up", style=DrawStyle.ARROW, color="#008000", size=5),
    ]

    def calculate(self, df):
        length = max(int(self.p.length), 3)
        ma = mql5.ma(mql5.applied_price(df, self.p.price), length, self.p.method)
        weights = nonlag_weights(length)
        n = len(ma)
        line = self.empty(n)
        if weights.sum() > 0 and n >= len(weights):
            # sum_k w[k] * ma[i-k]: a causal convolution.
            conv = np.convolve(np.nan_to_num(ma), weights, mode="full")[:n]
            line[:] = (1.0 + float(self.p.deviation) / 100.0) * conv / weights.sum()
        start = length + len(weights) + 1
        line[:start] = np.nan

        threshold = max(int(self.p.filter), 0) * mql5.point(df)
        trend = 0
        slot = self.empty(n)
        for i in range(start, n):
            if threshold > 0 and abs(line[i] - line[i - 1]) < threshold:
                line[i] = line[i - 1]
            if line[i] - line[i - 1] > threshold:
                trend = 1
            if line[i - 1] - line[i] > threshold:
                trend = -1
            slot[i] = 2 if trend > 0 else 1 if trend < 0 else 0

        shift = int(self.p.shift)
        out = {
            "flat": np.where(slot == 0, line, np.nan),
            "down": np.where(slot == 1, line, np.nan),
            "up": np.where(slot == 2, line, np.nan),
        }
        return {key: mql5.shift_forward(v, shift) for key, v in out.items()}
