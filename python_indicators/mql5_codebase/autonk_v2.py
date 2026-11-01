"""autonk_v2 — converted from MQL5: MQL5 Indicators/AutoNK/autonk_v2.mq5

Auto_NK, Karlson.
Copyright: 2012.Karlson

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2012.Karlson', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Auto_NK, Karlson.'], 'name': 'autonk_v2', 'source': 'MQL5 Indicators/AutoNK/autonk_v2.mq5', 'folder': 'AutoNK', 'inputs': [{'mql': 'name', 'py': 'name', 'param': None, 'type': 'string', 'default': '111', 'label': 'Name', 'sinput': False}, {'mql': 'width', 'py': 'width', 'param': 'width', 'type': 'int', 'default': 1, 'label': 'Width', 'sinput': False}, {'mql': 'style', 'py': 'style', 'param': 'style', 'type': 'int', 'default': 1, 'label': 'Style', 'sinput': False}, {'mql': 'ray', 'py': 'ray', 'param': 'ray', 'type': 'bool', 'default': True, 'label': 'Rays', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
name = _input('name', '111')  # Name
width = _input('width', 1)  # Width
style = _input('style', 1)  # Style
ray = _input('ray', True)  # Rays
KF = 0
pips = 0
tim = Arr(0, 0)
low = Arr(0, 0.0)

def OnInit():
    global KF, pips
    if Digits() == 5 or Digits() == 3:
        KF = 10
    else:
        KF = 1
    bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if Period() > PERIOD_H12:
        pips = 150
    if Period() > PERIOD_M30 and Period() <= PERIOD_H12:
        pips = 70
    if Period() > PERIOD_M5 and Period() <= PERIOD_M30:
        pips = 30
    if Period() <= PERIOD_M5:
        pips = 20
    if CopyLow(Symbol(), Period(), 0, 50, low) < 50:
        Print('Data Error')
        return
    if CopyTime(Symbol(), Period(), 0, 50, tim) < 50:
        Print('Data Error')
        return
    if ObjectFind(0, name) != 0:
        Line(name, name, tim[0], low[0], TimeCurrent(), bid + (pips * 2.0 * KF * Point()), clrBlack, width, style, ray)
        Line('', name + '_up', tim[0], low[0] + (pips * 2.0 * KF * Point()), TimeCurrent(), bid + (pips * 4.0 * KF * Point()), clrCrimson, width, style, ray)
        Line('', name + '_mid', tim[0], low[0] + (pips * 1.0 * KF * Point()), TimeCurrent(), bid + (pips * 3.0 * KF * Point()), clrSilver, width, style, ray)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    time1 = _int(ObjectGetInteger(0, name, OBJPROP_TIME, 0))
    time2 = _int(ObjectGetInteger(0, name, OBJPROP_TIME, 1))
    price1 = ObjectGetDouble(0, name, OBJPROP_PRICE, 0)
    price2 = ObjectGetDouble(0, name, OBJPROP_PRICE, 1)
    nk_up_price = ObjectGetDouble(0, name + '_up', OBJPROP_PRICE, 0)
    if price2 > price1 and time2 > time1:
        Line('', name + '_up', time1, nk_up_price, time2, price2 + MathAbs(nk_up_price - price1), clrCrimson, width, style, ray)
        Line('', name + '_mid', time1, price1 + (MathAbs(nk_up_price - price1) / 2.0), time2, price2 + (MathAbs(nk_up_price - price1) / 2.0), clrSilver, width, style, ray)
    if price2 < price1 and time2 > time1:
        Line('', name + '_up', time1, nk_up_price, time2, price2 - MathAbs(nk_up_price - price1), clrCrimson, width, style, ray)
        Line('', name + '_mid', time1, price1 - (MathAbs(nk_up_price - price1) / 2.0), time2, price2 - (MathAbs(nk_up_price - price1) / 2.0), clrSilver, width, style, ray)
    ChartRedraw(0)
    return rates_total

def Line(nnn, namez, tt1, pp1, tt2, pp2, col, wid, sty, rays):
    ObjectCreate(0, namez, OBJ_TREND, 0, tt1, pp1, tt2, pp2)
    ObjectSetInteger(0, namez, OBJPROP_COLOR, col)
    ObjectSetInteger(0, namez, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, namez, OBJPROP_WIDTH, wid)
    ObjectSetInteger(0, namez, OBJPROP_STYLE, sty)
    ObjectSetInteger(0, namez, OBJPROP_RAY_RIGHT, rays)
    ObjectSetString(0, namez, OBJPROP_TEXT, nnn)

def OnDeinit(reason):
    if reason == REASON_REMOVE:
        if ObjectFind(0, name + '_mid') == 0:
            ObjectDelete(0, name + '_mid')
        if ObjectFind(0, name + '_up') == 0:
            ObjectDelete(0, name + '_up')
        if ObjectFind(0, name) == 0:
            ObjectDelete(0, name)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AutonkV2(_MQL5Indicator):
    name = 'autonk_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'width': 1,  # Width
        'style': 1,  # Style
        'ray': True,  # Rays
    }

