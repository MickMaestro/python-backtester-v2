"""xprofuteroverlay — converted from MQL5: MQL5 Indicators/XprofuterOverlay/xprofuteroverlay.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Signal'}, 'levels': [], 'description': [], 'name': 'xprofuteroverlay', 'source': 'MQL5 Indicators/XprofuterOverlay/xprofuteroverlay.mq5', 'folder': 'XprofuterOverlay', 'inputs': [{'mql': 'per', 'py': 'per', 'param': 'per', 'type': 'uint', 'default': 14, 'label': 'Period for signal', 'sinput': False}, {'mql': 'drawShift', 'py': 'drawShift', 'param': 'drawShift', 'type': 'uint', 'default': 14, 'label': 'Forward shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
per = _input('per', 14)  # Period for signal
drawShift = _input('drawShift', 14)  # Forward shift
ExtLineBuffer = Arr(0, 0.0)
ExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(per)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, drawShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ExtBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Xprofuter(', per, ' ,', drawShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    lim = 0
    imp = 0.0
    barClose = 0.0
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
            imp += close[i] - open[i]
        ExtBuffer[bar] = imp
        ExtLineBuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, 0 - 1, -1)
    barClose = close[0] - ExtBuffer[per]
    bar = _int(per - 1)
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer[bar] = barClose + ExtBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xprofuteroverlay(_MQL5Indicator):
    name = 'xprofuteroverlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'per': 14,  # Period for signal
        'drawShift': 14,  # Forward shift
    }

