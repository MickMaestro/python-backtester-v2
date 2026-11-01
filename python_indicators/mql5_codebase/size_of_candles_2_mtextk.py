"""Size_of_candles_2_mtextk — converted from MQL5: MQL5 Indicators/Size of candles 2 (text)/Size_of_candles_2_mtextk.mq5

 
The size of the candles in the form of text above each bar
---
Calculation of candles size: the \\"Minuend\\" minus the \\"Subtrahend\\"
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [' ', 'The size of the candles in the form of text above each bar', '---', 'Calculation of candles size: the \\"Minuend\\" minus the \\"Subtrahend\\"'], 'name': 'Size_of_candles_2_mtextk', 'source': 'MQL5 Indicators/Size of candles 2 (text)/Size_of_candles_2_mtextk.mq5', 'folder': 'Size of candles 2 (text)', 'inputs': [{'mql': 'InpNumberOfBars', 'py': 'InpNumberOfBars', 'param': 'InpNumberOfBars', 'type': 'uchar', 'default': 3, 'label': 'Number of bars (do not use "0")', 'sinput': False}, {'mql': 'InpMinuend', 'py': 'InpMinuend', 'param': 'InpMinuend', 'type': 'int', 'default': 1, 'label': 'Minuend', 'sinput': False}, {'mql': 'InpSubtrahend', 'py': 'InpSubtrahend', 'param': 'InpSubtrahend', 'type': 'int', 'default': 2, 'label': 'Subtrahend', 'sinput': False}, {'mql': 'InpColorBullish', 'py': 'InpColorBullish', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'The color of bullish bars', 'sinput': False}, {'mql': 'InpColorBearish', 'py': 'InpColorBearish', 'param': None, 'type': 'color', 'default': 255, 'label': 'The color of bearish bars', 'sinput': False}, {'mql': 'InpIndent', 'py': 'InpIndent', 'param': 'InpIndent', 'type': 'bool', 'default': True, 'label': 'Indent', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum OHLC
Open = 0
High = 1
Low = 2
Close = 3
_enum('OHLC', {0: 'Open', 1: 'High', 2: 'Low', 3: 'Close'})

# ---- inputs and global variables
InpNumberOfBars = _input('InpNumberOfBars', 3)  # Number of bars (do not use "0")
InpMinuend = _input('InpMinuend', High)  # Minuend
InpSubtrahend = _input('InpSubtrahend', Low)  # Subtrahend
InpColorBullish = _input('InpColorBullish', clrBlue)  # The color of bullish bars
InpColorBearish = _input('InpColorBearish', clrRed)  # The color of bearish bars
InpIndent = _input('InpIndent', True)  # Indent
m_prefix = 'size_candles_'  # prefix for object
m_adjusted_point = 0.0  # point value adjusted for 3 or 5 points
m_arr_names = Arr(0, "")  # array of names of objects OBJ_TEXT

def OnInit():
    global m_adjusted_point, m_prefix
    if InpNumberOfBars == 0:
        Print('"Number of bars"==0. Do not use "0"')
        return INIT_PARAMETERS_INCORRECT
    m_prefix += EnumToString(Period(), '') + '_'
    digits_adjust = 1
    if Digits() == 3 or Digits() == 5:
        digits_adjust = 10
    m_adjusted_point = Point() * digits_adjust
    DeleteAll()
    ResetLastError()
    if ArrayResize(m_arr_names, InpNumberOfBars) == -1:
        Print('OnInit', ' ArrayResize error')
        return INIT_SUCCEEDED
    ArraySetAsSeries(m_arr_names, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    DeleteAll()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated == 0 or prev_calculated != rates_total:
        DeleteAll()
        ResetLastError()
        ArrayFree(m_arr_names)
        if ArrayResize(m_arr_names, InpNumberOfBars) == -1:
            Print('OnCalculate', ', prev_calculated==0, ArrayResize error')
            return 0
        limit = InpNumberOfBars - 1
        for i in range(limit, 0 - 1, -1):
            name = m_prefix + 'high_' + TimeToString(time[i])
            text = Calculate(open[i], high[i], low[i], close[i])
            if open[i] > close[i]:
                if InpIndent:
                    text = text + ' '
                if not TextCreate(0, name, 0, time[i], low[i], text, 90.0, 'Lucida Console', 10, InpColorBearish, ANCHOR_RIGHT):
                    return 0
            else:
                if InpIndent:
                    text = ' ' + text
                if not TextCreate(0, name, 0, time[i], high[i], text, 90.0, 'Lucida Console', 10, InpColorBullish, ANCHOR_LEFT):
                    return 0
            m_arr_names[i] = name
        return rates_total
    price_ = ObjectGetDouble(0, m_arr_names[0], OBJPROP_PRICE, 0)
    time_ = ObjectGetInteger(0, m_arr_names[0], OBJPROP_TIME, 0)
    text = Calculate(open[0], high[0], low[0], close[0])
    TextChange(0, m_arr_names[0], text)
    if high[0] > price_:
        TextMove(0, m_arr_names[0], time_, high[0])
    return rates_total

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', angle=90.0, font='Lucida Console', font_size=10, clr=clrBlue, anchor=ANCHOR_LEFT, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time, price):
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

def TextMove(chart_ID=0, name='Text', time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, time, price):
        Print('TextMove', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def TextChange(chart_ID=0, name='Text', text='Text'):
    ResetLastError()
    if not ObjectSetString(chart_ID, name, OBJPROP_TEXT, text):
        Print('TextChange', ': failed to change the text! Error code = ', GetLastError())
        return False
    return True

def DeleteAll():
    chart_id = 0
    prefix = m_prefix
    sub_window = 0
    object_type = OBJ_TEXT
    ObjectsDeleteAll(chart_id, prefix, sub_window, object_type)

def Calculate(open, high, low, close):
    minuend = 0.0
    _sw1 = InpMinuend
    if _sw1 == Open:
        minuend = open
    elif _sw1 == High:
        minuend = high
    elif _sw1 == Low:
        minuend = low
    elif _sw1 == Close:
        minuend = close
    subtrahend = 0.0
    _sw2 = InpSubtrahend
    if _sw2 == Open:
        subtrahend = open
    elif _sw2 == High:
        subtrahend = high
    elif _sw2 == Low:
        subtrahend = low
    elif _sw2 == Close:
        subtrahend = close
    text = DoubleToString(_fdiv(MathAbs(minuend - subtrahend), m_adjusted_point), 0)
    return text


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SizeOfCandles2Mtextk(_MQL5Indicator):
    name = 'Size_of_candles_2_mtextk'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpNumberOfBars': 3,  # Number of bars (do not use "0")
        'InpMinuend': _Choice({0: 'Open', 1: 'High', 2: 'Low', 3: 'Close'}, default=1),  # Minuend
        'InpSubtrahend': _Choice({0: 'Open', 1: 'High', 2: 'Low', 3: 'Close'}, default=2),  # Subtrahend
        'InpIndent': True,  # Indent
    }

