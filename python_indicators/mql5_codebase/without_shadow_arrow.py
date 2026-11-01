"""Without shadow arrow — converted from MQL5: MQL5 Indicators/Without shadow arrow/Without shadow arrow.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [64636], 2: [16436871]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Shadow high', 2: 'Shadow low'}, 'levels': [], 'description': [], 'name': 'Without shadow arrow', 'source': 'MQL5 Indicators/Without shadow arrow/Without shadow arrow.mq5', 'folder': 'Without shadow arrow', 'inputs': [{'mql': 'code', 'py': 'code', 'param': 'code', 'type': 'ushort', 'default': 174, 'label': 'Symbol code to draw Shadow', 'sinput': False}, {'mql': 'arrow_shift', 'py': 'arrow_shift', 'param': 'arrow_shift', 'type': 'int', 'default': 9, 'label': 'Arrow shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
code = _input('code', 174)  # Symbol code to draw Shadow
arrow_shift = _input('arrow_shift', 9)  # Arrow shift
ArrowsBufferHigh = Arr(0, 0.0)
ArrowsBufferLow = Arr(0, 0.0)
m_digits = -1

def OnInit():
    global m_digits
    m_digits = Digits()
    if m_digits < 0:
        m_digits = 0
    SetIndexBuffer(0, ArrowsBufferHigh, INDICATOR_DATA)
    SetIndexBuffer(1, ArrowsBufferLow, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, code)
    PlotIndexSetInteger(1, PLOT_ARROW, code)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -arrow_shift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, arrow_shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        if i == 0:
            ArrowsBufferHigh[0] = 0.0
            ArrowsBufferLow[0] = 0.0
            continue
        if CompareDoubles(high[i - 1], open[i - 1]) or CompareDoubles(high[i - 1], close[i - 1]):
            ArrowsBufferHigh[i - 1] = high[i - 1]
        else:
            ArrowsBufferHigh[i - 1] = 0.0
        if CompareDoubles(low[i - 1], open[i - 1]) or CompareDoubles(low[i - 1], close[i - 1]):
            ArrowsBufferLow[i - 1] = low[i - 1]
        else:
            ArrowsBufferLow[i - 1] = 0.0
    ArrowsBufferHigh[rates_total - 1] = 0.0
    ArrowsBufferLow[rates_total - 1] = 0.0
    return rates_total

def CompareDoubles(number1, number2):
    if NormalizeDouble(number1 - number2, m_digits) == 0:
        return True
    else:
        return False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WithoutShadowArrow(_MQL5Indicator):
    name = 'Without shadow arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'code': 174,  # Symbol code to draw Shadow
        'arrow_shift': 9,  # Arrow shift
    }

