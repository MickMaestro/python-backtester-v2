"""XprofuterDD — converted from MQL5: MQL5 Indicators/XprofuterDD_HTF/XprofuterDD.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [8421376]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 4}, 'labels': {1: 'Signal', 2: 'MA', 3: 'Signal2'}, 'levels': [], 'description': [], 'name': 'XprofuterDD', 'source': 'MQL5 Indicators/XprofuterDD_HTF/XprofuterDD.mq5', 'folder': 'XprofuterDD_HTF', 'inputs': [{'mql': 'per', 'py': 'per', 'param': 'per', 'type': 'uint', 'default': 14, 'label': 'Число баров для прогноза', 'sinput': False}, {'mql': 'drawShift', 'py': 'drawShift', 'param': 'drawShift', 'type': 'uint', 'default': 14, 'label': 'Количество баров для прогноза', 'sinput': False}, {'mql': 'maPeriod', 'py': 'maPeriod', 'param': 'maPeriod', 'type': 'uint', 'default': 34, 'label': 'Период усреднения', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
per = _input('per', 14)  # Число баров для прогноза
drawShift = _input('drawShift', 14)  # Количество баров для прогноза
maPeriod = _input('maPeriod', 34)  # Период усреднения
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(per + maPeriod)
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, drawShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, drawShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer2, True)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, drawShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer3, True)
    shortname = Box("")
    StringConcatenate(shortname, 'XprofuterDD(', per, ' ,', drawShift, ' ,', maPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    lim = 0
    imp = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = _int(rates_total - prev_calculated + per)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if _int(bar - per) < 0:
            lim = 0
        else:
            lim = _int(bar - per)
        imp = 0.0
        for i in range(bar, lim - 1, -1):
            imp += _fdiv(close[i] - open[i], Point())
        ExtLineBuffer1[bar] = imp
        ExtLineBuffer3[bar] = _fdiv(close[bar] - open[bar], Point())
        imp = 0.0
        for i in range(bar, _int(bar + maPeriod)):
            imp += ExtLineBuffer1[i]
        ExtLineBuffer2[bar] = imp / maPeriod
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XprofuterDD(_MQL5Indicator):
    name = 'XprofuterDD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'per': 14,  # Число баров для прогноза
        'drawShift': 14,  # Количество баров для прогноза
        'maPeriod': 34,  # Период усреднения
    }

