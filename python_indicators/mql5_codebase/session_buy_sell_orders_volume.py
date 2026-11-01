"""Session_Buy_Sell_Orders_Volume — converted from MQL5: MQL5 Indicators/Session Buy Sell Orders Volume/Session_Buy_Sell_Orders_Volume.mq5

Session Orders Volume: Open and Sell
Copyright: Copyright © 2016, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.003

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.003', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 4, 2: 4}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Max', 2: 'Min'}, 'levels': [], 'description': ['Session Orders Volume: Open and Sell'], 'name': 'Session_Buy_Sell_Orders_Volume', 'source': 'MQL5 Indicators/Session Buy Sell Orders Volume/Session_Buy_Sell_Orders_Volume.mq5', 'folder': 'Session Buy Sell Orders Volume', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SYMBOL_SESSION_BUY_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
BufferMaxUp = Arr(0, 0.0)
BufferMaxDown = Arr(0, 0.0)
BufferMinUp = Arr(0, 0.0)
BufferMinDown = Arr(0, 0.0)

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
    sov_buy = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_BUY_ORDERS_VOLUME)
    sov_sell = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_SELL_ORDERS_VOLUME)
    difference = sov_buy - sov_sell
    limit = rates_total - prev_calculated
    for i in range(0, limit):
        BufferMaxUp[i] = difference
        BufferMaxDown[i] = difference
        BufferMinUp[i] = difference
        BufferMinDown[i] = difference
    if difference > BufferMaxUp[0]:
        BufferMaxUp[0] = difference
    if difference < BufferMinDown[0]:
        BufferMinDown[0] = difference
    BufferMinUp[0] = difference
    BufferMaxDown[0] = BufferMinUp[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SessionBuySellOrdersVolume(_MQL5Indicator):
    name = 'Session_Buy_Sell_Orders_Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

