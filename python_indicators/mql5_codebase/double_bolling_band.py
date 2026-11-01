"""Double Bolling Band — converted from MQL5: MQL5 Indicators/Double Bolling Band Signal/Double Bolling Band.mq5

Copyright: 2023, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2023, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Double Bolling Band', 'source': 'MQL5 Indicators/Double Bolling Band Signal/Double Bolling Band.mq5', 'folder': 'Double Bolling Band Signal', 'inputs': [{'mql': 'BB_KIKAN', 'py': 'BB_KIKAN', 'param': 'BB_KIKAN', 'type': 'int', 'default': 20, 'label': 'BB period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BB_KIKAN = _input('BB_KIKAN', 20)  # BB period
waitBB = 0.0  # Initialize waitBB
prevtime = 0
orderPtn = 0  # 0: Do nothing, 1: Buy, 2: Sell
upperBuffer = Arr(0, 0.0)
lowerBuffer = Arr(0, 0.0)
BB3UP = 0.0  # Define these variables here to make them global
BB3LO = 0.0  # Define these variables here to make them global
BB2UP = 0.0  # Define these variables here to make them global
BB2LO = 0.0  # Define these variables here to make them global

def OnInit():
    return INIT_SUCCEEDED

def PlotArrow(direction, shift, price, clr):
    arrowName = ('BuyArrow' if (direction > 0) else 'SellArrow')
    arrowName += '_' + IntegerToString(shift)
    if ObjectFind(0, arrowName) != -1:
        ObjectDelete(0, arrowName)
    if direction > 0:
        ObjectCreate(0, arrowName, OBJ_ARROW_BUY, 0, iTime(Symbol(), Period(), shift), price)
    else:
        ObjectCreate(0, arrowName, OBJ_ARROW_SELL, 0, iTime(Symbol(), Period(), shift), price)
    ObjectSetInteger(0, arrowName, OBJPROP_COLOR, clr)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global BB2LO, BB2UP, BB3LO, BB3UP, orderPtn, waitBB
    handle = iBands(Symbol(), Period(), BB_KIKAN, 3, 0, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, rates_total, upperBuffer)
    CopyBuffer(handle, 2, 0, rates_total, lowerBuffer)
    BB3UP = upperBuffer[1]
    BB3LO = lowerBuffer[1]
    handle = iBands(Symbol(), Period(), BB_KIKAN, 2, 0, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, rates_total, upperBuffer)
    CopyBuffer(handle, 2, 0, rates_total, lowerBuffer)
    BB2UP = upperBuffer[1]
    BB2LO = lowerBuffer[1]
    if orderPtn == 1 or waitBB > 0:
        if BB2UP > close[1] and BB2LO < close[1]:
            orderPtn = 1
            waitBB = 0.0
            PlotArrow(1, 1, close[1], clrGreen)
        else:
            orderPtn = 0
            waitBB = 1.0
    if orderPtn == 2 or waitBB < 0:
        if BB2LO < close[1] and BB2UP > close[1]:
            orderPtn = 2
            waitBB = 0.0
            PlotArrow(-1, 1, close[1], clrRed)
        else:
            orderPtn = 0
            waitBB = -1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleBollingBand(_MQL5Indicator):
    name = 'Double Bolling Band'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BB_KIKAN': 20,  # BB period
    }

