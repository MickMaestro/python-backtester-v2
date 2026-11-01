"""price_channel — converted from MQL5: MQL5 Indicators/Price Channel/price_channel.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [16748574, 8421504], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Channel upper;Channel lower', 2: 'Channel median'}, 'levels': [], 'description': [], 'name': 'price_channel', 'source': 'MQL5 Indicators/Price Channel/price_channel.mq5', 'folder': 'Price Channel', 'inputs': [{'mql': 'InpChannelPeriod', 'py': 'InpChannelPeriod', 'param': 'InpChannelPeriod', 'type': 'int', 'default': 22, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpChannelPeriod = _input('InpChannelPeriod', 22)  # Period
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtMiddBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMiddBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpChannelPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, 1)
    PlotIndexSetInteger(1, PLOT_SHIFT, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price Channel(' + _str(InpChannelPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Channel(' + _str(InpChannelPeriod) + ') upper;Channel(' + _str(InpChannelPeriod) + ') lower')
    PlotIndexSetString(1, PLOT_LABEL, 'Median(' + _str(InpChannelPeriod) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)

def Highest(array, range_, fromIndex):
    res = 0.0
    i = 0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    res = 0.0
    i = 0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < InpChannelPeriod:
        return 0
    if prev_calculated == 0:
        limit = InpChannelPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtHighBuffer[i] = Highest(High, InpChannelPeriod, i)
        ExtLowBuffer[i] = Lowest(Low, InpChannelPeriod, i)
        ExtMiddBuffer[i] = (ExtHighBuffer[i] + ExtLowBuffer[i]) / 2.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceChannel(_MQL5Indicator):
    name = 'price_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpChannelPeriod': 22,  # Period
    }

