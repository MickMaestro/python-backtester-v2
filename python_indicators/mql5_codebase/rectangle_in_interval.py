"""Rectangle in interval — converted from MQL5: MQL5 Indicators/Rectangle in interval/Rectangle in interval.mq5

Always only one rectangle
Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.003

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.003', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Always only one rectangle'], 'name': 'Rectangle in interval', 'source': 'MQL5 Indicators/Rectangle in interval/Rectangle in interval.mq5', 'folder': 'Rectangle in interval', 'inputs': [{'mql': 'InpTimeLeft', 'py': 'InpTimeLeft', 'param': None, 'type': 'datetime', 'default': 1622444400, 'label': 'Time Left (use only HH:MM)', 'sinput': False}, {'mql': 'InpTimeRight', 'py': 'InpTimeRight', 'param': None, 'type': 'datetime', 'default': 1622451600, 'label': 'Time Right (use only HH:MM)', 'sinput': False}, {'mql': 'InpRecClr', 'py': 'InpRecClr', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'Rectangle color', 'sinput': False}, {'mql': 'InpRecStyle', 'py': 'InpRecStyle', 'param': 'InpRecStyle', 'type': 'int', 'default': 0, 'label': 'Style of rectangle lines', 'sinput': False}, {'mql': 'InpRecWidth', 'py': 'InpRecWidth', 'param': 'InpRecWidth', 'type': 'int', 'default': 1, 'label': 'Width of rectangle lines', 'sinput': False}, {'mql': 'InpRecFill', 'py': 'InpRecFill', 'param': 'InpRecFill', 'type': 'bool', 'default': False, 'label': 'Filling rectangle with color', 'sinput': False}, {'mql': 'InpRecBack', 'py': 'InpRecBack', 'param': 'InpRecBack', 'type': 'bool', 'default': False, 'label': 'In the background', 'sinput': False}, {'mql': 'InpRecSelection', 'py': 'InpRecSelection', 'param': 'InpRecSelection', 'type': 'bool', 'default': False, 'label': 'Highlight to move', 'sinput': False}, {'mql': 'InpRecHidden', 'py': 'InpRecHidden', 'param': 'InpRecHidden', 'type': 'bool', 'default': True, 'label': 'Hidden in the object list', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeLeft = _input('InpTimeLeft', 1622444400)  # Time Left (use only HH:MM)
InpTimeRight = _input('InpTimeRight', 1622451600)  # Time Right (use only HH:MM)
InpRecClr = _input('InpRecClr', clrDeepPink)  # Rectangle color
InpRecStyle = _input('InpRecStyle', STYLE_SOLID)  # Style of rectangle lines
InpRecWidth = _input('InpRecWidth', 1)  # Width of rectangle lines
InpRecFill = _input('InpRecFill', False)  # Filling rectangle with color
InpRecBack = _input('InpRecBack', False)  # In the background
InpRecSelection = _input('InpRecSelection', False)  # Highlight to move
InpRecHidden = _input('InpRecHidden', True)  # Hidden in the object list
m_prefix = 'RII_'  # prefix

def OnInit():
    TimeToStruct(InpTimeLeft, SDateTimeLeft)
    TimeToStruct(InpTimeRight, SDateTimeRigth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    STime = MqlDateTime()
    TimeToStruct(time[rates_total - 1], STime)
    STime.hour = 0
    STime.min = 0
    STime.sec = 0
    time_start_day = StructToTime(STime)
    STime.hour = SDateTimeLeft.hour
    STime.min = SDateTimeLeft.min
    STime.sec = 0
    time_left = StructToTime(STime)
    STime.hour = SDateTimeRigth.hour
    STime.min = SDateTimeRigth.min
    STime.sec = 0
    time_right = StructToTime(STime)
    if time[rates_total - 1] > time_right:
        return rates_total
    rates_m1 = Arr(0, 0, factory=MqlRates)
    result = CopyRates(Symbol(), PERIOD_M1, _DT(time_left), _DT(time_right), rates_m1)
    if result > 1:
        price_max = DBL_MIN
        price_min = DBL_MAX
        for i in range(0, result):
            if rates_m1[i].high > price_max:
                price_max = rates_m1[i].high
            if rates_m1[i].low < price_min:
                price_min = rates_m1[i].low
        if price_max != DBL_MIN and price_min != DBL_MAX:
            res_name = m_prefix + TimeToString(time_start_day, TIME_DATE | TIME_MINUTES)
            if ObjectFind(ChartID(), res_name) < 0:
                RectangleCreate(ChartID(), res_name, 0, time_left, price_max, time_right, price_min, InpRecClr, InpRecStyle, InpRecWidth, InpRecFill, InpRecBack, InpRecSelection, InpRecHidden)
            else:
                RectanglePointChange(ChartID(), res_name, 0, time_left, price_max)
                RectanglePointChange(ChartID(), res_name, 1, time_right, price_min)
    return rates_total

def RectangleCreate(chart_ID=0, name='Rectangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=False, back=False, selection=True, hidden=True, z_order=0):
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
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
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

def RectangleDelete(chart_ID=0, name='Rectangle'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('RectangleDelete', ': failed to delete rectangle! Error code = ', GetLastError())
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

def OnDeinit(reason):
    ObjectsDeleteAll(0, m_prefix, 0, OBJ_RECTANGLE)

# ---- global variables initialised from expressions
SDateTimeLeft = MqlDateTime()
SDateTimeRigth = MqlDateTime()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RectangleInInterval(_MQL5Indicator):
    name = 'Rectangle in interval'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRecStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style of rectangle lines
        'InpRecWidth': 1,  # Width of rectangle lines
        'InpRecFill': False,  # Filling rectangle with color
        'InpRecBack': False,  # In the background
        'InpRecSelection': False,  # Highlight to move
        'InpRecHidden': True,  # Hidden in the object list
    }

