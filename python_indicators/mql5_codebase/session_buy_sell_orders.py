"""Session_Buy_Sell_Orders — converted from MQL5: MQL5 Indicators/Session Buy Sell Orders/Session_Buy_Sell_Orders.mq5

Number of Buy and Sell orders at the moment
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Buy orders', 2: 'Sell orders'}, 'levels': [], 'description': ['Number of Buy and Sell orders at the moment'], 'name': 'Session_Buy_Sell_Orders', 'source': 'MQL5 Indicators/Session Buy Sell Orders/Session_Buy_Sell_Orders.mq5', 'folder': 'Session Buy Sell Orders', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SYMBOL_SESSION_BUY_ORDERS = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
BufferBuy = Arr(0, 0.0)
BufferSell = Arr(0, 0.0)

def OnInit():
    Print('OnInit')
    SetIndexBuffer(0, BufferBuy, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSell, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    sov_buy = float(SymbolInfoInteger(Symbol(), SYMBOL_SESSION_BUY_ORDERS))
    sov_sell = float(SymbolInfoInteger(Symbol(), SYMBOL_SESSION_SELL_ORDERS))
    limit = prev_calculated - 1
    if prev_calculated == 0:
        ArrayInitialize(BufferBuy, 0.0)
        ArrayInitialize(BufferSell, 0.0)
        return rates_total
    for i in range(limit, rates_total):
        BufferBuy[i] = sov_buy
        BufferSell[i] = -sov_sell
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SessionBuySellOrders(_MQL5Indicator):
    name = 'Session_Buy_Sell_Orders'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

