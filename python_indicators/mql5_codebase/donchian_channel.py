"""donchian_channel — converted from MQL5: MQL5 Indicators/Donchian Channel/donchian_channel.mq5

Copyright: Copyright© 2013, Swan; Link: https://login.mql5.com/ru/users/Swan; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright© 2013, Swan', 'link': 'https://login.mql5.com/ru/users/Swan', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16736256], 2: [6316287]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'donchian_channel', 'source': 'MQL5 Indicators/Donchian Channel/donchian_channel.mq5', 'folder': 'Donchian Channel', 'inputs': [{'mql': 'InpChannelPeriod', 'py': 'InpChannelPeriod', 'param': 'InpChannelPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpChannelPeriod = _input('InpChannelPeriod', 20)  # Period
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
i = 0
limit = 0
start = 0

def OnInit():
    SetIndexBuffer(0, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpChannelPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpChannelPeriod)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global i, limit, start
    if rates_total < InpChannelPeriod:
        return 0
    if prev_calculated == 0:
        limit = InpChannelPeriod
    else:
        limit = prev_calculated
    i = limit
    while i < rates_total:
        start = i - InpChannelPeriod
        ExtHighBuffer[i] = high[ArrayMaximum(high, start, InpChannelPeriod)]
        ExtLowBuffer[i] = low[ArrayMinimum(low, start, InpChannelPeriod)]
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannel(_MQL5Indicator):
    name = 'donchian_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpChannelPeriod': 20,  # Period
    }

