"""atrpivot — converted from MQL5: MQL5 Indicators/ATRPivot/atrpivot.mq5

ATRPivot
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['ATRPivot'], 'name': 'atrpivot', 'source': 'MQL5 Indicators/ATRPivot/atrpivot.mq5', 'folder': 'ATRPivot', 'inputs': [{'mql': 'PivotPeriod', 'py': 'PivotPeriod', 'param': 'PivotPeriod', 'type': 'int', 'default': 16408, 'label': 'ATR indicator time frame', 'sinput': False}, {'mql': 'CountBar', 'py': 'CountBar', 'param': 'CountBar', 'type': 'int', 'default': 1, 'label': 'Calculation bar', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 18, 'label': 'ATR period', 'sinput': False}, {'mql': 'Mult_Factor05', 'py': 'Mult_Factor05', 'param': 'Mult_Factor05', 'type': 'double', 'default': 0.8, 'label': 'First levels ratio', 'sinput': False}, {'mql': 'Mult_Factor10', 'py': 'Mult_Factor10', 'param': 'Mult_Factor10', 'type': 'double', 'default': 1.6, 'label': 'First levels ratio', 'sinput': False}, {'mql': 'Mult_Factor15', 'py': 'Mult_Factor15', 'param': 'Mult_Factor15', 'type': 'double', 'default': 2.4, 'label': 'First levels ratio', 'sinput': False}, {'mql': 'Mult_Factor20', 'py': 'Mult_Factor20', 'param': 'Mult_Factor20', 'type': 'double', 'default': 3.2, 'label': 'Second levels ratio', 'sinput': False}, {'mql': 'Mult_Factor25', 'py': 'Mult_Factor25', 'param': 'Mult_Factor25', 'type': 'double', 'default': 4.0, 'label': 'First levels ratio', 'sinput': False}, {'mql': 'Mult_Factor30', 'py': 'Mult_Factor30', 'param': 'Mult_Factor30', 'type': 'double', 'default': 4.8, 'label': 'Third levels ratio', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'int', 'default': 10, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Color_R30', 'py': 'Color_R30', 'param': None, 'type': 'color', 'default': 0, 'label': 'R30 level color', 'sinput': False}, {'mql': 'Color_R25', 'py': 'Color_R25', 'param': None, 'type': 'color', 'default': 0, 'label': 'R25 level color', 'sinput': False}, {'mql': 'Color_R20', 'py': 'Color_R20', 'param': None, 'type': 'color', 'default': 0, 'label': 'R20 level color', 'sinput': False}, {'mql': 'Color_R15', 'py': 'Color_R15', 'param': None, 'type': 'color', 'default': 0, 'label': 'R15 level color', 'sinput': False}, {'mql': 'Color_R10', 'py': 'Color_R10', 'param': None, 'type': 'color', 'default': 0, 'label': 'R10 level color', 'sinput': False}, {'mql': 'Color_R05', 'py': 'Color_R05', 'param': None, 'type': 'color', 'default': 0, 'label': 'R05 level color', 'sinput': False}, {'mql': 'Color_P', 'py': 'Color_P', 'param': None, 'type': 'color', 'default': 0, 'label': 'P level color', 'sinput': False}, {'mql': 'Color_S05', 'py': 'Color_S05', 'param': None, 'type': 'color', 'default': 0, 'label': 'S05 level color', 'sinput': False}, {'mql': 'Color_S10', 'py': 'Color_S10', 'param': None, 'type': 'color', 'default': 0, 'label': 'S10 level color', 'sinput': False}, {'mql': 'Color_S15', 'py': 'Color_S15', 'param': None, 'type': 'color', 'default': 0, 'label': 'S15 level color', 'sinput': False}, {'mql': 'Color_S20', 'py': 'Color_S20', 'param': None, 'type': 'color', 'default': 0, 'label': 'S20 level color', 'sinput': False}, {'mql': 'Color_S25', 'py': 'Color_S25', 'param': None, 'type': 'color', 'default': 0, 'label': 'S25 level color', 'sinput': False}, {'mql': 'Color_S30', 'py': 'Color_S30', 'param': None, 'type': 'color', 'default': 0, 'label': 'S30 level color', 'sinput': False}, {'mql': 'Style_R30', 'py': 'Style_R30', 'param': 'Style_R30', 'type': 'int', 'default': 0, 'label': 'R30 level line style', 'sinput': False}, {'mql': 'Style_R25', 'py': 'Style_R25', 'param': 'Style_R25', 'type': 'int', 'default': 4, 'label': 'R25 level line style', 'sinput': False}, {'mql': 'Style_R20', 'py': 'Style_R20', 'param': 'Style_R20', 'type': 'int', 'default': 0, 'label': 'R20 level line style', 'sinput': False}, {'mql': 'Style_R15', 'py': 'Style_R15', 'param': 'Style_R15', 'type': 'int', 'default': 4, 'label': 'R15 level line style', 'sinput': False}, {'mql': 'Style_R10', 'py': 'Style_R10', 'param': 'Style_R10', 'type': 'int', 'default': 0, 'label': 'R10 level line style', 'sinput': False}, {'mql': 'Style_R05', 'py': 'Style_R05', 'param': 'Style_R05', 'type': 'int', 'default': 4, 'label': 'R05 level line style', 'sinput': False}, {'mql': 'Style_P', 'py': 'Style_P', 'param': 'Style_P', 'type': 'int', 'default': 1, 'label': 'P level line style', 'sinput': False}, {'mql': 'Style_S05', 'py': 'Style_S05', 'param': 'Style_S05', 'type': 'int', 'default': 4, 'label': 'S05 level line style', 'sinput': False}, {'mql': 'Style_S10', 'py': 'Style_S10', 'param': 'Style_S10', 'type': 'int', 'default': 0, 'label': 'S10 level line style', 'sinput': False}, {'mql': 'Style_S15', 'py': 'Style_S15', 'param': 'Style_S15', 'type': 'int', 'default': 4, 'label': 'S15 level line style', 'sinput': False}, {'mql': 'Style_S20', 'py': 'Style_S20', 'param': 'Style_S20', 'type': 'int', 'default': 0, 'label': 'S20 level line style', 'sinput': False}, {'mql': 'Style_S25', 'py': 'Style_S25', 'param': 'Style_S25', 'type': 'int', 'default': 4, 'label': 'S25 level line style', 'sinput': False}, {'mql': 'Style_S30', 'py': 'Style_S30', 'param': 'Style_S30', 'type': 'int', 'default': 0, 'label': 'S30 level line style', 'sinput': False}, {'mql': 'Width_R30', 'py': 'Width_R30', 'param': 'Width_R30', 'type': 'int', 'default': 1, 'label': 'R30 level line width', 'sinput': False}, {'mql': 'Width_R25', 'py': 'Width_R25', 'param': 'Width_R25', 'type': 'int', 'default': 1, 'label': 'R25 level line width', 'sinput': False}, {'mql': 'Width_R20', 'py': 'Width_R20', 'param': 'Width_R20', 'type': 'int', 'default': 2, 'label': 'R20 level line width', 'sinput': False}, {'mql': 'Width_R15', 'py': 'Width_R15', 'param': 'Width_R15', 'type': 'int', 'default': 1, 'label': 'R15 level line width', 'sinput': False}, {'mql': 'Width_R10', 'py': 'Width_R10', 'param': 'Width_R10', 'type': 'int', 'default': 3, 'label': 'R10 level line width', 'sinput': False}, {'mql': 'Width_R05', 'py': 'Width_R05', 'param': 'Width_R05', 'type': 'int', 'default': 1, 'label': 'R05 level line width', 'sinput': False}, {'mql': 'Width_P', 'py': 'Width_P', 'param': 'Width_P', 'type': 'int', 'default': 1, 'label': 'P level line width', 'sinput': False}, {'mql': 'Width_S05', 'py': 'Width_S05', 'param': 'Width_S05', 'type': 'int', 'default': 1, 'label': 'S05 level line width', 'sinput': False}, {'mql': 'Width_S10', 'py': 'Width_S10', 'param': 'Width_S10', 'type': 'int', 'default': 3, 'label': 'S10 level line width', 'sinput': False}, {'mql': 'Width_S15', 'py': 'Width_S15', 'param': 'Width_S15', 'type': 'int', 'default': 1, 'label': 'S15 level line width', 'sinput': False}, {'mql': 'Width_S20', 'py': 'Width_S20', 'param': 'Width_S20', 'type': 'int', 'default': 2, 'label': 'S20 level line width', 'sinput': False}, {'mql': 'Width_S25', 'py': 'Width_S25', 'param': 'Width_S25', 'type': 'int', 'default': 1, 'label': 'S25 level line width', 'sinput': False}, {'mql': 'Width_S30', 'py': 'Width_S30', 'param': 'Width_S30', 'type': 'int', 'default': 1, 'label': 'S30 level line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

DarkOrange = 0x008CFF  # MQL4 colour name
DarkOrchid = 0xCC3299  # MQL4 colour name
DodgerBlue = 0xFF901E  # MQL4 colour name

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

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
PivotPeriod = _input('PivotPeriod', PERIOD_D1)  # ATR indicator time frame
CountBar = _input('CountBar', 1)  # Calculation bar
ATRPeriod = _input('ATRPeriod', 18)  # ATR period
Mult_Factor05 = _input('Mult_Factor05', 0.8)  # First levels ratio
Mult_Factor10 = _input('Mult_Factor10', 1.6)  # First levels ratio
Mult_Factor15 = _input('Mult_Factor15', 2.4)  # First levels ratio
Mult_Factor20 = _input('Mult_Factor20', 3.2)  # Second levels ratio
Mult_Factor25 = _input('Mult_Factor25', 4.0)  # First levels ratio
Mult_Factor30 = _input('Mult_Factor30', 4.8)  # Third levels ratio
MA_SMethod = _input('MA_SMethod', MODE_SMA)  # Smoothing method
MA_Length = _input('MA_Length', 10)  # Smoothing depth
MA_Phase = _input('MA_Phase', 100)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Style_R30 = _input('Style_R30', SOLID_)  # R30 level line style
Style_R25 = _input('Style_R25', DASHDOTDOT_)  # R25 level line style
Style_R20 = _input('Style_R20', SOLID_)  # R20 level line style
Style_R15 = _input('Style_R15', DASHDOTDOT_)  # R15 level line style
Style_R10 = _input('Style_R10', SOLID_)  # R10 level line style
Style_R05 = _input('Style_R05', DASHDOTDOT_)  # R05 level line style
Style_P = _input('Style_P', DASH_)  # P level line style
Style_S05 = _input('Style_S05', DASHDOTDOT_)  # S05 level line style
Style_S10 = _input('Style_S10', SOLID_)  # S10 level line style
Style_S15 = _input('Style_S15', DASHDOTDOT_)  # S15 level line style
Style_S20 = _input('Style_S20', SOLID_)  # S20 level line style
Style_S25 = _input('Style_S25', DASHDOTDOT_)  # S25 level line style
Style_S30 = _input('Style_S30', SOLID_)  # S30 level line style
Width_R30 = _input('Width_R30', Width_1)  # R30 level line width
Width_R25 = _input('Width_R25', Width_1)  # R25 level line width
Width_R20 = _input('Width_R20', Width_2)  # R20 level line width
Width_R15 = _input('Width_R15', Width_1)  # R15 level line width
Width_R10 = _input('Width_R10', Width_3)  # R10 level line width
Width_R05 = _input('Width_R05', Width_1)  # R05 level line width
Width_P = _input('Width_P', Width_1)  # P level line width
Width_S05 = _input('Width_S05', Width_1)  # S05 level line width
Width_S10 = _input('Width_S10', Width_3)  # S10 level line width
Width_S15 = _input('Width_S15', Width_1)  # S15 level line width
Width_S20 = _input('Width_S20', Width_2)  # S20 level line width
Width_S25 = _input('Width_S25', Width_1)  # S25 level line width
Width_S30 = _input('Width_S30', Width_1)  # S30 level line width
ATR_Handle = 0
XMA_Handle = 0
StartBarsXMA = 0
StartBarsATR = 0
StartBars = 0

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
    global ATR_Handle, StartBars, StartBarsATR, StartBarsXMA, XMA_Handle
    ATR_Handle = iATR(None, PivotPeriod, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    XMA_Handle = iCustom(None, PivotPeriod, 'XMA', MA_SMethod, MA_Length, MA_Phase, IPC, 0, 0)
    if XMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XMA indicator')
    StartBarsXMA = XMA.GetStartBars(MA_SMethod, MA_Length, MA_Phase) + 1
    StartBarsATR = StartBarsXMA + ATRPeriod
    StartBars = StartBarsXMA + StartBarsATR
    XMA.XMALengthCheck('Length', MA_Length)
    XMA.XMAPhaseCheck('Phase', MA_Phase, MA_SMethod)

def Deinit():
    ObjectDelete(0, 'Pivot_Line')
    ObjectDelete(0, 'R0.5_Line')
    ObjectDelete(0, 'R1.0_Line')
    ObjectDelete(0, 'R1.5_Line')
    ObjectDelete(0, 'R2.0_Line')
    ObjectDelete(0, 'R2.5_Line')
    ObjectDelete(0, 'R3.0_Line')
    ObjectDelete(0, 'S0.5_Line')
    ObjectDelete(0, 'S1.0_Line')
    ObjectDelete(0, 'S1.5_Line')
    ObjectDelete(0, 'S2.0_Line')
    ObjectDelete(0, 'S2.5_Line')
    ObjectDelete(0, 'S3.0_Line')

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_P, _s_OnCalculate_R10, _s_OnCalculate_R15, _s_OnCalculate_R20, _s_OnCalculate_R25, _s_OnCalculate_R30, _s_OnCalculate_S10, _s_OnCalculate_S15, _s_OnCalculate_S20, _s_OnCalculate_S25, _s_OnCalculate_S30
    if Period() >= PivotPeriod:
        return 0
    if (BarsCalculated(ATR_Handle) < (CountBar + 1) or BarsCalculated(XMA_Handle) < (CountBar + 1)) or rates_total < StartBars:
        return 0
    if rates_total != prev_calculated:
        to_copy = 1
        ATR_Buffer = Arr(0, 0.0)
        XMA_Buffer = Arr(0, 0.0)
        ArraySetAsSeries(ATR_Buffer, True)
        ArraySetAsSeries(XMA_Buffer, True)
        if CopyBuffer(ATR_Handle, 0, CountBar, to_copy, ATR_Buffer) <= 0:
            Deinit()
            return 0
        if CopyBuffer(XMA_Handle, 0, CountBar, to_copy, XMA_Buffer) <= 0:
            Deinit()
            return 0
        _s_OnCalculate_P = XMA_Buffer[0]
        _s_OnCalculate_R30 = _s_OnCalculate_P + (ATR_Buffer[0] * Mult_Factor30)
        _s_OnCalculate_R25 = _s_OnCalculate_P + (ATR_Buffer[0] * Mult_Factor25)
        _s_OnCalculate_R20 = _s_OnCalculate_P + (ATR_Buffer[0] * Mult_Factor20)
        _s_OnCalculate_R15 = _s_OnCalculate_P + (ATR_Buffer[0] * Mult_Factor15)
        _s_OnCalculate_R10 = _s_OnCalculate_P + (ATR_Buffer[0] * Mult_Factor10)
        _s_OnCalculate_S10 = _s_OnCalculate_P - (ATR_Buffer[0] * Mult_Factor10)
        _s_OnCalculate_S15 = _s_OnCalculate_P - (ATR_Buffer[0] * Mult_Factor15)
        _s_OnCalculate_S20 = _s_OnCalculate_P - (ATR_Buffer[0] * Mult_Factor20)
        _s_OnCalculate_S25 = _s_OnCalculate_P - (ATR_Buffer[0] * Mult_Factor25)
        _s_OnCalculate_S30 = _s_OnCalculate_P - (ATR_Buffer[0] * Mult_Factor30)
    SetHline(0, 'R3.0_Line', 0, _s_OnCalculate_R30, Color_R30, Style_R30, Width_R30, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_R30, Digits()))
    SetHline(0, 'R2.5_Line', 0, _s_OnCalculate_R25, Color_R25, Style_R25, Width_R25, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_R25, Digits()))
    SetHline(0, 'R2.0_Line', 0, _s_OnCalculate_R20, Color_R20, Style_R20, Width_R20, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_R20, Digits()))
    SetHline(0, 'R1.5_Line', 0, _s_OnCalculate_R15, Color_R15, Style_R15, Width_R15, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_R15, Digits()))
    SetHline(0, 'R1.0_Line', 0, _s_OnCalculate_R10, Color_R10, Style_R10, Width_R10, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_R10, Digits()))
    SetHline(0, 'R0.5_Line', 0, _s_OnCalculate_R05, Color_R05, Style_R05, Width_R05, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_R05, Digits()))
    SetHline(0, 'Pivot_Line', 0, _s_OnCalculate_P, Color_P, Style_P, Width_P, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_P, Digits()))
    SetHline(0, 'S0.5_Line', 0, _s_OnCalculate_S05, Color_S05, Style_S05, Width_S05, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_S05, Digits()))
    SetHline(0, 'S1.0_Line', 0, _s_OnCalculate_S10, Color_S10, Style_S10, Width_S10, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_S10, Digits()))
    SetHline(0, 'S1.5_Line', 0, _s_OnCalculate_S15, Color_S15, Style_S15, Width_S15, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_S15, Digits()))
    SetHline(0, 'S2.0_Line', 0, _s_OnCalculate_S20, Color_S20, Style_S20, Width_S20, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_S20, Digits()))
    SetHline(0, 'S2.5_Line', 0, _s_OnCalculate_S25, Color_S25, Style_S25, Width_S25, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_S25, Digits()))
    SetHline(0, 'S3.0_Line', 0, _s_OnCalculate_S30, Color_S30, Style_S30, Width_S30, 'ATR Pivot ' + DoubleToString(_s_OnCalculate_S30, Digits()))
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()
Color_R30 = _input('Color_R30', _uint(DodgerBlue))  # R30 level color
Color_R25 = _input('Color_R25', _uint(DodgerBlue))  # R25 level color
Color_R20 = _input('Color_R20', _uint(DodgerBlue))  # R20 level color
Color_R15 = _input('Color_R15', _uint(DodgerBlue))  # R15 level color
Color_R10 = _input('Color_R10', _uint(DodgerBlue))  # R10 level color
Color_R05 = _input('Color_R05', _uint(DodgerBlue))  # R05 level color
Color_P = _input('Color_P', _uint(DarkOrchid))  # P level color
Color_S05 = _input('Color_S05', _uint(DarkOrange))  # S05 level color
Color_S10 = _input('Color_S10', _uint(DarkOrange))  # S10 level color
Color_S15 = _input('Color_S15', _uint(DarkOrange))  # S15 level color
Color_S20 = _input('Color_S20', _uint(DarkOrange))  # S20 level color
Color_S25 = _input('Color_S25', _uint(DarkOrange))  # S25 level color
Color_S30 = _input('Color_S30', _uint(DarkOrange))  # S30 level color

# ---- static local variables
_s_OnCalculate_P = 0.0
_s_OnCalculate_S05 = 0.0
_s_OnCalculate_R05 = 0.0
_s_OnCalculate_S10 = 0.0
_s_OnCalculate_R10 = 0.0
_s_OnCalculate_S15 = 0.0
_s_OnCalculate_R15 = 0.0
_s_OnCalculate_S20 = 0.0
_s_OnCalculate_R20 = 0.0
_s_OnCalculate_S25 = 0.0
_s_OnCalculate_R25 = 0.0
_s_OnCalculate_S30 = 0.0
_s_OnCalculate_R30 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atrpivot(_MQL5Indicator):
    name = 'atrpivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PivotPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # ATR indicator time frame
        'CountBar': 1,  # Calculation bar
        'ATRPeriod': 18,  # ATR period
        'Mult_Factor05': 0.8,  # First levels ratio
        'Mult_Factor10': 1.6,  # First levels ratio
        'Mult_Factor15': 2.4,  # First levels ratio
        'Mult_Factor20': 3.2,  # Second levels ratio
        'Mult_Factor25': 4.0,  # First levels ratio
        'Mult_Factor30': 4.8,  # Third levels ratio
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'MA_Length': 10,  # Smoothing depth
        'MA_Phase': 100,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Style_R30': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # R30 level line style
        'Style_R25': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # R25 level line style
        'Style_R20': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # R20 level line style
        'Style_R15': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # R15 level line style
        'Style_R10': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # R10 level line style
        'Style_R05': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # R05 level line style
        'Style_P': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # P level line style
        'Style_S05': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # S05 level line style
        'Style_S10': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # S10 level line style
        'Style_S15': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # S15 level line style
        'Style_S20': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # S20 level line style
        'Style_S25': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # S25 level line style
        'Style_S30': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # S30 level line style
        'Width_R30': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R30 level line width
        'Width_R25': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R25 level line width
        'Width_R20': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # R20 level line width
        'Width_R15': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R15 level line width
        'Width_R10': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # R10 level line width
        'Width_R05': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R05 level line width
        'Width_P': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # P level line width
        'Width_S05': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S05 level line width
        'Width_S10': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # S10 level line width
        'Width_S15': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S15 level line width
        'Width_S20': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # S20 level line width
        'Width_S25': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S25 level line width
        'Width_S30': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S30 level line width
    }

