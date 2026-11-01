"""lemantrendhist — converted from MQL5: MQL5 Indicators/LeManTrendHist/lemantrendhist.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 2330219, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LeManTrend'}, 'levels': [], 'description': [], 'name': 'lemantrendhist', 'source': 'MQL5 Indicators/LeManTrendHist/lemantrendhist.mq5', 'folder': 'LeManTrendHist', 'inputs': [{'mql': 'Min', 'py': 'Min', 'param': 'Min', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Midle', 'py': 'Midle', 'param': 'Midle', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Max', 'py': 'Max', 'param': 'Max', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'PeriodEMA', 'py': 'PeriodEMA', 'param': 'PeriodEMA', 'type': 'int', 'default': 3, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'XMethod', 'py': 'XMethod', 'param': 'XMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания  индикатора', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'Глубина сглаживания индикатора', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Min = _input('Min', 13)
Midle = _input('Midle', 21)
Max = _input('Max', 34)
PeriodEMA = _input('PeriodEMA', 3)  # Период индикатора
XMethod = _input('XMethod', MODE_JJMA)  # Метод сглаживания  индикатора
XLength = _input('XLength', 5)  # Глубина сглаживания индикатора
XPhase = _input('XPhase', 100)  # Параметр сглаживания индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = MathMax(MathMax(Min, Midle), Max) + 1
    min_rates_2 = GetStartBars(XMethod, XLength, XPhase)
    min_rates_total = min_rates_1 + min_rates_2 + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LeManTrend(', Min, ', ', Midle, ', ', Max, ', ', PeriodEMA, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    clr = 0
    High1 = 0.0
    High2 = 0.0
    High3 = 0.0
    Low1 = 0.0
    Low2 = 0.0
    Low3 = 0.0
    HH = 0.0
    LL = 0.0
    Bulls = 0.0
    Bears = 0.0
    Range = 0.0
    XRange = 0.0
    maxbar1 = rates_total - min_rates_1 - 1
    maxbar2 = maxbar1 - min_rates_2
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        High1 = high[ArrayMaximum(high, bar + 1, Min)]
        High2 = high[ArrayMaximum(high, bar + 1, Midle)]
        High3 = high[ArrayMaximum(high, bar + 1, Max)]
        HH = high[bar] - High1 + (high[bar] - High2) + (high[bar] - High3)
        Low1 = low[ArrayMinimum(low, bar + 1, Min)]
        Low2 = low[ArrayMinimum(low, bar + 1, Midle)]
        Low3 = low[ArrayMinimum(low, bar + 1, Max)]
        LL = Low1 - low[bar] + (Low2 - low[bar]) + (Low3 - low[bar])
        Bulls = _s_OnCalculate_BULLS.MASeries(maxbar1, prev_calculated, rates_total, PeriodEMA, MODE_EMA, HH, bar, True)
        Bears = _s_OnCalculate_BEARS.MASeries(maxbar1, prev_calculated, rates_total, PeriodEMA, MODE_EMA, LL, bar, True)
        Range = Bulls - Bears
        XRange = _s_OnCalculate_SMOOTH.XMASeries(maxbar1, prev_calculated, rates_total, XMethod, XPhase, XLength, Range, bar, True)
        IndBuffer[bar] = XRange
        clr = 2
        if XRange > 0:
            if XRange > IndBuffer[bar + 1]:
                clr = 4
            if XRange < IndBuffer[bar + 1]:
                clr = 3
        if XRange < 0:
            if XRange < IndBuffer[bar + 1]:
                clr = 0
            if XRange > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_BULLS = CMoving_Average()
_s_OnCalculate_BEARS = CMoving_Average()
_s_OnCalculate_SMOOTH = CXMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lemantrendhist(_MQL5Indicator):
    name = 'lemantrendhist'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Min': 13,
        'Midle': 21,
        'Max': 34,
        'PeriodEMA': 3,  # Период индикатора
        'XMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания  индикатора
        'XLength': 5,  # Глубина сглаживания индикатора
        'XPhase': 100,  # Параметр сглаживания индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

