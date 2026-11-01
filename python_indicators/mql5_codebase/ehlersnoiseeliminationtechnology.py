"""EhlersNoiseEliminationTechnology — converted from MQL5: MQL5 Indicators/NoiseEliminationTechnology/EhlersNoiseEliminationTechnology.mq5

Telegram Channel: https://t.me/fxstill\\n
Noise Elimination Technology: John Ehlers, \\"Stocks & Commodities. Dec.2020 pg. 16-18\\"
Copyright: Copyright 2020, Andrei Novichkov.; Link: https://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'https://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'NET_Ehlers'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'Noise Elimination Technology: John Ehlers, \\"Stocks & Commodities. Dec.2020 pg. 16-18\\"'], 'name': 'EhlersNoiseEliminationTechnology', 'source': 'MQL5 Indicators/NoiseEliminationTechnology/EhlersNoiseEliminationTechnology.mq5', 'folder': 'NoiseEliminationTechnology', 'inputs': [{'mql': 'per', 'py': 'per', 'param': 'per', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'multi', 'py': 'multi', 'param': 'multi', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
per = _input('per', 14)  # Period
multi = _input('multi', 1.0)
net = Arr(0, 0.0)
MINBAR = 0
a1 = Arr(0, 0.0)
a2 = Arr(0, 0.0)
Denom = 0.0
period = 0

def OnInit():
    global Denom, MINBAR, period
    period = (14 if (per == 0) else per)
    MINBAR = period
    SetIndexBuffer(0, net, INDICATOR_DATA)
    ArraySetAsSeries(net, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersNoiseEliminationTechnology')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArrayResize(a1, period)
    ArrayResize(a2, period)
    Denom = 0.5 * period * (period - 1)
    return INIT_SUCCEEDED

def GetValue(price, shift):
    ArrayInitialize(a1, 0)
    ArrayInitialize(a2, 0)
    for i in range(1, period):
        a1[i] = price[shift + i - 1]
        a2[i] = -i
    Num = 0.0
    i = 2
    while i < period:
        for j in range(1, i - 1):
            Num = Num - sign(a1[i] - a1[j])
        i += 1
    net[shift] = _fdiv(multi * Num, Denom)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(net, EMPTY_VALUE)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total

def sign(x):
    if x == 0.0:
        return 0
    if x > 0.0:
        return 1
    return -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersNoiseEliminationTechnology(_MQL5Indicator):
    name = 'EhlersNoiseEliminationTechnology'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'per': 14,  # Period
        'multi': 1.0,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

