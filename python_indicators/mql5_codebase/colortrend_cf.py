"""colortrend_cf — converted from MQL5: MQL5 Indicators/ColorTrend_CF_HTF/colortrend_cf.mq5

Copyright: Converted by and Copyright: Ronald Verwer/ROVERCOM; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Converted by and Copyright: Ronald Verwer/ROVERCOM', 'link': '', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [7451452, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Trend_CF'}, 'levels': [], 'description': [], 'name': 'colortrend_cf', 'source': 'MQL5 Indicators/ColorTrend_CF_HTF/colortrend_cf.mq5', 'folder': 'ColorTrend_CF_HTF', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_ = _input('Period_', 30)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
StartBar = 0
x_p = Arr(0, 0.0)
x_n = Arr(0, 0.0)
y_p = Arr(0, 0.0)
y_n = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = _int(Period_) - 1
    for iii in range(0, _int(Period_)):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > (_int(Period_) - 1):
            numb -= _int(Period_)
        CoArr[iii] = numb

def OnInit():
    global StartBar
    StartBar = _int(Period_)
    ArrayResize(x_p, Period_)
    ArrayResize(x_n, Period_)
    ArrayResize(y_p, Period_)
    ArrayResize(y_n, Period_)
    ArrayResize(Count, Period_)
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Trend_CF(', Period_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (StartBar + begin):
        return 0
    first = 0
    bar = 0
    bar0 = 0
    bar1 = 0
    barq = 0
    chp = 0.0
    chn = 0.0
    cffp = 0.0
    cffn = 0.0
    dprice = 0.0
    if prev_calculated == 0:
        first = 1 + begin
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice = price[bar] - price[bar - 1]
        bar0 = Count[0]
        bar1 = Count[1]
        if dprice > 0:
            x_p[bar0] = dprice
            y_p[bar0] = x_p[bar0] + y_p[bar1]
            x_n[bar0] = 0.0
            y_n[bar0] = 0.0
        else:
            x_n[bar0] = -dprice
            y_n[bar0] = x_n[bar0] + y_n[bar1]
            x_p[bar0] = 0.0
            y_p[bar0] = 0.0
        if bar < (StartBar + begin):
            if bar < (rates_total - 1):
                Recount_ArrayZeroPos(Count)
            continue
        chp = 0.0
        chn = 0.0
        cffp = 0.0
        cffn = 0.0
        for q in range(_int(Period_) - 1, 0 - 1, -1):
            barq = Count[q]
            chp += x_p[barq]
            chn += x_n[barq]
            cffp += y_p[barq]
            cffn += y_n[barq]
        UpperBuffer[bar] = _fdiv(chp - cffn, Point())
        LowerBuffer[bar] = _fdiv(chn - cffp, Point())
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColortrendCf(_MQL5Indicator):
    name = 'colortrend_cf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 30,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

