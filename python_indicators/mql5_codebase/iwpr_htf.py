"""iwpr_htf — converted from MQL5: MQL5 Indicators/iWPR_HTF/iwpr_htf.mq5

Larry Williams' Percent Range
Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_maximum': 0.0, 'indicator_minimum': -100.0}, 'types': {1: 2}, 'colors': {1: [14822282]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [-80.0, -20.0], 'description': ["Larry Williams' Percent Range"], 'name': 'iwpr_htf', 'source': 'MQL5 Indicators/iWPR_HTF/iwpr_htf.mq5', 'folder': 'iWPR_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'WPR_Period', 'py': 'WPR_Period', 'param': 'WPR_Period', 'type': 'uint', 'default': 14, 'label': 'Period of averaging', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
WPR_Period = _input('WPR_Period', 14)  # Period of averaging
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
Init = False
Symbol_ = ""
Word = ""
Ind_Handle = 0
min_rates_total = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Init, Symbol_, Word, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('iWPR indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Ind_Handle = iWPR(None, TimeFrame, WPR_Period)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR indicator')
        return INIT_FAILED
    min_rates_total = _int(_idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) * (WPR_Period + 3))
    Symbol_ = Symbol()
    Word = 'iWPR' + '(' + Symbol_ + ',' + GetStringTimeframe(TimeFrame) + ',' + _str(WPR_Period) + ')'
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, Word)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if (BarsCalculated(Ind_Handle) < 2 or rates_total < min_rates_total) or (not Init):
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    iWpr = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
        _s_OnCalculate_LastCountBar = limit
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar + 1] = EMPTY_VALUE
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar + 1]), 1, iWpr) <= 0:
                return 0
            _s_OnCalculate_LastCountBar = bar
            IndBuffer[bar + 1] = iWpr[0]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if CopyBuffer(Ind_Handle, 0, _DT(time[0]), 1, iWpr) <= 0:
        return 0
    IndBuffer[0] = iWpr[0]
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IwprHtf(_MQL5Indicator):
    name = 'iwpr_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'WPR_Period': 14,  # Period of averaging
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (-100.0, 0.0)

