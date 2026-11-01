"""HorizontalLineNotif — converted from MQL5: MQL5 Indicators/Price Horizontal Line Notifications/HorizontalLineNotif.mq5

Agianto Simanullang
Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: TranslateKey
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Agianto Simanullang'], 'name': 'HorizontalLineNotif', 'source': 'MQL5 Indicators/Price Horizontal Line Notifications/HorizontalLineNotif.mq5', 'folder': 'Price Horizontal Line Notifications', 'inputs': [{'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Width', 'py': 'Width', 'param': 'Width', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ObjectColor', 'py': 'ObjectColor', 'param': None, 'type': 'color', 'default': 36095, 'label': '', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'ByMT4', 'py': 'ByMT4', 'param': None, 'type': 'string', 'default': 'By MT4', 'label': '', 'sinput': False}, {'mql': 'AlertMessage', 'py': 'AlertMessage', 'param': 'AlertMessage', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'AlertSound', 'py': 'AlertSound', 'param': 'AlertSound', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'AlertNotify', 'py': 'AlertNotify', 'param': 'AlertNotify', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'AlertEmail', 'py': 'AlertEmail', 'param': 'AlertEmail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SoundFile', 'py': 'SoundFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LineStyle = _input('LineStyle', STYLE_DOT)
Width = _input('Width', 1)
ObjectColor = _input('ObjectColor', clrDarkOrange)
FontType = _input('FontType', 'Arial')
FontSize = _input('FontSize', 6)
ByMT4 = _input('ByMT4', 'By MT4')
AlertMessage = _input('AlertMessage', True)
AlertSound = _input('AlertSound', True)
AlertNotify = _input('AlertNotify', True)
AlertEmail = _input('AlertEmail', False)
SoundFile = _input('SoundFile', 'alert.wav')
hl_text = ""
vdigits = 0
vperiod = PERIOD_CURRENT
pips2dbl = 0.0
vpoint = 0.0
price_signal = 0.0
vopen = 0.0
vclose = 0.0
curr_close_price = 0.0
last_close_price = 0.0
sTfTable = Arr.of(['M1', 'M5', 'M10', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN'], fill="")
iTfTable = Arr.of([1, 5, 10, 15, 30, 60, 240, 1440, 10080, 43200], fill=0)

def OnInit():
    global pips2dbl, price_signal, vdigits, vpoint
    vdigits = _int(SymbolInfoInteger(vsymbol, SYMBOL_DIGITS))
    vpoint = SymbolInfoDouble(vsymbol, SYMBOL_POINT)
    if _imod(vdigits, 2) == 1:
        pips2dbl = vpoint * 10
    else:
        pips2dbl = vpoint
    price_signal = iClose(vsymbol, vperiod, 1)
    price_signal = NormalizeDouble(price_signal + (30.0 * pips2dbl), vdigits)
    HorizontalLine('1', created_time, price_signal)
    HorizontalText('1', created_time, price_signal, 'Alert at ' + DoubleToString(price_signal, vdigits))
    Comment('[N] New signal \n[D] Deleted all signal')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global created_time, curr_close_price, hl_text, last_close_price, price_signal, vopen
    created_time = TimeCurrent()
    vopen = NormalizeDouble(iOpen(vsymbol, vperiod, 0), vdigits)
    curr_close_price = NormalizeDouble(iClose(vsymbol, vperiod, 0), vdigits)
    if last_close_price == 0:
        last_close_price = curr_close_price
    for obj_total in range(ObjectsTotal(0) - 1, 0 - 1, -1):
        on = ObjectName(0, obj_total)
        if StringFind(on, 'hl_') >= 0:
            price_signal = NormalizeDouble(ObjectGetDouble(0, on, OBJPROP_PRICE, 0), vdigits)
            index_signal = StringSubstr(on, 3, StringLen(on) - 3)
            hl_text = ObjectGetString(0, 'txt_' + index_signal, OBJPROP_TEXT, 0)
            HorizontalLine(index_signal, created_time, price_signal)
            HorizontalText(index_signal, created_time, price_signal, hl_text)
            if ((vopen < price_signal and last_close_price < price_signal) and curr_close_price > price_signal) or ((vopen > price_signal and last_close_price > price_signal) and curr_close_price < price_signal):
                if StringFind(hl_text, 'done') < 0:
                    SendNotifications(hl_text)
                    HorizontalText(index_signal, created_time, price_signal, hl_text + ', done!!!')
    last_close_price = curr_close_price
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global hl_text, price_signal
    obj_total = 0
    on = ""
    index_signal = 0
    if id_ == CHARTEVENT_OBJECT_DRAG:
        if StringFind(sparam, 'hl_') >= 0 or StringFind(sparam, 'txt_') >= 0:
            price_signal = NormalizeDouble(ObjectGetDouble(0, sparam, OBJPROP_PRICE, 0), vdigits)
            index_signal = StringToInteger(StringSubstr(sparam, 3, StringLen(sparam) - 3))
            hl_text = ObjectGetString(0, 'txt_' + _str(index_signal), OBJPROP_TEXT, 0)
            HorizontalText(_str(index_signal), created_time, price_signal, 'Alert at ' + DoubleToString(price_signal, vdigits))
    if id_ == CHARTEVENT_KEYDOWN:
        sym = _short(_missing('TranslateKey')(_int(lparam)))
        if sym > 0:
            if ShortToString(sym) == 'N' or ShortToString(sym) == 'n':
                index_signal = 1
                price_signal = 0.0
                price_signal_temp = 0.0
                obj_total = ObjectsTotal(0) - 1
                for obj_total in range(obj_total, 0 - 1, -1):
                    on = ObjectName(0, obj_total)
                    if StringFind(on, 'hl_') >= 0:
                        index_signal_temp = StringToInteger(StringSubstr(on, 3, StringLen(on) - 3))
                        if index_signal_temp >= index_signal:
                            index_signal = index_signal_temp + 1
                        price_signal_temp = NormalizeDouble(ObjectGetDouble(0, on, OBJPROP_PRICE, 0), vdigits)
                        if price_signal_temp > price_signal:
                            price_signal = price_signal_temp
                else:
                    obj_total = _range_end(obj_total, 0 - 1, -1)
                if price_signal == 0:
                    price_signal = iClose(vsymbol, vperiod, 1)
                price_signal = NormalizeDouble(price_signal + (30.0 * pips2dbl), vdigits)
                HorizontalLine(_str(index_signal), created_time, price_signal)
                HorizontalText(_str(index_signal), created_time, price_signal, 'Alert at ' + DoubleToString(price_signal, vdigits))
            if ShortToString(sym) == 'D' or ShortToString(sym) == 'd':
                DeleteAllObjects()

def HorizontalLine(name, time, price):
    name = 'hl_' + name
    if ObjectFind(0, name) < 0:
        if not ObjectCreate(0, name, OBJ_HLINE, 0, time, price):
            Print('Draw the line failed with error #', GetLastError())
        ObjectSetInteger(0, name, OBJPROP_WIDTH, Width)
        ObjectSetInteger(0, name, OBJPROP_STYLE, LineStyle)
        ObjectSetInteger(0, name, OBJPROP_COLOR, ObjectColor)
        ObjectSetInteger(0, name, OBJPROP_BACK, False)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name, OBJPROP_SELECTED, True)
    else:
        ObjectSetInteger(0, name, OBJPROP_TIME, time)
        ObjectSetDouble(0, name, OBJPROP_PRICE, price)
    ChartRedraw(0)

def HorizontalText(_name, _time, _price, _text):
    name = 'txt_' + _name
    _time = _time + (PeriodSeconds() * 2)
    if ObjectFind(0, name) < 0:
        if not ObjectCreate(0, name, OBJ_TEXT, 0, _time, _price):
            Print('Fail to draw the text ERROR CODE : ', GetLastError())
        ObjectSetString(0, name, OBJPROP_FONT, FontType)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(0, name, OBJPROP_TEXT, _text)
        ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, name, OBJPROP_COLOR, ObjectColor)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
    else:
        ObjectSetString(0, name, OBJPROP_TEXT, _text)
        ObjectSetInteger(0, name, OBJPROP_TIME, _time)
        ObjectSetDouble(0, name, OBJPROP_PRICE, _price)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
    ChartRedraw(0)

def OnDeinit(reason):
    DeleteAllObjects()
    Comment('')

def DeleteAllObjects():
    for iObj in range(ObjectsTotal(0) - 1, 0 - 1, -1):
        on = ObjectName(0, iObj)
        if StringFind(on, 'hl_') == 0 or StringFind(on, 'txt_') == 0:
            ObjectDelete(0, on)

def timeFrameToString(tf):
    for i in range(ArraySize(iTfTable) - 1, 0 - 1, -1):
        if tf == iTfTable[i]:
            return sTfTable[i]
    return ''

def SendNotifications(message):
    message = vsymbol + '.' + timeFrameToString(_idiv(PeriodSeconds(vperiod), 60)) + '.' + message
    if AlertMessage:
        Alert(message)
    if AlertEmail:
        SendMail('Notification price hits', message)
    if AlertNotify:
        SendNotification(StringSubstr(message, 0, 255))
    if AlertSound:
        PlaySound(SoundFile)

# ---- global variables initialised from expressions
vsymbol = Symbol()
created_time = TimeCurrent()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HorizontalLineNotif(_MQL5Indicator):
    name = 'HorizontalLineNotif'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'Width': 1,
        'FontSize': 6,
        'AlertMessage': True,
        'AlertSound': True,
        'AlertNotify': True,
        'AlertEmail': False,
    }

