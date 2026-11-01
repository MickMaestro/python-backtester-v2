"""Trend_Angle — converted from MQL5: MQL5 Indicators/Trend_Angle/Trend_Angle.mq5

Trend Angle indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TA'}, 'levels': [], 'description': ['Trend Angle indicator'], 'name': 'Trend_Angle', 'source': 'MQL5 Indicators/Trend_Angle/Trend_Angle.mq5', 'folder': 'Trend_Angle', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpLineColor', 'py': 'InpLineColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Line color', 'sinput': False}, {'mql': 'InpLineWidth', 'py': 'InpLineWidth', 'param': 'InpLineWidth', 'type': 'uint', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'InpLineStyle', 'py': 'InpLineStyle', 'param': 'InpLineStyle', 'type': 'int', 'default': 2, 'label': 'Line style', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'uchar', 'default': 10, 'label': 'Font size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # MA period
InpMethod = _input('InpMethod', MODE_EMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpLineColor = _input('InpLineColor', clrDodgerBlue)  # Line color
InpLineWidth = _input('InpLineWidth', 1)  # Line width
InpLineStyle = _input('InpLineStyle', STYLE_DOT)  # Line style
InpFontSize = _input('InpFontSize', 10)  # Font size
BufferTA = Arr(0, 0.0)
prefix = ""
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, prefix
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferTA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Angle (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    if rates_total <= (period_ma * 2):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferTA, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferTA)
    if copied != count:
        return 0
    nm = prefix + 'line'
    p1 = 0.0
    p0 = 0.0
    t1 = 0
    t0 = 0
    p1 = BufferTA[1]
    p0 = BufferTA[0]
    t1 = time[1]
    t0 = time[0]
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_TREND, 0, t1, p1, t0, p0)
        ObjectSetInteger(0, nm, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, nm, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, nm, OBJPROP_WIDTH, InpLineWidth)
        ObjectSetInteger(0, nm, OBJPROP_STYLE, InpLineStyle)
        ObjectSetInteger(0, nm, OBJPROP_COLOR, InpLineColor)
    else:
        if ObjectGetInteger(0, nm, OBJPROP_TIME, 0) != t1:
            ObjectSetInteger(0, nm, OBJPROP_TIME, 0, t1)
        if ObjectGetInteger(0, nm, OBJPROP_TIME, 1) != t0:
            ObjectSetInteger(0, nm, OBJPROP_TIME, 1, t0)
        if ObjectGetDouble(0, nm, OBJPROP_PRICE, 0) != p1:
            ObjectSetDouble(0, nm, OBJPROP_PRICE, 0, p1)
        if ObjectGetDouble(0, nm, OBJPROP_PRICE, 1) != p0:
            ObjectSetDouble(0, nm, OBJPROP_PRICE, 1, p0)
    angle = 0.0
    angle_str = ""
    x1 = Box(0)
    x2 = Box(0)
    y1 = Box(0)
    y2 = Box(0)
    ChartTimePriceToXY(0, 0, time[10], (10.0 * p1) - (9.0 * p0), x1, y1)
    ChartTimePriceToXY(0, 0, t0, p0, x2, y2)
    diff = float(y2.v - y1.v)
    angle = 90 - ((atan(_fdiv(x1.v - x2.v, (diff if (diff != 0) else DBL_MIN))) * 180.0) / M_PI)
    angle_str = DoubleToString(angle, 2)
    nm = prefix + 'label'
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_TEXT, 0, t0, p0)
        ObjectSetInteger(0, nm, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)
        ObjectSetString(0, nm, OBJPROP_FONT, 'Calibri')
        ObjectSetInteger(0, nm, OBJPROP_FONTSIZE, InpFontSize)
        ObjectSetInteger(0, nm, OBJPROP_COLOR, InpLineColor)
    else:
        if ObjectGetInteger(0, nm, OBJPROP_TIME, 0) != t0:
            ObjectSetInteger(0, nm, OBJPROP_TIME, 0, t0)
        if ObjectGetDouble(0, nm, OBJPROP_PRICE, 0) != p0:
            ObjectSetDouble(0, nm, OBJPROP_PRICE, 0, p0)
    ObjectSetString(0, nm, OBJPROP_TEXT, angle_str)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendAngle(_MQL5Indicator):
    name = 'Trend_Angle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpLineWidth': 1,  # Line width
        'InpLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Line style
        'InpFontSize': 10,  # Font size
    }

