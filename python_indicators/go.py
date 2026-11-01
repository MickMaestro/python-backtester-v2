"""Go — converted from ``go.mq5`` (Trading signals module based on Go).

The average candle body, close − open, over ``period`` bars, in points: a
histogram that is green above zero, red below, grey at zero.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators import smoothing as sm


class Go(Indicator):
    name = "Go"
    pane = Pane.SEPARATE
    params = {"period": 174, "shift": 0}
    plots = [
        Plot("flat", "Go", style=DrawStyle.HISTOGRAM, color="#808080"),
        Plot("up", "Go up", style=DrawStyle.HISTOGRAM, color="#00ff00"),
        Plot("down", "Go down", style=DrawStyle.HISTOGRAM, color="#ff0000"),
    ]
    levels = [Level(0.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        body = self.series(df, "close") - self.series(df, "open")
        value = sm.sma(body, period) / mql5.point(df)
        value[:period] = np.nan          # PLOT_DRAW_BEGIN
        shift = int(self.p.shift)
        return {
            key: mql5.shift_forward(np.where(mask, value, np.nan), shift)
            for key, mask in (("flat", value == 0), ("up", value > 0), ("down", value < 0))
        }
