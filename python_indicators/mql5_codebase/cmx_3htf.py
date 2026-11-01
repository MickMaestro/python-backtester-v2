"""cmx_3htf — converted from MQL5: MQL5 Indicators/CMx_3HTF/cmx_3htf.mq5

Three CMx oscillators with different timeframes with the same parameters on one chart.
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.50

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.50', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [13850042], 3: [7451452]}, 'widths': {1: 2, 2: 3, 3: 5}, 'styles': {}, 'labels': {1: 'CMx 1', 2: 'CMx 2', 3: 'CMx 3'}, 'levels': [], 'description': ['Three CMx oscillators with different timeframes with the same parameters on one chart.'], 'name': 'cmx_3htf', 'source': 'MQL5 Indicators/CMx_3HTF/cmx_3htf.mq5', 'folder': 'CMx_3HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 30, 'label': 'Indicator 1 chart period (smallest timeframe)', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Indicator 2 chart period (medium timeframe)', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'Indicator 3 chart period (highest timeframe)', 'sinput': False}, {'mql': 'F', 'py': 'F', 'param': 'F', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.682, 'label': '', 'sinput': False}, {'mql': 'L_adx', 'py': 'L_adx', 'param': 'L_adx', 'type': 'double', 'default': 18.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 423.6, 'label': 'Level 1', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 261.8, 'label': 'Level 2', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 161.8, 'label': 'Level 3', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 61.8, 'label': 'Level 4', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.0, 'label': 'Level 5', 'sinput': False}, {'mql': 'Level6', 'py': 'Level6', 'param': 'Level6', 'type': 'double', 'default': -61.8, 'label': 'Level 6', 'sinput': False}, {'mql': 'Level7', 'py': 'Level7', 'param': 'Level7', 'type': 'double', 'default': -161.8, 'label': 'Level 7', 'sinput': False}, {'mql': 'Level8', 'py': 'Level8', 'param': 'Level8', 'type': 'double', 'default': -261.8, 'label': 'Level 8', 'sinput': False}, {'mql': 'Level9', 'py': 'Level9', 'param': 'Level9', 'type': 'double', 'default': -423.6, 'label': 'Level 9', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_M30)  # Indicator 1 chart period (smallest timeframe)
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Indicator 2 chart period (medium timeframe)
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # Indicator 3 chart period (highest timeframe)
F = _input('F', 12)
k = _input('k', 1.682)
L_adx = _input('L_adx', 18.0)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Level1 = _input('Level1', 423.6)  # Level 1
Level2 = _input('Level2', 261.8)  # Level 2
Level3 = _input('Level3', 161.8)  # Level 3
Level4 = _input('Level4', 61.8)  # Level 4
Level5 = _input('Level5', 0.0)  # Level 5
Level6 = _input('Level6', -61.8)  # Level 6
Level7 = _input('Level7', -161.8)  # Level 7
Level8 = _input('Level8', -261.8)  # Level 8
Level9 = _input('Level9', -423.6)  # Level 9
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
    if not TimeFramesCheck('CMx', TimeFrame1, TimeFrame2, TimeFrame3):
        return INIT_FAILED
    min_rates_total = 2
    Ind1_Handle = iCustom(Symbol(), TimeFrame1, 'CMx', F, k, L_adx, 0)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of CMx 1')
        return INIT_FAILED
    Ind2_Handle = iCustom(Symbol(), TimeFrame2, 'CMx', F, k, L_adx, 0)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of CMx 2')
        return INIT_FAILED
    Ind3_Handle = iCustom(Symbol(), TimeFrame3, 'CMx', F, k, L_adx, 0)
    if Ind3_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of CMx 3')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, 0.0, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, 0.0, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'CMx', '(', GetStringTimeframe(TimeFrame1), ', ', GetStringTimeframe(TimeFrame2), ', ', GetStringTimeframe(TimeFrame3), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 9)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Level2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, Level3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, Level4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, Level5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, Level6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, Level7)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 7, Level8)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 8, Level9)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 5, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 6, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 7, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 8, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 5, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 6, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 7, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 8, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind1_Handle) < Bars(Symbol(), TimeFrame1):
        return prev_calculated
    if BarsCalculated(Ind2_Handle) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    if BarsCalculated(Ind3_Handle) < Bars(Symbol(), TimeFrame3):
        return prev_calculated
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
            IndBuf[bar] = Arr_[0]
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


class Cmx3htf(_MQL5Indicator):
    name = 'cmx_3htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Indicator 1 chart period (smallest timeframe)
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Indicator 2 chart period (medium timeframe)
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator 3 chart period (highest timeframe)
        'F': 12,
        'k': 1.682,
        'L_adx': 18.0,
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'Level1': 423.6,  # Level 1
        'Level2': 261.8,  # Level 2
        'Level3': 161.8,  # Level 3
        'Level4': 61.8,  # Level 4
        'Level5': 0.0,  # Level 5
        'Level6': -61.8,  # Level 6
        'Level7': -161.8,  # Level 7
        'Level8': -261.8,  # Level 8
        'Level9': -423.6,  # Level 9
    }

