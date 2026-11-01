"""dailylines — converted from MQL5: MQL5 Indicators/DailyLines Vertical lines starting new Day with above name of the DAY. Period Separators with option/dailylines.mq5

This indicator draws daily period separators
With telling what tradingday starts at each
Every day you can color like you want
what makes also the option to see weekly separator
Copyright: Copyright © 2014, deVries; Link: http://www.mql5.com/en/job/new?prefered=deVries; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, deVries', 'link': 'http://www.mql5.com/en/job/new?prefered=deVries', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['This indicator draws daily period separators', 'With telling what tradingday starts at each', 'Every day you can color like you want', 'what makes also the option to see weekly separator'], 'name': 'dailylines', 'source': 'MQL5 Indicators/DailyLines Vertical lines starting new Day with above name of the DAY. Period Separators with option/dailylines.mq5', 'folder': 'DailyLines Vertical lines starting new Day with above name of the DAY. Period Separators with option', 'inputs': [{'mql': 'MaxBarsToLookBackForSeparators', 'py': 'MaxBarsToLookBackForSeparators', 'param': 'MaxBarsToLookBackForSeparators', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MaximumBars', 'py': 'MaximumBars', 'param': None, 'type': 'string', 'default': 'Input 0', 'label': '', 'sinput': False}, {'mql': 'Sunday', 'py': 'Sunday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Monday', 'py': 'Monday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Tuesday', 'py': 'Tuesday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Wednesday', 'py': 'Wednesday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Thursday', 'py': 'Thursday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Friday', 'py': 'Friday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Saturday', 'py': 'Saturday', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InpStyle', 'py': 'InpStyle', 'param': 'InpStyle', 'type': 'int', 'default': 4, 'label': 'Line style', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'uchar', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'textplace', 'py': 'textplace', 'param': 'textplace', 'type': 'double', 'default': 30.0, 'label': '', 'sinput': False}, {'mql': 'InpFont', 'py': 'InpFont', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Font', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'uchar', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'InpAnchor', 'py': 'InpAnchor', 'param': 'InpAnchor', 'type': 'int', 'default': 1, 'label': 'Anchor type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
MaxBarsToLookBackForSeparators = _input('MaxBarsToLookBackForSeparators', 0)
MaximumBars = _input('MaximumBars', 'Input 0')
InpStyle = _input('InpStyle', STYLE_DASHDOTDOT)  # Line style
InpWidth = _input('InpWidth', 1)  # Line width
textplace = _input('textplace', 30.0)
InpFont = _input('InpFont', 'Arial')  # Font
InpFontSize = _input('InpFontSize', 8)  # Font size
InpAnchor = _input('InpAnchor', ANCHOR_BOTTOM)  # Anchor type
textprice = 0.0
newtextprice = 0.0
max_price = 0.0
min_price = 0.0
thisday = ''
daycheck1 = ''
daycheck2 = ''
limit = 0  # ,
min_rates_total = 1

def OnInit():
    global max_price, min_price, textprice
    max_price = ChartGetDouble(0, CHART_PRICE_MAX)
    min_price = ChartGetDouble(0, CHART_PRICE_MIN)
    heightinpixels = ChartHeightInPixelsGet(0, 0)
    textprice = max_price - ((max_price - min_price) * _fdiv(textplace, heightinpixels))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    i = 0
    obj_total = ObjectsTotal(0, 0, -1)
    i = obj_total
    for i in range(i, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringSubstr(name, 0, 14) == 'NewTradingDay ':
            TrendDelete(0, name)
        if StringSubstr(name, 0, 8) == 'DayText ':
            TextDelete(0, name)
    else:
        i = _range_end(i, 0 - 1, -1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global daycheck1, daycheck2, limit, thisday
    if rates_total < min_rates_total:
        return 0
    k = 0
    if prev_calculated < rates_total or prev_calculated <= 0:
        if MaxBarsToLookBackForSeparators <= 0 or MaxBarsToLookBackForSeparators > (rates_total - 1):
            limit = 0
        else:
            limit = rates_total - 1 - MaxBarsToLookBackForSeparators
    today = TimeToString(time[rates_total - 1], TIME_DATE)
    if thisday == ('NewTradingDay ' + today):
        return rates_total
    elif ObjectFind(0, 'NewTradingDay ' + today) == 0:
        thisday = 'NewTradingDay ' + today
        return rates_total
    daycheck1 = ''
    daycheck2 = ''
    k = limit
    for k in range(k, rates_total - 1 + 1):
        now = time[k]
        thisday = TimeToString(now, TIME_DATE)
        weekday = TimeDayOfWeekMQL4(now)
        clr = DaytoClr(weekday)
        if daycheck1 != ('NewTradingDay ' + thisday):
            if ObjectFind(0, 'NewTradingDay ' + thisday) == 0:
                daycheck1 = 'NewTradingDay ' + thisday
            else:
                if not TrendCreate(0, 'NewTradingDay ' + thisday, 0, now, Point(), now, textprice, clr, InpStyle, InpWidth, True, False, True, False, True, 0):
                    daycheck1 = ''
                else:
                    daycheck1 = 'NewTradingDay ' + thisday
        if daycheck2 != ('DayText ' + thisday):
            if ObjectFind(0, 'DayText ' + thisday) == 0:
                daycheck2 = 'DayText ' + thisday
            else:
                text = DaytoStr(weekday)
                if not TextCreate(0, 'DayText ' + thisday, 0, now, textprice, text, InpFont, InpFontSize, clr, 90.0, InpAnchor, False, False, True, 0):
                    daycheck2 = ''
                else:
                    daycheck2 = 'DayText ' + thisday
    else:
        k = _range_end(k, rates_total - 1 + 1, 1)
    ChartRedraw()
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global max_price, min_price, textprice
    if id_ == CHARTEVENT_CHART_CHANGE:
        max_price = ChartGetDouble(0, CHART_PRICE_MAX)
        min_price = ChartGetDouble(0, CHART_PRICE_MIN)
        heightinpixels = ChartHeightInPixelsGet(0, 0)
        textprice = max_price - ((max_price - min_price) * _fdiv(textplace, heightinpixels))
        if newtextprice > (textprice + Point()) or newtextprice < (textprice - Point()):
            ChangeTextPrice(textprice)

def DaytoStr(weekday):
    _sw1 = weekday
    if _sw1 == 0:
        return ' Sun'
    elif _sw1 == 1:
        return ' Mon'
    elif _sw1 == 2:
        return ' Tue'
    elif _sw1 == 3:
        return ' Wed'
    elif _sw1 == 4:
        return ' Thu'
    elif _sw1 == 5:
        return ' Fri'
    elif _sw1 == 6:
        return ' Sat'
    return ''

def DaytoClr(weekday):
    _sw2 = weekday
    if _sw2 == 0:
        return Sunday
    elif _sw2 == 1:
        return Monday
    elif _sw2 == 2:
        return Tuesday
    elif _sw2 == 3:
        return Wednesday
    elif _sw2 == 4:
        return Thursday
    elif _sw2 == 5:
        return Friday
    elif _sw2 == 6:
        return Saturday
    return CLR_NONE

def ChartHeightInPixelsGet(chart_ID=0, sub_window=0):
    result = Box(-1)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_HEIGHT_IN_PIXELS, sub_window, result):
        Print('ChartHeightInPixelsGet' + ', Error Code = ', GetLastError())
    return _int(result.v)

def TimeDayOfWeekMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

def TrendCreate(chart_ID=0, name='TrendLine', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, ray_left=False, ray_right=False, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    ChangeTrendEmptyPoints(time1, price1, time2, price2)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TREND, sub_window, time1.v, price1.v, time2.v, price2.v):
        Print('TrendCreate', ': failed to create a trend line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def ChangeTextPrice(price):
    global newtextprice
    obj_total = ObjectsTotal(0, 0, -1)
    for i in range(obj_total, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringSubstr(name, 0, 14) == 'NewTradingDay ':
            t1 = ObjectGetInteger(0, name, OBJPROP_TIME, 1)
            ObjectMove(0, name, 1, t1, price)
        if StringSubstr(name, 0, 8) == 'DayText ':
            t1 = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
            ObjectMove(0, name, 0, t1, price)
    newtextprice = textprice
    ChartRedraw()

def ChangeTrendEmptyPoints(time1, price1, time2, price2):
    if not time1.v:
        time1.v = TimeCurrent()
    if not price1.v:
        price1.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time2.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time1.v), 10, temp)
        time2.v = temp[0]
    if not price2.v:
        price2.v = price1.v

def TrendDelete(chart_ID=0, name='TrendLine'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('TrendDelete', ': failed to delete a trend line! Error code = ', GetLastError())
        return False
    return True

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    time = Box(time)
    price = Box(price)
    ChangeTextEmptyPoint(time, price)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time.v, price.v):
        Print('TextCreate', ': failed to create "Text" object! Error code = ', GetLastError())
        return False
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def ChangeTextEmptyPoint(time, price):
    if not time.v:
        time.v = TimeCurrent()
    if not price.v:
        price.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)

def TextDelete(chart_ID=0, name='Text'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('TextDelete', ': failed to delete "Text" object! Error code = ', GetLastError())
        return False
    return True

# ---- global variables initialised from expressions
Sunday = _input('Sunday', _uint(Blue))
Monday = _input('Monday', _uint(Yellow))
Tuesday = _input('Tuesday', _uint(Aqua))
Wednesday = _input('Wednesday', _uint(Aqua))
Thursday = _input('Thursday', _uint(Aqua))
Friday = _input('Friday', _uint(Aqua))
Saturday = _input('Saturday', _uint(Aqua))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailylines(_MQL5Indicator):
    name = 'dailylines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaxBarsToLookBackForSeparators': 0,
        'InpStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Line style
        'InpWidth': 1,  # Line width
        'textplace': 30.0,
        'InpFontSize': 8,  # Font size
        'InpAnchor': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=1),  # Anchor type
    }

