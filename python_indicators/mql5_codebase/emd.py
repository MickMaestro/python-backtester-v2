"""emd — converted from MQL5: MQL5 Indicators/EMD/emd.mq5

Visit my project NeuroPlus
https://www.mql5.com/ru/market/product/11550
Copyright: baramantan; Link: https://www.mql5.com/ru/market/product/11550; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.cemd_2 import *  # #include CEMD_2.mqh
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'baramantan', 'link': 'https://www.mql5.com/ru/market/product/11550', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [17919, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'EMD'}, 'levels': [], 'description': ['Visit my project NeuroPlus', 'https://www.mql5.com/ru/market/product/11550'], 'name': 'emd', 'source': 'MQL5 Indicators/EMD/emd.mq5', 'folder': 'EMD', 'inputs': [{'mql': 'CALC', 'py': 'CALC', 'param': 'CALC', 'type': 'int', 'default': 5000, 'label': '', 'sinput': False}, {'mql': 'EMD_1', 'py': 'EMD_1', 'param': 'EMD_1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'EMD_2', 'py': 'EMD_2', 'param': 'EMD_2', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'EMD_3', 'py': 'EMD_3', 'param': 'EMD_3', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'EMD_4', 'py': 'EMD_4', 'param': 'EMD_4', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'EMD_5', 'py': 'EMD_5', 'param': 'EMD_5', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'EMD_6', 'py': 'EMD_6', 'param': 'EMD_6', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'EMD_7', 'py': 'EMD_7', 'param': 'EMD_7', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'EMD_8', 'py': 'EMD_8', 'param': 'EMD_8', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'EMD_9', 'py': 'EMD_9', 'param': 'EMD_9', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'EMD_10', 'py': 'EMD_10', 'param': 'EMD_10', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'EMD_11', 'py': 'EMD_11', 'param': 'EMD_11', 'type': 'int', 'default': 11, 'label': '', 'sinput': False}, {'mql': 'EMD_12', 'py': 'EMD_12', 'param': 'EMD_12', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'EMD_13', 'py': 'EMD_13', 'param': 'EMD_13', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'EMD_14', 'py': 'EMD_14', 'param': 'EMD_14', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'EMD_15', 'py': 'EMD_15', 'param': 'EMD_15', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['CEMD_2.mqh', 'Object.mqh', 'StdLibErr.mqh']}

# ---- inputs and global variables
CALC = _input('CALC', 5000)
EMD_1 = _input('EMD_1', 1)
EMD_2 = _input('EMD_2', 2)
EMD_3 = _input('EMD_3', 3)
EMD_4 = _input('EMD_4', 4)
EMD_5 = _input('EMD_5', 5)
EMD_6 = _input('EMD_6', 6)
EMD_7 = _input('EMD_7', 7)
EMD_8 = _input('EMD_8', 8)
EMD_9 = _input('EMD_9', 9)
EMD_10 = _input('EMD_10', 10)
EMD_11 = _input('EMD_11', 11)
EMD_12 = _input('EMD_12', 12)
EMD_13 = _input('EMD_13', 13)
EMD_14 = _input('EMD_14', 14)
EMD_15 = _input('EMD_15', 15)
prev = -1
prev2 = 0
Buffer = Arr(0, 0.0)
Color = Arr(0, 0.0)
d1 = Arr(0, 0.0)
d2 = Arr(0, 0.0)

def Init():
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Color, INDICATOR_COLOR_INDEX)

def OnInit():
    global prev2
    Init()
    prev2 = CALC

def OnDeinit(reason):
    _delete(emd)

def OnCalculate(rates_total, prev_calculated, time, Open, High, Low, Close, tick_volume, volume, spread):
    global prev, prev2
    if prev < rates_total:
        prev = rates_total
    else:
        return rates_total
    ArrayInitialize(Buffer, EMPTY_VALUE)
    x = ArrayResize(d2, CopyClose(Symbol(), Period(), 0, prev2, d1))
    prev2 += 1
    ArrayInitialize(d2, 0)
    emd.Decomp(d1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMD - ' + _str(emd.nIMF - 1) + '    ')
    if EMD_1 > 0 and EMD_1 < emd.nIMF:
        emd.GetIMF(d1, EMD_1)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_2 > 0 and EMD_2 < emd.nIMF:
        emd.GetIMF(d1, EMD_2)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_3 > 0 and EMD_3 < emd.nIMF:
        emd.GetIMF(d1, EMD_3)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_4 > 0 and EMD_4 < emd.nIMF:
        emd.GetIMF(d1, EMD_4)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_5 > 0 and EMD_5 < emd.nIMF:
        emd.GetIMF(d1, EMD_5)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_6 > 0 and EMD_6 < emd.nIMF:
        emd.GetIMF(d1, EMD_6)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_7 > 0 and EMD_7 < emd.nIMF:
        emd.GetIMF(d1, EMD_7)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_8 > 0 and EMD_8 < emd.nIMF:
        emd.GetIMF(d1, EMD_8)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_9 > 0 and EMD_9 < emd.nIMF:
        emd.GetIMF(d1, EMD_9)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_10 > 0 and EMD_10 < emd.nIMF:
        emd.GetIMF(d1, EMD_10)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_11 > 0 and EMD_11 < emd.nIMF:
        emd.GetIMF(d1, EMD_11)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_12 > 0 and EMD_12 < emd.nIMF:
        emd.GetIMF(d1, EMD_12)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_13 > 0 and EMD_13 < emd.nIMF:
        emd.GetIMF(d1, EMD_13)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_14 > 0 and EMD_14 < emd.nIMF:
        emd.GetIMF(d1, EMD_14)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    if EMD_15 > 0 and EMD_15 < emd.nIMF:
        emd.GetIMF(d1, EMD_15)
        for y in range(0, ArraySize(d1)):
            d2[y] += d1[y]
    for kl in range(0, x):
        Buffer[rates_total - 1 - kl] = d2[x - 1 - kl]
        if kl > 0 and d2[x - 1 - kl] > d2[x - kl]:
            Color[rates_total - 1 - kl] = 1.0
        else:
            Color[rates_total - 1 - kl] = 0.0
    return rates_total

# ---- global variables initialised from expressions
emd = CEMD()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Emd(_MQL5Indicator):
    name = 'emd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'CALC': 5000,
        'EMD_1': 1,
        'EMD_2': 2,
        'EMD_3': 3,
        'EMD_4': 4,
        'EMD_5': 5,
        'EMD_6': 6,
        'EMD_7': 7,
        'EMD_8': 8,
        'EMD_9': 9,
        'EMD_10': 10,
        'EMD_11': 11,
        'EMD_12': 12,
        'EMD_13': 13,
        'EMD_14': 14,
        'EMD_15': 15,
    }

