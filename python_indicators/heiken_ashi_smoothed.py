"""Heiken_Ashi_Smoothed — converted from ``heiken_ashi_smoothed.mq5`` (Trading
signals module based on Heiken_Ashi_Smoothed).

Heiken Ashi candles built from smoothed prices: open, high, low and close are
each smoothed (JJMA by default) and then run through the Heiken Ashi
recursion. Blue while the HA close is above its open, red otherwise.
"""

import numpy as np

from backtester.indicators import smoothing as sm
from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot


class HeikenAshiSmoothed(Indicator):
    name = "Heiken Ashi Smoothed"
    pane = Pane.PRICE
    params = {"method": sm.method_choice("jjma"), "length": 30, "phase": 100}
    plots = [
        Plot("ha", "HA smoothed", style=DrawStyle.CANDLES,
             colors=("#1e90ff", "#ff0000"), color_key="ha_color"),
    ]

    def calculate(self, df):
        method, length, phase = self.p.method, int(self.p.length), int(self.p.phase)
        xo, xh, xl, xc = (
            sm.xma(self.series(df, part), method, length, phase)
            for part in ("open", "high", "low", "close")
        )
        n = len(xc)
        start = sm.start_bars(method, length, phase) + 1
        ha_o, ha_h, ha_l, ha_c = xo.copy(), xh.copy(), xl.copy(), xc.copy()
        color = self.empty(n)
        for i in range(start + 1, n):
            ha_o[i] = (ha_o[i - 1] + ha_c[i - 1]) / 2.0
            ha_c[i] = (xo[i] + xh[i] + xl[i] + xc[i]) / 4.0
            ha_h[i] = max(xh[i], ha_o[i], ha_c[i])
            ha_l[i] = min(xl[i], ha_o[i], ha_c[i])
            color[i] = 0.0 if ha_o[i] < ha_c[i] else 1.0
        # Before the recursion starts the source shows the raw smoothed
        # values uncoloured; keep them, but never draw a half-empty candle.
        valid = np.isfinite(ha_o) & np.isfinite(ha_c)
        return {
            "ha_open": np.where(valid, ha_o, np.nan),
            "ha_high": np.where(valid, ha_h, np.nan),
            "ha_low": np.where(valid, ha_l, np.nan),
            "ha_close": np.where(valid, ha_c, np.nan),
            "ha_color": color,
        }
