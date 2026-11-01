"""prevdayandfloatingpivot — converted from MQL5: MQL5 Indicators/PrevDayAndFloatingPivot_HTF/prevdayandfloatingpivot.mq5

Copyright: Copyright © 2006, mbkennel@gmail.com; Link: http://www.metatrader.org; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, mbkennel@gmail.com', 'link': 'http://www.metatrader.org', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [9639167], 2: [14822282]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Previous Day Pivot', 2: 'Floating current pivot'}, 'levels': [], 'description': [], 'name': 'prevdayandfloatingpivot', 'source': 'MQL5 Indicators/PrevDayAndFloatingPivot_HTF/prevdayandfloatingpivot.mq5', 'folder': 'PrevDayAndFloatingPivot_HTF', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def TodaysHighestLowest(Time, High, Low, shift, H, L):
    global _s_TodaysHighestLowest_Max, _s_TodaysHighestLowest_start
    if _s_TodaysHighestLowest_start:
        _s_TodaysHighestLowest_Max = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
        _s_TodaysHighestLowest_start = False
    tbs = TodaysBarShift(Time, shift)
    if tbs < 0:
        return -1
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(None, PERIOD_D1, tbs, 1, iTime_) <= 0:
        return -1
    H.v = High[shift]
    L.v = Low[shift]
    j = shift + 1
    while Time[j] >= iTime_[0]:
        Ht = High[j]
        Lt = Low[j]
        H.v = MathMax(H.v, Ht)
        L.v = MathMin(L.v, Lt)
        j += 1
        if (j - shift) > _s_TodaysHighestLowest_Max:
            Print('TodaysHighestLowest' + '(): Shit!')
            break
    return 1

def PreviousNonSundayBarShift(Time, shift):
    tbs = TodaysBarShift(Time, shift)
    if tbs < 0:
        return -1
    ybs = tbs + 1
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(None, PERIOD_D1, ybs, 1, iTime_) <= 0:
        return -1
    tm = MqlDateTime()
    TimeToStruct(iTime_[0], tm)
    if tm.day_of_week == SUNDAY:
        ybs += 1
    return ybs

def TodaysBarShift(Time, shift):
    idaybarshift = iBarShift_u("", PERIOD_D1, Time[shift])
    if idaybarshift < 0:
        return -1
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(None, PERIOD_D1, idaybarshift, 1, iTime_) <= 0:
        return -1
    if iTime_[0] > Time[shift]:
        idaybarshift += 1
    return idaybarshift

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def OnInit():
    global min_rates_total
    min_rates_total = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer1, True)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer2, True)
    shortname = Box("")
    StringConcatenate(shortname, 'PrevDayAndFloatingPivot(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    iHigh_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
    iOpen_ = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ybs = PreviousNonSundayBarShift(time, bar)
        if ybs < 0:
            return prev_calculated
        tdbar = TodaysBarShift(time, bar)
        if tdbar < 0:
            return prev_calculated
        if CopyOpen(None, PERIOD_D1, ybs, 1, iOpen_) <= 0:
            return prev_calculated
        if CopyLow(None, PERIOD_D1, ybs, 1, iLow_) <= 0:
            return prev_calculated
        if CopyHigh(None, PERIOD_D1, ybs, 1, iHigh_) <= 0:
            return prev_calculated
        if CopyClose(None, PERIOD_D1, tdbar, 1, iClose_) <= 0:
            return prev_calculated
        p = (iHigh_[0] + iLow_[0] + iClose_[0] + iOpen_[0]) * 0.25
        TH = Box(0.0)
        TL = Box(0.0)
        if TodaysHighestLowest(time, high, low, bar, TH, TL) < 0:
            return prev_calculated
        flp = (TH.v + TL.v + close[bar]) * 0.33333
        ExtMapBuffer1[bar] = p
        ExtMapBuffer2[bar] = flp
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_TodaysHighestLowest_Max = 0
_s_TodaysHighestLowest_start = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Prevdayandfloatingpivot(_MQL5Indicator):
    name = 'prevdayandfloatingpivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

