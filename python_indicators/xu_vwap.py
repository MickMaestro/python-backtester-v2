"""XU VWAP — converted from ``XU_VWAP_v1.04.mq5`` (XU v057).

Volume-weighted average of the typical price (HLC/3, tick volume), reset each
calendar day, with optional ±σ lines and shaded ribbons from the volume-
weighted variance. The source only paints the newest 5000 bars; here every
bar is drawn.
"""

import numpy as np
import pandas as pd

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class XuVwap(Indicator):
    name = "XU VWAP"
    pane = Pane.PRICE
    params = {
        "session_reset": True, "inner_sd": 1.0, "outer_sd": 2.0,
        "show_sd_lines": False, "show_inner_ribbon": False, "show_outer_ribbon": False,
    }
    plots = [
        Plot("inner_up", "Ribbon ±1σ", style=DrawStyle.FILL, color="#2e3840", fill_with="inner_lo"),
        Plot("outer_up_hi", "Ribbon +1σ→+2σ", style=DrawStyle.FILL, color="#602e38",
             fill_with="outer_up_lo"),
        Plot("outer_lo_hi", "Ribbon −2σ→−1σ", style=DrawStyle.FILL, color="#602e38",
             fill_with="outer_lo_lo"),
        Plot("vwap", "VWAP", color="#ffd700", width=2),
        Plot("sd1_up", "VWAP SD+1", color="#a9a9a9", width=1),
        Plot("sd1_lo", "VWAP SD-1", color="#a9a9a9", width=1),
        Plot("sd2_up", "VWAP SD+2", color="#a9a9a9", width=1),
        Plot("sd2_lo", "VWAP SD-2", color="#a9a9a9", width=1),
    ]

    def calculate(self, df):
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        vol = df["tick_volume"].to_numpy(dtype=float)
        typical = (h + l + c) / 3.0
        group = mql5.day_index(df) if self.p.session_reset else np.zeros(len(c), dtype=int)
        frame = pd.DataFrame({"g": group, "pv": typical * vol,
                              "pv2": typical * typical * vol, "v": vol})
        sums = frame.groupby("g")[["pv", "pv2", "v"]].cumsum()
        v = sums["v"].to_numpy()
        with np.errstate(divide="ignore", invalid="ignore"):
            vwap = np.where(v > 0, sums["pv"].to_numpy() / v, np.nan)
            variance = np.where(v > 0, sums["pv2"].to_numpy() / v - vwap * vwap, np.nan)
        sd = np.sqrt(np.maximum(variance, 0.0))
        nan = np.full(len(c), np.nan)
        inner, outer = float(self.p.inner_sd), float(self.p.outer_sd)
        # As in the source, the ribbons are built from the SD lines, so they
        # need those switched on to appear.
        lines = bool(self.p.show_sd_lines)
        sd1_up = vwap + inner * sd if lines else nan
        sd1_lo = vwap - inner * sd if lines else nan
        sd2_up = vwap + outer * sd if lines else nan
        sd2_lo = vwap - outer * sd if lines else nan
        inner_on = bool(self.p.show_inner_ribbon)
        outer_on = bool(self.p.show_outer_ribbon)
        return {
            "vwap": vwap,
            "sd1_up": sd1_up, "sd1_lo": sd1_lo, "sd2_up": sd2_up, "sd2_lo": sd2_lo,
            "inner_up": sd1_up if inner_on else nan, "inner_lo": sd1_lo if inner_on else nan,
            "outer_up_hi": sd2_up if outer_on else nan, "outer_up_lo": sd1_up if outer_on else nan,
            "outer_lo_hi": sd1_lo if outer_on else nan, "outer_lo_lo": sd2_lo if outer_on else nan,
        }
