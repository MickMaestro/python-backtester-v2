"""Ehlers2PoleButterworthFilter — converted from MQL5: MQL5 Indicators/The 2 Pole Butterworth Filter/Ehlers2PoleButterworthFilter.mq5

The 2 Pole Butterworth Filter:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.192
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 3329330]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['The 2 Pole Butterworth Filter:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.192'], 'name': 'Ehlers2PoleButterworthFilter', 'source': 'MQL5 Indicators/The 2 Pole Butterworth Filter/Ehlers2PoleButterworthFilter.mq5', 'folder': 'The 2 Pole Butterworth Filter', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
length = _input('length', 15)
bf = Arr(0, 0.0)
cf = Arr(0, 0.0)
MINBAR = 5
a = 0.0
b = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0

def OnInit():
    global a, b, c1, c2, c3
    SetIndexBuffer(0, bf, INDICATOR_DATA)
    SetIndexBuffer(1, cf, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(bf, True)
    ArraySetAsSeries(cf, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers2PoleButterworthFilter')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    a = MathExp(((-M_SQRT2) * M_PI) / length)
    b = 2 * a * MathCos((M_SQRT2 * M_PI) / length)
    c2 = b
    c3 = -MathPow(a, 2)
    c1 = (1 - b + MathPow(a, 2)) / 4
    return INIT_SUCCEEDED

def GetValue(price, shift):
    b1 = ZerroIfEmpty(bf[shift + 1])
    b2 = ZerroIfEmpty(bf[shift + 2])
    bf[shift] = (c1 * (price[shift] + (2 * price[shift + 1]) + price[shift + 3])) + (c2 * b1) + (c3 * b2)
    if bf[shift] < price[shift]:
        cf[shift] = 2.0
    elif bf[shift] > price[shift]:
        cf[shift] = 1.0

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
        ArrayInitialize(bf, EMPTY_VALUE)
        ArrayInitialize(cf, 0)
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


class Ehlers2PoleButterworthFilter(_MQL5Indicator):
    name = 'Ehlers2PoleButterworthFilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 15,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

