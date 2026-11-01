"""i4_DRF_v3 — converted from MQL5: MQL5 Indicators/i4_DRF_v3/i4_DRF_v3.mq5

Copyright: Copyright (c) 2005, goldenlion@ukr.net; Link: http://GlobeInvestFund.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright (c) 2005, goldenlion@ukr.net', 'link': 'http://GlobeInvestFund.com/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [13850042, 13749760]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i4_DRF_v3'}, 'levels': [100.0, -100.0], 'description': [], 'name': 'i4_DRF_v3', 'source': 'MQL5 Indicators/i4_DRF_v3/i4_DRF_v3.mq5', 'folder': 'i4_DRF_v3', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 11, 'label': 'период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 11)  # период индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(iPeriod)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'i4_DRF_v3(', iPeriod, ' ,', Shift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    diff = 0.0
    sum_ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum_ = 0.0
        for iii in range(0, _int(iPeriod)):
            diff = high[bar - iii] - high[bar - iii - 1]
            if diff > 0:
                sum_ += 1
            diff = low[bar - iii] - low[bar - iii - 1]
            if diff < 0:
                sum_ -= 1
        sum_ = sum_ / _int(iPeriod)
        sum_ *= 100
        ExtBuffer[bar] = sum_
        if sum_ > 0:
            ColorExtBuffer[bar] = 1.0
        else:
            ColorExtBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class I4DRFV3(_MQL5Indicator):
    name = 'i4_DRF_v3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 11,  # период индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

