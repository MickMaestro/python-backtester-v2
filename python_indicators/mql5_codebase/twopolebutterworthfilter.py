"""twopolebutterworthfilter — converted from MQL5: MQL5 Indicators/TwoPoleButterworthFilter/twopolebutterworthfilter.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Two-Pole Butterworth Filter'}, 'levels': [], 'description': [], 'name': 'twopolebutterworthfilter', 'source': 'MQL5 Indicators/TwoPoleButterworthFilter/twopolebutterworthfilter.mq5', 'folder': 'TwoPoleButterworthFilter', 'inputs': [{'mql': 'CutoffPeriod', 'py': 'CutoffPeriod', 'param': 'CutoffPeriod', 'type': 'int', 'default': 15, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CutoffPeriod = _input('CutoffPeriod', 15)  # Indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
coef1 = 0.0
coef2 = 0.0
coef3 = 0.0

def Get_Price(High, Low, bar):
    return (High[bar] + Low[bar]) / 2

def OnInit():
    global coef1, coef2, coef3, min_rates_total
    min_rates_total = 3
    tempReal = MathArctan(1.0)
    rad2Deg = _fdiv(45.0, tempReal)
    deg2Rad = _fdiv(1.0, rad2Deg)
    pi = MathArctan(1.0) * 4.0
    a1 = MathExp(((-MathSqrt(2.0)) * pi) / CutoffPeriod)
    b1 = 2 * a1 * MathCos((deg2Rad * MathSqrt(2.0) * 180) / CutoffPeriod)
    coef2 = b1
    coef3 = (-a1) * a1
    coef1 = (1.0 - b1 + (a1 * a1)) / 4.0
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Two-Pole Butterworth Filter(', CutoffPeriod, ' ,', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 10
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if bar > 3:
            ExtLineBuffer[bar] = (coef1 * (Get_Price(high, low, bar) + (2.0 * Get_Price(high, low, bar - 1)) + Get_Price(high, low, bar - 2))) + (coef2 * ExtLineBuffer[bar - 1]) + (coef3 * ExtLineBuffer[bar - 2])
        else:
            ExtLineBuffer[bar] = Get_Price(high, low, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Twopolebutterworthfilter(_MQL5Indicator):
    name = 'twopolebutterworthfilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CutoffPeriod': 15,  # Indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

