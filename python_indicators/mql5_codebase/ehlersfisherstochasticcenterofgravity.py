"""EhlersFisherStochasticCenterOfGravity — converted from MQL5: MQL5 Indicators/The Fisher Stochastic Center Of Gravity/EhlersFisherStochasticCenterOfGravity.mq5

The Fisher Stochastic Center Of Gravity:\\nJohn Ehlers
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 3329330], 2: [9109504]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'v3', 2: 'trigger'}, 'levels': [], 'description': ['The Fisher Stochastic Center Of Gravity:\\nJohn Ehlers'], 'name': 'EhlersFisherStochasticCenterOfGravity', 'source': 'MQL5 Indicators/The Fisher Stochastic Center Of Gravity/EhlersFisherStochasticCenterOfGravity.mq5', 'folder': 'The Fisher Stochastic Center Of Gravity', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
length = _input('length', 8)
v3 = Arr(0, 0.0)
vc = Arr(0, 0.0)
trigger = Arr(0, 0.0)
v1 = Arr(0, 0.0)
v2 = Arr(0, 0.0)
sg = Arr(0, 0.0)
MINBAR = length + 1
l = 0.0

def OnInit():
    global l
    SetIndexBuffer(0, v3, INDICATOR_DATA)
    SetIndexBuffer(1, vc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, trigger, INDICATOR_DATA)
    SetIndexBuffer(3, v1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, v2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, sg, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(v3, True)
    ArraySetAsSeries(vc, True)
    ArraySetAsSeries(trigger, True)
    ArraySetAsSeries(v1, True)
    ArraySetAsSeries(v2, True)
    ArraySetAsSeries(sg, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersFisherStochasticCenterOfGravity')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    l = _idiv(length + 1, 2)
    return INIT_SUCCEEDED

def GetValue(price, shift):
    num = 0.0
    denom = 0.0
    for i in range(0, length):
        num = num + ((1 + i) * price[shift + i])
        denom = denom + price[shift + i]
    if denom != 0:
        sg[shift] = l - _fdiv(num, denom)
    else:
        sg[shift] = 0.0
    maxCg = ArrayMaximum(sg, shift, length)
    minCg = ArrayMinimum(sg, shift, length)
    if maxCg == -1 or minCg == -1:
        return
    if sg[maxCg] != sg[minCg]:
        v1[shift] = _fdiv(sg[shift] - sg[minCg], sg[maxCg] - sg[minCg])
    else:
        v1[shift] = 0.0
    v2[shift] = ((4 * v1[shift]) + (3 * v1[shift + 1]) + (2 * v1[shift + 2]) + v1[shift + 3]) / 10
    v3[shift] = 0.5 * MathLog(_fdiv(1 + (1.98 * (v2[shift] - 0.5)), 1 - (1.98 * (v2[shift] - 0.5))))
    trigger[shift] = v3[shift + 1]
    if v3[shift] < trigger[shift]:
        vc[shift] = 1.0
    elif v3[shift] > trigger[shift]:
        vc[shift] = 2.0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total <= MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(v3, EMPTY_VALUE)
        ArrayInitialize(trigger, EMPTY_VALUE)
        ArrayInitialize(vc, 0)
        ArrayInitialize(v1, 0)
        ArrayInitialize(v2, 0)
        ArrayInitialize(sg, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersFisherStochasticCenterOfGravity(_MQL5Indicator):
    name = 'EhlersFisherStochasticCenterOfGravity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 8,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

