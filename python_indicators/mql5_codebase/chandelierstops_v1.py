"""chandelierstops_v1 — converted from MQL5: MQL5 Indicators/ChandelierStops_v1Trend_x10/chandelierstops_v1.mq5

Copyright: Copyright © 2006, Forex-TSD.com ; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Forex-TSD.com ', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [65280], 2: [16711935], 3: [13422920], 4: [9639167]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'ChandelierStops Up', 2: 'ChandelierStops Down', 3: 'Buy ChandelierStops signal', 4: 'Sell ChandelierStops signal'}, 'levels': [], 'description': [''], 'name': 'chandelierstops_v1', 'source': 'MQL5 Indicators/ChandelierStops_v1Trend_x10/chandelierstops_v1.mq5', 'folder': 'ChandelierStops_v1Trend_x10', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 20)
ATRPeriod = _input('ATRPeriod', 10)
Kv = _input('Kv', 3.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
smin = Arr(0, 0.0)
smax = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = _int(ATRPeriod + Length)
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return 1
    ArrayResize(Count, Length)
    ArrayResize(smin, Length)
    ArrayResize(smax, Length)
    ArrayInitialize(smin, -999999)
    ArrayInitialize(smax, 999999)
    ArraySetAsSeries(smin, True)
    ArraySetAsSeries(smax, True)
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    shortname = Box("")
    StringConcatenate(shortname, 'ChandelierStops_v1(', Length, ', ', ATRPeriod, ', ', Kv, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    trend0 = 0.0
    ATR = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - _int(ATRPeriod)
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar0 = Count[0]
        bar1 = Count[1]
        smin[Count[0]] = high[ArrayMaximum(high, bar, ATRPeriod)] - (Kv * ATR[bar])
        smax[Count[0]] = low[ArrayMinimum(low, bar, ATRPeriod)] + (Kv * ATR[bar])
        trend0 = _s_OnCalculate_trend1
        if close[bar] > smax[Count[1]]:
            trend0 = 1.0
        if close[bar] < smin[Count[1]]:
            trend0 = -1.0
        if trend0 > 0:
            if smin[bar0] < smin[bar1]:
                smin[bar0] = smin[bar1]
            TrendUp[bar] = smin[bar0]
            TrendDown[bar] = 0.0
        if trend0 < 0:
            if smax[bar0] > smax[bar1]:
                smax[bar0] = smax[bar1]
            TrendUp[bar] = 0.0
            TrendDown[bar] = smax[bar0]
        if bar:
            Recount_ArrayZeroPos(Count, Length)
            _s_OnCalculate_trend1 = trend0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        if TrendDown[bar + 1] and TrendUp[bar]:
            SignUp[bar] = TrendUp[bar]
        if TrendUp[bar + 1] and TrendDown[bar]:
            SignDown[bar] = TrendDown[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_trend1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandelierstopsV1(_MQL5Indicator):
    name = 'chandelierstops_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 20,
        'ATRPeriod': 10,
        'Kv': 3.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

