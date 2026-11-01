"""RSI ZigZag — converted from ``testrsizzxonbuffer.mq5`` (ZigZagExtremaOnArray).

RSI with the classic ZigZag run on the RSI line itself (``ZZOnBuffer``), drawn
as sections joining its turning points. ``search_mode`` keeps both kinds of
extreme, only the peaks, or only the bottoms (the source's default).

The zigzag starts once RSI is defined rather than running over the zeros MT5
leaves in RSI's warm-up, which would plant a false bottom at 0.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


class RsiZigZag(Indicator):
    name = "RSI ZigZag"
    pane = Pane.SEPARATE
    params = {
        "rsi_period": 8, "price": price_choice(),
        "depth": 12, "deviation": 5, "backstep": 3,
        "search_mode": Choice({"extremum": "ZigZag", "peak": "Peaks", "bottom": "Bottoms"},
                              default="bottom"),
    }
    plots = [
        Plot("rsi", "RSI", color="#ff6347", width=1),
        Plot("zz", "Extremes", style=DrawStyle.SECTION, color="#1e90ff", width=1),
    ]
    levels = [Level(30.0), Level(70.0)]
    y_range = (0, 100)

    def setup(self):
        self.repaint_window = max(1000, 30 * int(self.p.depth))

    def calculate(self, df):
        rsi = mql5.rsi(mql5.applied_price(df, self.p.price), int(self.p.rsi_period))
        n = len(rsi)
        zz = self.empty(n)
        valid = np.nonzero(np.isfinite(rsi))[0]
        if len(valid):
            s = int(valid[0])
            tail = rsi[s:]
            depth = int(self.p.depth)
            peaks, bottoms = mql5.zigzag(
                tail, tail, depth, int(self.p.deviation) * mql5.point(df),
                int(self.p.backstep), start=depth,
            )
            if self.p.search_mode in ("extremum", "peak"):
                zz[s:] = np.where(np.isfinite(peaks), peaks, zz[s:])
            if self.p.search_mode in ("extremum", "bottom"):
                zz[s:] = np.where(np.isfinite(bottoms), bottoms, zz[s:])
        return {"rsi": rsi, "zz": zz}
