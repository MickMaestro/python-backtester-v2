"""nxbreakout — converted from MQL5: MQL5 Indicators/NxBreakout/nxbreakout.mq5

Copyright: Copyright © 2005, Bill Sica; Link: http://www.tetsuyama.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Bill Sica', 'link': 'http://www.tetsuyama.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'nxbreakout', 'source': 'MQL5 Indicators/NxBreakout/nxbreakout.mq5', 'folder': 'NxBreakout', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': 'Chart period', 'sinput': False}, {'mql': 'StartBar', 'py': 'StartBar', 'param': 'StartBar', 'type': 'uint', 'default': 1, 'label': 'Starting bar for analysis', 'sinput': False}, {'mql': 'HowManyBars', 'py': 'HowManyBars', 'param': 'HowManyBars', 'type': 'uint', 'default': 5, 'label': 'Number of bars for analysis', 'sinput': False}, {'mql': 'Color_R', 'py': 'Color_R', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Color of the resistance level', 'sinput': False}, {'mql': 'Style_R', 'py': 'Style_R', 'param': 'Style_R', 'type': 'int', 'default': 0, 'label': 'Line style of the resistance level', 'sinput': False}, {'mql': 'Width_R', 'py': 'Width_R', 'param': 'Width_R', 'type': 'int', 'default': 2, 'label': 'Width of the resistance level line', 'sinput': False}, {'mql': 'Color_S', 'py': 'Color_S', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color of the support level', 'sinput': False}, {'mql': 'Style_S', 'py': 'Style_S', 'param': 'Style_S', 'type': 'int', 'default': 0, 'label': 'Line style of the support level', 'sinput': False}, {'mql': 'Width_S', 'py': 'Width_S', 'param': 'Width_S', 'type': 'int', 'default': 2, 'label': 'Width of the support level line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_D1)  # Chart period
StartBar = _input('StartBar', 1)  # Starting bar for analysis
HowManyBars = _input('HowManyBars', 5)  # Number of bars for analysis
Color_R = _input('Color_R', clrMediumSeaGreen)  # Color of the resistance level
Style_R = _input('Style_R', SOLID_)  # Line style of the resistance level
Width_R = _input('Width_R', Width_2)  # Width of the resistance level line
Color_S = _input('Color_S', clrRed)  # Color of the support level
Style_S = _input('Style_S', SOLID_)  # Line style of the support level
Width_S = _input('Width_S', Width_2)  # Width of the support level line

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)

def OnInit():
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Chart period for the NxBreakout indicator cannot be less than the current chart period')
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'NxBreakout( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'R_Line')
    ObjectDelete(0, 'S_Line')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), TimeFrame) < _int(StartBar + HowManyBars):
        return 0
    iHigh_ = Arr(0, 0.0)
    iLow_ = Arr(0, 0.0)
    ArraySetAsSeries(iHigh_, True)
    ArraySetAsSeries(iLow_, True)
    if CopyHigh(Symbol(), TimeFrame, StartBar, HowManyBars, iHigh_) < _int(HowManyBars):
        return 0
    if CopyLow(Symbol(), TimeFrame, StartBar, HowManyBars, iLow_) < _int(HowManyBars):
        return 0
    HH = NormalizeDouble(iHigh_[ArrayMaximum(iHigh_, 0, HowManyBars)], Digits())
    LL = NormalizeDouble(iLow_[ArrayMinimum(iLow_, 0, HowManyBars)], Digits())
    SetHline(0, 'R_Line', 0, HH, Color_R, Style_R, Width_R, 'R_Line' + DoubleToString(HH, Digits()))
    SetHline(0, 'S_Line', 0, LL, Color_S, Style_S, Width_S, 'S_Line' + DoubleToString(LL, Digits()))
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nxbreakout(_MQL5Indicator):
    name = 'nxbreakout'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Chart period
        'StartBar': 1,  # Starting bar for analysis
        'HowManyBars': 5,  # Number of bars for analysis
        'Style_R': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Line style of the resistance level
        'Width_R': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Width of the resistance level line
        'Style_S': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Line style of the support level
        'Width_S': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Width of the support level line
    }

