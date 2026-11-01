"""Percentage_Crossover_Channel — converted from MQL5: MQL5 Indicators/Channel at a percentage value of level breakout/Percentage_Crossover_Channel.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [5737262]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper', 2: 'Middle', 3: 'Lower'}, 'levels': [], 'description': [], 'name': 'Percentage_Crossover_Channel', 'source': 'MQL5 Indicators/Channel at a percentage value of level breakout/Percentage_Crossover_Channel.mq5', 'folder': 'Channel at a percentage value of level breakout', 'inputs': [{'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'double', 'default': 100.0, 'label': 'Percent', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPercent = _input('InpPercent', 100.0)  # Percent
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Applied price
BufferUpper = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
percent = 0.0
plus_value = 0.0
minus_value = 0.0
handle_ma = 0

def OnInit():
    global handle_ma, minus_value, percent, plus_value
    percent = (0.001 if (InpPercent <= 0) else InpPercent) / 100
    plus_value = 1 + (percent / 100)
    minus_value = 1 - (percent / 100)
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpPrice)
    if handle_ma == INVALID_HANDLE:
        Print('Error creating MA handle')
        return INIT_FAILED
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Percentage Crossover Channel')
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferSMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferSMA, EMPTY_VALUE)
        copied = CopyBuffer(handle_ma, 0, 0, rates_total, BufferSMA)
        if copied != rates_total:
            return 0
    for i in range(limit, 0 - 1, -1):
        total = (1 if (limit == 0) else limit)
        copied = CopyBuffer(handle_ma, 0, 0, total, BufferSMA)
        if copied != total:
            return 0
        price = BufferSMA[i]
        if limit > 1 and i == limit:
            BufferMiddle[i] = price
        else:
            BufferMiddle[i] = ((price * minus_value) if ((price * minus_value) > BufferMiddle[i + 1]) else (price * plus_value) if ((price * plus_value) < BufferMiddle[i + 1]) else BufferMiddle[i + 1])
        BufferUpper[i] = BufferMiddle[i] * plus_value
        BufferLower[i] = BufferMiddle[i] * minus_value
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PercentageCrossoverChannel(_MQL5Indicator):
    name = 'Percentage_Crossover_Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPercent': 100.0,  # Percent
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

