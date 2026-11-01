"""ZigzagColor — converted from ``zigzagcolor.mq5`` (Convenient use of
indicators).

MetaQuotes' classic ZigZag (depth / deviation / backstep), with legs into a
peak drawn blue and legs into a trough drawn red. On the replay the newest leg
is drawn to the swing as it stood at each bar.
"""

import numpy as np

from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5


class ZigzagColor(Indicator):
    name = "ZigzagColor"
    pane = Pane.PRICE
    params = {"depth": 12, "deviation": 5, "backstep": 3}
    plots = [
        Plot("up", "ZigZag (to peak)", color="#1e90ff", width=1, known_at="known"),
        Plot("down", "ZigZag (to trough)", color="#ff0000", width=1, known_at="known"),
    ]

    def setup(self):
        self.repaint_window = max(1000, 30 * int(self.p.depth))

    def calculate(self, df):
        peaks, troughs = mql5.zigzag(
            self.series(df, "high"), self.series(df, "low"),
            int(self.p.depth), int(self.p.deviation) * mql5.point(df), int(self.p.backstep),
        )
        pivots = np.where(np.isfinite(peaks), peaks, troughs)
        slots = np.where(np.isfinite(peaks), 0.0, 1.0)
        line, known = mql5.pivot_line(pivots)
        colour = mql5.leg_colors(pivots, slots)
        return {
            "up": mql5.segments(line, colour == 0),
            "down": mql5.segments(line, colour == 1),
            "known": known,
        }
