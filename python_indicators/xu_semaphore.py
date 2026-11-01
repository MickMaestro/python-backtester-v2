"""XU SEMAPHORE-X and XU SEMA LRG — converted from ``XU SEMAPHORE-X.mq5`` (XU
v057) and ``XU SEMA LRGv2.09.mq5`` (XU v042).

Four "semafor" zigzags of increasing period mark swing highs and lows: a small
dot (SEMA 1), a big dot (SEMA 2), an arrow on a white disc (SEMA 3) and a
square (SEMA 4). Each level is the classic 3-Level ZZ Semafor: the lowest low
(highest high) of the last ``period`` bars is marked when the bar sits within
``deviation`` points of it, the nearest weaker mark within ``backstep`` bars
is dropped, and of consecutive same-side marks only the most extreme
survives. Highs and lows are coloured separately; a bar carrying both shows
only its high, as in the source.

The two files differ only in their default periods, deviations and colours.
The "bias box" buttons (last SEMA 3 / SEMA 4 direction) are left out, and so
is SEMAPHORE-X's 15 000-bar work limit.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


def semafor(high, low, depth: int, deviation: float, backstep: int):
    """``ZigZag_Calc`` over the whole history → (highs, lows), 0 = no mark."""
    n = len(high)
    hi = np.zeros(n)
    lo = np.zeros(n)
    depth = max(int(depth), 1)
    start = depth + backstep - 1
    if n <= start:
        return hi, lo
    lowest = mql5.lowest(low, depth)
    highest = mql5.highest(high, depth)

    last_low_one = last_high_one = 0.0
    for i in range(start, n):
        val = lowest[i]
        if val != last_low_one:
            last_low_one = val
            if low[i] - val <= deviation:
                for j in range(1, backstep + 1):
                    k = i - j
                    if k < 0:
                        break
                    if lo[k] and lo[k] > val:
                        lo[k] = 0.0
                        break
            else:
                val = 0.0
        else:
            val = 0.0
        lo[i] = val

        val = highest[i]
        if val != last_high_one:
            last_high_one = val
            if val - high[i] <= deviation:
                for j in range(1, backstep + 1):
                    k = i - j
                    if k < 0:
                        break
                    if hi[k] and hi[k] < val:
                        hi[k] = 0.0
                        break
            else:
                val = 0.0
        else:
            val = 0.0
        hi[i] = val

    last_high_two = last_low_two = -1.0
    last_high_pos = last_low_pos = -1
    for i in range(start, n):
        cur_low, cur_high = lo[i], hi[i]
        if not cur_low and not cur_high:
            continue
        if cur_high:
            if last_high_two > 0:
                if last_high_two < cur_high:
                    hi[last_high_pos] = 0.0
                else:
                    hi[i] = 0.0
            if last_high_two < cur_high or last_high_two < 0:
                last_high_two, last_high_pos = cur_high, i
            last_low_two = -1.0
        else:
            if last_low_two > 0:
                if last_low_two > cur_low:
                    lo[last_low_pos] = 0.0
                else:
                    lo[i] = 0.0
            if cur_low < last_low_two or last_low_two < 0:
                last_low_two, last_low_pos = cur_low, i
            last_high_two = -1.0
    return hi, lo


class _SemaphoreMixin:
    """Shared plots and calculate(); not an Indicator itself."""

    up_colors: tuple = ()
    down_colors: tuple = ()

    def setup(self):
        longest = max(int(getattr(self.p, f"sema{level}_period")) for level in (1, 2, 3, 4))
        self.repaint_window = max(2000, 6 * longest)
        u, d = self.up_colors, self.down_colors
        self.plots = [
            Plot("s1_up", "SEMA 1 high", style=DrawStyle.ARROW, color=u[0], size=6),
            Plot("s1_dn", "SEMA 1 low", style=DrawStyle.ARROW, color=d[0], size=6),
            Plot("s2_up", "SEMA 2 high", style=DrawStyle.ARROW, color=u[1], size=11),
            Plot("s2_dn", "SEMA 2 low", style=DrawStyle.ARROW, color=d[1], size=11),
            Plot("s4_up", "SEMA 4 high", style=DrawStyle.ARROW, color=u[3], symbol="s", size=17),
            Plot("s4_dn", "SEMA 4 low", style=DrawStyle.ARROW, color=d[3], symbol="s", size=17),
            Plot("s3_bg", "SEMA 3 disc", style=DrawStyle.ARROW, color="#ffffff", size=20),
            Plot("s3_up", "SEMA 3 high", style=DrawStyle.ARROW, color=u[2],
                 symbol="arrow_up", size=15),
            Plot("s3_dn", "SEMA 3 low", style=DrawStyle.ARROW, color=d[2],
                 symbol="arrow_down", size=15),
        ]

    def calculate(self, df):
        h = self.series(df, "high")
        l = self.series(df, "low")
        point = mql5.point(df)
        out = {}
        for level in (1, 2, 3, 4):
            show = getattr(self.p, f"show_sema{level}")
            hi, lo = semafor(
                h, l, int(getattr(self.p, f"sema{level}_period")),
                int(getattr(self.p, f"sema{level}_deviation")) * point,
                max(int(getattr(self.p, f"sema{level}_backstep")), 0),
            )
            up = np.where(hi != 0, hi, np.nan)
            down = np.where((hi == 0) & (lo != 0), lo, np.nan)
            if level == 4:                      # nudged a point clear of the bar
                up, down = up + point, down - point
            if not show:
                up = down = np.full(len(h), np.nan)
            out[f"s{level}_up"] = up
            out[f"s{level}_dn"] = down
        out["s3_bg"] = np.where(np.isfinite(out["s3_up"]), out["s3_up"], out["s3_dn"])
        return out


def _params(periods, deviations, backsteps):
    params = {}
    for level, (per, dev, bck) in enumerate(zip(periods, deviations, backsteps), start=1):
        params[f"show_sema{level}"] = True
        params[f"sema{level}_period"] = per
        params[f"sema{level}_deviation"] = dev
        params[f"sema{level}_backstep"] = bck
    return params


class XuSemaphoreX(_SemaphoreMixin, Indicator):
    name = "XU SEMAPHORE-X"
    pane = Pane.PRICE
    params = _params((13, 52, 208, 832), (45, 75, 90, 105), (5, 15, 45, 135))
    up_colors = ("#dc143c", "#da70d6", "#da70d6", "#da70d6")
    down_colors = ("#1e90ff", "#1e90ff", "#1e90ff", "#1e90ff")


class XuSemaLrg(_SemaphoreMixin, Indicator):
    name = "XU SEMA LRG"
    pane = Pane.PRICE
    params = _params((12, 48, 192, 768), (5, 5, 5, 5), (2, 2, 2, 2))
    up_colors = ("#da70d6",) * 4
    down_colors = ("#008000",) * 4
