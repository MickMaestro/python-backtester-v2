"""SSL Channel — converted from ``SSL.mq5`` (Kalenzo, 2007).

Two linear-weighted moving averages, one of the highs and one of the lows.
Price closing above the high-MA turns the state up, below the low-MA turns it
down, and the *opposite* band is drawn as the trailing channel line. With NRTR
on ("no repaint trailing reverse"), the line only ever moves in the trend's
favour, so it works as a stop level.

Source buffers → plots: Upper SSL, Lower SSL, and the Buy/Sell dots the
original draws with ``PLOT_ARROW`` where a new line starts.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class SslChannel(Indicator):
    name = "SSL Channel"
    pane = Pane.PRICE
    params = {"period": 13, "nrtr": True}
    plots = [
        Plot("up", "Upper SSL", color="#2962ff", width=2, dash=True),
        Plot("down", "Lower SSL", color="#ff1493", width=2, dash=True),
        Plot("buy", "Buy SSL", style=DrawStyle.ARROW, color="#00bfff", size=9),
        Plot("sell", "Sell SSL", style=DrawStyle.ARROW, color="#ff3b30", size=9),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        close = self.series(df, "close")
        high_ma = mql5.lwma(self.series(df, "high"), period)
        low_ma = mql5.lwma(self.series(df, "low"), period)

        n = len(df)
        up = self.empty(n)
        down = self.empty(n)
        buy = self.empty(n)
        sell = self.empty(n)
        trend = 0

        for i in range(1, n):
            prev_high_ma = high_ma[i - 1]
            prev_low_ma = low_ma[i - 1]
            if close[i] > prev_high_ma:
                trend = 1
            elif close[i] < prev_low_ma:
                trend = -1

            if trend == -1:
                # NaN comparisons are False, so a missing previous value falls
                # through to "start a fresh line" — MT5's EMPTY_VALUE check.
                if not self.p.nrtr or np.isnan(down[i - 1]):
                    down[i] = prev_high_ma
                else:
                    down[i] = min(prev_high_ma, down[i - 1])
            else:
                if not self.p.nrtr or np.isnan(up[i - 1]):
                    up[i] = prev_low_ma
                else:
                    up[i] = max(prev_low_ma, up[i - 1])

            if np.isnan(up[i - 1]) and not np.isnan(up[i]):
                buy[i] = up[i]
            if np.isnan(down[i - 1]) and not np.isnan(down[i]):
                sell[i] = down[i]

        return {"up": up, "down": down, "buy": buy, "sell": sell}
