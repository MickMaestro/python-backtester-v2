"""Candle_size — converted from MQL5: MQL5 Indicators/Candle size/Candle_size.mq5

Exibe o tamanho dos candles no gráfico para um dia específico da semana usando enum.
Copyright: Copyright 2019-2025, Virologista Kerntopf Corp.; Link: https://www.mql5.com/en/users/gustavofk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019-2025, Virologista Kerntopf Corp.', 'link': 'https://www.mql5.com/en/users/gustavofk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Exibe o tamanho dos candles no gráfico para um dia específico da semana usando enum.'], 'name': 'Candle_size', 'source': 'MQL5 Indicators/Candle size/Candle_size.mq5', 'folder': 'Candle size', 'inputs': [{'mql': 'ProcessarTodosDias', 'py': 'ProcessarTodosDias', 'param': 'ProcessarTodosDias', 'type': 'bool', 'default': False, 'label': 'Processar todos os dias? (true = Sim, false = Não)', 'sinput': False}, {'mql': 'DiasSelecionados', 'py': 'DiasSelecionados', 'param': 'DiasSelecionados', 'type': 'int', 'default': 1, 'label': 'Escolher o dia da semana a ser medido', 'sinput': False}, {'mql': 'CorPesoAlta', 'py': 'CorPesoAlta', 'param': None, 'type': 'color', 'default': 2139610, 'label': 'Cor para candles de alta', 'sinput': False}, {'mql': 'CorPesoBaixa', 'py': 'CorPesoBaixa', 'param': None, 'type': 'color', 'default': 9470064, 'label': 'Cor para candles de baixa', 'sinput': False}, {'mql': 'Distanciar', 'py': 'Distanciar', 'param': 'Distanciar', 'type': 'bool', 'default': False, 'label': 'Ativar deslocamento?', 'sinput': False}, {'mql': 'Deslocamento', 'py': 'Deslocamento', 'param': 'Deslocamento', 'type': 'double', 'default': 50.0, 'label': 'Valor de deslocamento em pontos', 'sinput': False}, {'mql': 'Fonte', 'py': 'Fonte', 'param': None, 'type': 'string', 'default': 'Lucida Console', 'label': 'Fonte do texto', 'sinput': False}, {'mql': 'TamanhoFonte', 'py': 'TamanhoFonte', 'param': 'TamanhoFonte', 'type': 'int', 'default': 8, 'label': 'Tamanho da fonte', 'sinput': False}, {'mql': 'Ancora', 'py': 'Ancora', 'param': 'Ancora', 'type': 'int', 'default': 7, 'label': 'Tipo de ancoragem', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum DaysOfWeek
Domingo = 0
Segunda = 1
Terca = 2
Quarta = 3
Quinta = 4
Sexta = 5
Sabado = 6
_enum('DaysOfWeek', {0: 'Domingo', 1: 'Segunda', 2: 'Terca', 3: 'Quarta', 4: 'Quinta', 5: 'Sexta', 6: 'Sabado'})

# ---- inputs and global variables
ProcessarTodosDias = _input('ProcessarTodosDias', False)  # Processar todos os dias? (true = Sim, false = Não)
DiasSelecionados = _input('DiasSelecionados', Segunda)  # Escolher o dia da semana a ser medido
CorPesoAlta = _input('CorPesoAlta', clrGoldenrod)  # Cor para candles de alta
CorPesoBaixa = _input('CorPesoBaixa', clrSlateGray)  # Cor para candles de baixa
Distanciar = _input('Distanciar', False)  # Ativar deslocamento?
Deslocamento = _input('Deslocamento', 50.0)  # Valor de deslocamento em pontos
Fonte = _input('Fonte', 'Lucida Console')  # Fonte do texto
TamanhoFonte = _input('TamanhoFonte', 8)  # Tamanho da fonte
Ancora = _input('Ancora', ANCHOR_UPPER)  # Tipo de ancoragem
ObjectPrefix = 'MedidorCandle_'  # Prefixo para objetos

def OnInit():
    global ObjectPrefix
    if DiasSelecionados < Domingo or DiasSelecionados > Sabado:
        Print('Erro: Valor inválido para DiasSelecionados. Use um valor entre 0 (Domingo) e 6 (Sábado).')
        return INIT_PARAMETERS_INCORRECT
    ObjectPrefix += EnumToString(Period(), '') + '_'
    return INIT_SUCCEEDED

def OnDeinit(reason):
    DeleteObjects()

def GetDayOfWeek(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.day_of_week

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    start = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(start, rates_total):
        dayOfWeek = GetDayOfWeek(time[i])
        if (not ProcessarTodosDias) and dayOfWeek != DiasSelecionados:
            continue
        objectName = ObjectPrefix + TimeToString(time[i])
        labelText = CalculateSize(high[i], low[i])
        anchorPrice = 0.0
        textColor = 0
        anchorType = 0
        if open[i] > close[i]:
            anchorPrice = low[i] - ((Deslocamento * Point()) if Distanciar else 0)
            textColor = CorPesoBaixa
            anchorType = ANCHOR_UPPER
        elif open[i] < close[i]:
            anchorPrice = high[i] + ((Deslocamento * Point()) if Distanciar else 0)
            textColor = CorPesoAlta
            anchorType = ANCHOR_LOWER
        else:
            anchorPrice = (high[i] + low[i]) / 2.0
            textColor = clrWhiteSmoke
            anchorType = ANCHOR_CENTER
        anchorPrice = AdjustPriceToChartLimits(anchorPrice)
        if not CreateTextObject(0, objectName, 0, time[i], anchorPrice, labelText, 0.0, Fonte, TamanhoFonte, textColor, anchorType):
            Print('Falha ao criar o objeto de texto para o candle em ', TimeToString(time[i]))
            return 0
    return rates_total

def CalculateSize(high, low):
    size = MathAbs(high - low)
    pointAdjustment = ((Point() * 1000) if (Digits() == 3 or Digits() == 5) else Point())
    return DoubleToString(_fdiv(size, pointAdjustment), 1)

def CreateTextObject(chartID, name, subWindow, time, price, text, angle, font, size, clr, anchor):
    ResetLastError()
    if ObjectFind(chartID, name) != -1:
        ObjectDelete(chartID, name)
    if not ObjectCreate(chartID, name, OBJ_TEXT, subWindow, time, price):
        Print('CreateTextObject', ": Falha ao criar o objeto de texto '", name, "' no tempo ", TimeToString(time), '. Erro: ', GetLastError())
        return False
    ObjectSetString(chartID, name, OBJPROP_TEXT, text)
    ObjectSetString(chartID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, size)
    ObjectSetDouble(chartID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chartID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_BACK, False)
    ObjectSetInteger(chartID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chartID, name, OBJPROP_HIDDEN, True)
    return True

def DeleteObjects():
    ObjectsDeleteAll(0, ObjectPrefix)

def AdjustPriceToChartLimits(price):
    chartMin = ChartGetDouble(0, CHART_PRICE_MIN, 0)
    chartMax = ChartGetDouble(0, CHART_PRICE_MAX, 0)
    if price < chartMin:
        return chartMin
    if price > chartMax:
        return chartMax
    return price


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleSize(_MQL5Indicator):
    name = 'Candle_size'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ProcessarTodosDias': False,  # Processar todos os dias? (true = Sim, false = Não)
        'DiasSelecionados': _Choice({0: 'Domingo', 1: 'Segunda-feira', 2: 'Terça-feira', 3: 'Quarta-feira', 4: 'Quinta-feira', 5: 'Sexta-feira', 6: 'Sábado'}, default=1),  # Escolher o dia da semana a ser medido
        'Distanciar': False,  # Ativar deslocamento?
        'Deslocamento': 50.0,  # Valor de deslocamento em pontos
        'TamanhoFonte': 8,  # Tamanho da fonte
        'Ancora': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=7),  # Tipo de ancoragem
    }

