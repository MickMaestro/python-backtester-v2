"""X2MA_Osc — converted from ``x2ma_osc.mq5`` (Nikolay Kositsin, v1.10), which
ships in the ``MQL5 Include`` folder because ColorX2MA_Osc reads it with
``iCustom``.

Price is smoothed twice with the SmoothAlgorithms ``CXMA`` family (any of
SMA/EMA/SMMA/LWMA/JJMA/JurX/ParMA/T3/VIDYA/AMA for each stage), then placed
within the min–max range of its last ``n_period`` values and rescaled to
−50…+50.

Faithful to the source, including its warm-up: the range window starts
filled with zeros and receives ``EMPTY_VALUE`` while the second average is
still warming up, so for the first ``n_period`` bars after the drawing
begins the oscillator sits near −50 in MT5 too. ``PriceShift`` is an input
of the source that its calculation never uses; it is omitted.
"""

import numpy as np

from backtester.indicators.base import Choice, Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.mql5_include import smooth_algorithms as sa
from backtester.indicators.mql5_include.mql_runtime import EMPTY_VALUE, to_nan

METHODS = Choice({k: v for k, v in sa.SMOOTH_METHOD_NAMES.items()}, default=sa.MODE_SMA_)
#: Applied_price_ as this source declares it (1-based, no DeMark price).
PRICES = Choice({1: "Close", 2: "Open", 3: "High", 4: "Low", 5: "Median (HL/2)",
                 6: "Typical (HLC/3)", 7: "Weighted (HLCC/4)", 8: "Simple (OC/2)",
                 9: "Quarter (HLOC/4)", 10: "TrendFollow 1", 11: "TrendFollow 2"}, default=1)


def _interpolation(a, b, c, d, x):
    if b - a == 0:
        return 10000000.0
    return d - (b - x) * (d - c) / (b - a)


class X2MAOsc(Indicator):
    name = "X2MA_Osc"
    pane = Pane.SEPARATE
    params = {
        "n_period": 100,
        "ma_method1": METHODS, "length1": 12, "phase1": 15,
        "ma_method2": Choice(METHODS.options, default=sa.MODE_JJMA), "length2": 5, "phase2": 15,
        "price": PRICES, "shift": 0,
    }
    plots = [Plot("osc", "X2MA_Osc", color="#ba55d3", width=1)]
    levels = [Level(0.0)]

    def calculate(self, df):
        p = self.p
        n_period = max(int(p.n_period), 1)
        m1, m2 = int(p.ma_method1), int(p.ma_method2)
        l1, l2 = int(p.length1), int(p.length2)
        ph1, ph2 = int(p.phase1), int(p.phase2)
        min_rates_1 = sa.GetStartBars(m1, l1, ph1)
        min_rates_total = min_rates_1 + sa.GetStartBars(m2, l2, ph2)
        n = len(df)
        out = np.full(n, np.nan)
        if n < min_rates_total:
            return {"osc": out}
        # Series-ordered views (index 0 = newest), as the source sets them.
        o, h, l, c = (df[k].to_numpy(dtype=float)[::-1].tolist() for k in ("open", "high", "low", "close"))
        xma1, xma2 = sa.CXMA(), sa.CXMA()
        ring = [0.0] * n_period
        slot = 0                      # Count[0]
        count = 1                     # Recount_ArrayZeroPos's static
        osc = [EMPTY_VALUE] * n
        maxbar1 = n - 1
        maxbar2 = maxbar1 - min_rates_1
        for bar in range(n - 1, -1, -1):
            price = sa.PriceSeries(int(p.price), bar, o, l, h, c)
            x1 = xma1.XMASeries(maxbar1, 0, n, m1, ph1, l1, price, bar, True)
            ring[slot] = xma2.XMASeries(maxbar2, 0, n, m2, ph2, l2, x1, bar, True)
            osc[bar] = _interpolation(max(ring), min(ring), 100, 0, ring[slot]) - 50
            if bar > 0:
                count -= 1
                if count < 0:
                    count = n_period - 1
                slot = count
        line = to_nan(np.array(osc[::-1]))
        line[:min_rates_total] = np.nan                         # PLOT_DRAW_BEGIN
        return {"osc": mql5.shift_forward(line, int(p.shift))}
