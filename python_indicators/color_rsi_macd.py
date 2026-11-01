"""ColorRSI-MACD — converted from ``colorrsimacd.mq5`` (Smooth Algorithms -
Corrected_Modified library).

A MACD of RSI: fast and slow SmoothAlgorithms averages of RSI (T3 by default),
their difference as a histogram, and a JJMA signal line. Histogram colours:
teal/blue-violet above zero rising/falling, indian-red/magenta below zero
falling/rising. The signal line is blue while the histogram is above its
previous value, magenta while below.
"""

import numpy as np

from backtester.indicators import smoothing as sm
from backtester.indicators.base import DrawStyle, Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice

HIST_COLORS = ("#808080", "#008080", "#8a2be2", "#cd5c5c", "#ff00ff")


class ColorRsiMacd(Indicator):
    name = "ColorRSI-MACD"
    pane = Pane.SEPARATE
    params = {
        "rsi_period": 14, "rsi_price": price_choice(),
        "xma_method": sm.method_choice("t3"), "fast_xma": 12, "slow_xma": 26, "x_phase": 100,
        "signal_method": sm.method_choice("jjma"), "signal_xma": 9, "signal_phase": 100,
    }
    plots = [
        Plot(f"hist{k}", "RSI-MACD", style=DrawStyle.HISTOGRAM, color=colour)
        for k, colour in enumerate(HIST_COLORS)
    ] + [
        Plot("sig0", "Signal", color="#808080", width=1),
        Plot("sig1", "Signal (below)", color="#1e90ff", width=1),
        Plot("sig2", "Signal (above)", color="#ff00ff", width=1),
    ]
    levels = [Level(0.0)]

    def calculate(self, df):
        rsi_period = max(int(self.p.rsi_period), 1)
        method, phase = self.p.xma_method, int(self.p.x_phase)
        fast_n, slow_n = int(self.p.fast_xma), int(self.p.slow_xma)
        s_method, s_n, s_phase = self.p.signal_method, int(self.p.signal_xma), int(self.p.signal_phase)

        rsi = mql5.rsi(mql5.applied_price(df, self.p.rsi_price), rsi_period)
        min1 = rsi_period
        min2 = min1 + sm.start_bars(method, fast_n, phase)
        min3 = min2 + sm.start_bars(method, slow_n, phase)
        min_total = min3 + sm.start_bars(s_method, s_n, s_phase) + 2

        fast = sm.xma(rsi, method, fast_n, phase, begin=min1)
        slow = sm.xma(fast, method, slow_n, phase, begin=min2)
        macd = fast - slow
        signal = sm.xma(macd, s_method, s_n, s_phase, begin=min3)
        n = len(rsi)

        prev = mql5.previous(macd)
        hist_slot = np.zeros(n)
        hist_slot[(macd > 0) & (macd > prev)] = 1
        hist_slot[(macd > 0) & (macd < prev)] = 2
        hist_slot[(macd < 0) & (macd < prev)] = 3
        hist_slot[(macd < 0) & (macd > prev)] = 4
        prev_sig = mql5.previous(signal)
        sig_slot = np.zeros(n)
        sig_slot[macd > prev_sig] = 1
        sig_slot[macd < prev_sig] = 2

        shown = np.arange(n) >= min_total
        out = {}
        for k in range(len(HIST_COLORS)):
            out[f"hist{k}"] = np.where(shown & (hist_slot == k), macd, np.nan)
        signal = np.where(shown, signal, np.nan)
        for k in range(3):
            out[f"sig{k}"] = mql5.segments(signal, sig_slot == k)
        return out
