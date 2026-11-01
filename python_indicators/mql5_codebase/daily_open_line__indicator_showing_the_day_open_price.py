"""Daily_Open_Line — converted from MQL5: MQL5 Indicators/Indicator showing the day open price/Daily_Open_Line.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [65535]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DailyOpen'}, 'levels': [], 'description': [], 'name': 'Daily_Open_Line', 'source': 'MQL5 Indicators/Indicator showing the day open price/Daily_Open_Line.mq5', 'folder': 'Indicator showing the day open price', 'inputs': [{'mql': 'InpOpenHour', 'py': 'InpOpenHour', 'param': 'InpOpenHour', 'type': 'uint', 'default': 0, 'label': 'Hour of daily open', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpOpenHour = _input('InpOpenHour', 0)  # Hour of daily open
BufferDailyOpen = Arr(0, 0.0)
open_hour = 0

def OnInit():
    global open_hour
    SetIndexBuffer(0, BufferDailyOpen, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    open_hour = (23 if (InpOpenHour > 23) else InpOpenHour)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(BufferDailyOpen, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferDailyOpen, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        H_Curr = TimeHour_u(time[i])
        H_Prev = TimeHour_u(time[i + 1])
        if H_Curr == WRONG_VALUE or H_Prev == WRONG_VALUE:
            return 0
        if H_Prev == 23:
            H_Prev = -1
        if open_hour > H_Prev and open_hour <= H_Curr:
            BufferDailyOpen[i] = open[i]
        else:
            BufferDailyOpen[i] = BufferDailyOpen[i + 1]
    return rates_total

def TimeHour_u(time):
    tm = MqlDateTime()
    if TimeToStruct(time, tm):
        return tm.hour
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyOpenLine(_MQL5Indicator):
    name = 'Daily_Open_Line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpOpenHour': 0,  # Hour of daily open
    }

