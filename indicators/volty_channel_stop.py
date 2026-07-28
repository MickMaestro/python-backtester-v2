"""Volty Channel Stop — converted from ``volty_channel_stop.mq5`` (avoitenko,
after TrendLaboratory).

An ATR envelope around a moving average. The state flips when the envelope is
broken; while it holds, the band edge ratchets in the trend's favour and is
drawn as the stop line, offset further by the "offset factor". A dot marks each
flip.

Not converted: the alert/notification block (Alert, PlaySound,
SendNotification) — those are terminal services with no meaning here.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class VoltyChannelStop(Indicator):
    name = "Volty Channel Stop"
    pane = Pane.PRICE
    params = {
        "ma_period": 1,
        "ma_method": Choice(list(mql5.MA_METHODS), default="sma"),
        "ma_price": Choice(mql5.PRICE_CHOICES, default="weighted"),
        "atr_period": 10,
        "volatility_factor": 1.0,
        "offset_factor": 1.0,
        "use_break": False,
        "use_envelopes": False,
        "show_lines": False,
    }

    def setup(self):
        # The signal dots are the point of this one; the trailing stop lines
        # are available but off unless asked for.
        line_style = DrawStyle.LINE if self.p.show_lines else DrawStyle.NONE
        self.plots = [
            Plot("up", "Up trend stop", color="#26a69a", width=2, style=line_style),
            Plot("down", "Down trend stop", color="#ef5350", width=2, style=line_style),
            Plot(
                "up_signal", "Buy signal", style=DrawStyle.ARROW,
                color="#00bfff", size=10,
            ),
            Plot(
                "down_signal", "Sell signal", style=DrawStyle.ARROW,
                color="#db7093", size=10,
            ),
        ]

    def calculate(self, df):
        period = max(int(self.p.ma_period), 1)
        atr_period = max(int(self.p.atr_period), 1)
        volatility = float(self.p.volatility_factor)
        offset = float(self.p.offset_factor)

        high = self.series(df, "high")
        low = self.series(df, "low")
        atr = mql5.atr(high, low, self.series(df, "close"), atr_period)

        if self.p.use_envelopes:
            ma_up = mql5.ma(high, period, self.p.ma_method)
            ma_down = mql5.ma(low, period, self.p.ma_method)
        else:
            price = mql5.applied_price(df, self.p.ma_price)
            ma_up = ma_down = mql5.ma(price, period, self.p.ma_method)

        n = len(df)
        smax = ma_up + volatility * atr
        smin = ma_down - volatility * atr
        up = self.empty(n)
        down = self.empty(n)
        up_signal = self.empty(n)
        down_signal = self.empty(n)
        trend = np.zeros(n)

        for i in range(1, n):
            trend[i] = trend[i - 1]
            if self.p.use_break:
                if high[i] > smax[i - 1]:
                    trend[i] = 1
                if low[i] < smin[i - 1]:
                    trend[i] = -1
            else:
                if ma_up[i] > smax[i - 1]:
                    trend[i] = 1
                if ma_down[i] < smin[i - 1]:
                    trend[i] = -1

            if trend[i] > 0:
                if smin[i] < smin[i - 1]:
                    smin[i] = smin[i - 1]
                up[i] = smin[i] - (offset - 1.0) * atr[i]
                if up[i] < up[i - 1]:
                    up[i] = up[i - 1]
                if trend[i] != trend[i - 1]:
                    up_signal[i] = up[i]
            elif trend[i] < 0:
                if smax[i] > smax[i - 1]:
                    smax[i] = smax[i - 1]
                down[i] = smax[i] + (offset - 1.0) * atr[i]
                if down[i] > down[i - 1]:
                    down[i] = down[i - 1]
                if trend[i] != trend[i - 1]:
                    down_signal[i] = down[i]

        return {
            "up": up, "down": down,
            "up_signal": up_signal, "down_signal": down_signal,
        }
