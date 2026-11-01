"""Three Candles Other TimeFrame — converted from MQL5: MQL5 Indicators/Three Candles Other TimeFrame/Three Candles Other TimeFrame.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'Three Candles Other TimeFrame', 'source': 'MQL5 Indicators/Three Candles Other TimeFrame/Three Candles Other TimeFrame.mq5', 'folder': 'Three Candles Other TimeFrame', 'inputs': [{'mql': 'Inp_period_other', 'py': 'Inp_period_other', 'param': 'Inp_period_other', 'type': 'int', 'default': 5, 'label': 'Other timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_period_other = _input('Inp_period_other', PERIOD_M5)  # Other timeframe
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
m_prefix = 'TCOTF '
m_init_error = False  # error on InInit

def OnInit():
    global m_init_error
    if Inp_period_other == PERIOD_CURRENT or Inp_period_other < Period():
        err_text = "'Other timeframe' cannot be less or equal ('<=') of the current timeframe!"
        if MQLInfoInteger(MQL_TESTER):
            Print('Three Candles Other TimeFrame.mq5', ' ', 'OnInit', ', ERROR: ', err_text)
        else:
            Alert('Three Candles Other TimeFrame.mq5', ' ', 'OnInit', ', ERROR: ', err_text)
        m_init_error = True
        return INIT_SUCCEEDED
    chart_id = ChartID()
    RectangleCreate(chart_id, m_prefix + '#0')
    RectangleCreate(chart_id, m_prefix + '#1')
    RectangleCreate(chart_id, m_prefix + '#2')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), m_prefix, 0, OBJ_RECTANGLE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_prev_bars
    if m_init_error:
        return 0
    rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates, True)
    start_pos = 0
    count = 3
    if CopyRates(Symbol(), Inp_period_other, start_pos, count, rates) != count:
        return 0
    chart_id = ChartID()
    time_0 = time[rates_total - 1]
    if time_0 == m_prev_bars:
        RectanglePointChange(chart_id, m_prefix + '#0', 0, rates[0].time, rates[0].high)
        RectanglePointChange(chart_id, m_prefix + '#0', 1, time[rates_total - 1], rates[0].low)
        return rates_total
    m_prev_bars = time_0
    RectanglePointChange(chart_id, m_prefix + '#0', 0, rates[0].time, rates[0].high)
    RectanglePointChange(chart_id, m_prefix + '#0', 1, time[rates_total - 1], rates[0].low)
    RectanglePointChange(chart_id, m_prefix + '#1', 0, rates[1].time, rates[1].high)
    RectanglePointChange(chart_id, m_prefix + '#1', 1, rates[0].time - PeriodSeconds(), rates[1].low)
    RectanglePointChange(chart_id, m_prefix + '#2', 0, rates[2].time, rates[2].high)
    RectanglePointChange(chart_id, m_prefix + '#2', 1, rates[1].time - PeriodSeconds(), rates[2].low)
    return rates_total

def RectangleCreate(chart_ID=0, name='Rectangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=False, back=False, selection=False, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    ChangeRectangleEmptyPoints(time1, price1, time2, price2)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_RECTANGLE, sub_window, time1.v, price1.v, time2.v, price2.v):
        Print('RectangleCreate', ': failed to create a rectangle! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_FILL, fill)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def RectanglePointChange(chart_ID=0, name='Rectangle', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('RectanglePointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def ChangeRectangleEmptyPoints(time1, price1, time2, price2):
    if not time1.v:
        time1.v = TimeCurrent()
    if not price1.v:
        price1.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time2.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time1.v), 10, temp)
        time2.v = temp[0]
    if not price2.v:
        price2.v = price1.v - (300 * SymbolInfoDouble(Symbol(), SYMBOL_POINT))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ThreeCandlesOtherTimeFrame(_MQL5Indicator):
    name = 'Three Candles Other TimeFrame'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_period_other': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=5),  # Other timeframe
    }

