"""Fisher — converted from MQL5: MQL5 Indicators/Fisher Indicator MT5/Fisher.mq5

Version: 1.04

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.04', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Fisher', 'source': 'MQL5 Indicators/Fisher Indicator MT5/Fisher.mq5', 'folder': 'Fisher Indicator MT5', 'inputs': [{'mql': 'Period', 'py': 'Period_v', 'param': 'Period_v', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_v = _input('Period_v', 10)
ExtBuffer0 = Arr(0, 0.0)  # This buffer is for drawing.
ExtBuffer1 = Arr(0, 0.0)  # This buffer is for color.

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fisher')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, ExtBuffer0, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBuffer1, INDICATOR_COLOR_INDEX)

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, close, tick_volume, volume, spread):
    Value1 = 0.0
    Fish1 = 0.0
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    if prev_calculated == rates_total:
        return rates_total
    limit = rates_total
    for i in range(0, limit - Period_v):
        MaxH = High[ArrayMaximum(High, i, Period_v)]
        MinL = Low[ArrayMinimum(Low, i, Period_v)]
        price = (High[i] + Low[i]) / 2
        Value = (0.33 * 2 * (_fdiv(price - MinL, MaxH - MinL) - 0.5)) + (0.67 * Value1)
        Value = MathMin(MathMax(Value, -0.999), 0.999)
        indicator_index = rates_total - i - 1
        ExtBuffer0[indicator_index] = (0.5 * MathLog(_fdiv(1 + Value, 1 - Value))) + (0.5 * Fish1)
        if ExtBuffer0[indicator_index] < 0:
            ExtBuffer1[indicator_index] = 1.0
        else:
            ExtBuffer1[indicator_index] = 0.0
        Value1 = Value
        Fish1 = ExtBuffer0[indicator_index]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fisher(_MQL5Indicator):
    name = 'Fisher'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Period_v': 10,
    }

