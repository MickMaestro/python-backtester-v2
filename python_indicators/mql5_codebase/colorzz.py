"""colorzz — converted from MQL5: MQL5 Indicators/Color ZigZag/colorzz.mq5

Copyright: Copyright 2012, Yurich; Link: https://login.mql5.com/ru/users/Yurich; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Yurich', 'link': 'https://login.mql5.com/ru/users/Yurich', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [255, 55295, 65280, 16776960, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Color ZZ'}, 'levels': [], 'description': [], 'name': 'colorzz', 'source': 'MQL5 Indicators/Color ZigZag/colorzz.mq5', 'folder': 'Color ZigZag', 'inputs': [{'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 300, 'label': 'Minimum points in a ray', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Depth = _input('Depth', 300)  # Minimum points in a ray
zzH = Arr(0, 0.0)
zzL = Arr(0, 0.0)
zzC = Arr(0, 0.0)
fibo = Arr.of([0.382, 0.618, 1.0, 1.618], fill=0.0)
levels = Arr(0, 0.0)
depth = 0.0
cd = 0.0
last = 0
direction = 0
cnt = 0
prev = 0

def OnInit():
    global cd, cnt, depth, direction, last, prev
    SetIndexBuffer(0, zzH, INDICATOR_DATA)
    SetIndexBuffer(1, zzL, INDICATOR_DATA)
    SetIndexBuffer(2, zzC, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    depth = Depth * Point()
    cd = 0.0
    direction = 1
    prev = 0
    last = prev
    cnt = ArraySize(fibo)
    ArrayResize(levels, cnt)

def OnCalculate(total, calculated, time, open, high, low, close, tick, real, spread):
    global cd, direction, last, prev
    if calculated == 0:
        last = 0
        prev = last
        cd = prev
    for i in range(((calculated - 1) if (calculated > 0) else 0), total - 1):
        set_ = False
        ld = cd
        zzL[i] = 0.0
        zzH[i] = 0.0
        if direction > 0:
            if high[i] > zzH[last]:
                cd = high[i] - zzL[prev]
                zzH[last] = 0.0
                zzH[i] = high[i]
                if low[i] < (high[last] - depth):
                    if open[i] < close[i]:
                        zzH[last] = high[last]
                        cd = high[last] - low[i]
                        ld = high[last] - low[prev]
                        for _i in range(0, cnt):
                            levels[_i] = ld * fibo[_i]
                        zzC[i] = SetColor(cd)
                        prev = i
                    else:
                        direction = -1
                        zzC[i] = SetColor(cd)
                        for _i in range(0, cnt):
                            levels[_i] = cd * fibo[_i]
                        prev = i
                    zzL[i] = low[i]
                else:
                    zzC[i] = SetColor(cd)
                last = i
                set_ = True
            if low[i] < (zzH[last] - depth) and ((not set_) or open[i] > close[i]):
                zzL[i] = low[i]
                if high[i] > (zzL[i] + depth) and open[i] < close[i]:
                    zzH[i] = high[i]
                    cd = high[last] - low[i]
                    ld = high[last] - low[prev]
                    for _i in range(0, cnt):
                        levels[_i] = ld * fibo[_i]
                    zzC[i] = SetColor(cd)
                    for _i in range(0, cnt):
                        levels[_i] = cd * fibo[_i]
                    prev = i
                else:
                    direction = -1
                    if not set_:
                        cd = high[last] - low[i]
                        ld = high[last] - low[prev]
                        for _i in range(0, cnt):
                            levels[_i] = ld * fibo[_i]
                        zzC[i] = SetColor(cd)
                        cd = ld
                    else:
                        for _i in range(0, cnt):
                            levels[_i] = cd * fibo[_i]
                    prev = last
                last = i
        else:
            if low[i] < zzL[last]:
                cd = zzH[prev] - low[i]
                zzL[last] = 0.0
                zzL[i] = low[i]
                if high[i] > (low[last] + depth):
                    if open[i] > close[i]:
                        zzL[last] = low[last]
                        cd = high[i] - zzL[last]
                        ld = high[prev] - low[last]
                        for _i in range(0, cnt):
                            levels[_i] = ld * fibo[_i]
                        zzC[i] = SetColor(cd)
                        for _i in range(0, cnt):
                            levels[_i] = cd * fibo[_i]
                        prev = i
                    else:
                        direction = 1
                        zzC[i] = SetColor(cd)
                        for _i in range(0, cnt):
                            levels[_i] = cd * fibo[_i]
                        prev = i
                    zzH[i] = high[i]
                else:
                    zzC[i] = SetColor(cd)
                last = i
                set_ = True
            if high[i] > (zzL[last] + depth) and ((not set_) or open[i] < close[i]):
                zzH[i] = high[i]
                if low[i] < (zzH[i] - depth) and open[i] > close[i]:
                    zzL[i] = low[i]
                    cd = high[i] - low[last]
                    ld = high[prev] - low[last]
                    for _i in range(0, cnt):
                        levels[_i] = ld * fibo[_i]
                    zzC[i] = SetColor(cd)
                    for _i in range(0, cnt):
                        levels[_i] = cd * fibo[_i]
                    prev = i
                else:
                    direction = 1
                    if not set_:
                        cd = high[i] - low[last]
                        ld = high[prev] - low[last]
                        for _i in range(0, cnt):
                            levels[_i] = ld * fibo[_i]
                        zzC[i] = SetColor(cd)
                        cd = ld
                    else:
                        for _i in range(0, cnt):
                            levels[_i] = cd * fibo[_i]
                    prev = last
                last = i
    zzH[total - 1] = 0.0
    zzL[total - 1] = 0.0
    return total

def SetColor(d):
    i = 0
    i = 0
    for i in range(i, cnt):
        if d <= levels[i]:
            return i
    else:
        i = _range_end(i, cnt, 1)
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorzz(_MQL5Indicator):
    name = 'colorzz'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Depth': 300,  # Minimum points in a ray
    }

