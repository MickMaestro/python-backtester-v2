"""Triangle Day — converted from MQL5: MQL5 Indicators/Triangle Day/Triangle Day.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Triangle Day', 'source': 'MQL5 Indicators/Triangle Day/Triangle Day.mq5', 'folder': 'Triangle Day', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
m_init_error = False  # error on InInit

def OnInit():
    global m_init_error
    if Period() >= PERIOD_D1:
        m_init_error = True
        return INIT_SUCCEEDED
    TriangleCreate(ChartID(), 'Left', 0, 0, 0.0, 0, 0.0, 0, 0.0, 0xFFC8C8)
    TriangleCreate(ChartID(), 'Right', 0, 0, 0.0, 0, 0.0, 0, 0.0, 0xC8C8FF)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if m_init_error:
        return 0
    price_day_open = 0.0
    price_day_high = DBL_MIN
    price_day_low = DBL_MAX
    price_day_close = 0.0
    time_day_open = 0
    time_day_high = 0
    time_day_low = 0
    time_day_close = 0
    rates_d1 = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates_d1, True)
    start_pos = 0
    count = 2
    if CopyRates(Symbol(), PERIOD_D1, start_pos, count, rates_d1) != count:
        return 0
    price_day_open = rates_d1[0].open
    time_day_open = rates_d1[0].time
    price_day_close = close[rates_total - 1]
    time_day_close = time[rates_total - 1]
    for i in range(rates_total - 1, 0 - 1, -1):
        if time[i] < rates_d1[0].time:
            break
        if high[i] > price_day_high:
            price_day_high = high[i]
            time_day_high = time[i]
        if low[i] < price_day_low:
            price_day_low = low[i]
            time_day_low = time[i]
    TrianglePointChange(ChartID(), 'Left', 0, time_day_open, price_day_open)
    TrianglePointChange(ChartID(), 'Left', 1, time_day_high, price_day_high)
    TrianglePointChange(ChartID(), 'Left', 2, time_day_low, price_day_low)
    TrianglePointChange(ChartID(), 'Right', 0, time_day_close, price_day_close)
    TrianglePointChange(ChartID(), 'Right', 1, time_day_high, price_day_high)
    TrianglePointChange(ChartID(), 'Right', 2, time_day_low, price_day_low)
    return rates_total

def TriangleCreate(chart_ID=0, name='Triangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, time3=0, price3=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=True, back=False, selection=False, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    time3 = Box(time3)
    price3 = Box(price3)
    ChangeTriangleEmptyPoints(time1, price1, time2, price2, time3, price3)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TRIANGLE, sub_window, time1.v, price1.v, time2.v, price2.v, time3.v, price3.v):
        Print('TriangleCreate', ': failed to create a triangle! Error code = ', GetLastError())
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

def TrianglePointChange(chart_ID=0, name='Triangle', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('TrianglePointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def ChangeTriangleEmptyPoints(time1, price1, time2, price2, time3, price3):
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
    if not time3.v:
        time3.v = time2.v
    if not price3.v:
        price3.v = price1.v

def OnDeinit(reason):
    ObjectDelete(ChartID(), 'Left')
    ObjectDelete(ChartID(), 'Right')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TriangleDay(_MQL5Indicator):
    name = 'Triangle Day'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

