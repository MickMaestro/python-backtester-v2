"""st_lregr — converted from MQL5: MQL5 Indicators/St_LRegr/st_lregr.mq5

Indicator of the linear regression channel
Copyright: Copyright © 2009, Stajer59; Link: http://www.stajer59.ucoz.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Stajer59', 'link': 'http://www.stajer59.ucoz.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [255], 2: [8388736], 3: [255], 4: [16711680], 5: [16711680], 6: [255], 7: [8388736]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, 'labels': {1: 'St_LRegression chanell', 2: '+3Sigma', 3: '+2Sigma', 4: '+1Sigma', 5: '-1Sigma', 6: '-2Sigma', 7: '-3Sigma'}, 'levels': [], 'description': ['Indicator of the linear regression channel'], 'name': 'st_lregr', 'source': 'MQL5 Indicators/St_LRegr/st_lregr.mq5', 'folder': 'St_LRegr', 'inputs': [{'mql': 'N_', 'py': 'N_', 'param': 'N_', 'type': 'uint', 'default': 240, 'label': 'number of candles for analyze', 'sinput': False}, {'mql': 'StdDev', 'py': 'StdDev', 'param': 'StdDev', 'type': 'double', 'default': 1.0, 'label': 'deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N_ = _input('N_', 240)  # number of candles for analyze
StdDev = _input('StdDev', 1.0)  # deviation
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
LineBuffer = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
quotient2 = 0.0
quotient3 = 0.0
dPriceShift = 0.0
min_rates_total = 0
N = 0

def OnInit():
    global N, dPriceShift, min_rates_total
    N = _int(N_)
    min_rates_total = N
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(LineBuffer, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer6, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    shortname = Box("")
    StringConcatenate(shortname, 'St_LRegression chanell(', N, ', ', DoubleToString(StdDev, 2), ', ', Shift, ', ', PriceShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    j = 0
    x = 0
    drawbegin = 0
    a = 0.0
    b = 0.0
    Summ_x = 0.0
    Summ_y = 0.0
    Summ_x_2 = 0.0
    Summ_xy = 0.0
    Deviation = 0.0
    StdDeviation = 0.0
    Middle_y = 0.0
    drawbegin = rates_total - 1 - N
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, drawbegin)
    ArraySetAsSeries(close, True)
    Summ_x = 0.0
    Summ_y = 0.0
    Summ_xy = 0.0
    Summ_x_2 = 0.0
    x = 1
    for x in range(x, N + 1):
        j = N - x
        Summ_x += x
        Summ_y += close[j]
        Summ_xy += x * close[j]
        Summ_x_2 += MathPow(x, 2)
    else:
        x = _range_end(x, N + 1, 1)
    b = _fdiv((N * Summ_xy) - (Summ_x * Summ_y), (N * Summ_x_2) - MathPow(Summ_x, 2))
    a = _fdiv(Summ_y - (b * Summ_x), N)
    Middle_y = _fdiv(Summ_y, N)
    Deviation = 0.0
    x = 0
    for x in range(x, N):
        j = N - x
        Deviation += MathPow(close[j] - Middle_y, 2)
    else:
        x = _range_end(x, N, 1)
    StdDeviation = MathSqrt(_fdiv(Deviation, N))
    ExtLineBuffer1[N] = EMPTY_VALUE
    ExtLineBuffer2[N] = EMPTY_VALUE
    ExtLineBuffer3[N] = EMPTY_VALUE
    ExtLineBuffer4[N] = EMPTY_VALUE
    ExtLineBuffer5[N] = EMPTY_VALUE
    ExtLineBuffer6[N] = EMPTY_VALUE
    LineBuffer[N] = EMPTY_VALUE
    x = 0
    for x in range(x, N + 1):
        j = N - x
        LineBuffer[j] = (b * x) + a + dPriceShift
        ExtLineBuffer3[j] = (b * x) + a + (StdDev * StdDeviation) + dPriceShift
        ExtLineBuffer4[j] = (b * x) + a - (StdDev * StdDeviation) + dPriceShift
        ExtLineBuffer2[j] = (b * x) + a + (1.5 * StdDev * StdDeviation) + dPriceShift
        ExtLineBuffer5[j] = (b * x) + a - (1.5 * StdDev * StdDeviation) + dPriceShift
        ExtLineBuffer1[j] = (b * x) + a + (2.0 * StdDev * StdDeviation) + dPriceShift
        ExtLineBuffer6[j] = (b * x) + a - (2.0 * StdDev * StdDeviation) + dPriceShift
    else:
        x = _range_end(x, N + 1, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StLregr(_MQL5Indicator):
    name = 'st_lregr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'N_': 240,  # number of candles for analyze
        'StdDev': 1.0,  # deviation
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
    }

