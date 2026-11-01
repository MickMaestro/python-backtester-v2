"""EhlersLaguerreFilter — converted from MQL5: MQL5 Indicators/The Laguerre Filter Indicator/EhlersLaguerreFilter.mq5

Telegram Channel: https://t.me/fxstill\\n
The Laguerre Filter:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.216
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [9109504], 2: [32768, 255, 3329330]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'filt', 2: 'fir'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The Laguerre Filter:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.216'], 'name': 'EhlersLaguerreFilter', 'source': 'MQL5 Indicators/The Laguerre Filter Indicator/EhlersLaguerreFilter.mq5', 'folder': 'The Laguerre Filter Indicator', 'inputs': [{'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.8, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
gamma = _input('gamma', 0.8)
fi = Arr(0, 0.0)
fr = Arr(0, 0.0)
fc = Arr(0, 0.0)
l0 = Arr(0, 0.0)
l1 = Arr(0, 0.0)
l2 = Arr(0, 0.0)
l3 = Arr(0, 0.0)
MINBAR = 5

def OnInit():
    SetIndexBuffer(0, fi, INDICATOR_DATA)
    SetIndexBuffer(1, fr, INDICATOR_DATA)
    SetIndexBuffer(2, fc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, l0, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, l1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, l2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, l3, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(fi, True)
    ArraySetAsSeries(fr, True)
    ArraySetAsSeries(fc, True)
    ArraySetAsSeries(l0, True)
    ArraySetAsSeries(l1, True)
    ArraySetAsSeries(l2, True)
    ArraySetAsSeries(l3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersLaguerreFilter')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT__SUCCEEDED()

def GetValue(price, shift):
    l0[shift] = ((1 - gamma) * price[shift]) + (gamma * l0[shift + 1])
    l1[shift] = ((-gamma) * l0[shift]) + l0[shift + 1] + (gamma * l1[shift + 1])
    l2[shift] = ((-gamma) * l1[shift]) + l1[shift + 1] + (gamma * l2[shift + 1])
    l3[shift] = ((-gamma) * l2[shift]) + l2[shift + 1] + (gamma * l3[shift + 1])
    fi[shift] = (l0[shift] + (2 * l1[shift]) + (2 * l2[shift]) + l3[shift]) / 6
    fr[shift] = (price[shift] + (2 * price[shift + 1]) + (2 * price[shift + 2]) + price[shift + 3]) / 6
    if fi[shift] < fr[shift]:
        fc[shift] = 2.0
    elif fi[shift] > fr[shift]:
        fc[shift] = 1.0

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
        GetValue(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(fi, EMPTY_VALUE)
        ArrayInitialize(fr, EMPTY_VALUE)
        ArrayInitialize(fc, 0)
        ArrayInitialize(l0, 0)
        ArrayInitialize(l1, 0)
        ArrayInitialize(l2, 0)
        ArrayInitialize(l3, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersLaguerreFilter(_MQL5Indicator):
    name = 'EhlersLaguerreFilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'gamma': 0.8,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

