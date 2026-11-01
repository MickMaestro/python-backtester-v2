"""xhair — converted from MQL5: MQL5 Indicators/Custom crosshair cursor with synchronization/xhair.mq5

Copyright: Copyright 2024, seffx; Link: https://www.mql5.com/en/users/seffx; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, seffx', 'link': 'https://www.mql5.com/en/users/seffx', 'version': '1.20', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'xhair', 'source': 'MQL5 Indicators/Custom crosshair cursor with synchronization/xhair.mq5', 'folder': 'Custom crosshair cursor with synchronization', 'inputs': [{'mql': 'localTime', 'py': 'localTime', 'param': 'localTime', 'type': 'bool', 'default': True, 'label': 'Show localtime', 'sinput': True}, {'mql': 'cursorColor', 'py': 'cursorColor', 'param': None, 'type': 'color', 'default': 13882323, 'label': 'Cursor color', 'sinput': True}, {'mql': 'cursorName', 'py': 'cursorName', 'param': None, 'type': 'string', 'default': 'XHAIR', 'label': 'Cursor name', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
localTime = _input('localTime', True)  # Show localtime
cursorColor = _input('cursorColor', clrLightGray)  # Cursor color
cursorName = _input('cursorName', 'XHAIR')  # Cursor name
YLINE = '_xhair_Y'
XLINE = '_xhair_X'
xhair_price = ''
xhair_time = ''
last_time = 0
last_price = 0.0
started = 20
lines_hidden = False

def VLineCreate(name, time=0):
    chart_ID = 0
    sub_window = 0
    clr = cursorColor
    style = STYLE_DOT
    width = 1
    back = False
    selection = False
    ray = True
    hidden = True
    z_order = -1
    if not time:
        time = TimeCurrent()
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_VLINE, sub_window, time, 0):
        Print('VLineCreate', ': failed to create a vertical line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY, ray)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    ObjectSetString(chart_ID, name, OBJPROP_TOOLTIP, '\n')
    return True

def HLineCreate(name, price=0.0):
    chart_ID = 0
    sub_window = 0
    clr = cursorColor
    style = STYLE_DOT
    width = 1
    back = False
    selection = False
    ray = True
    hidden = True
    z_order = 0
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    ObjectSetString(chart_ID, name, OBJPROP_TOOLTIP, '\n')
    return True

def OnInit():
    global xhair_price, xhair_time
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, True)
    ChartSetInteger(0, CHART_AUTOSCROLL, False)
    xhair_price = StringFormat('%s_PRICE', cursorName)
    xhair_time = StringFormat('%s_TIME', cursorName)
    time = TimeCurrent()
    price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    VLineCreate(YLINE, time)
    HLineCreate(XLINE, price)
    EventSetMillisecondTimer(100)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()
    ObjectsDeleteAll(0, '_xhair_')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def showLocaltime(time, price):
    if localTime:
        tserver = TimeTradeServer()
        tlocal = TimeLocal()
        diff = _int(tserver - tlocal)
        localtime = time - diff
        localtime_str = TimeToString(localtime)
        ObjectSetString(0, YLINE, OBJPROP_TOOLTIP, localtime_str)
        ObjectSetString(0, XLINE, OBJPROP_TOOLTIP, localtime_str + '\n' + DoubleToString(price, Digits()))
    else:
        ObjectSetString(0, YLINE, OBJPROP_TOOLTIP, '\n')
        ObjectSetString(0, XLINE, OBJPROP_TOOLTIP, '\n')

def OnChartEvent(id_, lparam, dparam, sparam):
    global last_price, last_time, started
    if id_ == CHARTEVENT_KEYDOWN:
        if lparam == 27:
            t = _int(GlobalVariableGet(xhair_time))
            dt = t
            if t == 0:
                GlobalVariableSet(xhair_time, last_time)
            else:
                GlobalVariableSet(xhair_time, 0)
            return
    if id_ != CHARTEVENT_MOUSE_MOVE:
        return
    x = _int(lparam)
    y = _int(dparam)
    sub = Box(0)
    time = Box(0)
    price = Box(0.0)
    if ChartXYToTimePrice(0, x, y, sub, time, price):
        flags = StringToInteger(sparam)
        if ((flags & 8) == 8 or (flags & 4) == 4) or (flags & 16) == 16:
            started = 0
            last_price = price.v
            last_time = time.v
            GlobalVariableSet(xhair_price, price.v)
            GlobalVariableSet(xhair_time, time.v)
            ObjectMove(0, YLINE, 0, time.v, 0)
            ObjectMove(0, XLINE, 0, time.v, price.v)
            showLocaltime(time.v, price.v)
            ChartRedraw(0)

def NavigateTo(time, price):
    bar_index = iBarShift(None, PERIOD_CURRENT, time, False)
    if bar_index == -1:
        return False
    first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    total_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    last_bar = first_bar - total_bars
    if bar_index > first_bar:
        if not ChartNavigate(0, CHART_CURRENT_POS, first_bar - bar_index - _idiv(total_bars, 4)):
            return False
    elif bar_index < last_bar:
        if not ChartNavigate(0, CHART_CURRENT_POS, first_bar - bar_index - (total_bars - _idiv(total_bars, 4))):
            return False
    ObjectMove(0, XLINE, 0, 0, price)
    ObjectMove(0, YLINE, 0, time, 0)
    ChartRedraw(0)
    return True

def OnTimer():
    global last_price, last_time, lines_hidden, started
    tmp = Box(0.0)
    price = Box(0.0)
    time = 0
    if GlobalVariableGet(xhair_time, tmp):
        time = _long(tmp.v)
    else:
        if started > 0:
            started = started - 1
            if started <= 0:
                ObjectSetInteger(0, XLINE, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)
                ObjectSetInteger(0, YLINE, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)
                ChartRedraw(0)
                lines_hidden = True
        return
    if time == 0:
        ObjectSetInteger(0, XLINE, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)
        ObjectSetInteger(0, YLINE, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)
        ChartRedraw(0)
        lines_hidden = True
        return
    if not GlobalVariableGet(xhair_price, price):
        return
    ObjectSetInteger(0, XLINE, OBJPROP_TIMEFRAMES, OBJ_ALL_PERIODS)
    ObjectSetInteger(0, YLINE, OBJPROP_TIMEFRAMES, OBJ_ALL_PERIODS)
    ChartRedraw(0)
    price_changed = MathAbs(price.v - last_price) > DBL_EPSILON
    time_changed = time != last_time
    if (lines_hidden or time_changed) or price_changed:
        lines_hidden = False
        ChartSetInteger(0, CHART_AUTOSCROLL, False)
        ChartRedraw(0)
        last_price = price.v
        last_time = time
        NavigateTo(time, price.v)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xhair(_MQL5Indicator):
    name = 'xhair'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'localTime': True,  # Show localtime
    }

