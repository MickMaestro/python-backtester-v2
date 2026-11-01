"""parkinsonhistvolatility — converted from MQL5: MQL5 Indicators/ParkinsonHistVolatility/parkinsonhistvolatility.mq5

Copyright: Copyright © 2008, Victor Umnyashkin; Link: v354@hotbox.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Victor Umnyashkin', 'link': 'v354@hotbox.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 13382297, 16760576]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ParkinsonHistVolatility'}, 'levels': [], 'description': [], 'name': 'parkinsonhistvolatility', 'source': 'MQL5 Indicators/ParkinsonHistVolatility/parkinsonhistvolatility.mq5', 'folder': 'ParkinsonHistVolatility', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Trading_Day_In_Year', 'py': 'Trading_Day_In_Year', 'param': 'Trading_Day_In_Year', 'type': 'int', 'default': 365, 'label': '', 'sinput': False}, {'mql': 'Percent', 'py': 'Percent', 'param': 'Percent', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'Coeff', 'py': 'Coeff', 'param': 'Coeff', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Per = _input('Per', 21)
Trading_Day_In_Year = _input('Trading_Day_In_Year', 365)
Percent = _input('Percent', 100)
Coeff = _input('Coeff', 1.0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Hi = Arr(0, 0.0)
Lo = Arr(0, 0.0)
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
YearBase = 0
min_rates_total = 0

def OnInit():
    global YearBase, min_rates_total
    min_rates_total = Per + 1
    YearBase = _idiv(Trading_Day_In_Year * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    ArrayResize(Hi, Per)
    ArrayResize(Lo, Per)
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LineBuffer, True)
    SetIndexBuffer(1, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Parkinson Hi Vol(', Per, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    Volatility = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        for jj in range(0, Per):
            Hi[jj] = high[bar + jj]
            Lo[jj] = low[bar + jj]
        Volatility = WVHiVolParkinson(Per, Hi, Lo)
        LineBuffer[bar] = Volatility * MathSqrt((1.0 * YearBase) / Per) * Percent * Coeff
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorLineBuffer[bar] = 0.0
        if LineBuffer[bar] > LineBuffer[bar + 1]:
            ColorLineBuffer[bar] = 2.0
        if LineBuffer[bar] < LineBuffer[bar + 1]:
            ColorLineBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def WVHiVolParkinson(N, HiArr, LoArr):
    global _s_WVHiVolParkinson_Log2x4, _s_WVHiVolParkinson_first
    if _s_WVHiVolParkinson_first:
        _s_WVHiVolParkinson_first = False
        _s_WVHiVolParkinson_Log2x4 = 4 * MathLog(2.0)
    sum_ = 0.0
    for iii in range(0, N):
        sum_ += _fdiv(MathPow(MathLog(_fdiv(HiArr[iii], LoArr[iii])), 2), _s_WVHiVolParkinson_Log2x4)
    return MathSqrt(sum_)

# ---- static local variables
_s_WVHiVolParkinson_first = True
_s_WVHiVolParkinson_Log2x4 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Parkinsonhistvolatility(_MQL5Indicator):
    name = 'parkinsonhistvolatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Per': 21,
        'Trading_Day_In_Year': 365,
        'Percent': 100,
        'Coeff': 1.0,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

