"""Advanced Line Chart — converted from MQL5: MQL5 Indicators/Advanced Line Chart/Advanced Line Chart.mq5

Copyright: Copyright 2023, Igor Gerasimov.; Link: tgwls2@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, Igor Gerasimov.', 'link': 'tgwls2@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11119017]}, 'widths': {1: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Advanced Line Chart', 'source': 'MQL5 Indicators/Advanced Line Chart/Advanced Line Chart.mq5', 'folder': 'Advanced Line Chart', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Z = Arr(0, 0.0)
Z0 = Arr.of([0.0, 0.0, 0.0], fill=0.0, dyn=False, size=3)
T_v = 0

def OnInit():
    SetIndexBuffer(0, Z, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global T_v
    x = rates_total - 1
    y = prev_calculated - 1
    if T_v != time[x] or y <= 0:
        if y <= 0:
            ArrayFill(Z0, 0, 3, 0)
        y0 = (y if (y < x) else (y - 1))
        for z in range((y0 if (y0 >= 0) else 0), x):
            s = high[z] - low[z]
            t = (high[z] + low[z]) / 2
            u = (_fdiv(high[z] - Temp(open[z], high[z], low[z], close[z], t, s), s) - 0.5) * 2
            w = u - Z0[0]
            v = (_fdiv(w, MathMax(MathMax(MathAbs(w), MathAbs(Z0[0] - Z0[1])), MathAbs(Z0[1] - Z0[2]))) if (MathAbs(w) > 0) else 0)
            Z[z] = t - (((high[z] - t) * (u + v)) / 2)
            Z0[2] = Z0[1]
            Z0[1] = Z0[0]
            Z0[0] = u
    s0 = high[x - 1] - low[x - 1]
    s = high[x] - low[x]
    t = (high[x] + low[x]) / 2
    u = (_fdiv(high[x] - Temp(open[x], high[x], low[x], close[x], t, s), s) - 0.5) * 2
    w = u - Z0[0]
    v = (_fdiv(w, MathMax(MathMax(MathAbs(w), MathAbs(Z0[0] - Z0[1])), MathAbs(Z0[1] - Z0[2]))) if (MathAbs(w) > 0) else 0)
    r = MathMax(_fdiv(float(_int(TimeCurrent()) - _int(time[x]) + 1), PeriodSeconds(PERIOD_CURRENT)), (_fdiv(s, MathMax(s, s0)) if (MathMax(s, s0) > 0) else 0))
    d = 1 - r
    a = MathSin(d * M_PI_2)
    b = ((r * (1 - _fdiv(r * MathLog(_fdiv(1, r)), MathLog(2)))) if (r > 0) else 0)
    c = MathTanh(d * 12)
    Z[x] = _fdiv((Z[x - 1] * c) + ((t - (((high[x] - t) * (u + v)) / 2)) * b) + (((Z[x - 1] + ((Z[x - 1] - Z[x - 2]) / 2) + close[x]) * a) / 2), a + b + c)
    T_v = time[x]
    return rates_total

def Temp(o, h, l, c, m, r):
    a = 3 * MathPow(r, 2)
    b = ((_fdiv(4 * (MathPow(c, 2) + MathPow(o, 2)), a) - _fdiv(8 * c * o, a) - (1 / 3.0)) if (a > 0) else 0)
    return m + ((h - m) * (b if (MathMin(o, c) > m or c > o) else (-b) if (MathMax(o, c) < m or c < o) else 0))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvancedLineChart(_MQL5Indicator):
    name = 'Advanced Line Chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

