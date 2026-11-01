"""colorlemantrend — converted from MQL5: MQL5 Indicators/LeManTrend/colorlemantrend.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [8421376, 16711935], 2: [14822282], 3: [14822282]}, 'widths': {2: 1, 3: 1}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'LeManTrend', 2: 'LeManTrend Bulls', 3: 'LeManTrend Bears'}, 'levels': [], 'description': [], 'name': 'colorlemantrend', 'source': 'MQL5 Indicators/LeManTrend/colorlemantrend.mq5', 'folder': 'LeManTrend', 'inputs': [{'mql': 'Min', 'py': 'Min', 'param': 'Min', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Midle', 'py': 'Midle', 'param': 'Midle', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Max', 'py': 'Max', 'param': 'Max', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'PeriodEMA', 'py': 'PeriodEMA', 'param': 'PeriodEMA', 'type': 'int', 'default': 3, 'label': 'Indicator period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Min = _input('Min', 13)
Midle = _input('Midle', 21)
Max = _input('Max', 34)
PeriodEMA = _input('PeriodEMA', 3)  # Indicator period
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer_ = Arr(0, 0.0)
BearsBuffer_ = Arr(0, 0.0)
min_rates_total = 0
start = 0

def OnInit():
    global min_rates_total, start
    start = MathMax(MathMax(Min, Midle), Max)
    min_rates_total = start + PeriodEMA
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BearsBuffer, True)
    SetIndexBuffer(2, BullsBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer_, True)
    SetIndexBuffer(3, BearsBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BearsBuffer_, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LeManTrend(', Min, ', ', Midle, ', ', Max, ', ', PeriodEMA, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    High = 0.0
    Low = 0.0
    HH = 0.0
    LL = 0.0
    Bulls = 0.0
    Bears = 0.0
    maxbar = rates_total - 1 - start
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        High = 0.0
        High += high[ArrayMaximum(high, bar + 1, Min)]
        High += high[ArrayMaximum(high, bar + 1, Midle)]
        High += high[ArrayMaximum(high, bar + 1, Max)]
        HH = (3 * high[bar]) - High
        Low = 0.0
        Low += low[ArrayMinimum(low, bar + 1, Min)]
        Low += low[ArrayMinimum(low, bar + 1, Midle)]
        Low += low[ArrayMinimum(low, bar + 1, Max)]
        LL = Low - (3 * low[bar])
        Bulls = _s_OnCalculate_BULLS.MASeries(maxbar, prev_calculated, rates_total, PeriodEMA, MODE_EMA, HH, bar, True)
        Bears = _s_OnCalculate_BEARS.MASeries(maxbar, prev_calculated, rates_total, PeriodEMA, MODE_EMA, LL, bar, True)
        BullsBuffer[bar] = Bulls
        BearsBuffer[bar] = Bears
        BullsBuffer_[bar] = Bulls
        BearsBuffer_[bar] = Bears
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_BULLS = CMoving_Average()
_s_OnCalculate_BEARS = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorlemantrend(_MQL5Indicator):
    name = 'colorlemantrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Min': 13,
        'Midle': 21,
        'Max': 34,
        'PeriodEMA': 3,  # Indicator period
    }

