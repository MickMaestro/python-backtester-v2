"""CandleColorCounter — converted from MQL5: MQL5 Indicators/CandleColorCounter/CandleColorCounter.mq5

Copyright: Saeed Molanezhad (Iran) +989372946203; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Saeed Molanezhad (Iran) +989372946203', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 20.0, 'indicator_maximum': 80.0, 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [71.0, 62.0, 50.0, 38.0, 29.0], 'description': [], 'name': 'CandleColorCounter', 'source': 'MQL5 Indicators/CandleColorCounter/CandleColorCounter.mq5', 'folder': 'CandleColorCounter', 'inputs': [{'mql': 'Bar_Period', 'py': 'Bar_Period', 'param': 'Bar_Period', 'type': 'int', 'default': 89, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LineBullBuffer = Arr(0, 0.0)
LineBearBuffer = Arr(0, 0.0)
Bar_Period = _input('Bar_Period', 89)

def OnInit():
    SetIndexBuffer(0, LineBullBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LineBearBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Bar_Period)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Bar_Period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCC(' + _str(Bar_Period) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bar_Period < rates_total:
        BBullc = 0.0
        BBearc = 0.0
        i = 0
        j = 0
        i = rates_total - 1
        for i in range(i, Bar_Period - 1, -1):
            BBullc = 0.0
            BBearc = 0.0
            j = i
            for j in range(j, i - Bar_Period - 1, -1):
                if open[j] < close[j]:
                    BBullc += 1
                if open[j] > close[j]:
                    BBearc += 1
            else:
                j = _range_end(j, i - Bar_Period - 1, -1)
            LineBullBuffer[i] = (BBullc / Bar_Period) * 100
            LineBearBuffer[i] = (BBearc / Bar_Period) * 100
        else:
            i = _range_end(i, Bar_Period - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleColorCounter(_MQL5Indicator):
    name = 'CandleColorCounter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Bar_Period': 89,
    }
    y_range = (20.0, 80.0)

