"""mCandle_row — converted from MQL5: MQL5 Indicators/Candle_row/mCandle_row.mq5

Copyright: MVS © 2017; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'MVS © 2017', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'mCandle_row', 'source': 'MQL5 Indicators/Candle_row/mCandle_row.mq5', 'folder': 'Candle_row', 'inputs': [{'mql': 'ObjFs', 'py': 'ObjFs', 'param': 'ObjFs', 'type': 'int', 'default': 8, 'label': 'Font size arrow', 'sinput': False}, {'mql': 'BullArr', 'py': 'BullArr', 'param': None, 'type': 'color', 'default': 14772545, 'label': 'Bull arrow candle', 'sinput': False}, {'mql': 'BearArr', 'py': 'BearArr', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Bear arrow candle', 'sinput': False}, {'mql': 'CrossArr', 'py': 'CrossArr', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Cross arrow candle', 'sinput': False}, {'mql': 'Alerts', 'py': 'Alerts', 'param': 'Alerts', 'type': 'bool', 'default': True, 'label': 'Alert ON/OFF', 'sinput': False}, {'mql': 'Candles', 'py': 'Candles', 'param': 'Candles', 'type': 'int', 'default': 4, 'label': 'Count Candles', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ObjFs = _input('ObjFs', 8)  # Font size arrow
BullArr = _input('BullArr', clrRoyalBlue)  # Bull arrow candle
BearArr = _input('BearArr', clrMagenta)  # Bear arrow candle
CrossArr = _input('CrossArr', clrDarkOrange)  # Cross arrow candle
Alerts = _input('Alerts', True)  # Alert ON/OFF
Candles = _input('Candles', 4)  # Count Candles

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'Bull_')
    ObjectsDeleteAll(0, 'Bear_')
    ObjectsDeleteAll(0, 'Cross_')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    up = 0
    dn = 0
    res = 0
    limit = rates_total - prev_calculated
    if limit == 0:
        return rates_total
    if limit == 1:
        limit = 20
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    for i in range(limit - 1, 0, -1):
        if open[i] < close[i]:
            up += 1
            SetText('Bull_' + _str(time[i]), _str(up), time[i], high[i], BullArr)
        else:
            up = 0
        if open[i] > close[i]:
            dn += 1
            SetText('Bear_' + _str(time[i]), _str(dn), time[i], high[i], BearArr)
        else:
            dn = 0
        res = up + (dn * -1)
        if res == 0:
            SetText('Cross_' + _str(time[i]), _str(res), time[i], high[i], CrossArr)
    if Alerts and limit == 20:
        if up >= Candles:
            Alert(Symbol(), ': Time = ', time[0], ': UP = ', up)
        if dn >= Candles:
            Alert(Symbol(), ': Time = ', time[0], ': DN = ', dn)
    return rates_total

def SetText(nm, text, t, p, clr):
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_TEXT, 0, 0, 0)
        ObjectSetString(0, nm, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, nm, OBJPROP_FONTSIZE, ObjFs)
        ObjectSetInteger(0, nm, OBJPROP_ANCHOR, ANCHOR_LOWER)
        ObjectSetInteger(0, nm, OBJPROP_COLOR, clr)
        ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, nm, OBJPROP_SELECTED, False)
        ObjectSetInteger(0, nm, OBJPROP_BACK, False)
        ObjectSetInteger(0, nm, OBJPROP_HIDDEN, False)
        ObjectSetString(0, nm, OBJPROP_TEXT, text)
        ObjectSetDouble(0, nm, OBJPROP_PRICE, p)
        ObjectSetInteger(0, nm, OBJPROP_TIME, t)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MCandleRow(_MQL5Indicator):
    name = 'mCandle_row'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ObjFs': 8,  # Font size arrow
        'Alerts': True,  # Alert ON/OFF
        'Candles': 4,  # Count Candles
    }

