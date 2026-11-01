"""Open_Interest — converted from MQL5: MQL5 Indicators/Open Interest/Open_Interest.mq5

Copyright: Copyright © 2016, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 4, 2: 4}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Interest Max', 2: 'Interest Min'}, 'levels': [], 'description': [], 'name': 'Open_Interest', 'source': 'MQL5 Indicators/Open Interest/Open_Interest.mq5', 'folder': 'Open Interest', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SYMBOL_SESSION_INTEREST = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
BufferMaxUp = Arr(0, 0.0)
BufferMaxDown = Arr(0, 0.0)
BufferMinUp = Arr(0, 0.0)
BufferMinDown = Arr(0, 0.0)
StartDate = 0

def OnInit():
    Print('OnInit')
    SetIndexBuffer(0, BufferMaxUp, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMaxDown, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMinUp, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMinDown, INDICATOR_DATA)
    ArraySetAsSeries(BufferMaxUp, True)
    ArraySetAsSeries(BufferMaxDown, True)
    ArraySetAsSeries(BufferMinUp, True)
    ArraySetAsSeries(BufferMinDown, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global StartDate
    if prev_calculated == 0:
        Print('prev_calculated==0, StartDate=', StartDate)
        if StartDate < 1420070400:
            StartDate = TimeCurrent()
        else:
            return rates_total
    interest = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_INTEREST)
    limit = rates_total - prev_calculated
    for i in range(0, limit):
        BufferMaxUp[i] = interest
        BufferMaxDown[i] = interest
        BufferMinUp[i] = interest
        BufferMinDown[i] = interest
    if interest > BufferMaxUp[0]:
        BufferMaxUp[0] = interest
    if interest < BufferMinDown[0]:
        BufferMinDown[0] = interest
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OpenInterest(_MQL5Indicator):
    name = 'Open_Interest'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

