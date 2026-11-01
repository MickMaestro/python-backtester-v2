"""asymmetricstochnr_htf — converted from MQL5: MQL5 Indicators/AsymmetricStochNR_HTF/asymmetricstochnr_htf.mq5

Ergodic Oscillator with the timeframe selection option available in input parameters.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 11}, 'colors': {1: [16776960, 9639167], 2: [9639167, 42495, 8421504, 16748574, 16711680]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Signal', 2: 'INDICATOR_NAME'}, 'levels': [], 'description': ['Ergodic Oscillator with the timeframe selection option available in input parameters.'], 'name': 'asymmetricstochnr_htf', 'source': 'MQL5 Indicators/AsymmetricStochNR_HTF/asymmetricstochnr_htf.mq5', 'folder': 'AsymmetricStochNR_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period (timeframe)', 'sinput': False}, {'mql': 'KperiodShort', 'py': 'KperiodShort', 'param': 'KperiodShort', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'KperiodLong', 'py': 'KperiodLong', 'param': 'KperiodLong', 'type': 'uint', 'default': 12, 'label': '%K period', 'sinput': False}, {'mql': 'DMethod', 'py': 'DMethod', 'param': 'DMethod', 'type': 'int', 'default': 0, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'uint', 'default': 7, 'label': '%D signal line period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Signal line smoothing parameter', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Prices selection parameter for calculation', 'sinput': False}, {'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 7, 'label': 'Sensitivity in points', 'sinput': False}, {'mql': 'OverBought', 'py': 'OverBought', 'param': 'OverBought', 'type': 'uint', 'default': 80, 'label': 'Overbought level, %', 'sinput': False}, {'mql': 'OverSold', 'py': 'OverSold', 'param': 'OverSold', 'type': 'uint', 'default': 20, 'label': 'Oversold level, %', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color of levels', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Style of the levels', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Depth of the levels', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period (timeframe)
KperiodShort = _input('KperiodShort', 5)  # %K period
KperiodLong = _input('KperiodLong', 12)  # %K period
DMethod = _input('DMethod', MODE_SMA)  # Signal line smoothing method
Dperiod = _input('Dperiod', 7)  # %D signal line period
DPhase = _input('DPhase', 15)  # Signal line smoothing parameter
Slowing = _input('Slowing', 3)  # Slowing
PriceField = _input('PriceField', STO_LOWHIGH)  # Prices selection parameter for calculation
Sens = _input('Sens', 7)  # Sensitivity in points
OverBought = _input('OverBought', 80)  # Overbought level, %
OverSold = _input('OverSold', 20)  # Oversold level, %
LevelsColor = _input('LevelsColor', clrBlue)  # Color of levels
Levelstyle = _input('Levelstyle', DASH_)  # Style of the levels
LevelsWidth = _input('LevelsWidth', Width_1)  # Depth of the levels
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('AsymmetricStochNR', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'AsymmetricStochNR', KperiodShort, KperiodLong, DMethod, Dperiod, DPhase, Slowing, PriceField, Sens, OverBought, OverSold, clrNONE, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of AsymmetricStochNR')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    IndInit(2, IndBuffer1, INDICATOR_DATA)
    IndInit(3, IndBuffer2, INDICATOR_DATA)
    IndInit(4, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotInit(0, 0, Shift)
    PlotInit(1, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'AsymmetricStochNR', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, OverSold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrDarkOrchid)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, OverBought)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelsWidth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, IndBuffer1, IndBuffer2, ColorIndBuffer, UpIndBuffer, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, IndBuf1, IndBuf2, ColorIndBuf, UpIndBuf, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            IndArr = Arr(2, 0.0, dyn=False)
            SignArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 0, _DT(iTime_[bar]), 2, IndArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(iTime_[bar]), 1, SignArr) <= 0:
                return (0 != 0)
            IndBuf1[bar] = IndArr[1]
            IndBuf2[bar] = 50.0
            if not IndBuf1[bar]:
                IndBuf1[bar] = 1e-09
            UpIndBuf[bar] = IndBuf1[bar]
            DnIndBuf[bar] = SignArr[0]
            if not DnIndBuf[bar]:
                DnIndBuf[bar] = 1e-09
            clr = 2
            if IndArr[1] > 50:
                if IndArr[1] > IndArr[0]:
                    clr = 4
                if IndArr[1] < IndArr[0]:
                    clr = 3
            if IndArr[1] < 50:
                if IndArr[1] < IndArr[0]:
                    clr = 0
                if IndArr[1] > IndArr[0]:
                    clr = 1
            ColorIndBuf[bar] = clr
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            ColorIndBuf[bar] = ColorIndBuf[bar + 1]
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Chart period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AsymmetricstochnrHtf(_MQL5Indicator):
    name = 'asymmetricstochnr_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period (timeframe)
        'KperiodShort': 5,  # %K period
        'KperiodLong': 12,  # %K period
        'DMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Signal line smoothing method
        'Dperiod': 7,  # %D signal line period
        'DPhase': 15,  # Signal line smoothing parameter
        'Slowing': 3,  # Slowing
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Prices selection parameter for calculation
        'Sens': 7,  # Sensitivity in points
        'OverBought': 80,  # Overbought level, %
        'OverSold': 20,  # Oversold level, %
        'Levelstyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Style of the levels
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Depth of the levels
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

