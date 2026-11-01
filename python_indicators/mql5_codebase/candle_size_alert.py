"""Candle_Size_Alert — converted from MQL5: MQL5 Indicators/Marking of candlesticks larger than the specified size/Candle_Size_Alert.mq5

Shows candles with a size that is more than specified and,
if allowed in the settings, then displays an alert
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [65535]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HighSize'}, 'levels': [], 'description': ['Shows candles with a size that is more than specified and,', 'if allowed in the settings, then displays an alert'], 'name': 'Candle_Size_Alert', 'source': 'MQL5 Indicators/Marking of candlesticks larger than the specified size/Candle_Size_Alert.mq5', 'folder': 'Marking of candlesticks larger than the specified size', 'inputs': [{'mql': 'InpLevelSize', 'py': 'InpLevelSize', 'param': 'InpLevelSize', 'type': 'uint', 'default': 20, 'label': 'Size level', 'sinput': False}, {'mql': 'InpOnlyLastBar', 'py': 'InpOnlyLastBar', 'param': 'InpOnlyLastBar', 'type': 'int', 'default': 0, 'label': 'Displays only last bar', 'sinput': False}, {'mql': 'InpEnableAlert', 'py': 'InpEnableAlert', 'param': 'InpEnableAlert', 'type': 'int', 'default': 0, 'label': 'Use alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpLevelSize = _input('InpLevelSize', 20)  # Size level
InpOnlyLastBar = _input('InpOnlyLastBar', INPUT_NO)  # Displays only last bar
InpEnableAlert = _input('InpEnableAlert', INPUT_NO)  # Use alerts
BufferHighSize = Arr(0, 0.0)
level_size_pip = 0.0

def OnInit():
    global level_size_pip
    level_size_pip = InpLevelSize * Point()
    SetIndexBuffer(0, BufferHighSize, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candle size alert')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(BufferHighSize, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 1:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferHighSize, EMPTY_VALUE)
    beg = (0 if InpOnlyLastBar else limit)
    for i in range(beg, 0 - 1, -1):
        if NormalizeDouble(high[i] - low[i] - level_size_pip, Digits()) >= 0:
            if (InpEnableAlert and i == 0) and BufferHighSize[i] == EMPTY_VALUE:
                Alert(Symbol(), ', ', NameTimeframe(), ': Candle size>=', InpLevelSize, ' pips')
            BufferHighSize[i] = high[i]
            if InpOnlyLastBar:
                BufferHighSize[i + 1] = EMPTY_VALUE
        else:
            BufferHighSize[i] = EMPTY_VALUE
    return rates_total

def NameTimeframe():
    _sw1 = Period()
    if _sw1 == 1:
        return 'M1'
    elif _sw1 == 2:
        return 'M2'
    elif _sw1 == 3:
        return 'M3'
    elif _sw1 == 4:
        return 'M4'
    elif _sw1 == 5:
        return 'M5'
    elif _sw1 == 6:
        return 'M6'
    elif _sw1 == 10:
        return 'M10'
    elif _sw1 == 12:
        return 'M12'
    elif _sw1 == 15:
        return 'M15'
    elif _sw1 == 20:
        return 'M20'
    elif _sw1 == 30:
        return 'M30'
    elif _sw1 == 16385:
        return 'H1'
    elif _sw1 == 16386:
        return 'H2'
    elif _sw1 == 16387:
        return 'H3'
    elif _sw1 == 16388:
        return 'H4'
    elif _sw1 == 16390:
        return 'H6'
    elif _sw1 == 16392:
        return 'H8'
    elif _sw1 == 16396:
        return 'H12'
    elif _sw1 == 16408:
        return 'D1'
    elif _sw1 == 32769:
        return 'W1'
    elif _sw1 == 49153:
        return 'MN1'
    else:
        return 'Unknown Period'


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleSizeAlert(_MQL5Indicator):
    name = 'Candle_Size_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLevelSize': 20,  # Size level
        'InpOnlyLastBar': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Displays only last bar
        'InpEnableAlert': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use alerts
    }

