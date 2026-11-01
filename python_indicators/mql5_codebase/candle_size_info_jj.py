"""candle_size_info_jj — converted from MQL5: MQL5 Indicators/Candle Size Info/candle_size_info_jj.mq5

Script cria objeto grбfico de \\"Texto\\".

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Script cria objeto grбfico de \\"Texto\\".'], 'name': 'candle_size_info_jj', 'source': 'MQL5 Indicators/Candle Size Info/candle_size_info_jj.mq5', 'folder': 'Candle Size Info', 'inputs': [{'mql': 'IHistoryBars', 'py': 'IHistoryBars', 'param': 'IHistoryBars', 'type': 'int', 'default': 25, 'label': 'Check Historical Data', 'sinput': False}, {'mql': 'InpFont', 'py': 'InpFont', 'param': None, 'type': 'string', 'default': 'Tahoma', 'label': 'Font Type', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 7, 'label': 'Size of fonts', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Cor Up', 'sinput': False}, {'mql': 'DwColor', 'py': 'DwColor', 'param': None, 'type': 'color', 'default': 14772545, 'label': 'Cor Dw', 'sinput': False}, {'mql': 'HLColor', 'py': 'HLColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Cor Center', 'sinput': False}, {'mql': 'InpBack', 'py': 'InpBack', 'param': 'InpBack', 'type': 'bool', 'default': False, 'label': 'Objeto de fundo', 'sinput': False}, {'mql': 'InpSelection', 'py': 'InpSelection', 'param': 'InpSelection', 'type': 'bool', 'default': False, 'label': 'Destaque para mover', 'sinput': False}, {'mql': 'InpHidden', 'py': 'InpHidden', 'param': 'InpHidden', 'type': 'bool', 'default': True, 'label': 'Ocultar na lista de objetos', 'sinput': False}, {'mql': 'WithDigit', 'py': 'WithDigit', 'param': 'WithDigit', 'type': 'bool', 'default': True, 'label': 'Ocultar na lista de objetos', 'sinput': False}, {'mql': 'InpZOrder', 'py': 'InpZOrder', 'param': 'InpZOrder', 'type': 'long', 'default': 0, 'label': 'Prioridade para clique do mouse', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
IHistoryBars = _input('IHistoryBars', 25)  # Check Historical Data
InpFont = _input('InpFont', 'Tahoma')  # Font Type
InpFontSize = _input('InpFontSize', 7)  # Size of fonts
UpColor = _input('UpColor', clrGold)  # Cor Up
DwColor = _input('DwColor', clrRoyalBlue)  # Cor Dw
HLColor = _input('HLColor', clrAqua)  # Cor Center
InpBack = _input('InpBack', False)  # Objeto de fundo
InpSelection = _input('InpSelection', False)  # Destaque para mover
InpHidden = _input('InpHidden', True)  # Ocultar na lista de objetos
WithDigit = _input('WithDigit', True)  # Ocultar na lista de objetos
InpZOrder = _input('InpZOrder', 0)  # Prioridade para clique do mouse
digits = 0
extradig = 0
InpAngle = 0.0  # Вngulo de inclinaзгo em graus
InpAnchor = ANCHOR_CENTER  # Tipo de ancoragem
gBars = 0.0
gTotalRates = 0.0

def OnInit():
    global digits, extradig
    digits = _int(MathPow(10, Digits() - extradig))
    if WithDigit:
        extradig = 1

def TextMove(chart_ID=0, name='Text', time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, time, price):
        Print('TextMove', ': falha ao mover o ponto de ancoragem! Cуdigo de erro = ', GetLastError())
        return False
    return True

def ChangeTextEmptyPoint(time, price):
    if not time.v:
        time.v = TimeCurrent()
    if not price.v:
        price.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)

def OnDeinit(reason):
    ClearMyObjects()
    Print('Deinit Value Chart, reason = ' + IntegerToString(reason))

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global digits, gBars, gTotalRates
    scale = _int(ChartGetInteger(0, CHART_SCALE))
    bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS)) + 3
    value = 0.0
    digits = _int(MathPow(10, Digits() - extradig))
    step = 1
    _sw1 = scale
    if _sw1 == 0:
        step = 12
    elif _sw1 == 1:
        step = 6
    elif _sw1 == 2:
        step = 4
    elif _sw1 == 3:
        step = 2
    gTotalRates = rates_total
    gBars = bars
    i = rates_total - 1
    while i > (rates_total - bars):
        if Close[i] > Open[i]:
            value = (Close[i] - Open[i]) * digits
            TextCreate(0, 'Text_' + _str(i) + _str(PERIOD_CURRENT), 0, Time[i], (Close[i] + Open[i]) / 2, DoubleToString(value, extradig), InpFont, InpFontSize, UpColor, InpAngle, InpAnchor, InpBack, InpSelection, InpHidden, InpZOrder)
            value = (Open[i] - Low[i]) * digits
            if not TextCreate(0, 'TextL_' + _str(i) + _str(PERIOD_CURRENT), 0, Time[i], Low[i], DoubleToString(value, extradig), InpFont, InpFontSize, HLColor, InpAngle, InpAnchor, InpBack, InpSelection, InpHidden, InpZOrder):
                return 0
            value = (High[i] - Close[i]) * digits
            if not TextCreate(ChartID(), 'TextH_' + _str(i) + _str(PERIOD_CURRENT), 0, Time[i], High[i], DoubleToString(value, extradig), InpFont, InpFontSize, HLColor, InpAngle, InpAnchor, InpBack, InpSelection, InpHidden, InpZOrder):
                return 0
        else:
            value = (Open[i] - Close[i]) * digits
            if not TextCreate(ChartID(), 'Text_' + _str(i) + _str(PERIOD_CURRENT), 0, Time[i], (Close[i] + Open[i]) / 2, DoubleToString(value, extradig), InpFont, InpFontSize, DwColor, -InpAngle, InpAnchor, InpBack, InpSelection, InpHidden, InpZOrder):
                return 0
            value = (Close[i] - Low[i]) * digits
            if not TextCreate(ChartID(), 'TextL_' + _str(i) + _str(PERIOD_CURRENT), 0, Time[i], Low[i], DoubleToString(value, extradig), InpFont, InpFontSize, HLColor, InpAngle, InpAnchor, InpBack, InpSelection, InpHidden, InpZOrder):
                return 0
            value = (High[i] - Open[i]) * digits
            if not TextCreate(ChartID(), 'TextH_' + _str(i) + _str(PERIOD_CURRENT), 0, Time[i], High[i], DoubleToString(value, extradig), InpFont, InpFontSize, HLColor, InpAngle, InpAnchor, InpBack, InpSelection, InpHidden, InpZOrder):
                return 0
        i -= step
    ChartRedraw()
    return 0

def Trace(name, sens, price, time, couleur):
    ObjectCreate(0, name, OBJ_ARROW, 0, time, price)
    if sens == 1:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 233)
    if sens == -1:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 234)
    ObjectSetInteger(0, name, OBJPROP_COLOR, couleur)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, 5)

def ClearMyObjects():
    global digits
    name = ""
    scale = _int(ChartGetInteger(0, CHART_SCALE))
    bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS)) + 3
    value = 0.0
    digits = _int(MathPow(10, Digits() - extradig))
    step = 1
    _sw2 = scale
    if _sw2 == 0:
        step = 12
    elif _sw2 == 1:
        step = 6
    elif _sw2 == 2:
        step = 4
    elif _sw2 == 3:
        step = 2
    i = _int(gTotalRates - 1)
    while i > (gTotalRates - bars):
        if not TextDelete(ChartID(), 'Text_' + _str(i) + _str(PERIOD_CURRENT)):
            pass
        if not TextDelete(ChartID(), 'TextH_' + _str(i) + _str(PERIOD_CURRENT)):
            pass
        if not TextDelete(ChartID(), 'TextL_' + _str(i) + _str(PERIOD_CURRENT)):
            pass
        i -= step
    ChartRedraw()

def TextChange(chart_ID=0, name='Text', text='Text'):
    ResetLastError()
    if not ObjectSetString(chart_ID, name, OBJPROP_TEXT, text):
        Print('TextChange', ': falha ao alterar texto! Cуdigo de erro = ', GetLastError())
        return False
    return True

def TextDelete(chart_ID=0, name='Text'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('TextDelete', ': falha ao excluir o objeto "Texto"! Cуdigo de erro = ', GetLastError())
        return False
    return True

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_CENTER, back=False, selection=False, hidden=True, z_order=0):
    time = Box(time)
    price = Box(price)
    if ObjectFind(chart_ID, name) == -1:
        ResetLastError()
        if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time.v, price.v):
            Print('TextCreate', ': falha ao criar objeto "Texto"! Cуdigo de erro = ', GetLastError())
            return False
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
        ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
        ObjectSetInteger(chart_ID, name, OBJPROP_ALIGN, ALIGN_CENTER)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        ObjectSetDouble(chart_ID, name, OBJPROP_PRICE, price.v)
        ObjectSetInteger(chart_ID, name, OBJPROP_TIME, time.v)
        return True
    else:
        ChangeTextEmptyPoint(time, price)
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
        ObjectSetInteger(chart_ID, name, OBJPROP_ALIGN, ALIGN_CENTER)
        ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
        ObjectSetDouble(chart_ID, name, OBJPROP_PRICE, price.v)
        ObjectSetInteger(chart_ID, name, OBJPROP_TIME, time.v)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, 100)
        return True

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        ClearMyObjects()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleSizeInfoJj(_MQL5Indicator):
    name = 'candle_size_info_jj'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IHistoryBars': 25,  # Check Historical Data
        'InpFontSize': 7,  # Size of fonts
        'InpBack': False,  # Objeto de fundo
        'InpSelection': False,  # Destaque para mover
        'InpHidden': True,  # Ocultar na lista de objetos
        'WithDigit': True,  # Ocultar na lista de objetos
        'InpZOrder': 0,  # Prioridade para clique do mouse
    }

