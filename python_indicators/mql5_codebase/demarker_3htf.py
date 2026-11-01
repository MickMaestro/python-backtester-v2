"""demarker_3htf — converted from MQL5: MQL5 Indicators/DeMarker_3HTF/demarker_3htf.mq5

Three DeMarker indicators with different timeframes with the same parameters on one chart.
Copyright: Copyright © 2013, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [32896], 3: [2763429]}, 'widths': {1: 2, 2: 3, 3: 5}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME+"1"', 2: 'INDICATOR_NAME+"2"', 3: 'INDICATOR_NAME+"3"'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Three DeMarker indicators with different timeframes with the same parameters on one chart.'], 'name': 'demarker_3htf', 'source': 'MQL5 Indicators/DeMarker_3HTF/demarker_3htf.mq5', 'folder': 'DeMarker_3HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 30, 'label': 'Indicator 1 chart period (smallest timeframe)', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Indicator 2 chart period (medium timeframe)', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'Indicator 3 chart period (highest timeframe)', 'sinput': False}, {'mql': 'DeMarkerPeriod', 'py': 'DeMarkerPeriod', 'param': 'DeMarkerPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_M30)  # Indicator 1 chart period (smallest timeframe)
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Indicator 2 chart period (medium timeframe)
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # Indicator 3 chart period (highest timeframe)
DeMarkerPeriod = _input('DeMarkerPeriod', 14)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind1_Handle = 0
Ind2_Handle = 0
Ind3_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind1_Handle, Ind2_Handle, Ind3_Handle, min_rates_total
    if not TimeFramesCheck('DeMarker', TimeFrame1, TimeFrame2, TimeFrame3):
        return INIT_FAILED
    min_rates_total = 2
    Ind1_Handle = iDeMarker(Symbol(), TimeFrame1, DeMarkerPeriod)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Failed to get the DeMarker 1 indicator handle')
        return INIT_FAILED
    Ind2_Handle = iDeMarker(Symbol(), TimeFrame2, DeMarkerPeriod)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Failed to get the DeMarker 2 indicator handle')
        return INIT_FAILED
    Ind3_Handle = iDeMarker(Symbol(), TimeFrame3, DeMarkerPeriod)
    if Ind3_Handle == INVALID_HANDLE:
        Print(' Failed to get the DeMarker 3 indicator handle')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, 0.0, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, 0.0, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'DeMarker', '(', GetStringTimeframe(TimeFrame1), ', ', GetStringTimeframe(TimeFrame2), ', ', GetStringTimeframe(TimeFrame3), ', ', DeMarkerPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame1, Ind1_Handle, 0, Ind1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame2, Ind2_Handle, 0, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame3, Ind3_Handle, 0, Ind3Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

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
            IndBuf[bar] = Arr_[0] * 100
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame1, TFrame2, TFrame3):
    if TFrame1 < Period() and TFrame1 != PERIOD_CURRENT:
        Print('Chart 1 period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    if TFrame2 <= TFrame1:
        Print('Chart 2 period for the ' + IndName + ' indicator should be greater than the period of chart 1')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    if TFrame3 <= TFrame2:
        Print('Chart 3 period for the ' + IndName + ' indicator should be greater than the period of chart 2!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Demarker3htf(_MQL5Indicator):
    name = 'demarker_3htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Indicator 1 chart period (smallest timeframe)
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Indicator 2 chart period (medium timeframe)
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator 3 chart period (highest timeframe)
        'DeMarkerPeriod': 14,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

