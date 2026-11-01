"""stochasticcgoscillator_htf — converted from MQL5: MQL5 Indicators/StochasticCGOscillator_HTF/stochasticcgoscillator_htf.mq5

Stochastic CG Oscillator with the timeframe selection option available in input parameters.
Copyright: Copyright © 2014, Nikolay Kositsin; Link: arria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'arria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [8421376, 255], 2: [16711935, 55295, 8421504, 3329434, 8421376]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Signal', 2: 'INDICATOR_NAME'}, 'levels': [], 'description': ['Stochastic CG Oscillator with the timeframe selection option available in input parameters.'], 'name': 'stochasticcgoscillator_htf', 'source': 'MQL5 Indicators/StochasticCGOscillator_HTF/stochasticcgoscillator_htf.mq5', 'folder': 'StochasticCGOscillator_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period (timeframe)', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period (timeframe)
Length = _input('Length', 10)  # indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('StochasticCGOscillator', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'StochasticCGOscillator', Length, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of StochasticCGOscillator')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    IndInit(2, IndBuffer, INDICATOR_DATA)
    IndInit(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotInit(0, 0.0, 0, Shift)
    PlotInit(1, 0.0, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'StochasticCGOscillator', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, IndBuffer, ColorIndBuffer, 0, UpIndBuffer, 1, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, IndBuf, ColorIndBuf, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    clr = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            IndArr = Arr(2, 0.0, dyn=False)
            SignArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 2, IndArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, SignArr) <= 0:
                return (0 != 0)
            IndBuf[bar] = IndArr[1]
            if not IndBuf[bar]:
                IndBuf[bar] = 1e-09
            UpIndBuf[bar] = IndBuf[bar]
            DnIndBuf[bar] = SignArr[0]
            if not DnIndBuf[bar]:
                DnIndBuf[bar] = 1e-09
            clr = 2
            if IndArr[1] > 0:
                if IndArr[1] > IndArr[0]:
                    clr = 4
                if IndArr[1] < IndArr[0]:
                    clr = 3
            if IndArr[1] < 0:
                if IndArr[1] < IndArr[0]:
                    clr = 0
                if IndArr[1] > IndArr[0]:
                    clr = 1
            ColorIndBuf[bar] = clr
        else:
            IndBuf[bar] = IndBuf[bar + 1]
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


class StochasticcgoscillatorHtf(_MQL5Indicator):
    name = 'stochasticcgoscillator_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period (timeframe)
        'Length': 10,  # indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

