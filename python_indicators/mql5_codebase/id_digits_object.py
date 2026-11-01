"""id_digits_object — converted from MQL5: MQL5 Indicators/id_digits_object/id_digits_object.mq5

When you click on a graphical object, this indicator
shows in the tab of the trading terminal \\"Experts\\":
- name and type the object;
- time its anchor points;
- the values of its anchor points;
- the number of decimal digits in the anchor points.
Copyright: 2016, Dina Paches; Link: https://login.mql5.com/ru/users/dipach; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2016, Dina Paches', 'link': 'https://login.mql5.com/ru/users/dipach', 'version': '1.20', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['When you click on a graphical object, this indicator', 'shows in the tab of the trading terminal \\"Experts\\":', '- name and type the object;', '- time its anchor points;', '- the values of its anchor points;', '- the number of decimal digits in the anchor points.'], 'name': 'id_digits_object', 'source': 'MQL5 Indicators/id_digits_object/id_digits_object.mq5', 'folder': 'id_digits_object', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_OBJECT_CLICK:
        ActionsDependingOnTheObjectType(0, sparam)
        return
    return

def ActionsDependingOnTheObjectType(chart_id, name_obj):
    index = Box(-1)
    text = Box(TranslatedText(0))
    InitTypeObj(chart_id, name_obj, index, text)
    if index.v == -1:
        Print(text.v)
        return
    number = LocalKeysPriceArray(index.v)
    ArrayResizeAndSetAsSeries(_s_ActionsDependingOnTheObjectType_price_arr, number)
    ArrayResizeAndSetAsSeries(_s_ActionsDependingOnTheObjectType_digits_arr, number)
    PreparePriceData(chart_id, name_obj, _s_ActionsDependingOnTheObjectType_price_arr, _s_ActionsDependingOnTheObjectType_digits_arr)
    number = LocalKeysTimeArray(index.v)
    ArrayResizeAndSetAsSeries(_s_ActionsDependingOnTheObjectType_time_arr, number)
    PrepareTimeData(chart_id, name_obj, _s_ActionsDependingOnTheObjectType_time_arr)
    MessagePrint(_s_ActionsDependingOnTheObjectType_time_arr, _s_ActionsDependingOnTheObjectType_price_arr, _s_ActionsDependingOnTheObjectType_digits_arr, text)
    ArrayFree(_s_ActionsDependingOnTheObjectType_price_arr)
    ArrayFree(_s_ActionsDependingOnTheObjectType_digits_arr)
    ArrayFree(_s_ActionsDependingOnTheObjectType_time_arr)
    return

def InitTypeObj(chart_id, name, index, text):
    type_ = ObjectGetInteger(chart_id, name, OBJPROP_TYPE)
    StringConcatenate(text, text.v, name, TranslatedText(1), EnumToString(type_, 'ENUM_OBJECT'))
    index.v = LocalIndexTypeObjWithTimeAndPrice(type_)
    return index.v

def PrepareTimeData(chart_id, name, time_arr):
    for i in range(ArraySize(time_arr) - 1, 0 - 1, -1):
        time_arr[i] = ObjectGetInteger(chart_id, name, OBJPROP_TIME, i)
    return

def PreparePriceData(chart_id, name, price_arr, digits_arr):
    size = ArraySize(price_arr)
    for i in range(size - 1, 0 - 1, -1):
        price_arr[i] = ObjectGetDouble(chart_id, name, OBJPROP_PRICE, i)
    for i in range(size - 1, 0 - 1, -1):
        digits_arr[i] = NumberOfDigitsGet(price_arr[i])
    return

def NumberOfDigitsGet(value, digits=8):
    dig = (8 if (digits < 1 or digits > 8) else digits)
    if NormalizeDouble(value, dig) == 0:
        return 0
    val = value
    if NormalizeDouble(val, dig) < 0:
        val = MathAbs(val)
    int_value = MathFloor(val)
    val = NormalizeDouble(val - int_value, dig)
    if NormalizeDouble(val, dig) == 0:
        return 0
    point_pow = _int(MathPow(10, dig))
    variable = _int(NormalizeDouble(val * point_pow, 0))
    text = IntegerToString(variable)
    variable = StringLen(text)
    for i in range(variable - 1, 0 - 1, -1):
        if StringFind(text, '0', i) == i:
            dig -= 1
        else:
            return dig
    return dig

def ArrayResizeAndSetAsSeries(array, new_size, reserve_size=-1, flag=True):
    ArrayResize(array, new_size, reserve_size)
    if new_size > 1:
        ArraySetAsSeries(array, flag)
    return

def TextTimeSet(time, index, text):
    StringConcatenate(text, TranslatedText(2), '(', IntegerToString(index), '): ', TimeToString(time, TIME_DATE | TIME_SECONDS), '. ')
    return

def TextPriceAndDigitsSet(price, digits, index):
    text = Box(TranslatedText(4))
    DigitsTextSet(digits, text)
    StringConcatenate(text, TranslatedText(3), '(', IntegerToString(index), '): ', DoubleToString(price, digits), text.v, IntegerToString(digits))
    return text.v

def DigitsTextSet(digits, text):
    if digits >= 8:
        StringAdd(text, '>= ')
    else:
        StringAdd(text, '= ')
    return text.v

def MessagePrint(time_arr, price_arr, digits_arr, text):
    time_size = ArraySize(time_arr)
    price_size = ArraySize(price_arr)
    Print(text.v)
    for i in range(0, time_size):
        TextTimeSet(time_arr[i], i, text)
        if price_size > 0:
            add = TextPriceAndDigitsSet(price_arr[i], digits_arr[i], i)
            StringAdd(text, add)
            price_size -= 1
        Print(text.v)
    return

def TranslatedText(index):
    global _s_TranslatedText_first
    if _s_TranslatedText_first:
        TerminalLanguage(_s_TranslatedText_text_arr)
        _s_TranslatedText_first = False
    return _s_TranslatedText_text_arr[index]

def TerminalLanguage(text_arr):
    language = TerminalInfoString(TERMINAL_LANGUAGE)
    if language == 'Russian':
        text_arr[0] = 'Имя объекта: '
        text_arr[1] = ', тип: '
        text_arr[2] = 'Дата'
        text_arr[3] = 'Значение'
        text_arr[4] = ', digits '
        text_arr[5] = 'Я не работаю с таким типом объектов:'
    else:
        text_arr[0] = 'Object name: '
        text_arr[1] = ', type: '
        text_arr[2] = 'Date'
        text_arr[3] = 'Value'
        text_arr[4] = ', digits '
        text_arr[5] = "I don't work with this type of objects:"
    return

def LocalIndexTypeObjWithTimeAndPrice(type_):
    i = 0
    while i < 34:
        if type_ == _s_LocalIndexTypeObjWithTimeAndPrice_type_arr[i]:
            break
        i += 1
    if i < (34 - 1):
        return i
    else:
        Print(TranslatedText(5))
    return -1

def LocalKeysPriceArray(index):
    return _s_LocalKeysPriceArray_price_number_arr[index]

def LocalKeysTimeArray(index):
    return _s_LocalKeysTimeArray_time_number_arr[index]

# ---- static local variables
_s_ActionsDependingOnTheObjectType_price_arr = Arr(0, 0.0)
_s_ActionsDependingOnTheObjectType_digits_arr = Arr(0, 0)
_s_ActionsDependingOnTheObjectType_time_arr = Arr(0, 0)
_s_TranslatedText_text_arr = Arr(6, "", dyn=False)
_s_TranslatedText_first = True
_s_LocalIndexTypeObjWithTimeAndPrice_type_arr = Arr.of([OBJ_HLINE, OBJ_TREND, OBJ_TRENDBYANGLE, OBJ_CYCLES, OBJ_ARROWED_LINE, OBJ_CHANNEL, OBJ_PITCHFORK, OBJ_GANNLINE, OBJ_GANNFAN, OBJ_GANNGRID, OBJ_FIBO, OBJ_FIBOTIMES, OBJ_FIBOFAN, OBJ_FIBOARC, OBJ_FIBOCHANNEL, OBJ_EXPANSION, OBJ_ELLIOTWAVE5, OBJ_ELLIOTWAVE3, OBJ_RECTANGLE, OBJ_TRIANGLE, OBJ_ELLIPSE, OBJ_ARROW_THUMB_UP, OBJ_ARROW_THUMB_DOWN, OBJ_ARROW_UP, OBJ_ARROW_DOWN, OBJ_ARROW_STOP, OBJ_ARROW_CHECK, OBJ_ARROW_LEFT_PRICE, OBJ_ARROW_RIGHT_PRICE, OBJ_ARROW_BUY, OBJ_ARROW_SELL, OBJ_ARROW, OBJ_TEXT, -1], fill=0, dyn=False, size=34)
_s_LocalKeysPriceArray_price_number_arr = Arr.of([1, 2, 2, 2, 2, 3, 3, 1, 1, 1, 2, 2, 2, 2, 3, 3, 5, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], fill=0, dyn=False, size=33)
_s_LocalKeysTimeArray_time_number_arr = Arr.of([1, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 5, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], fill=0, dyn=False, size=33)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IdDigitsObject(_MQL5Indicator):
    name = 'id_digits_object'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

