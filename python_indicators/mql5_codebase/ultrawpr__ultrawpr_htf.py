"""ultrawpr — converted from MQL5: MQL5 Indicators/UltraWPR_HTF/ultrawpr.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65280, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Ultra WPR'}, 'levels': [], 'description': [], 'name': 'ultrawpr', 'source': 'MQL5 Indicators/UltraWPR_HTF/ultrawpr.mq5', 'folder': 'UltraWPR_HTF', 'inputs': [{'mql': 'WPR_Period', 'py': 'WPR_Period', 'param': 'WPR_Period', 'type': 'int', 'default': 13, 'label': 'WPR indicator period', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'Initial smoothing period', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'Period change step', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'Number of period changes', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'Overbought level, %', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'Oversold level, %', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Overbought level color', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Oversold level color', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Levels style', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Levels width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Blue = 0xFF0000  # MQL4 colour name

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
WPR_Period = _input('WPR_Period', 13)  # WPR indicator period
W_Method = _input('W_Method', MODE_JJMA)  # Smoothing method
StartLength = _input('StartLength', 3)  # Initial smoothing period
WPhase = _input('WPhase', 100)  # Smoothing parameter
Step = _input('Step', 5)  # Period change step
StepsTotal = _input('StepsTotal', 10)  # Number of period changes
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Smoothing method
SmoothLength = _input('SmoothLength', 3)  # Smoothing depth
SmoothPhase = _input('SmoothPhase', 100)  # Smoothing parameter
UpLevel = _input('UpLevel', 80)  # Overbought level, %
DnLevel = _input('DnLevel', 20)  # Oversold level, %
Levelstyle = _input('Levelstyle', DASH_)  # Levels style
LevelsWidth = _input('LevelsWidth', Width_1)  # Levels width
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
period = Arr(0, 0)
xwpr0 = Arr(0, 0.0)
xwpr1 = Arr(0, 0.0)
WPR_Handle = 0
StTot1 = 0
StTot2 = 0
min_rates_total = 0
min_rates_wpr = 0
min_rates_xma = 0

def OnInit():
    global StTot1, StTot2, WPR_Handle, min_rates_total, min_rates_wpr, min_rates_xma
    size = _int(StepsTotal + 3)
    if ArrayResize(XMA, size) < size:
        Print('Failed to distribute the memory for XMA[] array')
    size -= 2
    if ArrayResize(xwpr0, size) < size:
        Print('Failed to distribute the memory for xwpr0[] array')
    if ArrayResize(xwpr1, size) < size:
        Print('Failed to distribute the memory for xwpr1[] array')
    if ArrayResize(period, size) < size:
        Print('Failed to distribute the memory for period[] array')
    ZeroMemory(xwpr0)
    ZeroMemory(xwpr1)
    ZeroMemory(period)
    for sm in range(_int(StepsTotal), 0 - 1, -1):
        period[sm] = _int(StartLength + (sm * Step))
    XMA[0].XMALengthCheck('StartLength', StartLength)
    XMA[0].XMAPhaseCheck('WPhase', WPhase, W_Method)
    XMA[0].XMALengthCheck('SmoothLength', SmoothLength)
    XMA[0].XMAPhaseCheck('SmoothPhase', SmoothPhase, SmoothMethod)
    min_rates_wpr = WPR_Period
    min_rates_xma = min_rates_wpr + XMA[0].GetStartBars(W_Method, StartLength + (Step * StepsTotal), WPhase) + 1
    min_rates_total = min_rates_xma + XMA[0].GetStartBars(SmoothMethod, SmoothLength, SmoothPhase)
    StTot1 = StepsTotal + 1
    StTot2 = StepsTotal + 2
    WPR_Handle = iWPR(None, 0, WPR_Period)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the WPR indicator')
        return 1
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BearsBuffer, True)
    shortname = 'Ultra WPR'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _idiv(StepsTotal * UpLevel, 100))
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, _idiv(StepsTotal * DnLevel, 100))
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(WPR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    WPR = Arr(0, 0.0)
    upsch = 0.0
    dnsch = 0.0
    maxbar1 = rates_total - 1 - min_rates_wpr
    maxbar2 = rates_total - 1 - min_rates_xma
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            xwpr0[sm] = XMA[sm].XMASeries(maxbar1, prev_calculated, rates_total, W_Method, WPhase, period[sm], WPR[bar], bar, True)
        if bar > maxbar2:
            if bar:
                ArrayCopy(xwpr1, xwpr0, 0, 0, WHOLE_ARRAY)
            continue
        upsch = 0.0
        dnsch = 0.0
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            if xwpr0[sm] > xwpr1[sm]:
                upsch += 1
            else:
                dnsch += 1
        BullsBuffer[bar] = XMA[StTot1].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, upsch, bar, True)
        BearsBuffer[bar] = XMA[StTot2].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, dnsch, bar, True)
        if bar:
            ArrayCopy(xwpr1, xwpr0, 0, 0, WHOLE_ARRAY)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(0, 0, factory=CXMA)
UpLevelsColor = _input('UpLevelsColor', _uint(Blue))  # Overbought level color
DnLevelsColor = _input('DnLevelsColor', _uint(Blue))  # Oversold level color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ultrawpr(_MQL5Indicator):
    name = 'ultrawpr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPR_Period': 13,  # WPR indicator period
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'StartLength': 3,  # Initial smoothing period
        'WPhase': 100,  # Smoothing parameter
        'Step': 5,  # Period change step
        'StepsTotal': 10,  # Number of period changes
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'SmoothLength': 3,  # Smoothing depth
        'SmoothPhase': 100,  # Smoothing parameter
        'UpLevel': 80,  # Overbought level, %
        'DnLevel': 20,  # Oversold level, %
        'Levelstyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Levels style
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Levels width
    }

