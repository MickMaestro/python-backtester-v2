"""SuperTrend — converted from ``supertrend.mq5`` (Trading signals module based
on SuperTrend).

The CCI-driven SuperTrend: while CCI(typical) is above ``level`` the line sits
at low − ATR and only rises; below it, at high + ATR and only falls. Where
the trend flips, a dot marks the new line's first value.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class SuperTrend(Indicator):
    name = "SuperTrend"
    pane = Pane.PRICE
    params = {"cci_period": 50, "atr_period": 5, "level": 0, "shift": 0}
    plots = [
        Plot("up", "Supertrend Up", color="#00ff00", width=2),
        Plot("down", "Supertrend Down", color="#ff0000", width=2),
        Plot("buy", "Buy Supertrend signal", style=DrawStyle.ARROW,
             color="#48d1cc", size=8),
        Plot("sell", "Sell Supertrend signal", style=DrawStyle.ARROW,
             color="#ff8c00", size=8),
    ]

    def calculate(self, df):
        cci_period = max(int(self.p.cci_period), 1)
        atr_period = max(int(self.p.atr_period), 1)
        level = float(self.p.level)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        cci = mql5.cci(mql5.applied_price(df, "typical"), cci_period)
        atr = mql5.atr(h, l, c, atr_period)

        # The source works with 0 as "no value"; keep that, convert at the end.
        up = np.zeros(n)
        down = np.zeros(n)
        buy = self.empty(n)
        sell = self.empty(n)
        for i in range(max(cci_period, atr_period), n):
            now, before = cci[i], cci[i - 1]
            if now >= level and before < level:
                up[i] = down[i - 1]
            if now <= level and before > level:
                down[i] = up[i - 1]
            if now > level:
                up[i] = l[i] - atr[i]
                if up[i] < up[i - 1] and before >= level:
                    up[i] = up[i - 1]
            if now < level:
                down[i] = h[i] + atr[i]
                if down[i] > down[i - 1] and before <= level:
                    down[i] = down[i - 1]
            if down[i - 1] != 0 and up[i] != 0:
                buy[i] = up[i]
            if up[i - 1] != 0 and down[i] != 0:
                sell[i] = down[i]

        shift = int(self.p.shift)
        out = {
            "up": np.where(up != 0, up, np.nan),
            "down": np.where(down != 0, down, np.nan),
            "buy": buy,
            "sell": sell,
        }
        return {key: mql5.shift_forward(values, shift) for key, values in out.items()}
