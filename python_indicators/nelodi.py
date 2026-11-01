"""NELODI ADX, Chart and Volume — converted from ``nld_adx.mq5``, ``nld_chart.mq5``
and ``nld_volume.mq5`` (NELODI Trading Terminal for MT5).

- **NELODI ADX**: MT5's ADX rearranged — a band between ADX+DI+ and ADX+DI−,
  green while DI+ leads and red otherwise, with ADX shifted by half the DI
  spread through the middle.
- **NELODI Chart**: the price as shaded bands — high to close in dark red,
  close to low in dark green, and the open–close body in dark red/green. The
  source also blanks MT5's own candles; this app's candles stay visible.
- **NELODI Volume**: tick volume as a histogram. The source scales the
  forming bar's volume up by the time left in it; on closed bars that does
  not apply.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class NelodiAdx(Indicator):
    name = "NELODI ADX"
    pane = Pane.SEPARATE
    params = {"period": 15}
    plots = [
        Plot("di_up", "DI (+ leads)", style=DrawStyle.FILL, color="#009600", fill_with="di_up_lo"),
        Plot("di_dn", "DI (− leads)", style=DrawStyle.FILL, color="#960000", fill_with="di_dn_lo"),
        Plot("adx", "ADX", color="#c8c800", width=1),
    ]
    y_range = (5, 125)

    def calculate(self, df):
        period = int(self.p.period) if int(self.p.period) > 0 else 15
        adx, pdi, mdi = mql5.adx(self.series(df, "high"), self.series(df, "low"),
                                 self.series(df, "close"), period)
        top = adx + pdi
        bottom = adx + mdi
        top[:period] = np.nan
        bottom[:period] = np.nan
        line = adx + (pdi - mdi) / 2.0
        line[: period * 2] = np.nan
        lead = top > bottom
        return {
            "di_up": mql5.segments(top, lead), "di_up_lo": mql5.segments(bottom, lead),
            "di_dn": mql5.segments(top, ~lead), "di_dn_lo": mql5.segments(bottom, ~lead),
            "adx": line,
        }


class NelodiChart(Indicator):
    name = "NELODI Chart"
    pane = Pane.PRICE
    params = {}
    plots = [
        Plot("high", "H", style=DrawStyle.FILL, color="#800000", fill_with="close_top"),
        Plot("close_bot", "L", style=DrawStyle.FILL, color="#008000", fill_with="low"),
        Plot("body_dn", "OC (down)", style=DrawStyle.FILL, color="#400000", fill_with="body_dn_lo"),
        Plot("body_up", "OC (up)", style=DrawStyle.FILL, color="#004000", fill_with="body_up_lo"),
    ]

    def calculate(self, df):
        o = self.series(df, "open")
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        down = o > c
        return {
            "high": h, "close_top": c.copy(), "close_bot": c.copy(), "low": l,
            "body_dn": mql5.segments(o, down), "body_dn_lo": mql5.segments(c, down),
            "body_up": mql5.segments(o, ~down), "body_up_lo": mql5.segments(c, ~down),
        }


class NelodiVolume(Indicator):
    name = "NELODI Volume"
    pane = Pane.SEPARATE
    params = {}
    plots = [Plot("volume", "Volume", style=DrawStyle.HISTOGRAM, color="#3f3f3f")]

    def calculate(self, df):
        return {"volume": df["tick_volume"].to_numpy(dtype=float)}
