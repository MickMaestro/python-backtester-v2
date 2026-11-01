"""3LineBreak — converted from ``3linebreak.mq5`` (Trading signals module based
on 3LineBreak).

A swing state that flips up when a bar's high clears the highest high of the
previous ``lines_break`` bars, and down when its low breaks the lowest low.
The source paints each bar's high–low range blue or red
(``DRAW_COLOR_HISTOGRAM2``); here that becomes the candle colour.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class ThreeLineBreak(Indicator):
    name = "3LineBreak"
    pane = Pane.PRICE
    params = {"lines_break": 3}
    plots = [
        Plot("color", "Trend", style=DrawStyle.CANDLE_COLOR,
             colors=("#0000ff", "#ff0000")),
    ]

    def calculate(self, df):
        lines = max(int(self.p.lines_break), 1)
        high = self.series(df, "high")
        low = self.series(df, "low")
        n = len(high)
        # Extremes of the ``lines`` bars before this one.
        hh = mql5.previous(mql5.highest(high, lines))
        ll = mql5.previous(mql5.lowest(low, lines))
        hh[:lines] = np.nan
        ll[:lines] = np.nan

        color = self.empty(n)
        swing = False
        for i in range(lines, n):
            if swing and low[i] < ll[i]:
                swing = False
            elif not swing and high[i] > hh[i]:
                swing = True
            color[i] = 0 if swing else 1
        return {"color": color}
