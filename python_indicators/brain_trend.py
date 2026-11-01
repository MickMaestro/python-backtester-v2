"""BrainTrend1 and BrainTrend2 — converted from ``braintrend1.mq5`` and
``braintrend2.mq5`` (Modules of Trade Signals based on BrainTrend).

Both colour the candles. BrainTrend1 marks bars where a 2-bar close move beats
ATR/2.3 and the stochastic sits outside 47–53: blue for up, red for down,
following a state that only flips on such a bar; other bars keep their usual
colour. BrainTrend2 colours every bar by a volatility-stop "river": up (lime)
until the low breaks 0.7 × a weighted ATR below the running extreme, then
down (magenta) until the high breaks above it.

BrainTrend2 measures range including the spread (in points). Its warm-up
adds the raw spread to a price without scaling it by ``_Point``, unlike its
main loop; here both scale it.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class BrainTrend1(Indicator):
    name = "BrainTrend1"
    pane = Pane.PRICE
    params = {"atr_period": 7, "sto_period": 9,
              "ma_method": Choice(list(mql5.MA_METHODS), default="sma")}
    plots = [
        Plot("color", "BrainTrend1", style=DrawStyle.CANDLE_COLOR,
             colors=("#000000", "#0000ff", "#ff0000")),
    ]

    def calculate(self, df):
        atr_period = max(int(self.p.atr_period), 1)
        sto_period = max(int(self.p.sto_period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        atr = mql5.atr(h, l, c, atr_period)
        sto, _signal = mql5.stochastic(h, l, c, sto_period, sto_period, 1, self.p.ma_method)
        color = self.empty(n)
        state = 0
        for i in range(max(atr_period, sto_period) + 1, n):
            rng = atr[i] / 2.3
            move = abs(c[i] - c[i - 2])
            if sto[i] < 47 and move > rng:
                state = 1
            if sto[i] > 53 and move > rng:
                state = 2
            if move <= rng:
                continue
            if sto[i] < 47 and state in (0, 1):
                color[i] = 2
            if sto[i] > 53 and state in (0, 2):
                color[i] = 1
        return {"color": color}


class BrainTrend2(Indicator):
    name = "BrainTrend2"
    pane = Pane.PRICE
    params = {"atr_period": 7}
    plots = [
        Plot("color", "BrainTrend2", style=DrawStyle.CANDLE_COLOR,
             colors=("#000000", "#00ff00", "#ff00ff")),
    ]

    def calculate(self, df):
        period = max(int(self.p.atr_period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        spread = df["spread"].to_numpy(dtype=float) * mql5.point(df)
        n = len(c)
        color = self.empty(n)
        start = period + 1
        if n <= start:
            return {"color": color}

        def true_range(i):
            prev = c[i - 1]
            return max(spread[i] + h[i] - l[i], abs(spread[i] + h[i] - prev), abs(l[i] - prev))

        extreme = c[start - 1]
        river = c[start - 2] > c[start - 1]
        values = [true_range(start)] * period
        head = 0
        dartp, cecf = 7.0, 0.7
        weights = np.arange(period, 0, -1, dtype=float)      # newest first
        for i in range(start, n):
            values[head] = true_range(i)
            ordered = [values[(head - j) % period] for j in range(period)]
            atr = 2.0 * float(np.dot(ordered, weights)) / (dartp * (dartp + 1.0))
            head = (head + 1) % period
            width = cecf * atr
            top = spread[i] + h[i]
            if river and l[i] < extreme - width:
                river = False
                extreme = top
            if not river and top > extreme + width:
                river = True
                extreme = l[i]
            if river and l[i] > extreme:
                extreme = l[i]
            if not river and top < extreme:
                extreme = top
            color[i] = 1 if river else 2
        return {"color": color}
