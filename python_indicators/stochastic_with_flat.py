"""StochasticWithFlat — converted from ``stohasticwithflat.mq5`` (Convenient
use of indicators).

A stochastic that goes quiet in a flat market: while the Bollinger upper band
sits less than ``flat`` points above its middle line, the two lines are parked
at 55/45 (main above signal) or 45/55 instead of their real values.
"""

import numpy as np

from backtester.indicators.base import Choice, Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


class StochasticWithFlat(Indicator):
    name = "Stochastic With Flat"
    pane = Pane.SEPARATE
    params = {
        "bb_period": 20, "std_deviation": 2.0, "bb_price": price_choice(),
        "k_period": 5, "d_period": 3, "slowing": 3,
        "ma_method": Choice(list(mql5.MA_METHODS), default="sma"),
        "flat": 100, "shift": 0,
    }
    plots = [
        Plot("main", "Main", color="#da70d6", width=1),
        Plot("signal", "Signal", color="#0000ff", width=1),
    ]
    levels = [Level(75.0), Level(50.0), Level(25.0)]
    y_range = (0, 100)

    def calculate(self, df):
        bb_period = max(int(self.p.bb_period), 1)
        price = mql5.applied_price(df, self.p.bb_price)
        width = float(self.p.std_deviation) * mql5.stddev(price, bb_period, "sma")
        main, signal = mql5.stochastic(
            self.series(df, "high"), self.series(df, "low"), self.series(df, "close"),
            int(self.p.k_period), int(self.p.d_period), int(self.p.slowing),
            self.p.ma_method,
        )
        flat = width / mql5.point(df) < int(self.p.flat)
        out_main = np.where(flat, np.where(main > signal, 55.0, np.where(main < signal, 45.0, np.nan)), main)
        out_signal = np.where(flat, np.where(main > signal, 45.0, np.where(main < signal, 55.0, np.nan)), signal)
        start = max(bb_period, int(self.p.k_period) + int(self.p.d_period) + int(self.p.slowing))
        out_main[:start] = np.nan
        out_signal[:start] = np.nan
        shift = int(self.p.shift)
        return {"main": mql5.shift_forward(out_main, shift),
                "signal": mql5.shift_forward(out_signal, shift)}
