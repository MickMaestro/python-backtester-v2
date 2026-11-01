"""t3 — converted from MQL5: MQL5 Indicators/T3/t3.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'T3'}, 'levels': [], 'description': [], 'name': 't3', 'source': 'MQL5 Indicators/T3/t3.mq5', 'folder': 'T3', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'int', 'default': 14, 'label': 'Period of T3 average', 'sinput': False}, {'mql': 'b_', 'py': 'b_', 'param': 'b_', 'type': 'double', 'default': 70.0, 'label': 'Coefficient x100', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'T3Shift', 'py': 'T3Shift', 'param': 'T3Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
T3Period = _input('T3Period', 14)  # Period of T3 average
b_ = _input('b_', 70.0)  # Coefficient x100
IPC = _input('IPC', PRICE_CLOSE_)  # Applied price
T3Shift = _input('T3Shift', 0)  # Horizontal shift in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift in points
Ind_Buffer = Arr(0, 0.0)
dPriceShift = 0.0

def OnInit():
    global dPriceShift
    SetIndexBuffer(0, Ind_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, T3Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'T3')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'T3( T3Period = ', T3Period, ', b = ', b_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    T3_ = CT3()
    T3_.MALengthCheck_1('T3Period', T3Period)
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 0:
        return 0
    first = 0
    bar = 0
    series = 0.0
    t3 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        t3 = _s_OnCalculate_T3_.T3Series(0, prev_calculated, rates_total, 0, b_, T3Period, series, bar, False)
        Ind_Buffer[bar] = t3 + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_T3_ = CT3()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3(_MQL5Indicator):
    name = 't3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3Period': 14,  # Period of T3 average
        'b_': 70.0,  # Coefficient x100
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER', 10: 'PRICE_TRENDFOLLOW0', 11: 'PRICE_TRENDFOLLOW1'}, default=1),  # Applied price
        'T3Shift': 0,  # Horizontal shift in bars
        'PriceShift': 0,  # Vertical shift in points
    }

