"""vroc — converted from MQL5: MQL5 Indicators/VROC/vroc.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VROC'}, 'levels': [], 'description': [], 'name': 'vroc', 'source': 'MQL5 Indicators/VROC/vroc.mq5', 'folder': 'VROC', 'inputs': [{'mql': 'PeriodROC', 'py': 'PeriodROC', 'param': 'PeriodROC', 'type': 'uint', 'default': 25, 'label': 'Indicator period', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodROC = _input('PeriodROC', 25)  # Indicator period
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(PeriodROC + 1)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'VROC(', PeriodROC, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - min_rates_total
    if VolumeType == VOLUME_TICK:
        bar = first
        for bar in range(bar, rates_total):
            ExtLineBuffer[bar] = _fdiv(float(tick_volume[bar]) - float(tick_volume[bar - PeriodROC]), float(tick_volume[bar - PeriodROC])) * 100
        else:
            bar = _range_end(bar, rates_total, 1)
    else:
        bar = first
        for bar in range(bar, rates_total):
            ExtLineBuffer[bar] = _fdiv(float(volume[bar]) - float(volume[bar - PeriodROC]), float(volume[bar - PeriodROC])) * 100
        else:
            bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vroc(_MQL5Indicator):
    name = 'vroc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodROC': 25,  # Indicator period
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
    }

