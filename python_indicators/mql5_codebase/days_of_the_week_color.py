"""Days of the week color — converted from MQL5: MQL5 Indicators/Days of the week color/Days of the week color.mq5

Days of the week in the form of a color histogram
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960, 255, 3329434, 16711680, 65535, 8388608, 55295, 7451452]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Day colors'}, 'levels': [], 'description': ['Days of the week in the form of a color histogram'], 'name': 'Days of the week color', 'source': 'MQL5 Indicators/Days of the week color/Days of the week color.mq5', 'folder': 'Days of the week color', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HistogramBuffer = Arr(0, 0.0)
HistogramColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, HistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HistogramColors, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Day')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        STime = MqlDateTime()
        TimeToStruct(time[i], STime)
        _sw1 = STime.day_of_week
        if _sw1 == 0:
            HistogramBuffer[i] = 0.0
            HistogramColors[i] = 0.0
        elif _sw1 == 1:
            HistogramBuffer[i] = 1.0
            HistogramColors[i] = 1.0
        elif _sw1 == 2:
            HistogramBuffer[i] = 2.0
            HistogramColors[i] = 2.0
        elif _sw1 == 3:
            HistogramBuffer[i] = 3.0
            HistogramColors[i] = 3.0
        elif _sw1 == 4:
            HistogramBuffer[i] = 4.0
            HistogramColors[i] = 4.0
        elif _sw1 == 5:
            HistogramBuffer[i] = 5.0
            HistogramColors[i] = 5.0
        elif _sw1 == 6:
            HistogramBuffer[i] = 6.0
            HistogramColors[i] = 6.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DaysOfTheWeekColor(_MQL5Indicator):
    name = 'Days of the week color'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

