"""trendtriggermod_htf — converted from MQL5: MQL5 Indicators/TrendTriggerMod_HTF/trendtriggermod_htf.mq5

TrendTriggerMod
Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 16711935, 8388352]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrendTriggerMod HTF'}, 'levels': [], 'description': ['TrendTriggerMod'], 'name': 'trendtriggermod_htf', 'source': 'MQL5 Indicators/TrendTriggerMod_HTF/trendtriggermod_htf.mq5', 'folder': 'TrendTriggerMod_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period (timeframe)', 'sinput': False}, {'mql': 'Regress', 'py': 'Regress', 'param': 'Regress', 'type': 'uint', 'default': 15, 'label': 'Period for finding extrema', 'sinput': False}, {'mql': 'TLength', 'py': 'TLength', 'param': 'TLength', 'type': 'uint', 'default': 5, 'label': 'Depth of the JMA smoothing', 'sinput': False}, {'mql': 'TPhase', 'py': 'TPhase', 'param': 'TPhase', 'type': 'int', 'default': -100, 'label': 'JMA smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'UpTriggerLevel', 'py': 'UpTriggerLevel', 'param': 'UpTriggerLevel', 'type': 'int', 'default': 50, 'label': 'Overbought level', 'sinput': False}, {'mql': 'DnTriggerLevel', 'py': 'DnTriggerLevel', 'param': 'DnTriggerLevel', 'type': 'int', 'default': -50, 'label': 'Oversold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period (timeframe)
Regress = _input('Regress', 15)  # Period for finding extrema
TLength = _input('TLength', 5)  # Depth of the JMA smoothing
TPhase = _input('TPhase', -100)  # JMA smoothing parameter
IPC = _input('IPC', PRICE_CLOSE_)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpTriggerLevel = _input('UpTriggerLevel', 50)  # Overbought level
DnTriggerLevel = _input('DnTriggerLevel', -50)  # Oversold level
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('TrendTriggerMod', TimeFrame):
        return INIT_FAILED
    min_rates_total = _int((Regress + 30) * (_idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) + 1))
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'TrendTriggerMod', Regress, TLength, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the TrendTriggerMod indicator')
        return INIT_FAILED
    IndInit(0, IndBuffer, 0.0, min_rates_total, Shift)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'TrendTriggerMod', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpTriggerLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnTriggerLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBrown)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer, 1, ColorIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, ColorBuffNumb, ColorIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
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
            Arr_ = Arr(1, 0.0, dyn=False)
            CArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, ColorBuffNumb, _DT(iTime_[bar]), 1, CArr) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
            ColorIndBuf[bar] = CArr[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
            ColorIndBuf[bar] = ColorIndBuf[bar + 1]
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


class TrendtriggermodHtf(_MQL5Indicator):
    name = 'trendtriggermod_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period (timeframe)
        'Regress': 15,  # Period for finding extrema
        'TLength': 5,  # Depth of the JMA smoothing
        'TPhase': -100,  # JMA smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'UpTriggerLevel': 50,  # Overbought level
        'DnTriggerLevel': -50,  # Oversold level
    }

