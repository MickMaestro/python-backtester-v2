"""RSI MA Arrows — converted from ``RSI MA Arrows.mq5`` (mladen family).

An RSI of a *smoothed* price — the price is run through a moving average of the
RSI period first — that marks the candles wherever its state flips: an arrow
below the bar when it turns up, above when it turns down.

The RSI drives the arrows but is **not** drawn: this is an arrows-on-the-chart
indicator, with no oscillator sub-window. Everything that decides where the
arrows land is still configurable — six RSI formulas, the full applied-price
list including Heiken Ashi variants, five averaging methods, and three ways to
read the state (level cross, RSI against its average, or RSI slope).

Note the ``rsi`` method is this family's own smoothed change/absolute-change
ratio, not Wilder's classic RSI — the conversion follows the source.

Not converted: the oscillator pane with its signal average and level lines,
the multi-timeframe ``iCustom`` path, and the alerts.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class RsiMaArrows(Indicator):
    name = "RSI MA Arrows"
    pane = Pane.PRICE
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
        "arrow_gap_upper": 1.0,
        "arrow_gap_lower": 0.5,
    }
    plots = [
        Plot(
            "arrow_up", "Buy arrow", style=DrawStyle.ARROW, color="#00ff00",
            symbol="t1", size=12,
        ),
        Plot(
            "arrow_down", "Sell arrow", style=DrawStyle.ARROW, color="#ff0000",
            symbol="t", size=12,
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

        # Arrows sit an ATR away from the bar, as the source spaces them.
        high = self.series(df, "high")
        low = self.series(df, "low")
        gap = mql5.atr(high, low, self.series(df, "close"), 20)
        gap = np.where(np.isfinite(gap), gap, 0.0)
        changed = np.zeros(n, dtype=bool)
        changed[1:] = state[1:] != state[:-1]
        return {
            "arrow_up": np.where(
                changed & (state == 1),
                low - float(self.p.arrow_gap_lower) * gap,
                np.nan,
            ),
            "arrow_down": np.where(
                changed & (state == -1),
                high + float(self.p.arrow_gap_upper) * gap,
                np.nan,
            ),
        }
