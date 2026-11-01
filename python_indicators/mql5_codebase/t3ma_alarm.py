"""t3ma-alarm — converted from MQL5: MQL5 Indicators/T3MA-ALARM/t3ma-alarm.mq5

Rewritten from MQL4. Link to original - http://codebase.mql4.com/ru/7589, author is Martingeil (http://www.mql4.com/ru/users/Martingeil)
Copyright: Integer; Link: https://login.mql5.com/ru/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/ru/users/Integer', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [4294967295], 2: [16748574], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MA', 2: 'Buy', 3: 'Sell'}, 'levels': [], 'description': ['Rewritten from MQL4. Link to original - http://codebase.mql4.com/ru/7589, author is Martingeil (http://www.mql4.com/ru/users/Martingeil)'], 'name': 't3ma-alarm', 'source': 'MQL5 Indicators/T3MA-ALARM/t3ma-alarm.mq5', 'folder': 'T3MA-ALARM', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 4, 'label': 'MAPeriod', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': 'MAShift', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': 'MAMethod', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'MAPrice', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 4)  # MAPeriod
MAShift = _input('MAShift', 0)  # MAShift
MAMethod = _input('MAMethod', MODE_EMA)  # MAMethod
MAPrice = _input('MAPrice', PRICE_CLOSE)  # MAPrice
MAHandle1 = INVALID_HANDLE
MAHandle2 = INVALID_HANDLE
BufMA = Arr(0, 0.0)
BufBuy = Arr(0, 0.0)
BufSell = Arr(0, 0.0)
BufDir = Arr(0, 0.0)

def OnInit():
    global MAHandle1, MAHandle2
    MAHandle1 = iMA(None, PERIOD_CURRENT, MAPeriod, 0, MAMethod, MAPrice)
    if MAHandle1 != INVALID_HANDLE:
        MAHandle2 = iMA(None, PERIOD_CURRENT, MAPeriod, 0, MAMethod, MAHandle1)
    if MAHandle2 == INVALID_HANDLE:
        Alert('Failed to loading the indicator, try again')
        return -1
    SetIndexBuffer(0, BufMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufBuy, INDICATOR_DATA)
    SetIndexBuffer(2, BufSell, INDICATOR_DATA)
    SetIndexBuffer(3, BufDir, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetInteger(2, PLOT_ARROW, 234)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(0, PLOT_SHIFT, MAShift)
    return 0

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    start1 = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        start1 = start + MAShift + 2
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
        start1 = start
    if CopyBuffer(MAHandle2, 0, 0, rates_total - start, BufMA) == -1:
        _s_OnCalculate_error = True
        return 0
    for i in range(start1, rates_total):
        BufBuy[i] = 0.0
        BufSell[i] = 0.0
        BufDir[i] = BufDir[i - 1]
        if BufMA[i - MAShift] > BufMA[i - MAShift - 1]:
            BufDir[i] = 1.0
        if BufMA[i - MAShift] < BufMA[i - MAShift - 1]:
            BufDir[i] = -1.0
        if BufDir[i] == 1 and BufDir[i - 1] == -1:
            BufBuy[i] = low[i]
        if BufDir[i] == -1 and BufDir[i - 1] == 1:
            BufSell[i] = high[i]
    if BufDir[rates_total - 1] == 1:
        Comment('\n SWAPLONG = ', DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_LONG), 2), '   SWAPSHORT = ', DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_SHORT), 2), '\n BUY TREND ', DoubleToString(close[rates_total - 1], Digits()))
    elif BufDir[rates_total - 1] == -1:
        Comment('\n SWAPLONG = ', DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_LONG), 2), '   SWAPSHORT = ', DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_SHORT), 2), '\n SELL TREND ', DoubleToString(close[rates_total - 1], Digits()))
    return rates_total

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3maAlarm(_MQL5Indicator):
    name = 't3ma-alarm'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 4,  # MAPeriod
        'MAShift': 0,  # MAShift
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MAMethod
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MAPrice
    }

