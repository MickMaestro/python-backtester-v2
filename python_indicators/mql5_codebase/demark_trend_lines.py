"""DeMark Trend Lines — converted from MQL5: MQL5 Indicators/Demark Trendlines/DeMark Trend Lines.mq5

Copyright: GreenDog; Link: krot@inbox.ru

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'GreenDog', 'link': 'krot@inbox.ru', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'DeMark Trend Lines', 'source': 'MQL5 Indicators/Demark Trendlines/DeMark Trend Lines.mq5', 'folder': 'Demark Trendlines', 'inputs': [{'mql': 'LevDP', 'py': 'LevDP', 'param': 'LevDP', 'type': 'int', 'default': 2, 'label': 'Fractal Period or Levels Demar Pint', 'sinput': False}, {'mql': 'qSteps', 'py': 'qSteps', 'param': 'qSteps', 'type': 'int', 'default': 1, 'label': 'Number  Trendlines per UpTrend or DownTrend', 'sinput': False}, {'mql': 'BackStep', 'py': 'BackStep', 'param': 'BackStep', 'type': 'int', 'default': 0, 'label': 'Number of Steps Back', 'sinput': False}, {'mql': 'showBars', 'py': 'showBars', 'param': 'showBars', 'type': 'int', 'default': 500, 'label': 'Bars Back To Draw', 'sinput': False}, {'mql': 'ArrowCode', 'py': 'ArrowCode', 'param': 'ArrowCode', 'type': 'int', 'default': 159, 'label': '', 'sinput': False}, {'mql': 'UpTrendColor', 'py': 'UpTrendColor', 'param': None, 'type': 'color', 'default': 9109504, 'label': '', 'sinput': False}, {'mql': 'DownTrendColor', 'py': 'DownTrendColor', 'param': None, 'type': 'color', 'default': 2237106, 'label': '', 'sinput': False}, {'mql': 'TrendlineWidth', 'py': 'TrendlineWidth', 'param': 'TrendlineWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'TrendlineStyle', 'py': 'TrendlineStyle', 'param': 'TrendlineStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'TrendLINE', 'label': 'Indicator unique ID', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LevDP = _input('LevDP', 2)  # Fractal Period or Levels Demar Pint
qSteps = _input('qSteps', 1)  # Number  Trendlines per UpTrend or DownTrend
BackStep = _input('BackStep', 0)  # Number of Steps Back
showBars = _input('showBars', 500)  # Bars Back To Draw
ArrowCode = _input('ArrowCode', 159)
UpTrendColor = _input('UpTrendColor', clrDarkBlue)
DownTrendColor = _input('DownTrendColor', clrFireBrick)
TrendlineWidth = _input('TrendlineWidth', 1)
TrendlineStyle = _input('TrendlineStyle', STYLE_SOLID)
UniqueID = _input('UniqueID', 'TrendLINE')  # Indicator unique ID
Buf1 = Arr(0, 0.0)
Fractal1 = Arr(0, 0.0)
Buf2 = Arr(0, 0.0)
Fractal2 = Arr(0, 0.0)
_showBars = showBars

def OnInit():
    SetIndexBuffer(0, Fractal1, INDICATOR_DATA)
    ArraySetAsSeries(Fractal1, True)
    SetIndexBuffer(1, Fractal2, INDICATOR_DATA)
    ArraySetAsSeries(Fractal2, True)
    SetIndexBuffer(2, Buf1, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Buf1, True)
    SetIndexBuffer(3, Buf2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Buf2, True)
    PlotIndexSetInteger(0, PLOT_ARROW, ArrowCode)
    PlotIndexSetInteger(1, PLOT_ARROW, ArrowCode)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, UniqueID)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevTime, _showBars
    ArrayInitialize(Buf1, 0.0)
    ArrayInitialize(Buf2, 0.0)
    if _s_OnCalculate_prevTime != iTime(Symbol(), PERIOD_CURRENT, 0):
        cnt = 0
        if _showBars == 0 or _showBars > (rates_total - 1):
            _showBars = MathMin(MathMax(rates_total - prev_calculated, LevDP), rates_total - 1)
        cnt = _showBars
        for cnt in range(cnt, LevDP, -1):
            Buf1[cnt] = DemHigh(cnt, LevDP)
            Buf2[cnt] = DemLow(cnt, LevDP)
            Fractal1[cnt] = Buf1[cnt]
            Fractal2[cnt] = Buf2[cnt]
        else:
            cnt = _range_end(cnt, LevDP, -1)
        cnt = 1
        for cnt in range(cnt, qSteps + 1):
            TDMain(cnt)
        else:
            cnt = _range_end(cnt, qSteps + 1, 1)
        _s_OnCalculate_prevTime = iTime(Symbol(), PERIOD_CURRENT, 0)
    return rates_total

def TDMain(Step):
    H1 = 0
    H2 = 0
    L1 = 0
    L2 = 0
    Rem = ""
    H1 = GetTD(Step + BackStep, Buf1)
    H2 = GetNextHighTD(H1)
    if H1 < 0 or H2 < 0:
        Print('Demark: Not enough bars on the chart for construction')
    else:
        Rem = UniqueID + ' Down ' + IntegerToString(Step)
        ObjectDelete(0, Rem)
        ObjectCreate(0, Rem, OBJ_TREND, 0, iTime(Symbol(), Period(), H2), iHigh(Symbol(), Period(), H2), iTime(Symbol(), Period(), H1), iHigh(Symbol(), Period(), H1))
        ObjectSetInteger(0, Rem, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, Rem, OBJPROP_COLOR, DownTrendColor)
        ObjectSetInteger(0, Rem, OBJPROP_WIDTH, TrendlineWidth)
        ObjectSetInteger(0, Rem, OBJPROP_STYLE, TrendlineStyle)
    L1 = GetTD(Step + BackStep, Buf2)
    L2 = GetNextLowTD(L1)
    if L1 < 0 or L2 < 0:
        Print('Demark: Not enough bars on the chart for construction')
    else:
        Rem = UniqueID + ' Up ' + IntegerToString(Step)
        ObjectDelete(0, Rem)
        ObjectCreate(0, Rem, OBJ_TREND, 0, iTime(Symbol(), Period(), L2), iLow(Symbol(), Period(), L2), iTime(Symbol(), Period(), L1), iLow(Symbol(), Period(), L1))
        ObjectSetInteger(0, Rem, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, Rem, OBJPROP_COLOR, UpTrendColor)
        ObjectSetInteger(0, Rem, OBJPROP_WIDTH, TrendlineWidth)
        ObjectSetInteger(0, Rem, OBJPROP_STYLE, TrendlineStyle)
    return 0

def GetTD(P, Arr_):
    i = 0
    j = 0
    while j < P:
        i += 1
        while Arr_[i] == 0:
            i += 1
            if i > (_showBars - 2):
                return -1
        j += 1
    return i

def GetNextHighTD(P):
    i = P + 1
    while Buf1[i] <= iHigh(Symbol(), Period(), P):
        i += 1
        if i > (_showBars - 2):
            return -1
    return i

def GetNextLowTD(P):
    i = P + 1
    while Buf2[i] >= iLow(Symbol(), Period(), P) or Buf2[i] == 0:
        i += 1
        if i > (_showBars - 2):
            return -1
    return i

def DemHigh(cnt, sh):
    if iHigh(Symbol(), Period(), cnt) >= iHigh(Symbol(), Period(), cnt + sh) and iHigh(Symbol(), Period(), cnt) > iHigh(Symbol(), Period(), cnt - sh):
        if sh > 1:
            return DemHigh(cnt, sh - 1)
        else:
            return iHigh(Symbol(), Period(), cnt)
    else:
        return 0.0

def DemLow(cnt, sh):
    if iLow(Symbol(), Period(), cnt) <= iLow(Symbol(), Period(), cnt + sh) and iLow(Symbol(), Period(), cnt) < iLow(Symbol(), Period(), cnt - sh):
        if sh > 1:
            return DemLow(cnt, sh - 1)
        else:
            return iLow(Symbol(), Period(), cnt)
    else:
        return 0.0

# ---- static local variables
_s_OnCalculate_prevTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeMarkTrendLines(_MQL5Indicator):
    name = 'DeMark Trend Lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'LevDP': 2,  # Fractal Period or Levels Demar Pint
        'qSteps': 1,  # Number  Trendlines per UpTrend or DownTrend
        'BackStep': 0,  # Number of Steps Back
        'showBars': 500,  # Bars Back To Draw
        'ArrowCode': 159,
        'TrendlineWidth': 1,
        'TrendlineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
    }

