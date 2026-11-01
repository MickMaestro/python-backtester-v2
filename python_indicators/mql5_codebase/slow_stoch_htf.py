"""slow-stoch_htf — converted from MQL5: MQL5 Indicators/Slow-Stoch_HTF/slow-stoch_htf.mq5

A smooth stochastic with timeframe selection option available in input parameters
Copyright: Copyright © 2013, Nikolay Kositsin; Link: arria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'arria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -50.0, 'indicator_maximum': 50.0}, 'types': {1: 7}, 'colors': {1: [8421376, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Stochastic; Signal'}, 'levels': [25.0, 0.0, -25.0], 'description': ['A smooth stochastic with timeframe selection option available in input parameters'], 'name': 'slow-stoch_htf', 'source': 'MQL5 Indicators/Slow-Stoch_HTF/slow-stoch_htf.mq5', 'folder': 'Slow-Stoch_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period (timeframe)', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period (timeframe)
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
STO_Method = _input('STO_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Method of averaging
XLength = _input('XLength', 5)  # Smoothing depth
XPhase = _input('XPhase', 15)  # Smoothing parameter
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Slow-Stoch', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Slow-Stoch', KPeriod, DPeriod, Slowing, STO_Method, Price_field, XMA_Method, XLength, XPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Slow-Stoch indicator')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Slow-Stoch', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpIndBuffer, 1, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            UpArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = UpArr[0] - 50
            DnIndBuf[bar] = DnArr[0] - 50
        else:
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


class SlowStochHtf(_MQL5Indicator):
    name = 'slow-stoch_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period (timeframe)
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Method of averaging
        'XLength': 5,  # Smoothing depth
        'XPhase': 15,  # Smoothing parameter
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (-50.0, 50.0)

