"""Candles_Smoothed — converted from ``candles_smoothed.mq5`` (Trading signals
module based on Candles_Smoothed).

Draws a second set of candles whose open, high, low and close are each
smoothed with the chosen SmoothAlgorithms method (LWMA by default). Blue when
the smoothed close is above the smoothed open, magenta otherwise.
"""

import numpy as np

from backtester.indicators import smoothing as sm
from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot


class CandlesSmoothed(Indicator):
    name = "Candles Smoothed"
    pane = Pane.PRICE
    params = {"method": sm.method_choice("lwma"), "length": 30, "phase": 100}
    plots = [
        Plot("candle", "Smoothed candles", style=DrawStyle.CANDLES,
             colors=("#6a5acd", "#ff00ff"), color_key="candle_color"),
    ]

    def calculate(self, df):
        method, length, phase = self.p.method, int(self.p.length), int(self.p.phase)
        out = {
            f"candle_{part}": sm.xma(self.series(df, part), method, length, phase)
            for part in ("open", "high", "low", "close")
        }
        start = sm.start_bars(method, length, phase) + 1
        color = np.where(out["candle_open"] < out["candle_close"], 0.0, 1.0)
        color[: start + 1] = np.nan
        color[~np.isfinite(out["candle_close"])] = np.nan
        out["candle_color"] = color
        return out
