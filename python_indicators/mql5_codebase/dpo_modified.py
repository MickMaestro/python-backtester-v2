"""DPO_modified — converted from MQL5: MQL5 Indicators/DPO - MA modified/DPO_modified.mq5

Detrended Price Oscillator - modified
Copyright: Copyright 2000-2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2000-2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [0.0], 'description': ['Detrended Price Oscillator - modified'], 'name': 'DPO_modified', 'source': 'MQL5 Indicators/DPO - MA modified/DPO_modified.mq5', 'folder': 'DPO - MA modified', 'inputs': [{'mql': 'InpDetrendPeriod', 'py': 'InpDetrendPeriod', 'param': 'InpDetrendPeriod', 'type': 'int', 'default': 61, 'label': 'DPO Period', 'sinput': False}, {'mql': 'MAmethod', 'py': 'MAmethod', 'param': 'MAmethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'appliedprice', 'py': 'appliedprice', 'param': 'appliedprice', 'type': 'int', 'default': 1, 'label': 'MA Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpDetrendPeriod = _input('InpDetrendPeriod', 61)  # DPO Period
MAmethod = _input('MAmethod', MODE_SMA)  # MA Method
appliedprice = _input('appliedprice', PRICE_CLOSE)  # MA Applied price
ExtDPOBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
Extprice = Arr(0, 0.0)
helpMABuffer = 0
ExtMAPeriod = 0

def OnInit():
    global ExtMAPeriod
    ExtMAPeriod = InpDetrendPeriod
    SetIndexBuffer(0, ExtDPOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, Extprice, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtMAPeriod - 1)
    short_name = StringFormat('modified DPO(%d)', InpDetrendPeriod)
    _sw1 = MAmethod
    if _sw1 == MODE_EMA:
        short_name = short_name + ' (EMA)'
    elif _sw1 == MODE_LWMA:
        short_name = short_name + ' (LWMA)'
    elif _sw1 == MODE_SMA:
        short_name = short_name + ' (SMA)'
    elif _sw1 == MODE_SMMA:
        short_name = short_name + ' (SMMA)'
    else:
        short_name = short_name
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    begin = 0
    first_index = begin + ExtMAPeriod - 1
    if prev_calculated < first_index:
        ArrayInitialize(ExtDPOBuffer, 0.0)
        start = first_index
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, first_index)
    else:
        start = prev_calculated - 1
    if appliedprice >= 4:
        getLprice(rates_total, prev_calculated, begin, open, high, low, close, Extprice, appliedprice)
    _sw2 = appliedprice
    if _sw2 == PRICE_CLOSE:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, close, ExtMABuffer)
    elif _sw2 == PRICE_OPEN:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, open, ExtMABuffer)
    elif _sw2 == PRICE_HIGH:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, high, ExtMABuffer)
    elif _sw2 == PRICE_LOW:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, low, ExtMABuffer)
    elif _sw2 == PRICE_MEDIAN:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, Extprice, ExtMABuffer)
    elif _sw2 == PRICE_TYPICAL:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, Extprice, ExtMABuffer)
    elif _sw2 == PRICE_WEIGHTED:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, Extprice, ExtMABuffer)
    else:
        AverageOnArray(MAmethod, rates_total, prev_calculated, begin, ExtMAPeriod, close, ExtMABuffer)
    for i in range(start, rates_total):
        ExtDPOBuffer[i] = close[i] - ExtMABuffer[i]
    return rates_total

def AverageOnArray(mode, rates_total, prev_calculated, begin, period, source, destination):
    _sw3 = mode
    if _sw3 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)
    elif _sw3 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)
    elif _sw3 == MODE_LWMA:
        LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, begin, period, source, destination)
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)

def getLprice(rates_total, prev_calculated, begin, op, hi, lo, cl, destination, Lprice):
    as_series_destination = ArrayGetAsSeries(destination)
    ArraySetAsSeries(destination, False)
    start_position = prev_calculated - 1
    if start_position < 0:
        start_position = 0
    for i in range(start_position, rates_total):
        if Lprice == PRICE_WEIGHTED:
            destination[i] = (hi[i] + lo[i] + (cl[i] * 2)) / 4
        if Lprice == PRICE_TYPICAL:
            destination[i] = (hi[i] + lo[i] + cl[i]) / 3
        if Lprice == PRICE_MEDIAN:
            destination[i] = (hi[i] + lo[i]) / 2
    ArraySetAsSeries(destination, as_series_destination)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DPOModified(_MQL5Indicator):
    name = 'DPO_modified'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDetrendPeriod': 61,  # DPO Period
        'MAmethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'appliedprice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Applied price
    }

