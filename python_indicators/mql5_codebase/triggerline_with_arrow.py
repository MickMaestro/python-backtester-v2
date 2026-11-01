"""TriggerLine_with_Arrow — converted from MQL5: MQL5 Indicators/TriggerLine with Arrow/TriggerLine_with_Arrow.mq5

Copyright: Viktorov; Link: v4forex@yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Viktorov', 'link': 'v4forex@yandex.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 8, 2: 8, 3: 5, 4: 5}, 'colors': {1: [13828244, 3937500], 2: [13828244, 3937500], 3: [13828244], 4: [3937500]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'TriggerLine_with_Arrow', 'source': 'MQL5 Indicators/TriggerLine with Arrow/TriggerLine_with_Arrow.mq5', 'folder': 'TriggerLine with Arrow', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 24, 'label': 'Period', 'sinput': False}, {'mql': 'LSMA_Period', 'py': 'LSMA_Period', 'param': 'LSMA_Period', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'ShowArrow', 'py': 'ShowArrow', 'param': 'ShowArrow', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 24)  # Period
LSMA_Period = _input('LSMA_Period', 6)
ShowArrow = _input('ShowArrow', True)
length = 0
lsma_length = 0
lengthvar = 0.0
sum_ = Arr(1, 0.0, dyn=False)
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ColorIndBuffer1 = Arr(0, 0.0)
ColorIndBuffer2 = Arr(0, 0.0)
wt = Arr(0, 0.0)
lsma_ma = Arr(0, 0.0)
arrowUp = Arr(0, 0.0)
arrowDn = Arr(0, 0.0)

def OnInit():
    global length, lsma_length
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer1, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtMapBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer2, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, arrowUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 217)
    SetIndexBuffer(5, arrowDn, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, 218)
    SetIndexBuffer(6, wt, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, lsma_ma, INDICATOR_CALCULATIONS)
    PlotIndexSetString(2, PLOT_LABEL, 'arrowUp')
    PlotIndexSetString(3, PLOT_LABEL, 'arrowDn')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, 15)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, -15)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(ExtMapBuffer1, True)
    ArraySetAsSeries(ColorIndBuffer1, True)
    ArraySetAsSeries(ExtMapBuffer2, True)
    ArraySetAsSeries(ColorIndBuffer2, True)
    ArraySetAsSeries(arrowUp, True)
    ArraySetAsSeries(arrowDn, True)
    ArraySetAsSeries(wt, True)
    ArraySetAsSeries(lsma_ma, True)
    ArrayInitialize(wt, INT_MAX)
    length = period
    lsma_length = LSMA_Period
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lengthvar
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    shift = 0
    i = 0
    j = 0
    limit = ((rates_total - fmax(period, LSMA_Period)) if (prev_calculated <= 0) else (rates_total - prev_calculated))
    shift = limit
    for shift in range(shift, 0 - 1, -1):
        sum_[0] = 0.0
        i = length
        for i in range(i, 0, -1):
            lengthvar = length + 1
            lengthvar = lengthvar / 3
            tmp = 0.0
            tmp = (i - lengthvar) * open[length - i + shift]
            sum_[0] += tmp
        else:
            i = _range_end(i, 0, -1)
        wt[shift] = _fdiv(sum_[0] * 6, length * (length + 1))
        j = shift
        lsma_ma[shift] = wt[j + 1] + _fdiv((wt[j] - wt[j + 1]) * 2, lsma_length + 1)
        ExtMapBuffer1[shift] = wt[shift]
        ExtMapBuffer2[shift] = lsma_ma[shift]
        ColorIndBuffer1[shift] = 0.0
        ColorIndBuffer2[shift] = 0.0
        if wt[shift] < lsma_ma[shift]:
            ColorIndBuffer1[shift] = 1.0
            ColorIndBuffer2[shift] = 1.0
        arrowUp[shift] = 0.0
        arrowDn[shift] = 0.0
        if (ShowArrow and ExtMapBuffer1[shift + 1] < ExtMapBuffer2[shift + 1]) and ExtMapBuffer1[shift] >= ExtMapBuffer2[shift]:
            arrowUp[shift] = fmin(low[shift], fmin(ExtMapBuffer1[shift], ExtMapBuffer2[shift]))
        if (ShowArrow and ExtMapBuffer1[shift + 1] > ExtMapBuffer2[shift + 1]) and ExtMapBuffer1[shift] <= ExtMapBuffer2[shift]:
            arrowDn[shift] = fmax(high[shift], fmax(ExtMapBuffer1[shift], ExtMapBuffer2[shift]))
    else:
        shift = _range_end(shift, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TriggerLineWithArrow(_MQL5Indicator):
    name = 'TriggerLine_with_Arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 24,  # Period
        'LSMA_Period': 6,
        'ShowArrow': True,
    }

