"""f2a_ao — converted from MQL5: MQL5 Indicators/F2a_AO/f2a_ao.mq5

semaphore indicator on the basis of NavelEMA
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [4678655], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'F2a_AO Sell', 2: 'F2a_AO Buy'}, 'levels': [], 'description': ['semaphore indicator on the basis of NavelEMA'], 'name': 'f2a_ao', 'source': 'MQL5 Indicators/F2a_AO/f2a_ao.mq5', 'folder': 'F2a_AO', 'inputs': [{'mql': 'MA_Filtr', 'py': 'MA_Filtr', 'param': 'MA_Filtr', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Fast', 'py': 'MA_Fast', 'param': 'MA_Fast', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MA_Slow', 'py': 'MA_Slow', 'param': 'MA_Slow', 'type': 'uint', 'default': 144, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Filtr = _input('MA_Filtr', 3)
MA_Fast = _input('MA_Fast', 13)
MA_Slow = _input('MA_Slow', 144)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
Value1 = Arr(0, 0.0)
Value2 = Arr(0, 0.0)

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
    global min_rates_total
    nshift = 3
    min_rates_total = _int(MathMax(MathMax(MA_Filtr, MA_Fast), MA_Slow) + nshift + 9)
    ArrayResize(Count, nshift)
    ArrayResize(Value1, nshift)
    ArrayResize(Value2, nshift)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value1, 0.0)
    ArrayInitialize(Value2, 0.0)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'F2a_AO'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_startbar, _s_OnCalculate_trend
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    series = 0.0
    fema = 0.0
    sema = 0.0
    current = 0.0
    prev = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 10
        _s_OnCalculate_startbar = first
        _s_OnCalculate_trend = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = ((close[bar] * 5) + (open[bar] * 2) + high[bar] + low[bar]) / 9
        fema = _s_OnCalculate_EMA1.EMASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, MA_Fast, series, bar, False)
        sema = _s_OnCalculate_EMA2.EMASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, MA_Slow, series, bar, False)
        Value1[Count[0]] = fema - sema
        Value2[Count[0]] = _s_OnCalculate_EMA3.EMASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, MA_Filtr, series, bar, False)
        current = Value2[Count[0]]
        prev = Value2[Count[1]]
        AvgRange = 0.0
        for count in range(bar, bar - 9 - 1, -1):
            AvgRange += MathAbs(high[count] - low[count])
        Range = AvgRange / 10
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_trend <= 0:
            if (Value1[Count[0]] > Value1[Count[1]] and current >= prev) and Value1[Count[1]] <= Value1[Count[2]]:
                BuyBuffer[bar] = low[bar] - (Range * 0.5)
                if bar < (rates_total - 1):
                    _s_OnCalculate_trend = 1
        if _s_OnCalculate_trend >= 0:
            if (Value1[Count[0]] < Value1[Count[1]] and current <= prev) and Value1[Count[1]] >= Value1[Count[2]]:
                SellBuffer[bar] = high[bar] + (Range * 0.5)
                if bar < (rates_total - 1):
                    _s_OnCalculate_trend = -1
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, 3)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_startbar = 0
_s_OnCalculate_trend = 0
_s_OnCalculate_EMA1 = CMoving_Average()
_s_OnCalculate_EMA2 = CMoving_Average()
_s_OnCalculate_EMA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class F2aAo(_MQL5Indicator):
    name = 'f2a_ao'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Filtr': 3,
        'MA_Fast': 13,
        'MA_Slow': 144,
    }

