"""ibbfill — converted from MQL5: MQL5 Indicators/iBBFill_HTF/ibbfill.mq5

Copyright: Integer; Link: http://dmffx.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'http://dmffx.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1, 6: 1}, 'colors': {1: [4590090], 2: [657990], 3: [3289650], 4: [65535], 5: [16748574], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'UpTrend', 2: 'DnTrend', 3: 'Flat', 4: 'BB MA', 5: 'BB Upper', 6: 'BB Lower'}, 'levels': [], 'description': [], 'name': 'ibbfill', 'source': 'MQL5 Indicators/iBBFill_HTF/ibbfill.mq5', 'folder': 'iBBFill_HTF', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 20, 'label': 'Период BB', 'sinput': False}, {'mql': 'BBDeviation', 'py': 'BBDeviation', 'param': 'BBDeviation', 'type': 'double', 'default': 2.0, 'label': 'Ширина BB', 'sinput': False}, {'mql': 'BBPrice', 'py': 'BBPrice', 'param': 'BBPrice', 'type': 'int', 'default': 1, 'label': 'Цена BB', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # Период BB
BBDeviation = _input('BBDeviation', 2.0)  # Ширина BB
BBPrice = _input('BBPrice', PRICE_CLOSE)  # Цена BB
Upper1 = Arr(0, 0.0)
Lower1 = Arr(0, 0.0)
Upper2 = Arr(0, 0.0)
Lower2 = Arr(0, 0.0)
Upper3 = Arr(0, 0.0)
Lower3 = Arr(0, 0.0)
BCBuf = Arr(0, 0.0)
BUBuf = Arr(0, 0.0)
BLBuf = Arr(0, 0.0)
Trend = Arr(0, 0.0)
BBHand = 0

def OnInit():
    global BBHand
    SetIndexBuffer(0, Upper1, INDICATOR_DATA)
    SetIndexBuffer(1, Lower1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, Upper2, INDICATOR_DATA)
    SetIndexBuffer(3, Lower2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, Upper3, INDICATOR_DATA)
    SetIndexBuffer(5, Lower3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BCBuf, INDICATOR_DATA)
    SetIndexBuffer(7, BUBuf, INDICATOR_DATA)
    SetIndexBuffer(8, BLBuf, INDICATOR_DATA)
    SetIndexBuffer(9, Trend, INDICATOR_CALCULATIONS)
    BBHand = iBands(None, PERIOD_CURRENT, BBPeriod, 0, BBDeviation, BBPrice)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    limit1 = 0
    if prev_calculated > 0:
        limit = prev_calculated - 1
        limit1 = limit
    else:
        limit = 0
        limit1 = 1
    CopyBuffer(BBHand, 0, 0, rates_total - limit, BCBuf)
    CopyBuffer(BBHand, 1, 0, rates_total - limit, BUBuf)
    CopyBuffer(BBHand, 2, 0, rates_total - limit, BLBuf)
    for i in range(limit1, rates_total):
        Trend[i] = Trend[i - 1]
        Upper1[i] = 0.0
        Lower1[i] = 0.0
        Upper2[i] = 0.0
        Lower2[i] = 0.0
        Upper3[i] = 0.0
        Lower3[i] = 0.0
        if Trend[i] == 1 and close[i] < BCBuf[i]:
            Trend[i] = 0.0
        if Trend[i] == -1 and close[i] > BCBuf[i]:
            Trend[i] = 0.0
        if close[i] > BUBuf[i]:
            Trend[i] = 1.0
        if close[i] < BLBuf[i]:
            Trend[i] = -1.0
        _sw1 = _int(Trend[i])
        if _sw1 == 1:
            Upper1[i] = BUBuf[i]
            Lower1[i] = BLBuf[i]
            if Trend[i - 1] != 1:
                Upper1[i - 1] = BUBuf[i - 1]
                Lower1[i - 1] = BLBuf[i - 1]
        elif _sw1 == -1:
            Upper2[i] = BUBuf[i]
            Lower2[i] = BLBuf[i]
            if Trend[i - 1] != -1:
                Upper2[i - 1] = BUBuf[i - 1]
                Lower2[i - 1] = BLBuf[i - 1]
        elif _sw1 == 0:
            Upper3[i] = BUBuf[i]
            Lower3[i] = BLBuf[i]
            if Trend[i - 1] != 0:
                Upper3[i - 1] = BUBuf[i - 1]
                Lower3[i - 1] = BLBuf[i - 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ibbfill(_MQL5Indicator):
    name = 'ibbfill'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Период BB
        'BBDeviation': 2.0,  # Ширина BB
        'BBPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена BB
    }

