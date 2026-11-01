"""Ranging Market Detector — converted from MQL5: MQL5 Indicators/Ranging Market Detector/Ranging Market Detector.mq5

Copyright: Copyright phade 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright phade 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Ranging Market Detector', 'source': 'MQL5 Indicators/Ranging Market Detector/Ranging Market Detector.mq5', 'folder': 'Ranging Market Detector', 'inputs': [{'mql': 'chart_mode', 'py': 'chart_mode', 'param': 'chart_mode', 'type': 'int', 'default': 0, 'label': 'Chart Mode', 'sinput': False}, {'mql': 'dynamic_detection', 'py': 'dynamic_detection', 'param': 'dynamic_detection', 'type': 'bool', 'default': True, 'label': 'Use ATR for range detection', 'sinput': False}, {'mql': 'pointThreshold', 'py': 'pointThreshold', 'param': 'pointThreshold', 'type': 'int', 'default': 60, 'label': 'Point threshold if not using dynamic detection', 'sinput': False}, {'mql': 'atr_period', 'py': 'atr_period', 'param': 'atr_period', 'type': 'int', 'default': 20, 'label': 'ATR period', 'sinput': False}, {'mql': 'atr_multiplier', 'py': 'atr_multiplier', 'param': 'atr_multiplier', 'type': 'double', 'default': 0.5, 'label': 'ATR multiplier', 'sinput': False}, {'mql': 'backstep', 'py': 'backstep', 'param': 'backstep', 'type': 'int', 'default': 1, 'label': 'Box backstep', 'sinput': False}, {'mql': 'bar_lookback', 'py': 'bar_lookback', 'param': 'bar_lookback', 'type': 'int', 'default': 200, 'label': 'Lookback', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
consolidation_trend = Arr(0, 0.0)
atr = Arr(0, 0.0)
High = Arr(0, 0.0)
Low = Arr(0, 0.0)
buf_open = Arr(0, 0.0)
buf_high = Arr(0, 0.0)
buf_low = Arr(0, 0.0)
buf_close = Arr(0, 0.0)
buf_color = Arr(0, 0.0)
chart_mode = _input('chart_mode', CHART_BARS)  # Chart Mode
dynamic_detection = _input('dynamic_detection', True)  # Use ATR for range detection
pointThreshold = _input('pointThreshold', 60)  # Point threshold if not using dynamic detection
atr_period = _input('atr_period', 20)  # ATR period
atr_multiplier = _input('atr_multiplier', 0.5)  # ATR multiplier
backstep = _input('backstep', 1)  # Box backstep
bar_lookback = _input('bar_lookback', 200)  # Lookback
handle = INVALID_HANDLE
obj_name = ""
line_chart_col = clrNONE  # Line chart color

def OnInit():
    global handle
    SetIndexBuffer(0, buf_open, INDICATOR_DATA)
    SetIndexBuffer(1, buf_high, INDICATOR_DATA)
    SetIndexBuffer(2, buf_low, INDICATOR_DATA)
    SetIndexBuffer(3, buf_close, INDICATOR_DATA)
    SetIndexBuffer(4, buf_color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, consolidation_trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, High, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, Low, INDICATOR_CALCULATIONS)
    if chart_mode == CHART_BARS:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_BARS)
        ChartSetInteger(0, CHART_MODE, CHART_LINE)
        ChartSetInteger(0, CHART_COLOR_CHART_LINE, line_chart_col)
    if chart_mode == CHART_CANDLES:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
        ChartSetInteger(0, CHART_MODE, CHART_LINE)
        ChartSetInteger(0, CHART_COLOR_CHART_LINE, line_chart_col)
    if chart_mode == CHART_LINE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
        ChartSetInteger(0, CHART_MODE, CHART_LINE)
        ChartSetInteger(0, CHART_COLOR_CHART_LINE, line_chart_col)
        ChartSetInteger(0, CHART_COLOR_CHART_UP, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CHART_DOWN, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, clrNONE)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, clrDarkSlateGray)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clrSeaGreen)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, clrCrimson)
    ChartNavigate(0, CHART_END)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Market Range Detector')
    handle = iATR(Symbol(), 0, atr_period)
    return INIT_SUCCEEDED

def ZoneMark(startidx, endidx, time, high, low):
    global obj_name
    obj_name = 'ConsolidationZone_' + IntegerToString(startidx) + '_' + IntegerToString(endidx)
    if ObjectFind(0, obj_name) < 0:
        if not ObjectCreate(0, obj_name, OBJ_RECTANGLE, 0, time[startidx], high[startidx], time[endidx], low[endidx]):
            Print('ZoneMark', ': failed to create a rectangle! Error code = ', GetLastError())
            return
    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, clrGray)
    ObjectSetInteger(0, obj_name, OBJPROP_STYLE, STYLE_DASH)
    ObjectSetInteger(0, obj_name, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, obj_name, OBJPROP_FILL, True)
    ObjectSetInteger(0, obj_name, OBJPROP_BACK, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < atr_period:
        return rates_total
    recalculationPoint = bar_lookback
    if CopyBuffer(handle, 0, 0, recalculationPoint + 1, atr) < 0:
        Print('Failed to copy ATR values!')
        return rates_total
    in_consolidation = False
    startidx = -1
    endidx = -1
    start = rates_total - recalculationPoint
    for i in range(start, rates_total):
        buf_open[i] = open[i]
        buf_high[i] = high[i]
        buf_low[i] = low[i]
        buf_close[i] = close[i]
        High[i] = high[i]
        Low[i] = low[i]
        for j in range(1, backstep + 1):
            if high[i - j] > high[i]:
                High[i] = high[i - j]
            elif low[i - j] < low[i]:
                Low[i] = low[i - j]
        weak_change = False
        if dynamic_detection:
            weak_change = fabs(close[i] - close[i - 1]) < (atr[i] * atr_multiplier)
        else:
            weak_change = _fdiv(fabs(close[i] - close[i - 1]), Point()) < pointThreshold
        if weak_change:
            buf_color[i] = 0.0
            consolidation_trend[i] = 1.0
            if not in_consolidation:
                in_consolidation = True
                startidx = i
                ZoneMark(i, i, time, buf_high, buf_low)
            else:
                endidx = i
                if ObjectFind(0, obj_name) >= 0:
                    ObjectMove(0, obj_name, 1, time[endidx], low[endidx])
        else:
            if close[i] > open[i]:
                buf_color[i] = 1.0
            elif close[i] < open[i]:
                buf_color[i] = 2.0
            consolidation_trend[i] = 0.0
            if in_consolidation:
                in_consolidation = False
                endidx = i - 1
                if ObjectFind(0, obj_name) >= 0:
                    ObjectMove(0, obj_name, 1, time[endidx], low[endidx])
    RemoveHistoricObjects(rates_total - recalculationPoint, time)
    return rates_total

def RemoveHistoricObjects(shift, time):
    recalculationTime = time[shift]
    totalObjects = ObjectsTotal(0)
    for i in range(totalObjects - 1, 0 - 1, -1):
        objName = ObjectName(0, i)
        if StringFind(objName, 'ConsolidationZone_') != -1:
            objTime = ObjectGetInteger(0, objName, OBJPROP_TIME)
            if objTime < recalculationTime:
                ObjectDelete(0, objName)

def OnDeinit(reason):
    ChartSetInteger(0, CHART_MODE, CHART_CANDLES)
    ObjectsDeleteAll(0, 'ConsolidationZone_')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangingMarketDetector(_MQL5Indicator):
    name = 'Ranging Market Detector'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'chart_mode': _Choice({0: 'CHART_BARS', 1: 'CHART_CANDLES', 2: 'CHART_LINE'}, default=0),  # Chart Mode
        'dynamic_detection': True,  # Use ATR for range detection
        'pointThreshold': 60,  # Point threshold if not using dynamic detection
        'atr_period': 20,  # ATR period
        'atr_multiplier': 0.5,  # ATR multiplier
        'backstep': 1,  # Box backstep
        'bar_lookback': 200,  # Lookback
    }

