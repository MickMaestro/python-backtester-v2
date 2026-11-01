"""Three daily rectangles — converted from MQL5: MQL5 Indicators/Three daily rectangles/Three daily rectangles.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Three daily rectangles', 'source': 'MQL5 Indicators/Three daily rectangles/Three daily rectangles.mq5', 'folder': 'Three daily rectangles', 'inputs': [{'mql': 'Inp_0_Color', 'py': 'Inp_0_Color', 'param': None, 'type': 'color', 'default': 14381203, 'label': 'Rectangle 0: Color', 'sinput': False}, {'mql': 'Inp_1_Color', 'py': 'Inp_1_Color', 'param': None, 'type': 'color', 'default': 64636, 'label': 'Rectangle 1: Color', 'sinput': False}, {'mql': 'Inp_2_Color', 'py': 'Inp_2_Color', 'param': None, 'type': 'color', 'default': 5275647, 'label': 'Rectangle 2: Color', 'sinput': False}, {'mql': 'InpStyle', 'py': 'InpStyle', 'param': 'InpStyle', 'type': 'int', 'default': 1, 'label': 'Rectangles: Style', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'int', 'default': 2, 'label': 'Rectangles: Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_0_Color = _input('Inp_0_Color', clrMediumPurple)  # Rectangle 0: Color
Inp_1_Color = _input('Inp_1_Color', clrLawnGreen)  # Rectangle 1: Color
Inp_2_Color = _input('Inp_2_Color', clrCoral)  # Rectangle 2: Color
InpStyle = _input('InpStyle', STYLE_DASH)  # Rectangles: Style
InpWidth = _input('InpWidth', 2)  # Rectangles: Width
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
m_prefix = 'TDR '  # prefix
m_init_error = False  # error on InInit

def OnInit():
    global m_init_error
    if Period() >= PERIOD_D1:
        err_text = "Chart period cannot be >= 'D1'!"
        if MQLInfoInteger(MQL_TESTER):
            Print('Three daily rectangles.mq5', ' ', 'OnInit', ', ERROR: ', err_text)
        else:
            Alert('Three daily rectangles.mq5', ' ', 'OnInit', ', ERROR: ', err_text)
        m_init_error = True
        return INIT_SUCCEEDED
    rates_d1 = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates_d1, True)
    start_pos = 0
    count = 3
    CopyRates(Symbol(), PERIOD_D1, start_pos, count, rates_d1)
    chart_id = ChartID()
    RectangleCreate(chart_id, m_prefix + '#0', '#0', 0, 0, 0.0, 0, 0.0, Inp_0_Color, InpStyle, InpWidth)
    RectangleCreate(chart_id, m_prefix + '#1', '#1', 0, 0, 0.0, 0, 0.0, Inp_1_Color, InpStyle, InpWidth)
    RectangleCreate(chart_id, m_prefix + '#2', '#2', 0, 0, 0.0, 0, 0.0, Inp_2_Color, InpStyle, InpWidth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_prev_bars
    if m_init_error:
        return 0
    rates_d1 = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates_d1, True)
    start_pos = 0
    count = 3
    if CopyRates(Symbol(), PERIOD_D1, start_pos, count, rates_d1) != count:
        return 0
    time_0 = rates_d1[0].time
    chart_id = ChartID()
    if time_0 == m_prev_bars:
        RectanglePointChange(chart_id, m_prefix + '#0', 0, rates_d1[0].time, rates_d1[0].high)
        RectanglePointChange(chart_id, m_prefix + '#0', 1, time[rates_total - 1], rates_d1[0].low)
        return rates_total
    m_prev_bars = time_0
    RectanglePointChange(chart_id, m_prefix + '#2', 0, rates_d1[2].time, rates_d1[2].high)
    RectanglePointChange(chart_id, m_prefix + '#2', 1, rates_d1[1].time - 60, rates_d1[2].low)
    RectanglePointChange(chart_id, m_prefix + '#1', 0, rates_d1[1].time, rates_d1[1].high)
    RectanglePointChange(chart_id, m_prefix + '#1', 1, rates_d1[0].time - 60, rates_d1[1].low)
    return rates_total

def OnDeinit(reason):
    ObjectsDeleteAll(0, m_prefix, 0, OBJ_RECTANGLE)
    ChartRedraw()

def RectangleCreate(chart_ID=0, name='Rectangle', text='Rectangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=False, back=False, selection=False, hidden=True, z_order=0):
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
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
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


class ThreeDailyRectangles(_MQL5Indicator):
    name = 'Three daily rectangles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Rectangles: Style
        'InpWidth': 2,  # Rectangles: Width
    }

