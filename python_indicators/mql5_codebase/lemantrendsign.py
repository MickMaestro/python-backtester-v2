"""lemantrendsign — converted from MQL5: MQL5 Indicators/LeManTrendSign/lemantrendsign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'LeManTrend Sell', 2: 'LeManTrend Buy'}, 'levels': [], 'description': [], 'name': 'lemantrendsign', 'source': 'MQL5 Indicators/LeManTrendSign/lemantrendsign.mq5', 'folder': 'LeManTrendSign', 'inputs': [{'mql': 'Min', 'py': 'Min', 'param': 'Min', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Midle', 'py': 'Midle', 'param': 'Midle', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Max', 'py': 'Max', 'param': 'Max', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'PeriodEMA', 'py': 'PeriodEMA', 'param': 'PeriodEMA', 'type': 'int', 'default': 3, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Min = _input('Min', 13)
Midle = _input('Midle', 21)
Max = _input('Max', 34)
PeriodEMA = _input('PeriodEMA', 3)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
start = 0

def OnInit():
    global ATR_Handle, min_rates_total, start
    ATR_Period = 15
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    start = MathMax(MathMax(Min, Midle), Max)
    min_rates_total = start + PeriodEMA + 1
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LeManTrendSign(', Min, ', ', Midle, ', ', Max, ', ', PeriodEMA, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    maxbar = 0
    High1 = 0.0
    High2 = 0.0
    High3 = 0.0
    Low1 = 0.0
    Low2 = 0.0
    Low3 = 0.0
    HH = 0.0
    LL = 0.0
    ATR = Arr(0, 0.0)
    Bulls = 0.0
    Bears = 0.0
    trend = 0.0
    maxbar = rates_total - 1 - start
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        _s_OnCalculate_trend_prev = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
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
        Bulls = _s_OnCalculate_BULLS.MASeries(maxbar, prev_calculated, rates_total, PeriodEMA, MODE_EMA, HH, bar, True)
        Bears = _s_OnCalculate_BEARS.MASeries(maxbar, prev_calculated, rates_total, PeriodEMA, MODE_EMA, LL, bar, True)
        trend = Bulls - Bears
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_trend_prev <= 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_trend_prev >= 0 and trend < 0:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0.0
_s_OnCalculate_BULLS = CMoving_Average()
_s_OnCalculate_BEARS = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lemantrendsign(_MQL5Indicator):
    name = 'lemantrendsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Min': 13,
        'Midle': 21,
        'Max': 34,
        'PeriodEMA': 3,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

