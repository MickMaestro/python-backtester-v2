"""Renko Level — converted from MQL5: MQL5 Indicators/Renko Level/Renko Level.mq5

Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16711680, 255]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Histogram'}, 'levels': [], 'description': [], 'name': 'Renko Level', 'source': 'MQL5 Indicators/Renko Level/Renko Level.mq5', 'folder': 'Renko Level', 'inputs': [{'mql': 'InpSize', 'py': 'InpSize', 'param': 'InpSize', 'type': 'ushort', 'default': 30, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSize = _input('InpSize', 30)
ExtRenkoBufferUP = Arr(0, 0.0)
ExtRenkoBufferDOWN = Arr(0, 0.0)
ExtRenkoColorBuffer = Arr(0, 0.0)
ExtSize = 0.0
m_name_ceil = 'ceil'
m_name_round = 'round'
m_name_floor = 'floor'
InpColorCeil = clrBlue  # Line color
InpStyleCeil = STYLE_DASH  # Line style
InpWidthCeil = 1  # Line width
InpColorRound = clrGray  # Line color
InpStyleRound = STYLE_DASH  # Line style
InpWidthRound = 1  # Line width
InpColorFloor = clrRed  # Line color
InpStyleFloor = STYLE_DASH  # Line style
InpWidthFloor = 1  # Line width

def OnInit():
    global ExtSize
    SetIndexBuffer(0, ExtRenkoBufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, ExtRenkoBufferDOWN, INDICATOR_DATA)
    SetIndexBuffer(2, ExtRenkoColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    short_name = 'Renko(' + _str(InpSize) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    digits_adjust = 1
    if Digits() == 3 or Digits() == 5:
        digits_adjust = 10
    ExtSize = Point() * digits_adjust * InpSize
    if ObjectFind(0, m_name_ceil) < 0:
        HLineCreate(0, m_name_ceil, 0, 0.0, InpColorCeil, InpStyleCeil, InpWidthCeil)
    if ObjectFind(0, m_name_round) < 0:
        HLineCreate(0, m_name_round, 0, 0.0, InpColorRound, InpStyleRound, InpWidthRound)
    if ObjectFind(0, m_name_floor) < 0:
        HLineCreate(0, m_name_floor, 0, 0.0, InpColorFloor, InpStyleFloor, InpWidthFloor)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if reason == 1:
        HLineDelete(0, m_name_ceil)
        HLineDelete(0, m_name_round)
        HLineDelete(0, m_name_floor)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_time, _s_OnCalculate_price_DOWN, _s_OnCalculate_price_UP
    limit = prev_calculated - 1
    if prev_calculated == 0:
        Print('prev_calculated==0')
        _s_OnCalculate_price_UP = 0.0
        _s_OnCalculate_price_DOWN = 0.0
        _s_OnCalculate_prev_time = 0
        limit = 1
        price_ceil = Box(0.0)
        price_round = Box(0.0)
        price_floor = Box(0.0)
        Math(close[0], _fdiv(ExtSize, Point()), price_ceil, price_round, price_floor)
        _s_OnCalculate_price_UP = price_round.v
        _s_OnCalculate_price_DOWN = price_floor.v
        ArrayInitialize(ExtRenkoBufferUP, 0.0)
        ArrayInitialize(ExtRenkoBufferDOWN, 0.0)
    if time[rates_total - 1] == _s_OnCalculate_prev_time:
        return rates_total
    for i in range(limit, rates_total):
        price_ceil = Box(0.0)
        price_round = Box(0.0)
        price_floor = Box(0.0)
        if close[i] >= _s_OnCalculate_price_DOWN and close[i] <= _s_OnCalculate_price_UP:
            Math(close[i], _fdiv(ExtSize, Point()), price_ceil, price_round, price_floor)
            ExtRenkoBufferUP[i] = _s_OnCalculate_price_UP
            ExtRenkoBufferDOWN[i] = _s_OnCalculate_price_DOWN
            ExtRenkoColorBuffer[i] = ExtRenkoColorBuffer[i - 1]
            HLineMove(0, m_name_ceil, price_ceil.v)
            HLineMove(0, m_name_round, price_round.v)
            HLineMove(0, m_name_floor, price_floor.v)
        elif close[i] < _s_OnCalculate_price_DOWN:
            Math(close[i], _fdiv(ExtSize, Point()), price_ceil, price_round, price_floor)
            if CompareDoubles(price_round.v, _s_OnCalculate_price_DOWN):
                ExtRenkoBufferUP[i] = _s_OnCalculate_price_UP
                ExtRenkoBufferDOWN[i] = _s_OnCalculate_price_DOWN
                ExtRenkoColorBuffer[i] = ExtRenkoColorBuffer[i - 1]
            else:
                _s_OnCalculate_price_UP = price_ceil.v
                _s_OnCalculate_price_DOWN = price_round.v
                ExtRenkoBufferUP[i] = _s_OnCalculate_price_UP
                ExtRenkoBufferDOWN[i] = _s_OnCalculate_price_DOWN
                ExtRenkoColorBuffer[i] = 1.0
            HLineMove(0, m_name_ceil, price_ceil.v)
            HLineMove(0, m_name_round, price_round.v)
            HLineMove(0, m_name_floor, price_floor.v)
        elif close[i] > _s_OnCalculate_price_UP:
            Math(close[i], _fdiv(ExtSize, Point()), price_ceil, price_round, price_floor)
            if CompareDoubles(price_round.v, _s_OnCalculate_price_UP):
                ExtRenkoBufferUP[i] = _s_OnCalculate_price_UP
                ExtRenkoBufferDOWN[i] = _s_OnCalculate_price_DOWN
                ExtRenkoColorBuffer[i] = ExtRenkoColorBuffer[i - 1]
            else:
                _s_OnCalculate_price_DOWN = price_floor.v
                _s_OnCalculate_price_UP = price_round.v
                ExtRenkoBufferUP[i] = _s_OnCalculate_price_UP
                ExtRenkoBufferDOWN[i] = _s_OnCalculate_price_DOWN
                ExtRenkoColorBuffer[i] = 0.0
            HLineMove(0, m_name_ceil, price_ceil.v)
            HLineMove(0, m_name_round, price_round.v)
            HLineMove(0, m_name_floor, price_floor.v)
        else:
            f = 0
    _s_OnCalculate_prev_time = time[rates_total - 1]
    return rates_total

def Math(price, step, price_ceil, price_round, price_floor):
    point = Point()
    step1 = MathRound(_fdiv(_fdiv(price * 1, point), step))
    price_round.v = step * step1 * point
    step1_ceil = MathCeil(_fdiv(_fdiv((price_round.v + ((step / 2.0) * point)) * 1, point), step))
    step1_floor = MathFloor(_fdiv(_fdiv((price_round.v - ((step / 2.0) * point)) * 1, point), step))
    price_ceil.v = step * step1_ceil * point
    price_floor.v = step * step1_floor * point
    return

def CompareDoubles(number1, number2):
    if NormalizeDouble(number1 - number2, Digits() - 1) == 0:
        return True
    else:
        return False

def HLineCreate(chart_ID=0, name='HLine', sub_window=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, hidden=True, z_order=0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    return True

def HLineMove(chart_ID=0, name='HLine', price=0.0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, 0, price):
        Print('HLineMove', ': failed to move the horizontal line! Error code = ', GetLastError())
        return False
    return True

def HLineDelete(chart_ID=0, name='HLine'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('HLineDelete', ': failed to delete a horizontal line! Error code = ', GetLastError())
        return False
    return True

# ---- static local variables
_s_OnCalculate_price_UP = 0.0
_s_OnCalculate_price_DOWN = 0.0
_s_OnCalculate_prev_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RenkoLevel(_MQL5Indicator):
    name = 'Renko Level'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSize': 30,
    }

