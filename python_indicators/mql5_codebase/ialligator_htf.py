"""ialligator_htf — converted from MQL5: MQL5 Indicators/iAlligator_HTF/ialligator_htf.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 2, 2: 2, 3: 2}, 'colors': {1: [16711680], 2: [255], 3: [65280]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Jaws', 2: 'Teeth', 3: 'Lips'}, 'levels': [], 'description': [], 'name': 'ialligator_htf', 'source': 'MQL5 Indicators/iAlligator_HTF/ialligator_htf.mq5', 'folder': 'iAlligator_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'JawsPeriod', 'py': 'JawsPeriod', 'param': 'JawsPeriod', 'type': 'int', 'default': 13, 'label': 'Jaws period', 'sinput': False}, {'mql': 'JawsShift', 'py': 'JawsShift', 'param': 'JawsShift', 'type': 'int', 'default': 8, 'label': 'Jaws shift', 'sinput': False}, {'mql': 'TeethPeriod', 'py': 'TeethPeriod', 'param': 'TeethPeriod', 'type': 'int', 'default': 8, 'label': 'Teeth period', 'sinput': False}, {'mql': 'TeethShift', 'py': 'TeethShift', 'param': 'TeethShift', 'type': 'int', 'default': 5, 'label': 'Teeth shift', 'sinput': False}, {'mql': 'LipsPeriod', 'py': 'LipsPeriod', 'param': 'LipsPeriod', 'type': 'int', 'default': 5, 'label': 'Lips period', 'sinput': False}, {'mql': 'LipsShift', 'py': 'LipsShift', 'param': 'LipsShift', 'type': 'int', 'default': 3, 'label': 'Lips shift', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 2, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 5, 'label': 'price constant', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
JawsPeriod = _input('JawsPeriod', 13)  # Jaws period
JawsShift = _input('JawsShift', 8)  # Jaws shift
TeethPeriod = _input('TeethPeriod', 8)  # Teeth period
TeethShift = _input('TeethShift', 5)  # Teeth shift
LipsPeriod = _input('LipsPeriod', 5)  # Lips period
LipsShift = _input('LipsShift', 3)  # Lips shift
MA_Method = _input('MA_Method', MODE_SMMA)  # smoothing method
Applied_price = _input('Applied_price', PRICE_MEDIAN)  # price constant
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in points
ExtJaws = Arr(0, 0.0)
ExtTeeth = Arr(0, 0.0)
ExtLips = Arr(0, 0.0)
Init = False
dPriceShift = 0.0
Symbol_ = ""
Word = ""
Ind_Handle = 0
min_rates_total = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Init, Symbol_, Word, dPriceShift, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('iAlligator indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Ind_Handle = iAlligator(None, TimeFrame, JawsPeriod, 0, TeethPeriod, 0, LipsPeriod, 0, MA_Method, Applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iAlligator indicator')
        return INIT_FAILED
    perratio = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    min_rates_total = _int(perratio * (MathMax(MathMax(JawsPeriod, TeethPeriod), LipsPeriod) + 3))
    Symbol_ = Symbol()
    Word = 'iAlligator' + '(' + Symbol_ + ',' + GetStringTimeframe(TimeFrame) + ')'
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, ExtJaws, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, JawsPeriod + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_SHIFT, _int(perratio * JawsShift))
    ArraySetAsSeries(ExtJaws, True)
    SetIndexBuffer(1, ExtTeeth, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, TeethPeriod + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_SHIFT, _int(perratio * TeethShift))
    ArraySetAsSeries(ExtTeeth, True)
    SetIndexBuffer(2, ExtLips, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, LipsPeriod + 1)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_SHIFT, _int(perratio * LipsShift))
    ArraySetAsSeries(ExtLips, True)
    IndicatorSetString(INDICATOR_SHORTNAME, Word)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if (BarsCalculated(Ind_Handle) < 2 or rates_total < min_rates_total) or (not Init):
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    iMa = Arr(1, 0.0, dyn=False)
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
        ExtJaws[bar + 1] = 0.0
        ExtTeeth[bar + 1] = 0.0
        ExtLips[bar + 1] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            if CopyBuffer(Ind_Handle, GATORJAW_LINE, _DT(time[bar + 1]), 1, iMa) <= 0:
                return 0
            ExtJaws[bar + 1] = iMa[0] + dPriceShift
            if CopyBuffer(Ind_Handle, GATORTEETH_LINE, _DT(time[bar + 1]), 1, iMa) <= 0:
                return 0
            ExtTeeth[bar + 1] = iMa[0] + dPriceShift
            if CopyBuffer(Ind_Handle, GATORLIPS_LINE, _DT(time[bar + 1]), 1, iMa) <= 0:
                return 0
            ExtLips[bar + 1] = iMa[0] + dPriceShift
            _s_OnCalculate_LastCountBar = bar
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if CopyBuffer(Ind_Handle, GATORJAW_LINE, _DT(time[0]), 1, iMa) <= 0:
        return 0
    ExtJaws[0] = iMa[0] + dPriceShift
    if CopyBuffer(Ind_Handle, GATORTEETH_LINE, _DT(time[0]), 1, iMa) <= 0:
        return 0
    ExtTeeth[0] = iMa[0] + dPriceShift
    if CopyBuffer(Ind_Handle, GATORLIPS_LINE, _DT(time[0]), 1, iMa) <= 0:
        return 0
    ExtLips[0] = iMa[0] + dPriceShift
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IalligatorHtf(_MQL5Indicator):
    name = 'ialligator_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'JawsPeriod': 13,  # Jaws period
        'JawsShift': 8,  # Jaws shift
        'TeethPeriod': 8,  # Teeth period
        'TeethShift': 5,  # Teeth shift
        'LipsPeriod': 5,  # Lips period
        'LipsShift': 3,  # Lips shift
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # smoothing method
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # price constant
        'PriceShift': 0,  # vertical shift of the indicator in points
    }

