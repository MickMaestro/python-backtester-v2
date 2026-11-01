"""Candle_counter — converted from MQL5: MQL5 Indicators/Candle Counter/Candle_counter.mq5

Exibe a numeração sequencial dos candles da semana selecionada ou todos os candles
Copyright: Copyright 2019-2025, Virologista Kerntopf Corp.; Link: https://www.mql5.com/pt/users/virologustavo/news; Version: 2.40

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019-2025, Virologista Kerntopf Corp.', 'link': 'https://www.mql5.com/pt/users/virologustavo/news', 'version': '2.40', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Exibe a numeração sequencial dos candles da semana selecionada ou todos os candles'], 'name': 'Candle_counter', 'source': 'MQL5 Indicators/Candle Counter/Candle_counter.mq5', 'folder': 'Candle Counter', 'inputs': [{'mql': 'PriceOffsetFactor', 'py': 'PriceOffsetFactor', 'param': 'PriceOffsetFactor', 'type': 'double', 'default': 0.5, 'label': 'Fator dinâmico de espaçamento', 'sinput': False}, {'mql': 'InpTextColorAbove', 'py': 'InpTextColorAbove', 'param': None, 'type': 'color', 'default': 8388352, 'label': 'Cor do texto acima do candle', 'sinput': False}, {'mql': 'InpTextColorBelow', 'py': 'InpTextColorBelow', 'param': None, 'type': 'color', 'default': 13850042, 'label': 'Cor do texto abaixo do candle', 'sinput': False}, {'mql': 'InpFont', 'py': 'InpFont', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Tipo de fonte', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 8, 'label': 'Tamanho da fonte', 'sinput': False}, {'mql': 'Anchor', 'py': 'Anchor', 'param': 'Anchor', 'type': 'int', 'default': 8, 'label': 'Tipo de âncora', 'sinput': False}, {'mql': 'NumberFirstCandle', 'py': 'NumberFirstCandle', 'param': 'NumberFirstCandle', 'type': 'bool', 'default': True, 'label': 'O primeiro candle a ser contado é o último?', 'sinput': False}, {'mql': 'SelectedWeek', 'py': 'SelectedWeek', 'param': 'SelectedWeek', 'type': 'int', 'default': 1, 'label': 'Semana selecionada para contagem (0 = Todas as semanas)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PriceOffsetFactor = _input('PriceOffsetFactor', 0.5)  # Fator dinâmico de espaçamento
InpTextColorAbove = _input('InpTextColorAbove', clrSpringGreen)  # Cor do texto acima do candle
InpTextColorBelow = _input('InpTextColorBelow', clrMediumOrchid)  # Cor do texto abaixo do candle
InpFont = _input('InpFont', 'Arial')  # Tipo de fonte
InpFontSize = _input('InpFontSize', 8)  # Tamanho da fonte
Anchor = _input('Anchor', ANCHOR_CENTER)  # Tipo de âncora
NumberFirstCandle = _input('NumberFirstCandle', True)  # O primeiro candle a ser contado é o último?
SelectedWeek = _input('SelectedWeek', 1)  # Semana selecionada para contagem (0 = Todas as semanas)
ExtCounterBuffer = Arr(0, 0.0)
ObjectPrefix = 'Candle_Counter_'  # Prefixo único para evitar conflitos

def OnInit():
    SetIndexBuffer(0, ExtCounterBuffer, INDICATOR_DATA)
    ArrayInitialize(ExtCounterBuffer, EMPTY_VALUE)
    short_name = StringFormat('Bar Counter (%s)', ('First' if NumberFirstCandle else 'Last'))
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    DeleteObjects()

def GetDay(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.day

def GetWeekOfMonth(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    day_of_month = dt.day
    day_of_week = dt.day_of_week
    week_of_month = _idiv(day_of_month + (6 - day_of_week), 7) + 1
    return week_of_month

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    DeleteObjects()
    to_copy = ((rates_total - prev_calculated + 1) if (prev_calculated > 0 and prev_calculated <= rates_total) else rates_total)
    for i in range(rates_total - to_copy, rates_total):
        currentWeek = GetWeekOfMonth(time[i])
        if SelectedWeek != 0 and currentWeek != SelectedWeek:
            continue
        candleDay = GetDay(time[i])
        previousDay = (GetDay(time[i - 1]) if (i > 0) else -1)
        if candleDay != previousDay:
            ExtCounterBuffer[i] = (1 if NumberFirstCandle else EMPTY_VALUE)
        else:
            ExtCounterBuffer[i] = ((ExtCounterBuffer[i - 1] + 1) if NumberFirstCandle else EMPTY_VALUE)
        if ExtCounterBuffer[i] != EMPTY_VALUE:
            objectName = ObjectPrefix + TimeToString(time[i])
            text = IntegerToString(_int(ExtCounterBuffer[i]))
            priceOffset = PriceOffsetFactor * Point() * (SymbolInfoInteger(Symbol(), SYMBOL_DIGITS) * 150)
            price = ((low[i] - priceOffset) if (open[i] > close[i]) else (high[i] + priceOffset))
            textColor = (InpTextColorBelow if (open[i] > close[i]) else InpTextColorAbove)
            CreateText(0, objectName, 0, time[i], price, text, 0.0, InpFont, InpFontSize, textColor, Anchor)
    if not NumberFirstCandle:
        for i in range(rates_total - 1, 0 - 1, -1):
            currentWeek = GetWeekOfMonth(time[i])
            if SelectedWeek != 0 and currentWeek != SelectedWeek:
                continue
            candleDay = GetDay(time[i])
            nextDay = (GetDay(time[i + 1]) if (i < (rates_total - 1)) else -1)
            if candleDay != nextDay:
                ExtCounterBuffer[i] = 1.0
                count = 1
                j = i - 1
                while j >= 0 and GetDay(time[j]) == candleDay:
                    ExtCounterBuffer[j] = (count := count + 1)
                    j -= 1
        for i in range(0, rates_total):
            currentWeek = GetWeekOfMonth(time[i])
            if SelectedWeek != 0 and currentWeek != SelectedWeek:
                continue
            if ExtCounterBuffer[i] != EMPTY_VALUE:
                objectName = ObjectPrefix + TimeToString(time[i])
                text = IntegerToString(_int(ExtCounterBuffer[i]))
                priceOffset = PriceOffsetFactor * Point() * (SymbolInfoInteger(Symbol(), SYMBOL_DIGITS) * 150)
                price = ((low[i] - priceOffset) if (open[i] > close[i]) else (high[i] + priceOffset))
                textColor = (InpTextColorBelow if (open[i] > close[i]) else InpTextColorAbove)
                CreateText(0, objectName, 0, time[i], price, text, 0.0, InpFont, InpFontSize, textColor, Anchor)
    return rates_total

def CreateText(chartID, name, subWindow, time, price, text, angle, font, size, clr, anchor):
    ResetLastError()
    if not ObjectCreate(chartID, name, OBJ_TEXT, subWindow, time, price):
        Print('CreateText', ": Falha ao criar objeto '", name, "'. Erro: ", GetLastError())
        return False
    if (((((not ObjectSetString(chartID, name, OBJPROP_TEXT, text)) or (not ObjectSetString(chartID, name, OBJPROP_FONT, font))) or (not ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, size))) or (not ObjectSetDouble(chartID, name, OBJPROP_ANGLE, angle))) or (not ObjectSetInteger(chartID, name, OBJPROP_ANCHOR, anchor))) or (not ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)):
        Print('CreateText', ": Falha ao configurar propriedades do objeto '", name, "'. Erro: ", GetLastError())
        ObjectDelete(chartID, name)
        return False
    ObjectSetInteger(chartID, name, OBJPROP_BACK, False)
    ObjectSetInteger(chartID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chartID, name, OBJPROP_HIDDEN, True)
    return True

def DeleteObjects():
    ResetLastError()
    totalObjects = ObjectsTotal(0, 0, OBJ_TEXT)
    for i in range(totalObjects - 1, 0 - 1, -1):
        objectName = ObjectName(0, i, 0, OBJ_TEXT)
        if StringFind(objectName, ObjectPrefix) == 0:
            if not ObjectDelete(0, objectName):
                PrintFormat("Erro ao excluir objeto '%s'. Código: %i", objectName, GetLastError())


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleCounter(_MQL5Indicator):
    name = 'Candle_counter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'PriceOffsetFactor': 0.5,  # Fator dinâmico de espaçamento
        'InpFontSize': 8,  # Tamanho da fonte
        'Anchor': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=8),  # Tipo de âncora
        'NumberFirstCandle': True,  # O primeiro candle a ser contado é o último?
        'SelectedWeek': 1,  # Semana selecionada para contagem (0 = Todas as semanas)
    }

