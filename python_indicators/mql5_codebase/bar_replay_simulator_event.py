"""Bar_Replay_Simulator_Event — converted from MQL5: MQL5 Indicators/Manual Backtest Bar Replay Simulator/Bar_Replay_Simulator_Event.mq5

Copyright: Copyright 2025, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'Bar_Replay_Simulator_Event', 'source': 'MQL5 Indicators/Manual Backtest Bar Replay Simulator/Bar_Replay_Simulator_Event.mq5', 'folder': 'Manual Backtest Bar Replay Simulator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Color_Bar_Up_1 = 0
Color_Bar_Down_1 = 0
Color_Bar_Up_0 = 0
Color_Bar_Down_0 = 0
buf_open = Arr(0, 0.0)  # Buffers for data
buf_high = Arr(0, 0.0)  # Buffers for data
buf_low = Arr(0, 0.0)  # Buffers for data
buf_close = Arr(0, 0.0)  # Buffers for data
buf_color_line = Arr(0, 0.0)  # Buffer for color indexes
vl_time = 0
vl_name = 'VL'

def OnInit():
    global Color_Bar_Down_0, Color_Bar_Down_1, Color_Bar_Up_0, Color_Bar_Up_1
    ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, True)
    ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, True)
    Color_Bar_Up_1 = ChartBearColorGet(0)
    Color_Bar_Down_1 = ChartBackColorGet(0)
    Color_Bar_Up_0 = ChartBullColorGet(0)
    Color_Bar_Down_0 = ChartBackColorGet(0)
    SetIndexBuffer(0, buf_open, INDICATOR_DATA)
    SetIndexBuffer(1, buf_high, INDICATOR_DATA)
    SetIndexBuffer(2, buf_low, INDICATOR_DATA)
    SetIndexBuffer(3, buf_close, INDICATOR_DATA)
    SetIndexBuffer(4, buf_color_line, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 4)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Color_Bar_Up_0)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Color_Bar_Down_0)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, Color_Bar_Up_1)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 3, Color_Bar_Down_1)
    UpdateBuffers()
    return INIT_SUCCEEDED

def OnChartEvent(id_, lparam, dparam, sparam):
    global vl_time
    if id_ == CHARTEVENT_OBJECT_DRAG and sparam == vl_name:
        UpdateBuffers()
    if id_ == CHARTEVENT_KEYDOWN and lparam == 0x11:
        Print('ctrl')
        vl_time = ObjectGetInteger(0, vl_name, OBJPROP_TIME)
        current_bar_shift = iBarShift(Symbol(), Period(), vl_time)
        new_bar_shift = current_bar_shift - 1
        if new_bar_shift < 0:
            Print('Cannot shift beyond the first bar!')
            return
        new_time = iTime(Symbol(), Period(), new_bar_shift)
        ObjectSetInteger(0, vl_name, OBJPROP_TIME, new_time)
        UpdateBuffers()

def UpdateBuffers():
    global vl_time
    rates_total = Bars(Symbol(), Period())
    time = Arr(0, 0)
    open = Arr(0, 0.0)
    high = Arr(0, 0.0)
    low = Arr(0, 0.0)
    close = Arr(0, 0.0)
    copied_time = CopyTime(Symbol(), Period(), 0, rates_total, time)
    copied_open = CopyOpen(Symbol(), Period(), 0, rates_total, open)
    copied_high = CopyHigh(Symbol(), Period(), 0, rates_total, high)
    copied_low = CopyLow(Symbol(), Period(), 0, rates_total, low)
    copied_close = CopyClose(Symbol(), Period(), 0, rates_total, close)
    if ((((copied_time != rates_total or copied_open != rates_total) or copied_high != rates_total) or copied_low != rates_total) or copied_close != rates_total) or ObjectFind(0, vl_name) == -1:
        return
    vl_time = ObjectGetInteger(0, vl_name, OBJPROP_TIME)
    buffer_size = ArraySize(buf_open)
    i = 0
    while i < buffer_size and i < rates_total:
        buf_open[i] = open[i]
        buf_high[i] = high[i]
        buf_low[i] = low[i]
        buf_close[i] = close[i]
        candle_time = time[i]
        if candle_time > vl_time:
            buf_color_line[i] = (3 if (open[i] >= close[i]) else 1)
        else:
            buf_color_line[i] = (2 if (open[i] >= close[i]) else 0)
        i += 1
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def ChartBackColorGet(chart_ID=0):
    result = Box(clrNONE)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_COLOR_BACKGROUND, 0, result):
        Print('ChartBackColorGet' + ', Error Code = ', GetLastError())
    return _uint(result.v)

def ChartBullColorGet(chart_ID=0):
    result = Box(clrNONE)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_COLOR_CANDLE_BULL, 0, result):
        Print('ChartBullColorGet' + ', Error Code = ', GetLastError())
    return _uint(result.v)

def ChartBearColorGet(chart_ID=0):
    result = Box(clrNONE)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_COLOR_CANDLE_BEAR, 0, result):
        Print('ChartBearColorGet' + ', Error Code = ', GetLastError())
    return _uint(result.v)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BarReplaySimulatorEvent(_MQL5Indicator):
    name = 'Bar_Replay_Simulator_Event'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

