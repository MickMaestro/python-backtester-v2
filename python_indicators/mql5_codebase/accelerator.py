"""accelerator — converted from MQL5: MQL5 Indicators/Accelerator Oscillator (AC)/accelerator.mq5

Accelerator/Decelerator
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'AC'}, 'levels': [], 'description': ['Accelerator/Decelerator'], 'name': 'accelerator', 'source': 'MQL5 Indicators/Accelerator Oscillator (AC)/accelerator.mq5', 'folder': 'Accelerator Oscillator (AC)', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtACBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ExtFastBuffer = Arr(0, 0.0)
ExtSlowBuffer = Arr(0, 0.0)
ExtAOBuffer = Arr(0, 0.0)
ExtSMABuffer = Arr(0, 0.0)
ExtFastSMAHandle = 0
ExtSlowSMAHandle = 0

def OnInit():
    global ExtFastSMAHandle, ExtSlowSMAHandle
    SetIndexBuffer(0, ExtACBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtFastBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtSlowBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtAOBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtSMABuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 37)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AC')
    ExtFastSMAHandle = iMA(None, 0, 5, 0, MODE_SMA, PRICE_MEDIAN)
    ExtSlowSMAHandle = iMA(None, 0, 34, 0, MODE_SMA, PRICE_MEDIAN)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < 37:
        return 0
    calculated = BarsCalculated(ExtFastSMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastSMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowSMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowSMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtFastSMAHandle, 0, 0, to_copy, ExtFastBuffer) <= 0:
        Print('Getting fast SMA is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowSMAHandle, 0, 0, to_copy, ExtSlowBuffer) <= 0:
        Print('Getting slow SMA is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated <= 33:
        i = 0
        for i in range(i, 33):
            ExtACBuffer[i] = 0.0
            ExtAOBuffer[i] = 0.0
        else:
            i = _range_end(i, 33, 1)
        limit = 33
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, 37):
        ExtACBuffer[i] = 0.0
        ExtAOBuffer[i] = ExtFastBuffer[i] - ExtSlowBuffer[i]
    else:
        i = _range_end(i, 37, 1)
    while i < rates_total:
        ExtAOBuffer[i] = ExtFastBuffer[i] - ExtSlowBuffer[i]
        sumAO = 0.0
        for j in range(0, 5):
            sumAO += ExtAOBuffer[i - j]
        ExtSMABuffer[i] = sumAO / 5.0
        ExtACBuffer[i] = ExtAOBuffer[i] - ExtSMABuffer[i]
        if ExtACBuffer[i] >= ExtACBuffer[i - 1]:
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Accelerator(_MQL5Indicator):
    name = 'accelerator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

