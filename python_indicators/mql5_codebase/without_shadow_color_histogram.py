"""Without shadow color histogram — converted from MQL5: MQL5 Indicators/Without shadow color histogram/Without shadow color histogram.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [4294967295, 64636, 16436871]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Shadow'}, 'levels': [], 'description': [], 'name': 'Without shadow color histogram', 'source': 'MQL5 Indicators/Without shadow color histogram/Without shadow color histogram.mq5', 'folder': 'Without shadow color histogram', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HistogramBuffer = Arr(0, 0.0)
HistogramColors = Arr(0, 0.0)
m_digits = -1

def OnInit():
    global m_digits
    m_digits = Digits()
    if m_digits < 0:
        m_digits = 0
    SetIndexBuffer(0, HistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HistogramColors, INDICATOR_COLOR_INDEX)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0.1)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 2.1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        if i == 0:
            HistogramBuffer[0] = 0.0
            HistogramColors[0] = 0.0
            continue
        count = 0.0
        HistogramBuffer[i - 1] = 0.0
        HistogramColors[i - 1] = 0.0
        if CompareDoubles(high[i - 1], open[i - 1]) or CompareDoubles(high[i - 1], close[i - 1]):
            count = count + 1.0
        if CompareDoubles(low[i - 1], open[i - 1]) or CompareDoubles(low[i - 1], close[i - 1]):
            count = count + 1.0
        if count == 1.0:
            HistogramBuffer[i - 1] = 1.0
            HistogramColors[i - 1] = 1.0
            d = 0
        elif count == 2.0:
            HistogramBuffer[i - 1] = 2.0
            HistogramColors[i - 1] = 2.0
            d = 0
    HistogramBuffer[rates_total - 1] = 0.0
    HistogramColors[rates_total - 1] = 0.0
    return rates_total

def CompareDoubles(number1, number2):
    if NormalizeDouble(number1 - number2, m_digits) == 0:
        return True
    else:
        return False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WithoutShadowColorHistogram(_MQL5Indicator):
    name = 'Without shadow color histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

