"""wprfix — converted from MQL5: MQL5 Indicators/WPRfix/wprfix.mq5

Copyright: Copyright 2012, kazakov.v; Link: kazakov.v@fxmail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, kazakov.v', 'link': 'kazakov.v@fxmail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13422920]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Main'}, 'levels': [], 'description': [], 'name': 'wprfix', 'source': 'MQL5 Indicators/WPRfix/wprfix.mq5', 'folder': 'WPRfix', 'inputs': [{'mql': 'Range', 'py': 'Range', 'param': 'Range', 'type': 'int', 'default': 800, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Range = _input('Range', 800)
MainBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, '%Rfix(' + IntegerToString(Range) + ') ')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    min_ = 0.0
    max_ = 0.0
    X = Range * Point()
    i = 0
    j = 0
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(close, False)
    i = prev_calculated
    for i in range(i, rates_total):
        min_ = low[i]
        max_ = high[i] + Point()
        j = i
        while ((j := j - 1) + 1) > 0:
            if (max_ - min_) > X:
                break
            if low[j] < min_:
                min_ = low[j]
            if high[j] > max_:
                max_ = high[j]
        MainBuffer[i] = (_fdiv(close[i] - min_, max_ - min_) * 100) - 50
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total - 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wprfix(_MQL5Indicator):
    name = 'wprfix'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Range': 800,
    }

