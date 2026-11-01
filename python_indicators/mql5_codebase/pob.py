"""POB — converted from MQL5: MQL5 Indicators/POB/POB.mq5

Point of Balance
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'BL (Up)', 2: 'POB', 3: 'BR (Down)'}, 'levels': [], 'description': ['Point of Balance'], 'name': 'POB', 'source': 'MQL5 Indicators/POB/POB.mq5', 'folder': 'POB', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferBL = Arr(0, 0.0)
BufferPOB = Arr(0, 0.0)
BufferBR = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferBL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPOB, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBR, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'POB(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBL, True)
    ArraySetAsSeries(BufferPOB, True)
    ArraySetAsSeries(BufferBR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferBL, EMPTY_VALUE)
        ArrayInitialize(BufferPOB, EMPTY_VALUE)
        ArrayInitialize(BufferBR, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        highest_h = Highest("", PERIOD_CURRENT, PRICE_HIGH, period, i)
        highest_l = Highest("", PERIOD_CURRENT, PRICE_LOW, period, i)
        lowest_h = Lowest("", PERIOD_CURRENT, PRICE_HIGH, period, i)
        lowest_l = Lowest("", PERIOD_CURRENT, PRICE_LOW, period, i)
        if ((highest_h == WRONG_VALUE or highest_l == WRONG_VALUE) or lowest_h == WRONG_VALUE) or lowest_l == WRONG_VALUE:
            return 0
        MinH = high[lowest_h]
        MaxH = high[highest_h]
        MinL = low[lowest_l]
        MaxL = low[highest_l]
        BufferBL[i] = (MinH + MaxH) / 2
        BufferBR[i] = (MinL + MaxL) / 2
        BufferPOB[i] = (BufferBL[i] + BufferBR[i]) / 2
    return rates_total

def Highest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw1 = price_type
    if _sw1 == PRICE_CLOSE:
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_OPEN:
        if CopyOpen(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_HIGH:
        if CopyHigh(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_LOW:
        if CopyLow(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    else:
        return WRONG_VALUE
    return WRONG_VALUE

def Lowest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw2 = price_type
    if _sw2 == PRICE_CLOSE:
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_OPEN:
        if CopyOpen(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_HIGH:
        if CopyHigh(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_LOW:
        if CopyLow(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    else:
        return WRONG_VALUE
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class POB(_MQL5Indicator):
    name = 'POB'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

