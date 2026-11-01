"""VR Alert Lite — converted from MQL5: MQL5 Indicators/VR Alert МТ5 Lite/VR Alert Lite.mq5

VR Alert the indicator warns the trader that the price reached specified levels.
Copyright: Copyright 2018, Trading-go Project.; Link: http://trading-go.ru; Version: 18.010

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Trading-go Project.', 'link': 'http://trading-go.ru', 'version': '18.010'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['VR Alert the indicator warns the trader that the price reached specified levels.'], 'name': 'VR Alert Lite', 'source': 'MQL5 Indicators/VR Alert МТ5 Lite/VR Alert Lite.mq5', 'folder': 'VR Alert МТ5 Lite', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Chart_ID = 0
Prefix = 'DFSER-'
PriceUP = 9999999.0
PriceDW = 0.0
prices = 0.0
counter_up = 0
counter_dw = 0
counter_ti = 0
signals = 3

def OnInit():
    global Chart_ID
    Comment('')
    Chart_ID = ChartID()
    if ObjectFind(Chart_ID, Prefix + 'ButtonUP') != 0:
        ButtonCreate(Chart_ID, Prefix + 'ButtonUP', 4, 15, 20, 16, CORNER_LEFT_UPPER, 'UP', 'Arial', 8, clrWhite, clrBlue, clrNONE, False, False, False, True, 0)
    if ObjectFind(Chart_ID, Prefix + 'ButtonDW') != 0:
        ButtonCreate(Chart_ID, Prefix + 'ButtonDW', 26, 15, 20, 16, CORNER_LEFT_UPPER, 'DW', 'Arial', 8, clrWhite, clrTomato, clrNONE, False, False, False, True, 0)
    if ObjectFind(Chart_ID, Prefix + 'ButtonTI') != 0:
        ButtonCreate(Chart_ID, Prefix + 'ButtonTI', 48, 15, 20, 16, CORNER_LEFT_UPPER, 'TI', 'Arial', 8, clrWhite, clrGreen, clrNONE, False, False, False, True, 0)
    EventSetTimer(1)
    ChartSetInteger(Chart_ID, CHART_EVENT_MOUSE_MOVE, True)
    return INIT_SUCCEEDED

def OnChartEvent(id_, lparam, dparam, sparam):
    chart_max = ChartGetDouble(Chart_ID, CHART_PRICE_MAX, 0)
    chart_min = ChartGetDouble(Chart_ID, CHART_PRICE_MIN, 0)
    if id_ == CHARTEVENT_OBJECT_CLICK:
        chart_del = (chart_max - chart_min) / 10
        if ObjectFind(Chart_ID, Prefix + 'ButtonUP') == 0:
            if GetState(Prefix + 'ButtonUP'):
                if ObjectFind(Chart_ID, Prefix + 'LineUP') != 0:
                    HLineCreate(Chart_ID, Prefix + 'LineUP', NormalizeDouble(chart_max - chart_del, Digits()), clrBlue, STYLE_DASH, 1, False, True, True, 0)
                if ObjectFind(Chart_ID, Prefix + 'TextUP') != 0:
                    TextCreate(Chart_ID, Prefix + 'TextUP', 0, 0.0, CharToString(233), 'Wingdings', 12, clrBlue, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
            else:
                if ObjectFind(Chart_ID, Prefix + 'LineUP') == 0:
                    ObjectDelete(Chart_ID, Prefix + 'LineUP')
                if ObjectFind(Chart_ID, Prefix + 'TextUP') == 0:
                    ObjectDelete(Chart_ID, Prefix + 'TextUP')
        if ObjectFind(Chart_ID, Prefix + 'ButtonDW') == 0:
            if GetState(Prefix + 'ButtonDW'):
                if ObjectFind(Chart_ID, Prefix + 'LineDW') != 0:
                    HLineCreate(Chart_ID, Prefix + 'LineDW', NormalizeDouble(chart_min + chart_del, Digits()), clrRed, STYLE_DASH, 1, False, True, True, 0)
                if ObjectFind(Chart_ID, Prefix + 'TextDW') != 0:
                    TextCreate(Chart_ID, Prefix + 'TextDW', 0, 0.0, CharToString(234), 'Wingdings', 12, clrRed, 0.0, ANCHOR_LEFT_LOWER, False, False, True, 0)
            else:
                if ObjectFind(Chart_ID, Prefix + 'LineDW') == 0:
                    ObjectDelete(Chart_ID, Prefix + 'LineDW')
                if ObjectFind(Chart_ID, Prefix + 'TextDW') == 0:
                    ObjectDelete(Chart_ID, Prefix + 'TextDW')
        if ObjectFind(Chart_ID, Prefix + 'ButtonTI') == 0:
            if GetState(Prefix + 'ButtonTI'):
                if ObjectFind(Chart_ID, Prefix + 'LineTI') != 0:
                    VLineCreate(Chart_ID, Prefix + 'LineTI', TimeCurrent() + (PeriodSeconds() * 5), clrGreen, STYLE_DASH, 1, False, True, True, (0 != 0))
                if ObjectFind(Chart_ID, Prefix + 'TextTI') != 0:
                    TextCreate(Chart_ID, Prefix + 'TextTI', 0, 0.0, CharToString(232), 'Wingdings', 12, clrGreen, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
            else:
                if ObjectFind(Chart_ID, Prefix + 'LineTI') == 0:
                    ObjectDelete(Chart_ID, Prefix + 'LineTI')
                if ObjectFind(Chart_ID, Prefix + 'TextTI') == 0:
                    ObjectDelete(Chart_ID, Prefix + 'TextTI')
        ChartRedraw(Chart_ID)
    if id_ == CHARTEVENT_MOUSE_MOVE:
        if ObjectFind(Chart_ID, Prefix + 'LineUP') == 0:
            price_line = GetPrice(Prefix + 'LineUP')
            time_line = TimeCurrent()
            SetPrice(Prefix + 'TextUP', price_line)
            SetTime(Prefix + 'TextUP', time_line)
        if ObjectFind(Chart_ID, Prefix + 'LineDW') == 0:
            price_line = GetPrice(Prefix + 'LineDW')
            time_line = TimeCurrent()
            SetPrice(Prefix + 'TextDW', price_line)
            SetTime(Prefix + 'TextDW', time_line)
        if ObjectFind(Chart_ID, Prefix + 'LineTI') == 0:
            time_line = GetTime(Prefix + 'LineTI')
            SetPrice(Prefix + 'TextTI', prices)
            SetTime(Prefix + 'TextTI', time_line)
        ChartRedraw(Chart_ID)

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnTimer():
    global counter_dw, counter_ti, counter_up, prices
    if not SymbolInfoTick(Symbol(), tick):
        Print('SymbolInfoTick() failed, error = ', GetLastError())
    prices = tick.ask
    if ObjectFind(Chart_ID, Prefix + 'LineUP') == 0:
        line_price = NormalizeDouble(GetPrice(Prefix + 'LineUP'), Digits())
        if (line_price - tick.ask) >= (50 * Point()):
            counter_up = 0
    if ObjectFind(Chart_ID, Prefix + 'LineDW') == 0:
        line_price = NormalizeDouble(GetPrice(Prefix + 'LineDW'), Digits())
        if (tick.bid - line_price) >= (50 * Point()):
            counter_dw = 0
    if ObjectFind(Chart_ID, Prefix + 'LineTI') == 0:
        line_time = GetTime(Prefix + 'LineTI')
        if (line_time - tick.time) >= (PeriodSeconds() * 5):
            counter_ti = 0
    text = Symbol() + ' ' + StringSubstr(EnumToString(Period(), ''), 7)
    if GetState(Prefix + 'ButtonUP'):
        if ObjectFind(Chart_ID, Prefix + 'LineUP') == 0 and counter_up < signals:
            Price = ObjectGetDouble(Chart_ID, Prefix + 'LineUP', OBJPROP_PRICE)
            if tick.ask >= NormalizeDouble(Price, Digits()) and Price > 0:
                Alert(text, ' Current price >= Line UP')
                counter_up += 1
    if GetState(Prefix + 'ButtonDW'):
        if ObjectFind(Chart_ID, Prefix + 'LineDW') == 0 and counter_dw < signals:
            Price = ObjectGetDouble(Chart_ID, Prefix + 'LineDW', OBJPROP_PRICE)
            if tick.bid <= NormalizeDouble(Price, Digits()) and Price > 0:
                Alert(text, ' Current price <= Line DW')
                counter_dw += 1
    if GetState(Prefix + 'ButtonTI'):
        if ObjectFind(Chart_ID, Prefix + 'LineTI') == 0 and counter_ti < signals:
            Times = ObjectGetInteger(Chart_ID, Prefix + 'LineTI', OBJPROP_TIME)
            if tick.time >= Times and Times != 0:
                Alert(text, ' Current time >= Line TI')
                counter_ti += 1

def OnDeinit(reason):
    if (reason == REASON_REMOVE or reason == REASON_RECOMPILE) or reason == REASON_INITFAILED:
        ObjectsDeleteAll(Chart_ID, Prefix)
    EventKillTimer()

def GetState(aName):
    value = Box(0)
    ObjectGetInteger(Chart_ID, aName, OBJPROP_STATE, 0, value)
    return _bool(value.v)

def SetState(aName, SetState_):
    return ObjectSetInteger(Chart_ID, aName, OBJPROP_STATE, SetState_)

def GetPrice(aName):
    return ObjectGetDouble(Chart_ID, aName, OBJPROP_PRICE)

def GetTime(aName):
    aValue = Box(0)
    ObjectGetInteger(Chart_ID, aName, OBJPROP_TIME, 0, aValue)
    return aValue.v

def SetPrice(aName, aPrice):
    return ObjectSetDouble(Chart_ID, aName, OBJPROP_PRICE, 0, aPrice)

def SetTime(aName, aTime):
    return ObjectSetInteger(Chart_ID, aName, OBJPROP_TIME, 0, aTime)

def ButtonCreate(chart_ID=0, name='Button', x=0, y=0, width=50, height=18, corner=CORNER_LEFT_UPPER, text='Button', font='Arial', font_size=10, clr=clrBlack, back_clr=0xD8E9EC, border_clr=clrNONE, state=False, back=False, selection=False, hidden=True, z_order=0):
    if ObjectCreate(chart_ID, name, OBJ_BUTTON, 0, 0, 0):
        ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
        ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_STATE, state)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    else:
        return False
    return True

def HLineCreate(chart_ID=0, name='HLine', price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, hidden=True, z_order=0):
    if ObjectCreate(chart_ID, name, OBJ_HLINE, 0, 0, price):
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    else:
        return False
    return True

def VLineCreate(chart_ID=0, name='VLine', time=0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, ray=True, hidden=True, z_order=0):
    if ObjectCreate(chart_ID, name, OBJ_VLINE, 0, time, 0):
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_RAY, ray)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    else:
        return False
    return True

def TextCreate(chart_ID=0, name='Text', time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    if ObjectCreate(chart_ID, name, OBJ_TEXT, 0, time, price):
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
    else:
        return False
    return True

# ---- global variables initialised from expressions
tick = MqlTick()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VRAlertLite(_MQL5Indicator):
    name = 'VR Alert Lite'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

