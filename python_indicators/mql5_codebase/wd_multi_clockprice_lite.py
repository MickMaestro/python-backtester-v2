"""wd.Multi_ClockPrice lite! — converted from MQL5: MQL5 Indicators/wd.Multi_ClockPrice lite!/wd.Multi_ClockPrice lite!.mq5

The 'wd.Multi_ClockPrice lite!' is the lite version of 'wd.Multi_ClockPrice'.
Provides visual representation of server time and bid prices on the chart.
It synchronizes with PC clock every seconds, allowing seamless updates even when MT5 is offline.
Real-time bid prices are displayed, efficiently meeting the need for price information.
Place informational labels in the specified sub-window, adjusting positions as needed.
Copyright: Copyright © 2024, Karya Prima Rajasa Mediavestama.; Link: https://www.mql5.com/en/code/47847; Version: 2.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2024, Karya Prima Rajasa Mediavestama.', 'link': 'https://www.mql5.com/en/code/47847', 'version': '2.24', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["The 'wd.Multi_ClockPrice lite!' is the lite version of 'wd.Multi_ClockPrice'.", 'Provides visual representation of server time and bid prices on the chart.', 'It synchronizes with PC clock every seconds, allowing seamless updates even when MT5 is offline.', 'Real-time bid prices are displayed, efficiently meeting the need for price information.', 'Place informational labels in the specified sub-window, adjusting positions as needed.'], 'name': 'wd.Multi_ClockPrice lite!', 'source': 'MQL5 Indicators/wd.Multi_ClockPrice lite!/wd.Multi_ClockPrice lite!.mq5', 'folder': 'wd.Multi_ClockPrice lite!', 'inputs': [{'mql': 'SubWindow', 'py': 'SubWindow', 'param': 'SubWindow', 'type': 'int', 'default': 0, 'label': 'Sub-Window placement', 'sinput': False}, {'mql': 'YDist', 'py': 'YDist', 'param': 'YDist', 'type': 'int', 'default': 10, 'label': 'Y-Position label', 'sinput': False}, {'mql': 'Comment1', 'py': 'Comment1', 'param': None, 'type': 'string', 'default': '===== Server Clock Settings =======', 'label': '=======================', 'sinput': False}, {'mql': 'FontSvrClockColor', 'py': 'FontSvrClockColor', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Font color', 'sinput': False}, {'mql': 'increment', 'py': 'increment', 'param': 'increment', 'type': 'int', 'default': 1, 'label': 'Seconds incremented', 'sinput': False}, {'mql': 'Comment2', 'py': 'Comment2', 'param': None, 'type': 'string', 'default': '======= Bid Price Settings =======', 'label': '=======================', 'sinput': False}, {'mql': 'FontPriceColor', 'py': 'FontPriceColor', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Font color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SubWindow = _input('SubWindow', 0)  # Sub-Window placement
YDist = _input('YDist', 10)  # Y-Position label
Comment1 = _input('Comment1', '===== Server Clock Settings =======')  # =======================
FontSvrClockColor = _input('FontSvrClockColor', clrOrange)  # Font color
increment = _input('increment', 1)  # Seconds incremented
Comment2 = _input('Comment2', '======= Bid Price Settings =======')  # =======================
FontPriceColor = _input('FontPriceColor', clrLime)  # Font color
labelServerClockHandle = 0  # Handle for the Server Clock label
labelPriceHandle = 0  # Handle for the Price label

def CreateLabelInSubWindow(subWindowNumber):
    global labelPriceHandle, labelServerClockHandle
    labelServerClockHandle = ObjectCreate(0, 'MT5ServerClock', OBJ_LABEL, subWindowNumber, 0, 0)
    ObjectSetInteger(0, 'MT5ServerClock', OBJPROP_COLOR, FontSvrClockColor)
    ObjectSetInteger(0, 'MT5ServerClock', OBJPROP_FONTSIZE, 11)
    ObjectSetInteger(0, 'MT5ServerClock', OBJPROP_XDISTANCE, 2)
    ObjectSetInteger(0, 'MT5ServerClock', OBJPROP_YDISTANCE, YDist)
    ObjectSetString(0, 'MT5ServerClock', OBJPROP_FONT, 'Arial Bold')
    ObjectSetString(0, 'MT5ServerClock', OBJPROP_TEXT, 'Server time: ')
    labelPriceHandle = ObjectCreate(0, 'Price', OBJ_LABEL, subWindowNumber, 0, 0)
    ObjectSetInteger(0, 'Price', OBJPROP_COLOR, FontPriceColor)
    ObjectSetInteger(0, 'Price', OBJPROP_FONTSIZE, 12)
    ObjectSetInteger(0, 'Price', OBJPROP_XDISTANCE, 2)
    ObjectSetInteger(0, 'Price', OBJPROP_YDISTANCE, YDist + 13)
    ObjectSetString(0, 'Price', OBJPROP_FONT, 'Arial Black')
    ObjectSetString(0, 'Price', OBJPROP_TEXT, 'Bid price: ')

def OnInit():
    subWindowNumber = SubWindow
    CreateLabelInSubWindow(subWindowNumber)
    EventSetTimer(1)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'MT5ServerClock')
    ObjectDelete(0, 'Price')
    EventKillTimer()

def OnTimer():
    global _s_OnTimer_calculated_server_time
    _s_OnTimer_calculated_server_time = TimeTradeServer() + increment
    counterMT5ServerClock = StringFormat('Server time: %s\r\n', TimeToString(_s_OnTimer_calculated_server_time, TIME_MINUTES | TIME_SECONDS))
    ObjectSetString(0, 'MT5ServerClock', OBJPROP_TEXT, counterMT5ServerClock)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    bidPrice = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ObjectSetString(0, 'Price', OBJPROP_TEXT, StringFormat('Bid price: %s', DoubleToString(bidPrice, Digits())))
    return rates_total

# ---- static local variables
_s_OnTimer_calculated_server_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WdMultiClockPriceLite(_MQL5Indicator):
    name = 'wd.Multi_ClockPrice lite!'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SubWindow': 0,  # Sub-Window placement
        'YDist': 10,  # Y-Position label
        'increment': 1,  # Seconds incremented
    }

