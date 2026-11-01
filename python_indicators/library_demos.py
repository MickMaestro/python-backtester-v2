"""Two small library demos — converted from ``donchian.mq5`` (CDonchian class)
and ``line.mq5`` (The Moving Average Class).

Both sources compute over only the newest ``size``/``dim`` bars, recomputed
as each bar arrives. A history chart has no "newest bar", so here they run
over every bar.

- **Donchian Blocks**: the high and low of consecutive, non-overlapping
  ``period``-bar blocks, plotted at each block's last bar and joined. The
  source aligns its blocks to the newest bar, which shifts them as bars
  arrive; here they are aligned to the first bar so they never move.
- **MA Class Line**: a plain simple moving average of the chosen price.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


class DonchianBlocks(Indicator):
    name = "Donchian Blocks"
    pane = Pane.PRICE
    params = {"period": 5}
    plots = [
        Plot("high", "Block high", style=DrawStyle.SECTION, color="#ff6347", width=1),
        Plot("low", "Block low", style=DrawStyle.SECTION, color="#afeeee", width=1),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(h)
        high = self.empty(n)
        low = self.empty(n)
        ends = np.arange(period - 1, n, period)
        for end in ends:
            high[end] = h[end - period + 1: end + 1].max()
            low[end] = l[end - period + 1: end + 1].min()
        return {"high": high, "low": low}


class MaClassLine(Indicator):
    name = "MA Class Line"
    pane = Pane.PRICE
    params = {"period": 20, "price": price_choice()}
    plots = [Plot("ma", "SMA", color="#90ee90", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        line = mql5.sma(mql5.applied_price(df, self.p.price), period)
        line[:period] = np.nan          # the source starts one bar after a full window
        return {"ma": line}
