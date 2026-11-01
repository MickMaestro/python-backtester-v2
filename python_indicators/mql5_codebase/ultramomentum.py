"""ultramomentum — converted from MQL5: MQL5 Indicators/Ultra Momentum/ultramomentum.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 7}, 'colors': {1: [255], 2: [65280], 3: [3329330, 4678655]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Ultra Momentum Speed Down', 2: 'Ultra Momentum Speed Up', 3: 'Ultra Momentum'}, 'levels': [], 'description': [], 'name': 'ultramomentum', 'source': 'MQL5 Indicators/Ultra Momentum/ultramomentum.mq5', 'folder': 'Ultra Momentum', 'inputs': [{'mql': 'Momentum_Period', 'py': 'Momentum_Period', 'param': 'Momentum_Period', 'type': 'int', 'default': 14, 'label': 'Momentum indicator period', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'Initial smoothing period', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'Period change step', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'Number of period changes', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'Overbought level, %%', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'Oversold level, %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Overbought level color', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Oversold level color', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 4, 'label': 'Levels style', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Levels width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

DarkViolet = 0xD30094  # MQL4 colour name

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
Momentum_Period = _input('Momentum_Period', 14)  # Momentum indicator period
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Applied price
W_Method = _input('W_Method', MODE_JJMA)  # Smoothing method
StartLength = _input('StartLength', 3)  # Initial smoothing period
WPhase = _input('WPhase', 100)  # Smoothing parameter
Step = _input('Step', 5)  # Period change step
StepsTotal = _input('StepsTotal', 10)  # Number of period changes
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Smoothing method
SmoothLength = _input('SmoothLength', 3)  # Smoothing depth
SmoothPhase = _input('SmoothPhase', 100)  # Smoothing parameter
UpLevel = _input('UpLevel', 80)  # Overbought level, %%
DnLevel = _input('DnLevel', 20)  # Oversold level, %%
Levelstyle = _input('Levelstyle', DASHDOTDOT_)  # Levels style
LevelsWidth = _input('LevelsWidth', Width_1)  # Levels width
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
period = Arr(0, 0)
momentum0 = Arr(0, 0.0)
momentum1 = Arr(0, 0.0)
Momentum_Handle = 0
middle = 0.0
StTot1 = 0
StTot2 = 0
min_rates_total = 0
min_rates_cci = 0
min_rates_xma = 0

def OnInit():
    global Momentum_Handle, StTot1, StTot2, middle, min_rates_cci, min_rates_total, min_rates_xma
    size = _int(StepsTotal + 3)
    if ArrayResize(XMA, size) < size:
        Print('Failed to distribute the memory for XMA[] array')
    size -= 2
    if ArrayResize(momentum0, size) < size:
        Print('Failed to distribute the memory for momentum0[] array')
    if ArrayResize(momentum1, size) < size:
        Print('Failed to distribute the memory for momentum1[] array')
    if ArrayResize(period, size) < size:
        Print('Failed to distribute the memory for period[] array')
    ZeroMemory(momentum0)
    ZeroMemory(momentum1)
    ZeroMemory(period)
    for sm in range(_int(StepsTotal), 0 - 1, -1):
        period[sm] = _int(StartLength + (sm * Step))
    middle = -((StepsTotal * UpLevel * 3.0) / 1000.0)
    XMA[0].XMALengthCheck('StartLength', StartLength)
    XMA[0].XMAPhaseCheck('WPhase', WPhase, W_Method)
    XMA[0].XMALengthCheck('SmoothLength', SmoothLength)
    XMA[0].XMAPhaseCheck('SmoothPhase', SmoothPhase, SmoothMethod)
    min_rates_cci = Momentum_Period
    min_rates_xma = min_rates_cci + XMA[0].GetStartBars(W_Method, StartLength + (Step * StepsTotal), WPhase) + 1
    min_rates_total = min_rates_xma + XMA[0].GetStartBars(SmoothMethod, SmoothLength, SmoothPhase)
    StTot1 = StepsTotal + 1
    StTot2 = StepsTotal + 2
    Momentum_Handle = iMomentum(None, 0, Momentum_Period, Applied_price)
    if Momentum_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Momentum indicator')
        return 1
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 110)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 110)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(2, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(3, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BearsBuffer, True)
    shortname = 'Ultra Momentum'
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
    if BarsCalculated(Momentum_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    Momentum = Arr(0, 0.0)
    upsch = 0.0
    dnsch = 0.0
    maxbar1 = rates_total - 1 - min_rates_cci
    maxbar2 = rates_total - 1 - min_rates_xma
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(Momentum_Handle, 0, 0, to_copy, Momentum) <= 0:
        return 0
    ArraySetAsSeries(Momentum, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            momentum0[sm] = XMA[sm].XMASeries(maxbar1, prev_calculated, rates_total, W_Method, WPhase, period[sm], Momentum[bar], bar, True)
        if bar > maxbar2:
            if bar:
                ArrayCopy(momentum1, momentum0, 0, 0, WHOLE_ARRAY)
            continue
        upsch = 0.0
        dnsch = 0.0
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            if momentum0[sm] > momentum1[sm]:
                upsch += 1
            else:
                dnsch += 1
        BullsBuffer[bar] = XMA[StTot1].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, upsch, bar, True)
        BearsBuffer[bar] = XMA[StTot2].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, dnsch, bar, True)
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        if BullsBuffer[bar] < BearsBuffer[bar]:
            if BearsBuffer[bar + 1] <= BearsBuffer[bar]:
                DnBuffer[bar] = middle
            else:
                UpBuffer[bar] = middle
        else:
            if BullsBuffer[bar + 1] <= BullsBuffer[bar]:
                UpBuffer[bar] = middle
            else:
                DnBuffer[bar] = middle
        if bar:
            ArrayCopy(momentum1, momentum0, 0, 0, WHOLE_ARRAY)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(0, 0, factory=CXMA)
UpLevelsColor = _input('UpLevelsColor', _uint(DarkViolet))  # Overbought level color
DnLevelsColor = _input('DnLevelsColor', _uint(DarkViolet))  # Oversold level color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ultramomentum(_MQL5Indicator):
    name = 'ultramomentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Momentum_Period': 14,  # Momentum indicator period
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'StartLength': 3,  # Initial smoothing period
        'WPhase': 100,  # Smoothing parameter
        'Step': 5,  # Period change step
        'StepsTotal': 10,  # Number of period changes
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'SmoothLength': 3,  # Smoothing depth
        'SmoothPhase': 100,  # Smoothing parameter
        'UpLevel': 80,  # Overbought level, %%
        'DnLevel': 20,  # Oversold level, %%
        'Levelstyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # Levels style
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Levels width
    }

