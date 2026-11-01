"""EhlersPredictiveMovingAverage — converted from MQL5: MQL5 Indicators/The Predictive Moving Average/EhlersPredictiveMovingAverage.mq5

The Predictive Moving Average:\\nJohn Ehlers, \\"Rocket Science For Traders\\", pg.212
Copyright: Copyright 2020, Andrei Novichkov.; Link: https://www.mql5.com/ru/users/andreifx60; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'https://www.mql5.com/ru/users/andreifx60', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [9109504], 2: [32768, 255, 3329330]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'predict', 2: 'trigger'}, 'levels': [], 'description': ['The Predictive Moving Average:\\nJohn Ehlers, \\"Rocket Science For Traders\\", pg.212'], 'name': 'EhlersPredictiveMovingAverage', 'source': 'MQL5 Indicators/The Predictive Moving Average/EhlersPredictiveMovingAverage.mq5', 'folder': 'The Predictive Moving Average', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
pb = Arr(0, 0.0)
tr = Arr(0, 0.0)
tc = Arr(0, 0.0)
wma1 = Arr(0, 0.0)
wma2 = Arr(0, 0.0)
MINBAR = 13

def OnInit():
    SetIndexBuffer(0, pb, INDICATOR_DATA)
    SetIndexBuffer(1, tr, INDICATOR_DATA)
    SetIndexBuffer(2, tc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, wma1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, wma2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(pb, True)
    ArraySetAsSeries(tr, True)
    ArraySetAsSeries(tc, True)
    ArraySetAsSeries(wma1, True)
    ArraySetAsSeries(wma2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersPredictiveMovingAverage')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def GetValue(price, shift):
    wma1[shift] = ((7 * price[shift]) + (6 * price[shift + 1]) + (5 * price[shift + 2]) + (4 * price[shift + 3]) + (3 * price[shift + 4]) + (2 * price[shift + 5]) + price[shift + 6]) / 28
    wma2[shift] = ((7 * wma1[shift]) + (6 * wma1[shift + 1]) + (5 * wma1[shift + 2]) + (4 * wma1[shift + 3]) + (3 * wma1[shift + 4]) + (2 * wma1[shift + 5]) + wma1[shift + 6]) / 28
    tr[shift] = (2 * wma1[shift]) - wma2[shift]
    pb[shift] = ((4 * tr[shift]) + (3 * tr[shift + 1]) + (2 * tr[shift + 2]) + tr[shift + 3]) / 10
    if pb[shift] < tr[shift]:
        tc[shift] = 2.0
    elif pb[shift] > tr[shift]:
        tc[shift] = 1.0

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
        ArrayInitialize(pb, EMPTY_VALUE)
        ArrayInitialize(tr, EMPTY_VALUE)
        ArrayInitialize(tc, 0)
        ArrayInitialize(wma1, 0)
        ArrayInitialize(wma2, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersPredictiveMovingAverage(_MQL5Indicator):
    name = 'EhlersPredictiveMovingAverage'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

