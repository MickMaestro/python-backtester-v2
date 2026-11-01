"""YABSI — converted from MQL5: MQL5 Indicators/YABSI/YABSI.mq5

YABSI Buy/Sell indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Sell signal', 2: 'Buy signal', 3: 'Typical price'}, 'levels': [], 'description': ['YABSI Buy/Sell indicator'], 'name': 'YABSI', 'source': 'MQL5 Indicators/YABSI/YABSI.mq5', 'folder': 'YABSI', 'inputs': [{'mql': 'InpShowMA', 'py': 'InpShowMA', 'param': 'InpShowMA', 'type': 'int', 'default': 0, 'label': 'Show price typical', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpShowMA = _input('InpShowMA', INPUT_NO)  # Show price typical
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferSwitch = Arr(0, 0.0)
handle_ma = 0

def OnInit():
    global handle_ma
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSwitch, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'YABSI Buy/Sell')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if InpShowMA:
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(2, PLOT_SHOW_DATA, True)
    else:
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferSwitch, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_TYPICAL)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_TYPICAL object was not created: Error ', GetLastError())
        return INIT_FAILED
    ChartRedraw()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 4
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferSwitch, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferUP[i] = EMPTY_VALUE
        BufferDN[i] = BufferUP[i]
        BufferSwitch[i] = BufferSwitch[i + 1]
        if (close[i + 1] < high[i] and BufferMA[i + 2] < close[i + 1]) or BufferMA[i + 3] < close[i + 1]:
            if BufferSwitch[i] != 1:
                BufferUP[i] = open[i]
                BufferSwitch[i] = 1.0
        if (close[i + 1] > low[i] and BufferMA[i + 2] > close[i + 1]) or BufferMA[i + 3] > close[i + 1]:
            if BufferSwitch[i] != -1:
                BufferDN[i] = open[i]
                BufferSwitch[i] = -1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YABSI(_MQL5Indicator):
    name = 'YABSI'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpShowMA': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show price typical
    }

