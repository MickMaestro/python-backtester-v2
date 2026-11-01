"""flat — converted from MQL5: MQL5 Indicators/Flat/flat.mq5

Copyright: Pedro Puado; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Pedro Puado', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 12}, 'colors': {1: [8421504], 2: [8421504, 16711680, 16711935, 255]}, 'widths': {1: 1, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Line', 2: 'Arrows'}, 'levels': [], 'description': [], 'name': 'flat', 'source': 'MQL5 Indicators/Flat/flat.mq5', 'folder': 'Flat', 'inputs': [{'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Price type', 'sinput': False}, {'mql': 'HLRef', 'py': 'HLRef', 'param': 'HLRef', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'ExtraHighLevel', 'py': 'ExtraHighLevel', 'param': 'ExtraHighLevel', 'type': 'uint', 'default': 60, 'label': 'Maximum trend level', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 40, 'label': 'Strong trend level', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 20, 'label': 'Weak trend level', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 4, 'label': 'Style of level lines', 'sinput': False}, {'mql': 'LevelColor', 'py': 'LevelColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color of levels', 'sinput': False}, {'mql': 'LevelWidth', 'py': 'LevelWidth', 'param': 'LevelWidth', 'type': 'int', 'default': 0, 'label': 'Width of levels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 0
w_2 = 1
w_3 = 2
w_4 = 3
w_5 = 4
_enum('ENUM_WIDTH', {0: 'w_1', 1: 'w_2', 2: 'w_3', 3: 'w_4', 4: 'w_5'})

# ---- inputs and global variables
Smooth = _input('Smooth', 10)  # Smoothing period
ma_method = _input('ma_method', MODE_SMA)  # Smoothing type
applied_price = _input('applied_price', PRICE_CLOSE)  # Price type
HLRef = _input('HLRef', 100)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtraHighLevel = _input('ExtraHighLevel', 60)  # Maximum trend level
HighLevel = _input('HighLevel', 40)  # Strong trend level
LowLevel = _input('LowLevel', 20)  # Weak trend level
LevelStyle = _input('LevelStyle', STYLE_DASHDOTDOT)  # Style of level lines
LevelColor = _input('LevelColor', clrBlue)  # Color of levels
LevelWidth = _input('LevelWidth', w_1)  # Width of levels
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
ColorInd2Buffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
Value = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = _int(2 * Smooth)
    Ind_Handle = iStdDev(None, 0, Smooth, 0, ma_method, applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStdDev indicator')
        return INIT_FAILED
    ArrayResize(Count, HLRef)
    ArrayResize(Value, HLRef)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value, 0.0)
    ArraySetAsSeries(Value, True)
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ind2Buffer, True)
    SetIndexBuffer(2, ColorInd2Buffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorInd2Buffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Flat( ', Smooth, ', ', HLRef, ', ', Shift, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtraHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelWidth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Std = Arr(0, 0.0)
    Sum = 0.0
    sStd = 0.0
    HH = 0.0
    LL = 0.0
    Range = 0.0
    ArraySetAsSeries(Std, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = _int(rates_total - 1 - Smooth)
    else:
        limit = rates_total - prev_calculated
    to_copy = _int(limit + 1 + Smooth)
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, Std) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sum = 0.0
        for iii in range(0, _int(Smooth)):
            Sum += Std[bar + iii]
        sStd = Sum / Smooth
        Sum = 0.0
        for iii in range(0, _int(Smooth)):
            Sum += MathAbs((Std[bar + iii] - sStd) * 2)
        Value[Count[0]] = MathSqrt(Sum / Smooth)
        HH = Value[ArrayMaximum(Value, 0, HLRef)]
        LL = Value[ArrayMinimum(Value, 0, HLRef)]
        Range = HH - LL
        if Range:
            Ind1Buffer[bar] = _fdiv(100 * (Value[Count[0]] - LL), Range)
        else:
            Ind1Buffer[bar] = 100.0
        Ind2Buffer[bar] = Ind1Buffer[bar]
        if bar:
            Recount_ArrayZeroPos(Count, HLRef)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorInd2Buffer[bar] = 1.0
        if Ind1Buffer[bar] > ExtraHighLevel:
            ColorInd2Buffer[bar] = 3.0
        elif Ind1Buffer[bar] > HighLevel:
            ColorInd2Buffer[bar] = 2.0
        elif Ind1Buffer[bar] < LowLevel:
            ColorInd2Buffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Flat(_MQL5Indicator):
    name = 'flat'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Smooth': 10,  # Smoothing period
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price type
        'HLRef': 100,
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'ExtraHighLevel': 60,  # Maximum trend level
        'HighLevel': 40,  # Strong trend level
        'LowLevel': 20,  # Weak trend level
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Style of level lines
        'LevelWidth': _Choice({0: '1', 1: '2', 2: '3', 3: '4', 4: '5'}, default=0),  # Width of levels
    }

