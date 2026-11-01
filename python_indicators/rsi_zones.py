"""RSI Zones — converted from ``simple_rpc.mq5`` (the example indicator of the
LSTM Neural Network library).

RSI centred on zero (RSI − 50) with four EMA-smoothed distance lines: how far
RSI has been, on average, from the overbought (70), oversold (30) and upper /
lower neutral (55 / 45) levels. Lines crossing zero mark RSI settling beyond
the matching level.
"""

import numpy as np

from backtester.indicators.base import Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


class RsiZones(Indicator):
    name = "RSI Zones"
    pane = Pane.SEPARATE
    params = {
        "rsi_period": 14, "price": price_choice(), "smoothing": 14,
        "overbought": 70.0, "oversold": 30.0, "upper_neutral": 55.0, "lower_neutral": 45.0,
    }
    plots = [
        Plot("rsi", "RSI − 50", color="#00008b", width=1),
        Plot("oversold", "From oversold", color="#8b0000", width=1),
        Plot("lower_neutral", "From lower neutral", color="#c0c0c0", width=1),
        Plot("upper_neutral", "From upper neutral", color="#c0c0c0", width=1),
        Plot("overbought", "From overbought", color="#006400", width=1),
    ]
    levels = [Level(0.0)]

    def calculate(self, df):
        rsi = mql5.rsi(mql5.applied_price(df, self.p.price), int(self.p.rsi_period))
        # The source feeds 0 for RSI's warm-up bars into its EMAs.
        si = np.nan_to_num(rsi, nan=0.0)
        period = float(self.p.smoothing)

        def smooth(level):
            return mql5.running_ema(si - float(level), period)

        return {
            "rsi": rsi - 50.0,
            "overbought": smooth(self.p.overbought),
            "oversold": smooth(self.p.oversold),
            "upper_neutral": smooth(self.p.upper_neutral),
            "lower_neutral": smooth(self.p.lower_neutral),
        }
