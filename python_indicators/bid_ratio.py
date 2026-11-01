"""Bid Ratio — converted from ``Bid Ratio.mq5``.

Where the day is closing within its own range: 100% means the close is at the
day's high on an up day, 0% at the low. Above 80 is a strong close, below 20 a
weak one, and the reading is coloured to say so.

Like the original it is a corner readout, not a line — text in a corner of the
chart with the current bar's value. On a historical chart "current" means the
last bar drawn, so during a replay it updates as the bars arrive, and the value
is computed from the day *so far*, never from how the day ended.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5
from backtester.ui.chart.chart_text import CORNERS


class BidRatio(Indicator):
    name = "Bid Ratio"
    pane = Pane.PRICE
    params = {
        "strong": 80.0,
        "weak": 20.0,
        "corner": Choice(CORNERS, default="bottom-left"),
    }

    def setup(self):
        self.plots = [
            Plot(
                "ratio", "D1 Bid Ratio", style=DrawStyle.CORNER_TEXT,
                text="D1 Bid Ratio {value:.2f}%",
                corner=self.p.corner,
                color="#9598a1",
                color_key="ratio_color",
                # strong / weak / mild-up / mild-down, as the source colours it
                colors=("#1e90ff", "#ff1493", "#87ceeb", "#ffb6c1"),
            ),
            Plot("ratio_color", "Colour slot", style=DrawStyle.NONE),
        ]

    def calculate(self, df):
        day = mql5.running_daily(df)
        day_open, day_high = day["open"], day["high"]
        day_low, day_close = day["low"], day["close"]

        day_range = day_high - day_low
        with np.errstate(divide="ignore", invalid="ignore"):
            up_day = (day_close - day_low) * 100.0 / day_range
            down_day = (day_range + day_close - day_high) * 100.0 / day_range
        ratio = np.where(day_close >= day_open, up_day, down_day)
        ratio = np.where(day_range > 0, ratio, np.nan)

        strong, weak = float(self.p.strong), float(self.p.weak)
        colour = np.full(len(df), np.nan)
        colour = np.where(ratio > 50.0, 2.0, colour)      # mild up
        colour = np.where(ratio < 50.0, 3.0, colour)      # mild down
        colour = np.where(ratio >= strong, 0.0, colour)
        colour = np.where(ratio <= weak, 1.0, colour)

        return {"ratio": ratio, "ratio_color": colour}
