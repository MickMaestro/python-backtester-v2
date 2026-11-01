"""ultraspearmanrankcorrelation — converted from MQL5: MQL5 Indicators/Ultra Spearman Rank Correlation/ultraspearmanrankcorrelation.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [8421504, 16711935, 11823615, 255, 2763429, 14772545, 13434880, 16760576, 16436871]}, 'widths': {1: 4}, 'styles': {}, 'labels': {1: 'Ultra SpearmanRankCorrelation'}, 'levels': [], 'description': [], 'name': 'ultraspearmanrankcorrelation', 'source': 'MQL5 Indicators/Ultra Spearman Rank Correlation/ultraspearmanrankcorrelation.mq5', 'folder': 'Ultra Spearman Rank Correlation', 'inputs': [{'mql': 'rangeN', 'py': 'rangeN', 'param': 'rangeN', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'Smooth method', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'Start length', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'Phase', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'Period step', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'Steps total', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Smooth method', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'Smooth length', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'Smooth phase', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'Overbought level (in %)', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'Oversold level (in %)', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Overbought level color', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Oversold level color', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Level style', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Level width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
rangeN = _input('rangeN', 14)
W_Method = _input('W_Method', MODE_JJMA)  # Smooth method
StartLength = _input('StartLength', 3)  # Start length
WPhase = _input('WPhase', 100)  # Phase
Step = _input('Step', 5)  # Period step
StepsTotal = _input('StepsTotal', 10)  # Steps total
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Smooth method
SmoothLength = _input('SmoothLength', 3)  # Smooth length
SmoothPhase = _input('SmoothPhase', 100)  # Smooth phase
UpLevel = _input('UpLevel', 80)  # Overbought level (in %)
DnLevel = _input('DnLevel', 20)  # Oversold level (in %)
Levelstyle = _input('Levelstyle', DASH_)  # Level style
LevelsWidth = _input('LevelsWidth', Width_1)  # Level width
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
period = Arr(0, 0)
invalue0 = Arr(0, 0.0)
invalue1 = Arr(0, 0.0)
dUpLevel = 0.0
dDnLevel = 0.0
SRC_Handle = 0
Maxrange = 30
StTot1 = 0
StTot2 = 0
min_rates_total = 0
min_rates_src = 0
min_rates_xma = 0

def OnInit():
    global SRC_Handle, StTot1, StTot2, dDnLevel, dUpLevel, min_rates_src, min_rates_total, min_rates_xma
    size = _int(StepsTotal + 3)
    if ArrayResize(XMA, size) < size:
        Print('Error in ArrayResize of XMA[] array')
    size -= 2
    if ArrayResize(invalue0, size) < size:
        Print('Error in ArrayResize of invalue0[] array')
    if ArrayResize(invalue1, size) < size:
        Print('Error in ArrayResize of invalue1[] array')
    if ArrayResize(period, size) < size:
        Print('Error in ArrayResize of period[] array')
    ArrayInitialize(invalue0, 0)
    ArrayInitialize(invalue1, 0)
    ArrayInitialize(period, 0)
    SRC_Handle = iCustom(None, 0, 'SpearmanRankCorrelation', rangeN, 0, Maxrange, True)
    if SRC_Handle == INVALID_HANDLE:
        Print('Error in creation of SpearmanRankCorrelation indicator')
        return 1
    for sm in range(_int(StepsTotal), 0 - 1, -1):
        period[sm] = _int(StartLength + (sm * Step))
    dUpLevel = (StepsTotal * UpLevel) / 100.0
    dDnLevel = (StepsTotal * DnLevel) / 100.0
    XMA[0].XMALengthCheck('StartLength', StartLength)
    XMA[0].XMAPhaseCheck('WPhase', WPhase, W_Method)
    XMA[0].XMALengthCheck('SmoothLength', SmoothLength)
    XMA[0].XMAPhaseCheck('SmoothPhase', SmoothPhase, SmoothMethod)
    min_rates_src = rangeN
    min_rates_xma = min_rates_src + XMA[0].GetStartBars(W_Method, StartLength + (Step * StepsTotal), WPhase) + 1
    min_rates_total = min_rates_xma + XMA[0].GetStartBars(SmoothMethod, SmoothLength, SmoothPhase)
    StTot1 = StepsTotal + 1
    StTot2 = StepsTotal + 2
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BearsBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total + 1)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = 'Ultra Spearman RankCorrelation'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, dUpLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, dDnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(SRC_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar0 = 0
    maxbar1 = 0
    maxbar2 = 0
    upsch = 0.0
    dnsch = 0.0
    SRC = Arr(0, 0.0)
    maxbar0 = rates_total - 1
    maxbar1 = maxbar0 - min_rates_src
    maxbar2 = maxbar0 - min_rates_xma
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(SRC, True)
    if CopyBuffer(SRC_Handle, 0, 0, to_copy, SRC) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            invalue0[sm] = XMA[sm].XMASeries(maxbar1, prev_calculated, rates_total, W_Method, WPhase, period[sm], SRC[bar], bar, True)
        if bar > maxbar2:
            if bar:
                ArrayCopy(invalue1, invalue0, 0, 0, WHOLE_ARRAY)
            continue
        upsch = 0.0
        dnsch = 0.0
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            if invalue0[sm] > invalue1[sm]:
                upsch += 1
            else:
                dnsch += 1
        BullsBuffer[bar] = XMA[StTot1].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, upsch, bar, True)
        BearsBuffer[bar] = XMA[StTot2].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, dnsch, bar, True)
        if bar:
            ArrayCopy(invalue1, invalue0, 0, 0, WHOLE_ARRAY)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorBuffer[bar] = 0.0
        if BullsBuffer[bar] > BearsBuffer[bar]:
            if BullsBuffer[bar] > dUpLevel or BearsBuffer[bar] < dDnLevel:
                if BullsBuffer[bar + 1] <= BullsBuffer[bar]:
                    ColorBuffer[bar] = 7.0
                else:
                    ColorBuffer[bar] = 8.0
            else:
                if BullsBuffer[bar + 1] <= BullsBuffer[bar]:
                    ColorBuffer[bar] = 5.0
                else:
                    ColorBuffer[bar] = 6.0
        if BullsBuffer[bar] < BearsBuffer[bar]:
            if BullsBuffer[bar] < dDnLevel or BearsBuffer[bar] > dUpLevel:
                if BearsBuffer[bar + 1] <= BearsBuffer[bar]:
                    ColorBuffer[bar] = 1.0
                else:
                    ColorBuffer[bar] = 2.0
            else:
                if BearsBuffer[bar + 1] <= BearsBuffer[bar]:
                    ColorBuffer[bar] = 3.0
                else:
                    ColorBuffer[bar] = 4.0
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


class Ultraspearmanrankcorrelation(_MQL5Indicator):
    name = 'ultraspearmanrankcorrelation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'rangeN': 14,
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smooth method
        'StartLength': 3,  # Start length
        'WPhase': 100,  # Phase
        'Step': 5,  # Period step
        'StepsTotal': 10,  # Steps total
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smooth method
        'SmoothLength': 3,  # Smooth length
        'SmoothPhase': 100,  # Smooth phase
        'UpLevel': 80,  # Overbought level (in %)
        'DnLevel': 20,  # Oversold level (in %)
        'Levelstyle': _Choice({0: 'solid', 1: 'dash', 2: 'dot', 3: 'dash-dot', 4: 'dash-dot-dot'}, default=1),  # Level style
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Level width
    }

