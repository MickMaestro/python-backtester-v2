"""PYHighLow — converted from MQL5: MQL5 Indicators/PYHighLow/PYHighLow.mq5

Copyright: I Made Purnama Yasa; Link: -; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'I Made Purnama Yasa', 'link': '-', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PYHighLow', 'source': 'MQL5 Indicators/PYHighLow/PYHighLow.mq5', 'folder': 'PYHighLow', 'inputs': [{'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 5, 'label': 'Shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpShift = _input('InpShift', 5)  # Shift
ExtHighLowBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtHighLowBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PYHighLow(' + _str(InpShift) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    highsum = 0.0
    lowsum = 0.0
    for i in range(0, rates_total):
        highsum += high[i]
        lowsum += low[i]
    highlowsum = _fdiv(highsum - lowsum, rates_total) * InpShift
    for i in range(0, rates_total):
        highlow = high[i] - low[i]
        if highlowsum > highlow:
            ExtHighLowBuffer[i] = 100 - (_fdiv(highlowsum - highlow, highlowsum) * 100)
        elif highlowsum < highlow:
            ExtHighLowBuffer[i] = 100 - (_fdiv(highlow - highlowsum, highlowsum) * 100)
        else:
            ExtHighLowBuffer[i] = 0.0
    return rates_total

def OnTimer():
    pass

def OnChartEvent(id_, lparam, dparam, sparam):
    pass


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PYHighLow(_MQL5Indicator):
    name = 'PYHighLow'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpShift': 5,  # Shift
    }

