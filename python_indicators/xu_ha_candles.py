"""XU HA Candles + EMA Ribbon — converted from
``XU_HA_Candles+EMA_Ribbon-v1.24.mq5`` (XU v057).

Heiken Ashi candles whose close is replaced by a fast EMA (12), coloured blue
when that EMA is above both the 13- and 89-period EMAs, orchid when below both
and grey otherwise; behind them a ribbon between EMA 13 and EMA 89, green
while the faster is on top and red otherwise. The symbol header is left out.

``tf_resonance_4x`` multiplies the EMA periods by 4 on M1 charts, as in the
source; the timeframe is read from the bar spacing.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


def _is_m1(df) -> bool:
    if len(df) < 3:
        return False
    step = df["time"].diff().dropna().median()
    return step.total_seconds() == 60


class XuHaCandles(Indicator):
    name = "XU HA Candles + EMA Ribbon"
    pane = Pane.PRICE
    params = {
        "show_ha_candles": True, "show_ema4_line": False,
        "ema4_period": 12, "ema9_period": 13, "ema36_period": 89,
        "tf_resonance_4x": False,
    }
    plots = [
        Plot("ribbon_up", "EMA ribbon (fast above)", style=DrawStyle.FILL, color="#2e6038",
             fill_with="ribbon_up_lo"),
        Plot("ribbon_dn", "EMA ribbon (fast below)", style=DrawStyle.FILL, color="#802e38",
             fill_with="ribbon_dn_lo"),
        Plot("ha", "HeikinAshi", style=DrawStyle.CANDLES,
             colors=("#1e90ff", "#da70d6", "#a9a9a9"), color_key="ha_color"),
        Plot("ema4", "EMA 4", color="#fffafa", width=2),
    ]

    def calculate(self, df):
        e4, e9, e36 = (max(int(v), 1) for v in
                       (self.p.ema4_period, self.p.ema9_period, self.p.ema36_period))
        if self.p.tf_resonance_4x and _is_m1(df):
            e4, e9, e36 = e4 * 4, e9 * 4, e36 * 4
        o = self.series(df, "open")
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        # MT5's iMA EMA is seeded with the first price and has a value on
        # every bar (PLOT_DRAW_BEGIN only hides the early ones).
        ema4 = mql5.running_ema(c, e4)
        ema9 = mql5.running_ema(c, e9)
        ema36 = mql5.running_ema(c, e36)

        ha_close_std = (o + h + l + c) / 4.0
        ha_open = np.empty(n)
        if n:
            ha_open[0] = o[0]
            for i in range(1, n):
                ha_open[i] = (ha_open[i - 1] + ha_close_std[i - 1]) / 2.0
        ha_close = ema4
        color = np.full(n, 2.0)
        color[(ema4 > ema9) & (ema4 > ema36)] = 0.0
        color[(ema4 < ema9) & (ema4 < ema36)] = 1.0

        ribbon_begin = max(e36, e9) - 1
        shown = np.arange(n) >= ribbon_begin
        fast_on_top = ema9 > ema36
        out = {
            "ribbon_up": mql5.segments(np.where(shown, ema9, np.nan), fast_on_top),
            "ribbon_up_lo": mql5.segments(np.where(shown, ema36, np.nan), fast_on_top),
            "ribbon_dn": mql5.segments(np.where(shown, ema9, np.nan), ~fast_on_top),
            "ribbon_dn_lo": mql5.segments(np.where(shown, ema36, np.nan), ~fast_on_top),
            "ema4": ema4 if self.p.show_ema4_line else np.full(n, np.nan),
        }
        begin = max(e4, 1) - 1
        if self.p.show_ha_candles:
            out.update({
                "ha_open": ha_open, "ha_close": ha_close,
                "ha_high": np.maximum(h, np.maximum(ha_open, ha_close)),
                "ha_low": np.minimum(l, np.minimum(ha_open, ha_close)),
                "ha_color": color,
            })
            for key in ("ha_open", "ha_close", "ha_high", "ha_low"):
                out[key] = out[key].copy()
                out[key][:begin] = np.nan
        else:
            for key in ("ha_open", "ha_close", "ha_high", "ha_low", "ha_color"):
                out[key] = np.full(n, np.nan)
        return out
