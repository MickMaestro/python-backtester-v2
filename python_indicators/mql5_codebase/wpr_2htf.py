"""wpr_2htf — converted from MQL5: MQL5 Indicators/WPR_2HTF/wpr_2htf.mq5

A colored cloud made of WPR oscillators with different timeframes on one chart.
Copyright: Copyright © 2006, lukas1; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, lukas1', 'link': '', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [64636, 36095]}, 'widths': {}, 'styles': {}, 'labels': {1: 'WPR_2HTF'}, 'levels': [-20.0, -50.0, -80.0], 'description': ['A colored cloud made of WPR oscillators with different timeframes on one chart.'], 'name': 'wpr_2htf', 'source': 'MQL5 Indicators/WPR_2HTF/wpr_2htf.mq5', 'folder': 'WPR_2HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 15, 'label': 'Indicator 1 chart period (lower timeframe)', 'sinput': False}, {'mql': 'WPRPeriod1', 'py': 'WPRPeriod1', 'param': 'WPRPeriod1', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16388, 'label': 'Indicator 2 chart period (higher timeframe)', 'sinput': False}, {'mql': 'WPRPeriod2', 'py': 'WPRPeriod2', 'param': 'WPRPeriod2', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_M15)  # Indicator 1 chart period (lower timeframe)
WPRPeriod1 = _input('WPRPeriod1', 7)
TimeFrame2 = _input('TimeFrame2', PERIOD_H4)  # Indicator 2 chart period (higher timeframe)
WPRPeriod2 = _input('WPRPeriod2', 7)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind1_Handle = 0
Ind2_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind1_Handle, Ind2_Handle, min_rates_total
    if not TimeFramesCheck('WPR', TimeFrame1, TimeFrame2):
        return INIT_FAILED
    min_rates_total = 2
    Ind1_Handle = iWPR(Symbol(), TimeFrame1, WPRPeriod1)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the WPR 1 indicator')
        return INIT_FAILED
    Ind2_Handle = iWPR(Symbol(), TimeFrame2, WPRPeriod2)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the WPR 2 indicator')
        return INIT_FAILED
    IndInit(0, Ind1Buffer)
    IndInit(1, Ind2Buffer)
    PlotInit(0, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'WPR', '(', GetStringTimeframe(TimeFrame1), ', ', GetStringTimeframe(TimeFrame2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind1_Handle) < Bars(Symbol(), TimeFrame1):
        return prev_calculated
    if BarsCalculated(Ind2_Handle) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame1, Ind1_Handle, 0, Ind1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame2, Ind2_Handle, 0, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame1, TFrame2):
    if TFrame1 < Period() and TFrame1 != PERIOD_CURRENT:
        Print('Chart 1 period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    if TFrame2 <= TFrame1:
        Print('Chart 2 period for the ' + IndName + ' indicator should be greater than the period of chart 1!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(2, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wpr2htf(_MQL5Indicator):
    name = 'wpr_2htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=15),  # Indicator 1 chart period (lower timeframe)
        'WPRPeriod1': 7,
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator 2 chart period (higher timeframe)
        'WPRPeriod2': 7,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

