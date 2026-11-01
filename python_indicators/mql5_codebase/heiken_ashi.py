"""heiken_ashi — converted from MQL5: MQL5 Indicators/Heiken-Ashi/heiken_ashi.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Heiken Ashi Open;Heiken Ashi High;Heiken Ashi Low;Heiken Ashi Close'}, 'levels': [], 'description': [], 'name': 'heiken_ashi', 'source': 'MQL5 Indicators/Heiken-Ashi/heiken_ashi.mq5', 'folder': 'Heiken-Ashi', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtOBuffer = Arr(0, 0.0)
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken Ashi')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if prev_calculated == 0:
        ExtLBuffer[0] = Low[0]
        ExtHBuffer[0] = High[0]
        ExtOBuffer[0] = Open[0]
        ExtCBuffer[0] = Close[0]
        limit = 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        haOpen = (ExtOBuffer[i - 1] + ExtCBuffer[i - 1]) / 2
        haClose = (Open[i] + High[i] + Low[i] + Close[i]) / 4
        haHigh = MathMax(High[i], MathMax(haOpen, haClose))
        haLow = MathMin(Low[i], MathMin(haOpen, haClose))
        ExtLBuffer[i] = haLow
        ExtHBuffer[i] = haHigh
        ExtOBuffer[i] = haOpen
        ExtCBuffer[i] = haClose
        if haOpen < haClose:
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshi(_MQL5Indicator):
    name = 'heiken_ashi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

