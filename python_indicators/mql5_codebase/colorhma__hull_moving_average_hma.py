"""colorhma — converted from MQL5: MQL5 Indicators/Hull Moving Average (HMA)/colorhma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 14381203, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'colorhma', 'source': 'MQL5 Indicators/Hull Moving Average (HMA)/colorhma.mq5', 'folder': 'Hull Moving Average (HMA)', 'inputs': [{'mql': 'HMA_Period', 'py': 'HMA_Period', 'param': 'HMA_Period', 'type': 'int', 'default': 13, 'label': 'Moving average period', 'sinput': False}, {'mql': 'HMA_Shift', 'py': 'HMA_Shift', 'param': 'HMA_Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
HMA_Period = _input('HMA_Period', 13)  # Moving average period
HMA_Shift = _input('HMA_Shift', 0)  # Horizontal shift of the average in bars
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
Hma2_Period = 0
Sqrt_Period = 0
min_rates_total = 0

def OnInit():
    global Hma2_Period, Sqrt_Period, min_rates_total
    Hma2_Period = _int(MathFloor(_idiv(HMA_Period, 2)))
    Sqrt_Period = _int(MathFloor(MathSqrt(HMA_Period)))
    min_rates_total = HMA_Period + Sqrt_Period
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, HMA_Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    short_name = 'HMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(HMA_Period) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    begin0 = min_rates_total + begin
    if rates_total < begin0:
        return 0
    first = 0
    bar = 0
    begin1 = 0
    lwma1 = 0.0
    lwma2 = 0.0
    dma = 0.0
    begin1 = HMA_Period + begin
    if prev_calculated == 0:
        first = begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin0 + 1)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin0 + 1)
        bar = 0
        for bar in range(bar, begin0 + 1):
            ColorExtLineBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, begin0 + 1, 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        lwma1 = _s_OnCalculate_MA1.LWMASeries(begin, prev_calculated, rates_total, Hma2_Period, price[bar], bar, False)
        lwma2 = _s_OnCalculate_MA2.LWMASeries(begin, prev_calculated, rates_total, HMA_Period, price[bar], bar, False)
        dma = (2 * lwma1) - lwma2
        ExtLineBuffer[bar] = _s_OnCalculate_MA3.LWMASeries(begin1, prev_calculated, rates_total, Sqrt_Period, dma, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin0
    bar = first
    for bar in range(bar, rates_total):
        ColorExtLineBuffer[bar] = 0.0
        if ExtLineBuffer[bar - 1] < ExtLineBuffer[bar]:
            ColorExtLineBuffer[bar] = 1.0
        if ExtLineBuffer[bar - 1] > ExtLineBuffer[bar]:
            ColorExtLineBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorhma(_MQL5Indicator):
    name = 'colorhma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HMA_Period': 13,  # Moving average period
        'HMA_Shift': 0,  # Horizontal shift of the average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

