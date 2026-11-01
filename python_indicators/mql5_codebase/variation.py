"""variation — converted from MQL5: MQL5 Indicators/Variation/variation.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [7504122]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Variation'}, 'levels': [0.0], 'description': [], 'name': 'variation', 'source': 'MQL5 Indicators/Variation/variation.mq5', 'folder': 'Variation', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'int', 'default': 12, 'label': 'Averaging period', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'Averaging method', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Period_ = _input('Period_', 12)  # Averaging period
MA_Method_ = _input('MA_Method_', MODE_SMA)  # Averaging method
Shift = _input('Shift', 0)  # Horizontal shift in bars
ExtMapBuffer = Arr(0, 0.0)
start = 0
dPriceShift = 0.0

def OnInit():
    global start
    SetIndexBuffer(0, ExtMapBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    if MA_Method_ != MODE_EMA:
        start = 2 * Period_
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, 'Variation')
    shortname = Box("")
    StringConcatenate(shortname, 'Variation( Period_ = ', Period_, ', MA_Method_ = ', MA_Method_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_start1, _s_OnCalculate_start2, _s_OnCalculate_start3, start
    start += begin
    if rates_total < start:
        return 0
    first = 0
    bar = 0
    ma1 = 0.0
    ma2 = 0.0
    ma3 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin
        _s_OnCalculate_start1 = begin
        if MA_Method_ != MODE_EMA:
            _s_OnCalculate_start2 = Period_ + begin
            _s_OnCalculate_start3 = _s_OnCalculate_start2 + Period_
        else:
            _s_OnCalculate_start2 = begin
            _s_OnCalculate_start3 = begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ma1 = _s_OnCalculate_MA1.MASeries(_s_OnCalculate_start1, prev_calculated, rates_total, Period_, MA_Method_, price[bar], bar, False)
        ma2 = _s_OnCalculate_MA2.MASeries(_s_OnCalculate_start2, prev_calculated, rates_total, Period_, MA_Method_, price[bar] - ma1, bar, False)
        ma3 = _s_OnCalculate_MA3.MASeries(_s_OnCalculate_start3, prev_calculated, rates_total, Period_, MA_Method_, price[bar] - ma2 - ma1, bar, False)
        ExtMapBuffer[bar] = ma3
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_start1 = 0
_s_OnCalculate_start2 = 0
_s_OnCalculate_start3 = 0
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Variation(_MQL5Indicator):
    name = 'variation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 12,  # Averaging period
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Averaging method
        'Shift': 0,  # Horizontal shift in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

