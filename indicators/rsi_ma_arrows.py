"""RSI MA Arrows — converted from ``RSI MA Arrows.mq5`` (mladen family).

An RSI of a *smoothed* price — the price is run through a moving average of the
RSI period first — drawn in its own pane and coloured by state, with a signal
average over it and arrows on the price chart wherever the state flips.

Everything the original makes optional is kept: six RSI formulas, the full
applied-price list including Heiken Ashi variants, five averaging methods, and
three ways to decide the state (level cross, RSI vs its average, or RSI slope).

Note the ``rsi`` method is this family's own smoothed change/absolute-change
ratio, not Wilder's classic RSI — the conversion follows the source.

Not converted: the multi-timeframe ``iCustom`` path and the alerts.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Level, Pane, Plot
from backtester.indicators import mql5


class RsiMaArrows(Indicator):
    name = "RSI MA Arrows"
    pane = Pane.SEPARATE
    params = {
        "rsi_period": 16,
        "rsi_method": Choice(
            {
                "rsi": "Regular RSI", "slow": "Slow RSI", "rapid": "Rapid RSI",
                "harris": "Harris RSI", "rsx": "RSX", "cuttler": "Cuttler's RSI",
            },
            default="rsi",
        ),
        "price": Choice(mql5.PRICE_CHOICES, default="close"),
        "average_period": 9,
        "average_method": Choice(list(mql5.MA_METHODS), default="ema"),
        "show_average": False,
        "level_up": 60.0,
        "level_down": 40.0,
        "arrows_on": Choice(
            {
                "level": "RSI crosses a level",
                "average": "RSI crosses its average",
                "slope": "RSI slope",
            },
            default="level",
        ),
        "show_arrows": True,
        "arrow_gap_upper": 1.0,
        "arrow_gap_lower": 0.5,
    }
    y_range = (0.0, 100.0)

    def setup(self):
        self.levels = [
            Level(float(self.p.level_up)),
            Level(float(self.p.level_down)),
        ]
        self.plots = [
            Plot("rsi", "RSI", color="#9598a1", width=2),
            Plot("rsi_up", "RSI up", color="#26a69a", width=2),
            Plot("rsi_down", "RSI down", color="#ef5350", width=2),
            Plot(
                "average", "Signal average", color="#ffffe0", width=1, dash=True,
                style=DrawStyle.LINE if self.p.show_average else DrawStyle.NONE,
            ),
            # The arrows belong on the candles, not in the oscillator pane.
            Plot(
                "arrow_up", "Buy arrow", style=DrawStyle.ARROW, color="#00ff00",
                symbol="t1", size=12, pane=Pane.PRICE,
            ),
            Plot(
                "arrow_down", "Sell arrow", style=DrawStyle.ARROW, color="#ff0000",
                symbol="t", size=12, pane=Pane.PRICE,
            ),
        ]

    def calculate(self, df):
        rsi_period = max(int(self.p.rsi_period), 1)
        price = mql5.applied_price(df, self.p.price)
        smoothed = mql5.running_ma(price, rsi_period, self.p.average_method)
        rsi = mql5.rsi_variant(smoothed, rsi_period, self.p.rsi_method)
        average = mql5.running_ma(
            rsi, max(int(self.p.average_period), 1), self.p.average_method
        )

        n = len(df)
        state = np.zeros(n)
        mode = self.p.arrows_on
        level_up = float(self.p.level_up)
        level_down = float(self.p.level_down)
        for i in range(n):
            previous = state[i - 1] if i else 0.0
            if mode == "level":
                state[i] = 1 if rsi[i] > level_up else -1 if rsi[i] < level_down else 0
            elif mode == "average":
                state[i] = 1 if rsi[i] > average[i] else -1 if rsi[i] < average[i] else previous
            else:
                if i == 0:
                    state[i] = 0
                else:
                    state[i] = (
                        1 if rsi[i] > rsi[i - 1]
                        else -1 if rsi[i] < rsi[i - 1] else previous
                    )

        out = {
            "rsi": rsi,
            "rsi_up": mql5.segments(rsi, state == 1),
            "rsi_down": mql5.segments(rsi, state == -1),
            "average": average,
            "arrow_up": self.empty(n),
            "arrow_down": self.empty(n),
        }
        if not self.p.show_arrows:
            return out

        # Arrows sit an ATR away from the bar, as the source spaces them.
        high = self.series(df, "high")
        low = self.series(df, "low")
        gap = mql5.atr(high, low, self.series(df, "close"), 20)
        gap = np.where(np.isfinite(gap), gap, 0.0)
        changed = np.zeros(n, dtype=bool)
        changed[1:] = state[1:] != state[:-1]
        out["arrow_up"] = np.where(
            changed & (state == 1), low - float(self.p.arrow_gap_lower) * gap, np.nan
        )
        out["arrow_down"] = np.where(
            changed & (state == -1), high + float(self.p.arrow_gap_upper) * gap, np.nan
        )
        return out
