"""Count of candles in interval (histogram) — converted from MQL5: MQL5 Indicators/Count of candles in interval (histogram)/Count of candles in interval (histogram).mq5

Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls', 2: 'Bears'}, 'levels': [], 'description': [], 'name': 'Count of candles in interval (histogram)', 'source': 'MQL5 Indicators/Count of candles in interval (histogram)/Count of candles in interval (histogram).mq5', 'folder': 'Count of candles in interval (histogram)', 'inputs': [{'mql': 'InputRightBar', 'py': 'InputRightBar', 'param': 'InputRightBar', 'type': 'ushort', 'default': 2, 'label': 'The number of the starting bar', 'sinput': False}, {'mql': 'InputLeftBar', 'py': 'InputLeftBar', 'param': 'InputLeftBar', 'type': 'ushort', 'default': 5, 'label': 'The number of the end bar', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InputRightBar = _input('InputRightBar', 2)  # The number of the starting bar
InputLeftBar = _input('InputLeftBar', 5)  # The number of the end bar
ExtBullsBuffer = Arr(0, 0.0)
ExtBearsBuffer = Arr(0, 0.0)
ExtBullsBufferTemp = Arr(0, 0.0)
ExtBearsBufferTemp = Arr(0, 0.0)

def OnInit():
    if InputRightBar == InputLeftBar:
        Print('The starting and ending bars can not be equal')
        return INIT_PARAMETERS_INCORRECT
    if InputRightBar > InputLeftBar:
        Print('The starting bar can not be more than the final bar')
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, ExtBullsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBearsBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtBullsBufferTemp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBearsBufferTemp, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Count (' + IntegerToString(InputLeftBar) + ',' + IntegerToString(InputRightBar) + ')')
    ArraySetAsSeries(ExtBullsBuffer, True)
    ArraySetAsSeries(ExtBearsBuffer, True)
    ArraySetAsSeries(ExtBullsBufferTemp, True)
    ArraySetAsSeries(ExtBearsBufferTemp, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated + 1
    if prev_calculated == 0:
        limit = rates_total - 1
    for i in range(limit, 0 - 1, -1):
        ExtBullsBufferTemp[i] = (1.0 if (open[i] < close[i]) else 0.0)
        ExtBearsBufferTemp[i] = (-1.0 if (open[i] > close[i]) else 0.0)
        limit_left_bar = i + InputLeftBar
        if limit_left_bar >= rates_total:
            ExtBullsBuffer[i] = 0.0
            ExtBearsBuffer[i] = 0.0
        else:
            ExtBearsBuffer[i] = 0.0
            ExtBullsBuffer[i] = ExtBearsBuffer[i]
            for j in range(limit_left_bar, i + InputRightBar - 1, -1):
                ExtBullsBuffer[i] += ExtBullsBufferTemp[j]
                ExtBearsBuffer[i] += ExtBearsBufferTemp[j]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CountOfCandlesInIntervalHistogram(_MQL5Indicator):
    name = 'Count of candles in interval (histogram)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InputRightBar': 2,  # The number of the starting bar
        'InputLeftBar': 5,  # The number of the end bar
    }

