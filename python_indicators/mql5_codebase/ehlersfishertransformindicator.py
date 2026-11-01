"""EhlersFisherTransformIndicator — converted from MQL5: MQL5 Indicators/The Fisher Transform Indicator/EhlersFisherTransformIndicator.mq5

The Fisher Transform Indicator:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.7-8
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 3329330], 2: [9109504]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'fb', 2: 'f1'}, 'levels': [], 'description': ['The Fisher Transform Indicator:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.7-8'], 'name': 'EhlersFisherTransformIndicator', 'source': 'MQL5 Indicators/The Fisher Transform Indicator/EhlersFisherTransformIndicator.mq5', 'folder': 'The Fisher Transform Indicator', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
length = _input('length', 10)
fb = Arr(0, 0.0)
fc = Arr(0, 0.0)
f1 = Arr(0, 0.0)
v1 = Arr(0, 0.0)
MINBAR = 5

def OnInit():
    SetIndexBuffer(0, fb, INDICATOR_DATA)
    SetIndexBuffer(1, fc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, f1, INDICATOR_DATA)
    SetIndexBuffer(3, v1, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(fb, True)
    ArraySetAsSeries(fc, True)
    ArraySetAsSeries(f1, True)
    ArraySetAsSeries(v1, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersFisherTransformIndicator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def GetValue(price, shift):
    mx = ArrayMaximum(price, shift, length)
    mn = ArrayMinimum(price, shift, length)
    if mx == -1 or mn == -1:
        return
    if price[mx] != price[mn]:
        v1[shift] = _fdiv(price[shift] - price[mn], price[mx] - price[mn]) - 0.5 + (0.5 * v1[shift + 1])
    else:
        v1[shift] = 0.0
    v1[shift] = MathMax(MathMin(v1[shift], 0.999), -0.999)
    ft = ZerroIfEmpty(fb[shift + 1])
    fb[shift] = (0.25 * MathLog(_fdiv(1 + v1[shift], 1 - v1[shift]))) + (0.5 * ft)
    f1[shift] = fb[shift + 1]
    if fb[shift] < f1[shift]:
        fc[shift] = 1.0
    elif fb[shift] > f1[shift]:
        fc[shift] = 2.0

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
        ArrayInitialize(fb, EMPTY_VALUE)
        ArrayInitialize(f1, EMPTY_VALUE)
        ArrayInitialize(fc, 0)
        ArrayInitialize(v1, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersFisherTransformIndicator(_MQL5Indicator):
    name = 'EhlersFisherTransformIndicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 10,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

