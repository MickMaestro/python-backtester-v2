"""XU EFFECT — converted from ``XU_EFFECT_v2.23.mq5`` (XU v042).

The chart part of the indicator: a session VWAP of the typical price (tick
volume, at least 1 per bar) that resets on each new day and after a weekend
or a gap longer than ``max_gap_hours``; ±σ bands around it and the wider
"Dev Band 2.0" (switched off on H1 and above, as in the source); and the
"Sniper" candle colours — blue for an up candle closing above VWAP, pink for
a down candle closing below, grey otherwise.

Left out: the on-chart HUDs (extension/over-extension gauges, ΔVol, memory
module, account-protection and status banners) and the alerts. They describe
only the latest bar and live account state. The source also only computes
the newest ``InpMaxCalcBars`` bars; here every bar is computed.
"""

import numpy as np
import pandas as pd

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot


class XuEffect(Indicator):
    name = "XU EFFECT"
    pane = Pane.PRICE
    params = {
        "skip_weekend_reset": True, "max_gap_hours": 72,
        "show_vwap_bands": True, "band_multiplier": 1.0,
        "show_dev_bands": True, "dev_band_multiplier": 2.0,
        "sniper_candles": True,
    }
    plots = [
        Plot("vwap", "Daily VWAP", color="#ffd700", width=2, dash=True),
        Plot("color", "Sniper Candles", style=DrawStyle.CANDLE_COLOR,
             colors=("#696969", "#1e90ff", "#ff1493")),
        Plot("upper", "VWAP Upper Band", color="#a9a9a9", width=1, dash=True),
        Plot("lower", "VWAP Lower Band", color="#a9a9a9", width=1, dash=True),
        Plot("dev_upper", "Dev Band 2.0 Upper", color="#a9a9a9", width=1, dash=True),
        Plot("dev_lower", "Dev Band 2.0 Lower", color="#a9a9a9", width=1, dash=True),
    ]

    def _new_session(self, df) -> np.ndarray:
        t = pd.to_datetime(df["time"])
        day = (t.astype("int64") // 86_400_000_000_000).to_numpy()
        new = np.ones(len(t), dtype=bool)
        if len(t) > 1:
            gap_h = t.diff().dt.total_seconds().to_numpy()[1:] / 3600.0
            dow = t.dt.dayofweek.to_numpy()
            # IsTradingGap() is false — a session break — for long gaps and
            # Friday→Monday, but only when weekend resets are enabled.
            breaks = (gap_h > int(self.p.max_gap_hours)) | ((dow[:-1] == 4) & (dow[1:] == 0))
            if not self.p.skip_weekend_reset:
                breaks[:] = False
            new[1:] = (day[1:] != day[:-1]) | breaks
        return new

    def calculate(self, df):
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        o = self.series(df, "open")
        n = len(c)
        vol = np.maximum(df["tick_volume"].to_numpy(dtype=float), 1.0)
        typical = (h + l + c) / 3.0
        session = np.cumsum(self._new_session(df))
        frame = pd.DataFrame({"s": session, "pv": typical * vol,
                              "pv2": typical * typical * vol, "v": vol})
        sums = frame.groupby("s")[["pv", "pv2", "v"]].cumsum()
        v = sums["v"].to_numpy()
        vwap = sums["pv"].to_numpy() / v
        vwap = np.where(vwap > 0, vwap, np.where(c > 0, c, (h + l) / 2.0))
        sd = np.sqrt(np.maximum(sums["pv2"].to_numpy() / v - vwap * vwap, 0.0))
        sd = sd * float(self.p.band_multiplier)

        nan = np.full(n, np.nan)
        bands = bool(self.p.show_vwap_bands)
        step = pd.to_datetime(df["time"]).diff().dropna().median() if n > 2 else pd.Timedelta(0)
        high_tf = step >= pd.Timedelta(hours=1)
        dev_on = bands and self.p.show_dev_bands and not high_tf
        dev = sd * float(self.p.dev_band_multiplier)

        if self.p.sniper_candles:
            above = c > vwap
            up = c >= o
            color = np.where(above, np.where(up, 1.0, 0.0), np.where(up, 0.0, 2.0))
        else:
            color = nan
        return {
            "vwap": vwap,
            "color": color,
            "upper": vwap + sd if bands else nan,
            "lower": vwap - sd if bands else nan,
            "dev_upper": vwap + dev if dev_on else nan,
            "dev_lower": vwap - dev if dev_on else nan,
        }
