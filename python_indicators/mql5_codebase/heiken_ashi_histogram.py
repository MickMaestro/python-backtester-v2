"""Heiken ashi histogram — converted from MQL5: MQL5 Indicators/Heiken ashi - histogram/Heiken ashi histogram.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 10}, 'colors': {1: [16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Heken ashi histogram'}, 'levels': [], 'description': [], 'name': 'Heiken ashi histogram', 'source': 'MQL5 Indicators/Heiken ashi - histogram/Heiken ashi histogram.mq5', 'folder': 'Heiken ashi - histogram', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken ashi histogram')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_workHaSize
    if _s_OnCalculate_workHaSize < rates_total:
        _s_OnCalculate_workHaSize = ArrayResize(workHa, rates_total + 500)
        if _s_OnCalculate_workHaSize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        haOpen = (((workHa[i - 1][2] + workHa[i - 1][3]) / 2.0) if (i > 0) else ((open[i] + close[i]) / 2))
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        workHa[i][4] = (haOpen + haClose) / 2
        val[i] = (1 if (haOpen > haClose) else -1 if (haOpen < haClose) else 0)
        valc[i] = (1 if (haOpen > haClose) else 0)
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_workHaSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiHistogram(_MQL5Indicator):
    name = 'Heiken ashi histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }
    y_range = (-1.0, 1.0)

