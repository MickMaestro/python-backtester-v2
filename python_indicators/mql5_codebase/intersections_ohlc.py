"""Intersections_OHLC — converted from MQL5: MQL5 Indicators/Intersections OHLC/Intersections_OHLC.mq5

Intersections OHLC
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Intersections OHLC'}, 'levels': [], 'description': ['Intersections OHLC'], 'name': 'Intersections_OHLC', 'source': 'MQL5 Indicators/Intersections OHLC/Intersections_OHLC.mq5', 'folder': 'Intersections OHLC', 'inputs': [{'mql': 'intersections', 'py': 'intersections', 'param': 'intersections', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INTERSECTIONS
HighLow = 0
_enum('ENUM_INTERSECTIONS', {0: 'HighLow'})

# ---- inputs and global variables
intersections = _input('intersections', HighLow)
ExtDataBuffer = Arr(0, 0.0)
ColorLineColors = Arr(0, 0.0)
ExtCalcBuffer = Arr(0, 0.0)
colors = Arr.of([clrRed, clrBlue], fill=0)

def OnInit():
    Print('OnInit', ' In')
    SetIndexBuffer(0, ExtDataBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorLineColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtCalcBuffer, INDICATOR_CALCULATIONS)
    text = ''
    _sw1 = intersections
    text = 'High and Low '
    IndicatorSetString(INDICATOR_SHORTNAME, 'Intersections ' + text)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    Print('OnInit', ' Out')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_time
    limit = -1
    if prev_calculated == 0:
        limit = 2
        ArrayInitialize(ExtDataBuffer, 1.0)
        ArrayInitialize(ColorLineColors, 0.0)
        ArrayInitialize(ExtCalcBuffer, 1.0)
        _s_OnCalculate_prev_time = 0
    else:
        limit = prev_calculated
    if _s_OnCalculate_prev_time == time[rates_total - 1]:
        return rates_total
    _s_OnCalculate_prev_time = time[rates_total - 1]
    for i in range(limit, rates_total):
        _sw2 = intersections
        ExtCalcBuffer[i] = ExtCalcBuffer[i - 1]
        if high[i - 1] > high[i - 2]:
            ExtCalcBuffer[i] += 1
        if low[i - 1] < low[i - 2]:
            ExtCalcBuffer[i] -= 1
        ExtDataBuffer[i] = ExtCalcBuffer[i]
    for i in range(limit, rates_total):
        if ExtDataBuffer[i] > ExtDataBuffer[i - 1]:
            ColorLineColors[i] = 0.0
        else:
            ColorLineColors[i] = 1.0
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntersectionsOHLC(_MQL5Indicator):
    name = 'Intersections_OHLC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'intersections': _Choice({0: 'High and Low'}, default=0),
    }

