"""HiLo — converted from MQL5: MQL5 Indicators/HiLo/HiLo.mq5

Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'HiLo', 'source': 'MQL5 Indicators/HiLo/HiLo.mq5', 'folder': 'HiLo', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HighLineBuffer = Arr(0, 0.0)
LowLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, HighLineBuffer)
    SetIndexBuffer(1, LowLineBuffer)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Daily High/Low')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'Highest')
    PlotIndexSetString(1, PLOT_LABEL, 'Lowest')
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(start, rates_total):
        if i == 0:
            HighLineBuffer[i] = high[i]
            LowLineBuffer[i] = low[i]
            continue
        current_time = MqlDateTime()
        previous_time = MqlDateTime()
        TimeToStruct(time[i], current_time)
        TimeToStruct(time[i - 1], previous_time)
        if current_time.day == previous_time.day and current_time.mon == previous_time.mon:
            if high[i] >= HighLineBuffer[i - 1]:
                HighLineBuffer[i] = high[i]
            else:
                HighLineBuffer[i] = HighLineBuffer[i - 1]
            if low[i] <= LowLineBuffer[i - 1]:
                LowLineBuffer[i] = low[i]
            else:
                LowLineBuffer[i] = LowLineBuffer[i - 1]
        else:
            HighLineBuffer[i] = high[i]
            LowLineBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HiLo(_MQL5Indicator):
    name = 'HiLo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

