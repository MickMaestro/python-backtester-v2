"""SlopeDirectionLine — converted from ``slopedirectionline.mq5`` (Convenient
use of indicators).

A Hull-style moving average built from SmoothAlgorithms: 2 × MA(length/2) −
MA(length), smoothed again over √length. Violet while rising, pink while
falling, grey when flat. (The source's alert/push/e-mail options are left
out.)
"""

import math

import numpy as np

from backtester.indicators import smoothing as sm
from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5


class SlopeDirectionLine(Indicator):
    name = "SlopeDirectionLine"
    pane = Pane.PRICE
    params = {
        "method1": sm.method_choice("lwma"), "length1": 12, "phase1": 15,
        "method2": sm.method_choice("sma"), "phase2": 15,
        "price": sm.price_choice(), "shift": 0, "price_shift": 0,
    }
    plots = [
        Plot("down", "SDL falling", color="#ff1493", width=2),
        Plot("flat", "SDL flat", color="#808080", width=2),
        Plot("up", "SDL rising", color="#9400d3", width=2),
    ]

    def calculate(self, df):
        length = max(int(self.p.length1), 1)
        half = max(length // 2, 1)
        root = max(int(math.sqrt(length)), 1)
        m1, ph1 = self.p.method1, int(self.p.phase1)
        m2, ph2 = self.p.method2, int(self.p.phase2)
        price = sm.price_series(df, self.p.price)
        hull = 2.0 * sm.xma(price, m1, half, ph1) - sm.xma(price, m1, length, ph1)
        begin = sm.start_bars(m1, length, ph1)
        line = sm.xma(hull, m2, root, ph2, begin=begin)
        line = line + int(self.p.price_shift) * mql5.point(df)
        start = begin + sm.start_bars(m2, root, ph2) - 1
        line[:max(start, 0)] = np.nan

        prev = mql5.previous(line)
        rising, falling = line > prev, line < prev
        flat = ~rising & ~falling & np.isfinite(line)
        shift = int(self.p.shift)
        return {
            key: mql5.shift_forward(mql5.segments(line, mask), shift)
            for key, mask in (("down", falling), ("flat", flat), ("up", rising))
        }
