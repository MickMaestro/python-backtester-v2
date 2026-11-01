"""bw-zonetrade — converted from MQL5: MQL5 Indicators/BW-ZoneTrade/bw-zonetrade.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [32768, 255, 8421504]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'bw-zonetrade', 'source': 'MQL5 Indicators/BW-ZoneTrade/bw-zonetrade.mq5', 'folder': 'BW-ZoneTrade', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtOBuffer = Arr(0, 0.0)
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ExtAOBuffer = Arr(0, 0.0)
ExtACBuffer = Arr(0, 0.0)
ExtACHandle = 0
ExtAOHandle = 0

def OnInit():
    global ExtACHandle, ExtAOHandle
    SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, ExtACBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtAOBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BW ZoneTrade')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 38)
    ExtACHandle = iAC(None, 0)
    ExtAOHandle = iAO(None, 0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < 38:
        return 0
    calculated = BarsCalculated(ExtACHandle)
    if calculated < rates_total:
        Print('Not all data of ExtACHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtAOHandle)
    if calculated < rates_total:
        Print('Not all data of ExtAOHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtACHandle, 0, 0, to_copy, ExtACBuffer) <= 0:
        Print('Getting iAC is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtAOHandle, 0, 0, to_copy, ExtAOBuffer) <= 0:
        Print('Getting iAO is failed! Error', GetLastError())
        return 0
    if prev_calculated < 38:
        limit = 38
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtOBuffer[i] = Open[i]
        ExtHBuffer[i] = High[i]
        ExtLBuffer[i] = Low[i]
        ExtCBuffer[i] = Close[i]
        ExtColorBuffer[i] = 2.0
        if ExtACBuffer[i] > ExtACBuffer[i - 1] and ExtAOBuffer[i] > ExtAOBuffer[i - 1]:
            ExtColorBuffer[i] = 0.0
        if ExtACBuffer[i] < ExtACBuffer[i - 1] and ExtAOBuffer[i] < ExtAOBuffer[i - 1]:
            ExtColorBuffer[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BwZonetrade(_MQL5Indicator):
    name = 'bw-zonetrade'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

