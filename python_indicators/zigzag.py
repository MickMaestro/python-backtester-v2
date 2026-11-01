"""ZigZag — converted from MetaQuotes' ``ZigZag.mq5`` (as shipped in XU v042).

Joins swing highs and lows: a new extreme must be the highest high (lowest
low) of the last ``depth`` bars, within ``deviation`` points of the bar, and
replaces any weaker one within ``backstep`` bars. The newest leg keeps
extending until price turns, so the last turning point can still move; on
the replay the newest swing is shown as it stood at each bar.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class ZigZag(Indicator):
    name = "ZigZag"
    pane = Pane.PRICE
    params = {"depth": 12, "deviation": 5, "backstep": 3}
    plots = [Plot("zigzag", "ZigZag", style=DrawStyle.SECTION, color="#ff0000", width=1)]

    def setup(self):
        self.repaint_window = max(1000, 30 * int(self.p.depth))

    def calculate(self, df):
        depth = int(self.p.depth)
        peaks, troughs = mql5.zigzag(
            self.series(df, "high"), self.series(df, "low"), depth,
            int(self.p.deviation) * mql5.point(df), int(self.p.backstep), start=depth,
        )
        return {"zigzag": np.where(np.isfinite(peaks), peaks, troughs)}
