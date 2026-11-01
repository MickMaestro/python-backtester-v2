"""PriceChannel_Stop — converted from ``pricechannel_stop.mq5`` (Trading
signals module based on PriceChannel_Stop).

A Donchian channel pulled in by ``risk`` × its width gives a stop on each
side. Closing beyond the opposite stop flips the trend; the active stop only
ratchets in the trend's favour. Big dots mark the first bar of a new trend,
small dots the rest, with an optional line through them.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class PriceChannelStop(Indicator):
    name = "PriceChannel Stop"
    pane = Pane.PRICE
    params = {"channel_period": 5, "risk": 0.10, "signal": True, "line": True}
    plots = [
        Plot("sell_signal", "SellSignal", style=DrawStyle.ARROW, color="#ff00ff", size=8),
        Plot("sell_stop", "SellStopSignal", style=DrawStyle.ARROW, color="#ff00ff", size=4),
        Plot("sell_line", "SellStopLine", color="#ff00ff", width=1),
        Plot("buy_signal", "BuySignal", style=DrawStyle.ARROW, color="#00ff00", size=8),
        Plot("buy_stop", "BuyStopSignal", style=DrawStyle.ARROW, color="#00ff00", size=4),
        Plot("buy_line", "BuyStopLine", color="#00ff00", width=1),
    ]

    def calculate(self, df):
        p = max(int(self.p.channel_period), 1)
        risk = float(self.p.risk)
        c = self.series(df, "close")
        hh = mql5.highest(self.series(df, "high"), p)
        ll = mql5.lowest(self.series(df, "low"), p)
        width = (hh - ll) * risk
        bsmax = hh - width
        bsmin = ll + width
        n = len(c)

        # The source keeps 0 as "empty" in these buffers and tests ``> 0``.
        out = {key: np.zeros(n) for key in (
            "sell_signal", "sell_stop", "sell_line", "buy_signal", "buy_stop", "buy_line",
        )}
        trend = 0
        prev_max = prev_min = 0.0          # the static carry-over starts at 0
        for i in range(p, n):
            if c[i] > prev_max:
                trend = 1
            if c[i] < prev_min:
                trend = -1
            if trend > 0 and bsmin[i] < prev_min:
                bsmin[i] = prev_min
            if trend < 0 and bsmax[i] > prev_max:
                bsmax[i] = prev_max
            if trend > 0:
                price = bsmin[i]
                key = "buy_signal" if self.p.signal and out["sell_stop"][i - 1] > 0 else "buy_stop"
                out[key][i] = price
                if self.p.line:
                    out["buy_line"][i] = price
            if trend < 0:
                price = bsmax[i]
                key = "sell_signal" if self.p.signal and out["buy_stop"][i - 1] > 0 else "sell_stop"
                out[key][i] = price
                if self.p.line:
                    out["sell_line"][i] = price
            prev_max, prev_min = bsmax[i], bsmin[i]
        return {key: np.where(v != 0, v, np.nan) for key, v in out.items()}
