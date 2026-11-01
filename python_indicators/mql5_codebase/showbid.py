"""ShowBid — converted from MQL5: MQL5 Indicators/Show Bid/ShowBid.mq5

Copyright: Copyright 2014,Viktor Moss; Link: https://login.mql5.com/ru/users/vicmos; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014,Viktor Moss', 'link': 'https://login.mql5.com/ru/users/vicmos', 'version': '1.10', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ShowBid', 'source': 'MQL5 Indicators/Show Bid/ShowBid.mq5', 'folder': 'Show Bid', 'inputs': [{'mql': 'Color', 'py': 'Color', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Color', 'sinput': False}, {'mql': 'Width', 'py': 'Width', 'param': 'Width', 'type': 'int', 'default': 3, 'label': 'Size (1-5)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Color = _input('Color', clrYellow)  # Color
Width = _input('Width', 3)  # Size (1-5)

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'ShowBid')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, begin, price):
    SetLevelLeft(Symbol())
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        SetLevelLeft(Symbol())

def SetLevelLeft(smb, chid=0):
    np_ = Box(0)
    dt = Box(0)
    pr = Box(0.0)
    ChartXYToTimePrice(chid, _int(ChartGetInteger(chid, CHART_WIDTH_IN_PIXELS)), 30, np_, dt, pr)
    PriceBid = SymbolInfoDouble(smb, SYMBOL_BID)
    if ObjectFind(chid, 'ShowBid') != 0:
        ObjectCreate(chid, 'ShowBid', OBJ_ARROW_LEFT_PRICE, 0, dt.v, PriceBid)
        ObjectSetInteger(chid, 'ShowBid', OBJPROP_WIDTH, Width)
        ObjectSetInteger(chid, 'ShowBid', OBJPROP_COLOR, Color)
        return
    ObjectSetDouble(chid, 'ShowBid', OBJPROP_PRICE, PriceBid)
    ObjectSetInteger(chid, 'ShowBid', OBJPROP_TIME, dt.v)
    ObjectSetInteger(chid, 'ShowBid', OBJPROP_COLOR, Color)
    ObjectSetInteger(chid, 'ShowBid', OBJPROP_WIDTH, Width)
    ChartRedraw()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ShowBid(_MQL5Indicator):
    name = 'ShowBid'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Width': 3,  # Size (1-5)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

