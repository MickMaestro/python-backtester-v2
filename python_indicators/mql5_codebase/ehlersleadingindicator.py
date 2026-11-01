"""EhlersLeadingIndicator — converted from MQL5: MQL5 Indicators/The Leading Indicator/EhlersLeadingIndicator.mq5

Telegram Channel: https://t.me/fxstill\\n
The Leading Indicator:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.235
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 3329330], 2: [9109504]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'netLead', 2: 'ema'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The Leading Indicator:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.235'], 'name': 'EhlersLeadingIndicator', 'source': 'MQL5 Indicators/The Leading Indicator/EhlersLeadingIndicator.mq5', 'folder': 'The Leading Indicator', 'inputs': [{'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 0.33, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
alpha1 = _input('alpha1', 0.25)
alpha2 = _input('alpha2', 0.33)
nb = Arr(0, 0.0)
nc = Arr(0, 0.0)
eb = Arr(0, 0.0)
lb = Arr(0, 0.0)
MINBAR = 5

def OnInit():
    SetIndexBuffer(0, nb, INDICATOR_DATA)
    SetIndexBuffer(1, nc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, eb, INDICATOR_DATA)
    SetIndexBuffer(3, lb, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(nb, True)
    ArraySetAsSeries(nc, True)
    ArraySetAsSeries(eb, True)
    ArraySetAsSeries(lb, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersLeadingIndicator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT__SUCCEEDED()

def GetValue(price, shift):
    lb[shift] = (2 * price[shift]) + ((alpha1 - 2) * price[shift + 1]) + ((1 - alpha1) * lb[shift + 1])
    nb1 = ZerroIfEmpty(nb[shift + 1])
    nb[shift] = (alpha2 * lb[shift]) + ((1 - alpha2) * nb1)
    e1 = ZerroIfEmpty(eb[shift + 1])
    eb[shift] = (0.5 * price[shift]) + (0.5 * e1)
    if nb[shift] < eb[shift]:
        nc[shift] = 1.0
    elif nb[shift] > eb[shift]:
        nc[shift] = 2.0

def INIT__SUCCEEDED():
    PlaySound('ok.wav')
    cm = 'Subscribe! https://t.me/fxstill'
    Print(cm)
    Comment('\n' + cm)
    return INIT_SUCCEEDED

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total <= MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        pass
    elif limit > 1:
        ArrayInitialize(nb, EMPTY_VALUE)
        ArrayInitialize(eb, EMPTY_VALUE)
        ArrayInitialize(nc, 0)
        ArrayInitialize(lb, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersLeadingIndicator(_MQL5Indicator):
    name = 'EhlersLeadingIndicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'alpha1': 0.25,
        'alpha2': 0.33,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

