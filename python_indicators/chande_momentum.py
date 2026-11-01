"""Chande Momentum Oscillator — converted from ``chande_momentum_oscillator.mq5``
(Module of Trade Signals based on the Chande Momentum Oscillator).

Built on SmoothAlgorithms' ``CCMO``, which returns the *absolute* CMO; the
indicator rescales it as |CMO| × 200 − 100, so it reads −100 with no net
direction and +100 for a one-way run either up or down.
"""

from backtester.indicators.base import Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators import smoothing as sm
from backtester.indicators.onarray import price_choice


class ChandeMomentumOscillator(Indicator):
    name = "Chande Momentum Oscillator"
    pane = Pane.SEPARATE
    params = {"period": 9, "shift": 0, "price": price_choice()}
    plots = [Plot("cmo", "CMO", color="#ffd700", width=1)]
    levels = [Level(50.0, color="#ff00ff"), Level(0.0, color="#ff00ff"),
              Level(-50.0, color="#ff00ff")]

    def calculate(self, df):
        price = mql5.applied_price(df, self.p.price)
        cmo = sm.cmo_abs(price, max(int(self.p.period), 1)) * 200.0 - 100.0
        return {"cmo": mql5.shift_forward(cmo, int(self.p.shift))}
