"""MACD Histogram — converted from ``macd_histogram.mq5`` (Convenient use of
indicators).

MT5's MACD as two lines — the EMA difference (blue) and its SMA signal (red) —
plus their difference as a histogram.
"""

from backtester.indicators.base import DrawStyle, Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


class MacdHistogram(Indicator):
    name = "MACD Histogram"
    pane = Pane.SEPARATE
    params = {"fast_ema": 12, "slow_ema": 26, "signal_sma": 9, "price": price_choice()}
    plots = [
        Plot("histogram", "Histogram", style=DrawStyle.HISTOGRAM, color="#00ffff"),
        Plot("macd", "MACD", color="#0000ff", width=1),
        Plot("signal", "Signal", color="#ff0000", width=1),
    ]
    levels = [Level(0.0)]

    def calculate(self, df):
        price = mql5.applied_price(df, self.p.price)
        main, signal = mql5.macd(price, int(self.p.fast_ema), int(self.p.slow_ema),
                                 int(self.p.signal_sma))
        return {"macd": main, "signal": signal, "histogram": main - signal}
