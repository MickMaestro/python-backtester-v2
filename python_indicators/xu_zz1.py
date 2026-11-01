"""XU ZZ1 — converted from ``XU_ZZ1_v3.mq5`` (XU v057).

A slow zigzag: a bar is a candidate low when no low in the previous ``depth``
bars is lower and it sits at least ``deviation`` points under the average low
of the ``depth``-bar window centred on it (highs likewise); weaker candidates
within ``backstep`` bars are dropped, and the survivors are linked into
alternating swings. Pivots are drawn as a thick grey line.

Two things differ from the live indicator, both because the centred average
reaches ``depth/2`` bars past the pivot:

- On the replay a pivot appears once that window has printed and its value
  is final (``depth/2`` bars later, at least ``confirmation_bars``). Live MT5
  shows it after ``confirmation_bars`` using a partial average and may later
  move or drop it.
- The live-only extras — the dashed tentative tip, the "continuity" line to
  the current close, the symbol header, alerts and the JSON file export —
  are left out.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


def _centred_mean(values: np.ndarray, half: int) -> np.ndarray:
    """Mean over [i-half, i+half], clipped at both ends (CalculateAverage)."""
    n = len(values)
    csum = np.r_[0.0, np.cumsum(values)]
    idx = np.arange(n)
    lo = np.maximum(idx - half, 0)
    hi = np.minimum(idx + half, n - 1)
    return (csum[hi + 1] - csum[lo]) / (hi - lo + 1)


def _candidates(values, depth, backstep, dev, avg, lows: bool) -> np.ndarray:
    """The eager pivot map, oldest to newest, with backstep clearing."""
    n = len(values)
    out = np.zeros(n)
    sign = 1.0 if lows else -1.0
    v = values * sign                       # lows as-is, highs negated
    # "no lower value in the previous depth bars": a rolling min over i-depth..i
    prior = np.r_[np.full(1, np.inf), v[:-1]]
    windows_min = mql5.lowest(prior, depth)  # min over i-depth .. i-1
    for i in range(depth, n):
        if windows_min[i] < v[i]:
            continue
        gap = (avg[i] - values[i]) if lows else (values[i] - avg[i])
        if avg[i] > 0 and gap >= dev:
            for b in range(1, backstep + 1):
                j = i - b
                if j < 0:
                    break
                if out[j] != 0 and out[j] * sign > v[i]:
                    out[j] = 0.0
            out[i] = values[i]
    return out


class XuZZ1(Indicator):
    name = "XU ZZ1"
    pane = Pane.PRICE
    params = {"depth": 208, "deviation": 90, "backstep": 45, "confirmation_bars": 3}
    plots = [Plot("zz", "ZZ1 Confirmed", style=DrawStyle.SECTION, color="#a9a9a9",
                  width=3, known_at="known")]

    def setup(self):
        self.repaint_window = max(2000, 10 * int(self.p.depth))

    def calculate(self, df):
        depth = max(int(self.p.depth), 2)
        backstep = max(int(self.p.backstep), 0)
        confirm = max(int(self.p.confirmation_bars), 0)
        dev = int(self.p.deviation) * mql5.point(df)
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(h)
        out = {"zz": self.empty(n), "known": np.full(n, np.inf)}
        if n < depth * 2:
            return out

        half = depth // 2
        low_map = _candidates(l, depth, backstep, dev, _centred_mean(l, half), lows=True)
        high_map = _candidates(h, depth, backstep, dev, _centred_mean(h, half), lows=False)

        high_calc = np.zeros(n)
        low_calc = np.zeros(n)
        state = 0                                   # 0 neutral, 1 up, -1 down
        last_high = last_low = 0.0
        last_high_at = last_low_at = -1
        for i in range(depth, n):
            if state == 0:
                if high_map[i]:
                    high_calc[i] = last_high = high_map[i]
                    last_high_at, state = i, -1
                elif low_map[i]:
                    low_calc[i] = last_low = low_map[i]
                    last_low_at, state = i, 1
            elif state == 1:
                if low_map[i] and i > last_low_at and low_map[i] < last_low:
                    if last_low_at >= 0:
                        low_calc[last_low_at] = 0.0
                    low_calc[i] = last_low = low_map[i]
                    last_low_at = i
                if high_map[i] and (i > last_low_at or last_low_at == -1):
                    high_calc[i] = last_high = high_map[i]
                    last_high_at, state = i, -1
            else:
                if high_map[i] and i > last_high_at and high_map[i] > last_high:
                    if last_high_at >= 0:
                        high_calc[last_high_at] = 0.0
                    high_calc[i] = last_high = high_map[i]
                    last_high_at = i
                if low_map[i] and (i > last_high_at or last_high_at == -1):
                    low_calc[i] = last_low = low_map[i]
                    last_low_at, state = i, 1

        pivots = np.where(low_calc != 0, low_calc, np.where(high_calc != 0, high_calc, np.nan))
        # Confirmed means at least ``confirm`` bars old.
        pivots[max(n - confirm, 0):] = np.nan
        idx = np.nonzero(np.isfinite(pivots))[0]
        out["zz"] = pivots
        out["known"][idx] = idx + max(confirm, half)
        return out
