"""fastzz — converted from MQL5: MQL5 Indicators/Fast ZigZag/fastzz.mq5

Copyright: Copyright 2012, Yurich; Link: https://login.mql5.com/ru/users/Yurich; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Yurich', 'link': 'https://login.mql5.com/ru/users/Yurich', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Fast ZZ'}, 'levels': [], 'description': [], 'name': 'fastzz', 'source': 'MQL5 Indicators/Fast ZigZag/fastzz.mq5', 'folder': 'Fast ZigZag', 'inputs': [{'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 300, 'label': 'Minimum points in a ray', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Depth = _input('Depth', 300)  # Minimum points in a ray
zzH = Arr(0, 0.0)
zzL = Arr(0, 0.0)
depth = 0.0  # , deviation;
last = 0
direction = 0

def OnInit():
    global depth, direction, last
    SetIndexBuffer(0, zzH, INDICATOR_DATA)
    SetIndexBuffer(1, zzL, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    depth = Depth * Point()
    direction = 1
    last = 0

def OnCalculate(total, calculated, time, open, high, low, close, tick, real, spread):
    global direction, last
    if calculated == 0:
        last = 0
    for i in range(((calculated - 1) if (calculated > 0) else 0), total - 1):
        set_ = False
        zzL[i] = 0.0
        zzH[i] = 0.0
        if direction > 0:
            if high[i] > zzH[last]:
                zzH[last] = 0.0
                zzH[i] = high[i]
                if low[i] < (high[last] - depth):
                    if open[i] < close[i]:
                        zzH[last] = high[last]
                    else:
                        direction = -1
                    zzL[i] = low[i]
                last = i
                set_ = True
            if low[i] < (zzH[last] - depth) and ((not set_) or open[i] > close[i]):
                zzL[i] = low[i]
                if high[i] > (zzL[i] + depth) and open[i] < close[i]:
                    zzH[i] = high[i]
                else:
                    direction = -1
                last = i
        else:
            if low[i] < zzL[last]:
                zzL[last] = 0.0
                zzL[i] = low[i]
                if high[i] > (low[last] + depth):
                    if open[i] > close[i]:
                        zzL[last] = low[last]
                    else:
                        direction = 1
                    zzH[i] = high[i]
                last = i
                set_ = True
            if high[i] > (zzL[last] + depth) and ((not set_) or open[i] < close[i]):
                zzH[i] = high[i]
                if low[i] < (zzH[i] - depth) and open[i] > close[i]:
                    zzL[i] = low[i]
                else:
                    direction = 1
                last = i
    zzH[total - 1] = 0.0
    zzL[total - 1] = 0.0
    return total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fastzz(_MQL5Indicator):
    name = 'fastzz'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Depth': 300,  # Minimum points in a ray
    }

