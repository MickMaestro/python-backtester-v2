"""fibo_retrace — converted from MQL5: MQL5 Indicators/Fibonacci retracement/fibo_retrace.mq5

Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [16711680], 2: [16711680], 3: [255], 4: [255], 5: [255], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 2, 4: 2, 5: 2, 6: 2}, 'labels': {1: 'baseline1', 2: 'baseline2', 3: '23.6%', 4: '38.2%', 5: '50.0%', 6: '61.8%'}, 'levels': [], 'description': [], 'name': 'fibo_retrace', 'source': 'MQL5 Indicators/Fibonacci retracement/fibo_retrace.mq5', 'folder': 'Fibonacci retracement', 'inputs': [{'mql': 'pastbars', 'py': 'pastbars', 'param': 'pastbars', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
pastbars = _input('pastbars', 30)
baseline1Buffer = Arr(0, 0.0)
baseline2Buffer = Arr(0, 0.0)
level236Buffer = Arr(0, 0.0)
level382Buffer = Arr(0, 0.0)
level500Buffer = Arr(0, 0.0)
level618Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, baseline1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, baseline2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, level236Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, level382Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, level500Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, level618Buffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, pastbars + 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, pastbars + 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, pastbars + 1)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, pastbars + 1)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, pastbars + 1)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, pastbars + 1)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (pastbars + 1):
        return 0
    i = 0
    j = 0
    locationmax = 0
    locationmin = 0
    max_ = 0.0
    min_ = 0.0
    h = 0.0
    l = 0.0
    h2 = 0.0
    l2 = 0.0
    i = rates_total - 1 - pastbars
    for i in range(i, rates_total):
        for k in range(0, rates_total - pastbars):
            baseline1Buffer[k] = 0.0
            baseline2Buffer[k] = 0.0
            level236Buffer[k] = 0.0
            level382Buffer[k] = 0.0
            level500Buffer[k] = 0.0
            level618Buffer[k] = 0.0
        j = 0
        for j in range(j, pastbars):
            if (i - j) <= (rates_total - 1 - pastbars):
                break
            h = high[i]
            h2 = high[i - j]
            l = low[i]
            l2 = low[i - j]
            if max_ == 0:
                max_ = MathMax(h, h2)
                if max_ == h:
                    locationmax = i
                else:
                    locationmax = i - j
            else:
                if MathMax(h, h2) > max_:
                    max_ = MathMax(h, h2)
                    if max_ == h:
                        locationmax = i
                    else:
                        locationmax = i - j
            if min_ == 0:
                min_ = MathMin(l, l2)
                if min_ == l:
                    locationmin = i
                else:
                    locationmin = i - j
            else:
                if MathMin(l, l2) < min_:
                    min_ = MathMin(l, l2)
                    if min_ == l:
                        locationmin = i
                    else:
                        locationmin = i - j
        else:
            j = _range_end(j, pastbars, 1)
        baseline1Buffer[i] = max_
        baseline2Buffer[i] = min_
        if locationmax > locationmin:
            level236Buffer[i] = NormalizeDouble(max_ - ((max_ - min_) * 0.236), Digits())
            level382Buffer[i] = NormalizeDouble(max_ - ((max_ - min_) * 0.382), Digits())
            level500Buffer[i] = NormalizeDouble(max_ - ((max_ - min_) * 0.5), Digits())
            level618Buffer[i] = NormalizeDouble(max_ - ((max_ - min_) * 0.618), Digits())
        else:
            level236Buffer[i] = NormalizeDouble(min_ + ((max_ - min_) * 0.236), Digits())
            level382Buffer[i] = NormalizeDouble(min_ + ((max_ - min_) * 0.382), Digits())
            level500Buffer[i] = NormalizeDouble(min_ + ((max_ - min_) * 0.5), Digits())
            level618Buffer[i] = NormalizeDouble(min_ + ((max_ - min_) * 0.618), Digits())
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboRetrace(_MQL5Indicator):
    name = 'fibo_retrace'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'pastbars': 30,
    }

