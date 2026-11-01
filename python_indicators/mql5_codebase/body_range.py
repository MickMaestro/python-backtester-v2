"""Body_Range — converted from MQL5: MQL5 Indicators/Candlestick Body, High Low and Wick Range/Body_Range.mq5

Copyright: Copyright 2023, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Body_Range', 'source': 'MQL5 Indicators/Candlestick Body, High Low and Wick Range/Body_Range.mq5', 'folder': 'Candlestick Body, High Low and Wick Range', 'inputs': [{'mql': 'InpFont', 'py': 'InpFont', 'param': None, 'type': 'string', 'default': 'Courier New', 'label': 'Font', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 12, 'label': 'Font size', 'sinput': False}, {'mql': 'InpFontColor', 'py': 'InpFontColor', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'Font color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFont = _input('InpFont', 'Courier New')  # Font
InpFontSize = _input('InpFontSize', 12)  # Font size
InpFontColor = _input('InpFontColor', clrSnow)  # Font color
m_prefix = 'BR_Info_'  # prefix for object
m_init_error = False  # error on InInit

def OnInit():
    ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global m_init_error
    if m_init_error:
        return
    if id_ == CHARTEVENT_CLICK:
        sub_window = Box(0)
        time = Box(0)
        price = Box(0.0)
        price_offset = Box(0.0)
        if not ChartXYToTimePrice(ChartID(), _int(lparam), _int(dparam), sub_window, time, price):
            return
        if not ChartXYToTimePrice(ChartID(), _int(lparam), _int(dparam) + 20, sub_window, time, price_offset):
            return
        bar_shift = iBarShift(Symbol(), Period(), time.v, False)
        if bar_shift < 0:
            return
        rates = Arr(0, 0, factory=MqlRates)
        if CopyRates(Symbol(), Period(), bar_shift, 1, rates) != 1:
            return
        vertical_offset = price.v - price_offset.v
        if not TextCreate(0, m_prefix + 'Bull_BR', 0, 0, 0.0, 'BR ', 0.0, InpFont, InpFontSize, InpFontColor, ANCHOR_LEFT_UPPER):
            ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)
            m_init_error = True
            return
        if not TextCreate(0, m_prefix + 'Bear_BR', 0, 0, 0.0, 'BR ', 0.0, InpFont, InpFontSize, InpFontColor, ANCHOR_LEFT_UPPER):
            ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)
            m_init_error = True
            return
        if rates[0].open > rates[0].close:
            TextChange(ChartID(), m_prefix + 'Bull_BR', 'BR:  ' + DoubleToString(-(rates[0].close - rates[0].open), Digits()))
        else:
            TextChange(ChartID(), m_prefix + 'Bear_BR', 'BR:  ' + DoubleToString(-(rates[0].open - rates[0].close), Digits()))
        TextMove(ChartID(), m_prefix + 'Bull_BR', rates[0].time + PeriodSeconds(), price.v - (vertical_offset * 1.0))
        TextMove(ChartID(), m_prefix + 'Bear_BR', rates[0].time + PeriodSeconds(), price.v - (vertical_offset * 1.0))
        ChartRedraw()
    if id_ == CHARTEVENT_KEYDOWN:
        _sw1 = _int(lparam)
        if _sw1 == 68:
            ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)
            ChartRedraw()
        return

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BodyRange(_MQL5Indicator):
    name = 'Body_Range'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFontSize': 12,  # Font size
    }

