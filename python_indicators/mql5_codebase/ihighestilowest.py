"""iHighestiLowest — converted from MQL5: MQL5 Indicators/High Low Lines/iHighestiLowest.mq5

Copyright: Copyright 2022, D4rk Ryd3r; Link: https://twitter.com/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, D4rk Ryd3r', 'link': 'https://twitter.com/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'iHighestiLowest', 'source': 'MQL5 Indicators/High Low Lines/iHighestiLowest.mq5', 'folder': 'High Low Lines', 'inputs': [{'mql': 'PrevBars', 'py': 'PrevBars', 'param': 'PrevBars', 'type': 'int', 'default': 55, 'label': 'Enter Previous number of Bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PrevBars = _input('PrevBars', 55)  # Enter Previous number of Bars
HighestCandle = 0
LowestCandle = 0
SecondHigh = Arr(0, 0.0)
SecondLow = Arr(0, 0.0)
prefix = 'Line_'

def OnInit():
    ArraySetAsSeries(History, True)
    ArraySetAsSeries(SecondHigh, True)
    ArraySetAsSeries(SecondLow, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global HighestCandle, LowestCandle
    CopyRates(Symbol(), Period(), 0, PrevBars, History)
    CopyHigh(Symbol(), Period(), 0, PrevBars, SecondHigh)
    HighestCandle = ArrayMaximum(SecondHigh, 0, PrevBars)
    CopyLow(Symbol(), Period(), 0, PrevBars, SecondLow)
    LowestCandle = ArrayMinimum(SecondLow, 0, PrevBars)
    ObjectCreate(None, prefix + 'SecondHigh', OBJ_HLINE, 0, 0, History[HighestCandle].high)
    ObjectSetInteger(0, prefix + 'SecondHigh', OBJPROP_COLOR, clrMagenta)
    ObjectSetInteger(0, prefix + 'SecondHigh', OBJPROP_WIDTH, 3)
    ObjectMove(None, prefix + 'SecondHigh', 0, 0, History[HighestCandle].high)
    ObjectCreate(None, prefix + 'SecondLow', OBJ_HLINE, 0, 0, History[LowestCandle].low)
    ObjectSetInteger(0, prefix + 'SecondLow', OBJPROP_COLOR, clrCrimson)
    ObjectSetInteger(0, prefix + 'SecondLow', OBJPROP_WIDTH, 3)
    ObjectMove(None, prefix + 'SecondLow', 0, 0, History[LowestCandle].low)
    return rates_total

# ---- global variables initialised from expressions
History = Arr(0, 0, factory=MqlRates)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IHighestiLowest(_MQL5Indicator):
    name = 'iHighestiLowest'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PrevBars': 55,  # Enter Previous number of Bars
    }

