"""pricechannel — converted from MQL5: MQL5 Indicators/Price_Channel/pricechannel.mq5

Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16760576], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Up', 2: 'Medium', 3: 'Down'}, 'levels': [], 'description': [], 'name': 'pricechannel', 'source': 'MQL5 Indicators/Price_Channel/pricechannel.mq5', 'folder': 'Price_Channel', 'inputs': [{'mql': 'PeriodPR', 'py': 'PeriodPR', 'param': 'PeriodPR', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodPR = _input('PeriodPR', 26)
UpBuffer = Arr(0, 0.0)
MediumBuffer = Arr(0, 0.0)
DownBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MediumBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DownBuffer, INDICATOR_DATA)
    return 0

def Highest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def OnCalculate(rates_total, prev_calculated, time, Open, High, Low, Close, tick_volume, volume, spread):
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        high = Highest(High, PeriodPR, i)
        low = Lowest(Low, PeriodPR, i)
        UpBuffer[i] = Highest(High, PeriodPR, i)
        DownBuffer[i] = Lowest(Low, PeriodPR, i)
        MediumBuffer[i] = (high + low) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pricechannel(_MQL5Indicator):
    name = 'pricechannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodPR': 26,
    }

