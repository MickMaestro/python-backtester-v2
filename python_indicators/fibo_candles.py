"""FiboCandles — converted from ``fibocandles.mq5`` (Trading signals module
based on FiboCandles).

Recolours the candles by a trend that only flips when a bar retraces more than
a Fibonacci fraction of the last ``period`` bars' range against it. The
source redraws each candle with its body flipped to match the trend
(``DRAW_COLOR_CANDLES``); the shape is unchanged, so here that becomes the
candle colour. (Its alert/sound options are left out.)
"""

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class FiboCandles(Indicator):
    name = "FiboCandles"
    pane = Pane.PRICE
    params = {
        "period": 10,
        "fibo_level": Choice(
            {0.236: "0.236", 0.382: "0.382", 0.5: "0.500", 0.618: "0.618", 0.762: "0.762"},
            default=0.236,
        ),
    }
    plots = [
        Plot("color", "FiboCandles", style=DrawStyle.CANDLE_COLOR,
             colors=("#008080", "#ff00ff")),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        level = float(self.p.fibo_level)
        o = self.series(df, "open")
        c = self.series(df, "close")
        max_high = mql5.highest(self.series(df, "high"), period)
        min_low = mql5.lowest(self.series(df, "low"), period)
        n = len(c)
        color = self.empty(n)
        trend = 0
        for i in range(period, n):
            rng = max_high[i] - min_low[i]
            if o[i] > c[i]:
                trend = -1 if (trend < 0 and rng * level < c[i] - min_low[i]) else 1
            else:
                trend = 1 if (trend > 0 and rng * level < max_high[i] - c[i]) else -1
            # Trend +1 draws the body open-above-close: the source's colour 1.
            color[i] = 1 if trend == 1 else 0
        return {"color": color}
