"""ticker_ama — converted from MQL5: MQL5 Indicators/Ticker_AMA/ticker_ama.mq5

Copyright: Copyright © 2004, by GOODMAN & Mstera и AF; Link: http://forum.viac.ru/viewforum.php?f=7; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, by GOODMAN & Mstera и AF', 'link': 'http://forum.viac.ru/viewforum.php?f=7', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [8421376, 11823615]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Ticker_AMA'}, 'levels': [], 'description': [], 'name': 'ticker_ama', 'source': 'MQL5 Indicators/Ticker_AMA/ticker_ama.mq5', 'folder': 'Ticker_AMA', 'inputs': [{'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'uint', 'default': 9, 'label': 'AMA period', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 2, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 30, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'G', 'py': 'G', 'param': 'G', 'type': 'double', 'default': 2.0, 'label': 'A power the smoothing constant is raised to', 'sinput': False}, {'mql': 'AMAShift', 'py': 'AMAShift', 'param': 'AMAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ama_period = _input('ama_period', 9)  # AMA period
fast_ma_period = _input('fast_ma_period', 2)  # Fast MA period
slow_ma_period = _input('slow_ma_period', 30)  # Slow MA period
G = _input('G', 2.0)  # A power the smoothing constant is raised to
AMAShift = _input('AMAShift', 0)  # Horizontal shift of the indicator in bars
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
dSC = 0.0
slowSC = 0.0
fastSC = 0.0

def OnInit():
    global dSC, fastSC, min_rates_total, slowSC
    min_rates_total = _int(ama_period + 1)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, AMAShift)
    shortname = Box("")
    StringConcatenate(shortname, 'Ticker_AMA( ', ama_period, ', ', fast_ma_period, ', ', slow_ma_period, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    slowSC = 2.0 / (slow_ma_period + 1)
    fastSC = 2.0 / (fast_ma_period + 1)
    dSC = fastSC - slowSC

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return min_rates_total
    first = 0
    bar = 0
    iii = 0
    noise = 0.0
    signal = 0.0
    price0 = 0.0
    price1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1 + begin
        ExtBBuffer[first - 1] = price[first - 1]
        if begin:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + min_rates_total)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtABuffer[bar] = price[bar]
        noise = Point() / 10000
        iii = 0
        for iii in range(iii, _int(ama_period)):
            price0 = price[bar - iii]
            price1 = price[bar - iii - 1]
            noise += MathAbs(price0 - price1)
        else:
            iii = _range_end(iii, _int(ama_period), 1)
        price0 = price[bar]
        price1 = price[bar - ama_period]
        signal = MathAbs(price0 - price1)
        ExtBBuffer[bar] = ExtBBuffer[bar - 1] + (MathPow(_fdiv(dSC * signal, noise) + slowSC, G) * (price0 - ExtBBuffer[bar - 1]))
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TickerAma(_MQL5Indicator):
    name = 'ticker_ama'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ama_period': 9,  # AMA period
        'fast_ma_period': 2,  # Fast MA period
        'slow_ma_period': 30,  # Slow MA period
        'G': 2.0,  # A power the smoothing constant is raised to
        'AMAShift': 0,  # Horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

