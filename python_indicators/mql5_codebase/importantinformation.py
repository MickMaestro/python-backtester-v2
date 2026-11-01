"""ImportantInformation — converted from MQL5: MQL5 Indicators/ImportantInformation/ImportantInformation.mq5

Copyright: Copyright 2014, papaklass; Link: https://login.mql5.com/ru/users/papaklass; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, papaklass', 'link': 'https://login.mql5.com/ru/users/papaklass', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ImportantInformation', 'source': 'MQL5 Indicators/ImportantInformation/ImportantInformation.mq5', 'folder': 'ImportantInformation', 'inputs': [{'mql': 'FirstColor', 'py': 'FirstColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': '', 'sinput': False}, {'mql': 'SecondColor', 'py': 'SecondColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Areal', 'label': '', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 0, 'label': 'Corner = 0 - LeftTop. (0 - 3)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FirstColor = _input('FirstColor', clrWhite)
SecondColor = _input('SecondColor', clrAqua)
FontSize = _input('FontSize', 10)
Font = _input('Font', 'Areal')
Corner = _input('Corner', 0)  # Corner = 0 - LeftTop. (0 - 3)
nameObject = Arr.of(['time', 'account', 'symbol', 'symbol2'], fill="", dyn=False, size=4)

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    size = ArraySize(nameObject)
    distance = FontSize + _idiv(FontSize, 2)
    for i in range(0, size):
        ObjectCreate(0, nameObject[i], OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, nameObject[i], OBJPROP_CORNER, Corner)
        ObjectSetInteger(0, nameObject[i], OBJPROP_XDISTANCE, 280)
        ObjectSetInteger(0, nameObject[i], OBJPROP_YDISTANCE, (i + 1) * distance)
    text = Box('')
    StringAdd(text, 'cur: ')
    StringAdd(text, TimeToString(TimeCurrent(), TIME_SECONDS))
    StringAdd(text, '  loc: ')
    StringAdd(text, TimeToString(TimeLocal(), TIME_SECONDS))
    StringAdd(text, '  gmt: ')
    StringAdd(text, TimeToString(TimeGMT(), TIME_SECONDS))
    ObjectSetString(0, 'time', OBJPROP_TEXT, text.v)
    ObjectSetString(0, 'time', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'time', OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, 'time', OBJPROP_COLOR, FirstColor)
    account_type = AccountInfoInteger(ACCOUNT_TRADE_MODE)
    trade_mode = ""
    _sw1 = account_type
    if _sw1 == ACCOUNT_TRADE_MODE_DEMO:
        trade_mode = 'Demo'
    elif _sw1 == ACCOUNT_TRADE_MODE_CONTEST:
        trade_mode = 'Contest'
    else:
        trade_mode = 'Live'
    text1 = Box('')
    StringAdd(text1, trade_mode)
    StringAdd(text1, '  lev: ')
    StringAdd(text1, IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)))
    StringAdd(text1, '  bal: ')
    StringAdd(text1, DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2))
    StringAdd(text1, '  equ: ')
    StringAdd(text1, DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2))
    ObjectSetString(0, 'account', OBJPROP_TEXT, text1.v)
    ObjectSetString(0, 'account', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'account', OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, 'account', OBJPROP_COLOR, SecondColor)
    text2 = Box('')
    StringAdd(text2, 'spread: ')
    StringAdd(text2, IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD), 2))
    StringAdd(text2, '  swapL: ')
    StringAdd(text2, DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_LONG), 2))
    StringAdd(text2, '  swapS: ')
    StringAdd(text2, DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_SHORT), 2))
    ObjectSetString(0, 'symbol', OBJPROP_TEXT, text2.v)
    ObjectSetString(0, 'symbol', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'symbol', OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, 'symbol', OBJPROP_COLOR, FirstColor)
    text3 = Box('')
    StringAdd(text3, 'tickVal: ')
    StringAdd(text3, DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE), Digits()))
    StringAdd(text3, '  minLot: ')
    StringAdd(text3, DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_MIN), 2))
    StringAdd(text3, '  maxLot: ')
    StringAdd(text3, DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_MAX), 2))
    ObjectSetString(0, 'symbol2', OBJPROP_TEXT, text3.v)
    ObjectSetString(0, 'symbol2', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'symbol2', OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, 'symbol2', OBJPROP_COLOR, SecondColor)
    ChartRedraw(0)
    return rates_total

def OnDeinit(reason):
    size = ArraySize(nameObject)
    for j in range(0, size):
        if not ObjectDelete(0, nameObject[j]):
            Alert('Объект ', nameObject[j], 'не удален. Error = ', GetLastError())


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ImportantInformation(_MQL5Indicator):
    name = 'ImportantInformation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 10,
        'Corner': 0,  # Corner = 0 - LeftTop. (0 - 3)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

