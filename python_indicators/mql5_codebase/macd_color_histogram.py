"""MACD_Color_Histogram — converted from MQL5: MQL5 Indicators/MACD coloured histogram/MACD_Color_Histogram.mq5

Histograma dinâmico popularizado por Thomas Aspray em 1986
MACD-Histograma mede a distância entre o MACD e sua linha sinal
A coloração das barras alterá-se conforme a inflexão das linhas MACD e sinal
O alerta aciona conforme alternam-se as linhas MACD e sinal
Copyright: Copyright 2019-2025, Virologista Kerntopf Corp.; Link: https://www.mql5.com/en/users/gustavofk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2019-2025, Virologista Kerntopf Corp.', 'link': 'https://www.mql5.com/en/users/gustavofk', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 10}, 'colors': {}, 'widths': {1: 1, 2: 1, 3: 10}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Linha MACD', 2: 'Linha Sinal', 3: 'Histograma MACD'}, 'levels': [], 'description': ['Histograma dinâmico popularizado por Thomas Aspray em 1986', 'MACD-Histograma mede a distância entre o MACD e sua linha sinal', 'A coloração das barras alterá-se conforme a inflexão das linhas MACD e sinal', 'O alerta aciona conforme alternam-se as linhas MACD e sinal'], 'name': 'MACD_Color_Histogram', 'source': 'MQL5 Indicators/MACD coloured histogram/MACD_Color_Histogram.mq5', 'folder': 'MACD coloured histogram', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Período da Média Móvel Curta', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Período da Média Móvel Longa', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Período da Média Móvel do Sinal', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Preço aplicado ao cálculo', 'sinput': False}, {'mql': 'InpSound', 'py': 'InpSound', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Nome do arquivo de som para alertas', 'sinput': False}, {'mql': 'InpRepetitions', 'py': 'InpRepetitions', 'param': 'InpRepetitions', 'type': 'uchar', 'default': 1, 'label': 'Número máximo de repetições do alerta', 'sinput': False}, {'mql': 'InpPause', 'py': 'InpPause', 'param': 'InpPause', 'type': 'uchar', 'default': 0, 'label': 'Pausa entre alertas (em segundos)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Período da Média Móvel Curta
InpSlowEMA = _input('InpSlowEMA', 26)  # Período da Média Móvel Longa
InpSignalSMA = _input('InpSignalSMA', 9)  # Período da Média Móvel do Sinal
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Preço aplicado ao cálculo
InpSound = _input('InpSound', 'alert.wav')  # Nome do arquivo de som para alertas
InpRepetitions = _input('InpRepetitions', 1)  # Número máximo de repetições do alerta
InpPause = _input('InpPause', 0)  # Pausa entre alertas (em segundos)
ExtMACDBuffer = Arr(0, 0.0)
ExtMACDColors = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtSignalColors = Arr(0, 0.0)
ExtHistogramBuffer = Arr(0, 0.0)
ExtHistogramColors = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0
ExtSoundHandle = 0  # Data/hora do último alerta sonoro
ExtRepetitionsHandle = 0  # Contador de repetições do alerta
ExtBarsHandle = 0  # Data/hora da última barra processada

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    if (InpFastEMA <= 0 or InpSlowEMA <= 0) or InpSignalSMA <= 0:
        Print('Erro: Os períodos das médias móveis devem ser maiores que zero.')
        return INIT_FAILED
    if InpFastEMA >= InpSlowEMA:
        Print('Erro: O período da média rápida deve ser menor que o da média lenta.')
        return INIT_FAILED
    SetIndexBuffer(0, ExtMACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMACDColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtSignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtSignalColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ExtHistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHistogramColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    ConfigurePlotColors()
    short_name = StringFormat('MACD Histograma (%d,%d,%d)', InpFastEMA, InpSlowEMA, InpSignalSMA)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    ExtFastMaHandle = iMA(Symbol(), Period(), InpFastEMA, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(Symbol(), Period(), InpSlowEMA, 0, MODE_EMA, InpAppliedPrice)
    if ExtFastMaHandle == INVALID_HANDLE or ExtSlowMaHandle == INVALID_HANDLE:
        Print('Erro ao criar as médias móveis. Código de erro: ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def ConfigurePlotColors():
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 4)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, clrForestGreen)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clrDarkRed)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, clrIndigo)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 3, clrDarkCyan)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, 4)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, clrLime)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, clrCrimson)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 2, clrDarkViolet)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 3, clrCyan)
    PlotIndexSetInteger(2, PLOT_COLOR_INDEXES, 9)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 0, clrDarkCyan)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 1, clrCyan)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 2, clrForestGreen)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 3, clrLime)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 4, clrIndigo)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 5, clrDarkViolet)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 6, clrDarkRed)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 7, clrCrimson)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 8, clrWhite)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < InpSignalSMA:
        return 0
    if not CalculateMAs(rates_total, prev_calculated):
        return 0
    CalculateMACDAndSignal(rates_total, prev_calculated)
    CheckAlerts(rates_total, time)
    return rates_total

def CalculateMAs(rates_total, prev_calculated):
    to_copy = ((rates_total - prev_calculated + 1) if (prev_calculated > 0) else rates_total)
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0 or CopyBuffer(ExtSlowMaHandle, 0, 0, to_copy, ExtSlowMaBuffer) <= 0:
        Print('Erro ao copiar buffers das médias móveis. Código de erro: ', GetLastError())
        return False
    return True

def CalculateMACDAndSignal(rates_total, prev_calculated):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        ExtMACDBuffer[i] = ExtFastMaBuffer[i] - ExtSlowMaBuffer[i]
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, InpSignalSMA, ExtMACDBuffer, ExtSignalBuffer)
        ExtHistogramBuffer[i] = ExtMACDBuffer[i] - ExtSignalBuffer[i]
        SetColors(i)

def SetColors(index):
    ExtMACDColors[index] = (3 if (ExtMACDBuffer[index] > 0 and ExtMACDBuffer[index] > ExtSignalBuffer[index]) else 2 if (ExtMACDBuffer[index] > 0 and ExtMACDBuffer[index] < ExtSignalBuffer[index]) else 1 if (ExtMACDBuffer[index] < ExtSignalBuffer[index]) else 0)
    ExtSignalColors[index] = (3 if (ExtSignalBuffer[index] > 0 and ExtMACDBuffer[index] > ExtSignalBuffer[index]) else 2 if (ExtSignalBuffer[index] > 0 and ExtMACDBuffer[index] < ExtSignalBuffer[index]) else 1 if (ExtMACDBuffer[index] < ExtSignalBuffer[index]) else 0)
    if ((ExtHistogramBuffer[index] > 0 and ExtMACDBuffer[index] > 0) and ExtMACDBuffer[index] > ExtHistogramBuffer[index]) and ExtSignalBuffer[index] < ExtHistogramBuffer[index]:
        ExtHistogramColors[index] = 0.0
    elif ((ExtHistogramBuffer[index] > 0 and ExtMACDBuffer[index] > 0) and ExtMACDBuffer[index] > ExtHistogramBuffer[index]) and ExtSignalBuffer[index] > ExtHistogramBuffer[index]:
        ExtHistogramColors[index] = 1.0
    elif ((ExtHistogramBuffer[index] > 0 and ExtMACDBuffer[index] > 0) and ExtMACDBuffer[index] < ExtHistogramBuffer[index]) and ExtSignalBuffer[index] < ExtHistogramBuffer[index]:
        ExtHistogramColors[index] = 2.0
    elif ExtHistogramBuffer[index] > 0 and ExtMACDBuffer[index] < 0:
        ExtHistogramColors[index] = 3.0
    elif ((ExtHistogramBuffer[index] < 0 and ExtMACDBuffer[index] < 0) and ExtMACDBuffer[index] > ExtHistogramBuffer[index]) and ExtSignalBuffer[index] > ExtHistogramBuffer[index]:
        ExtHistogramColors[index] = 4.0
    elif ExtHistogramBuffer[index] < 0 and ExtMACDBuffer[index] > 0:
        ExtHistogramColors[index] = 5.0
    elif ((ExtHistogramBuffer[index] < 0 and ExtMACDBuffer[index] < 0) and ExtMACDBuffer[index] < ExtHistogramBuffer[index]) and ExtSignalBuffer[index] > ExtHistogramBuffer[index]:
        ExtHistogramColors[index] = 6.0
    elif ((ExtHistogramBuffer[index] < 0 and ExtMACDBuffer[index] < 0) and ExtMACDBuffer[index] < ExtHistogramBuffer[index]) and ExtSignalBuffer[index] < ExtHistogramBuffer[index]:
        ExtHistogramColors[index] = 7.0
    else:
        ExtHistogramColors[index] = 8.0

def CheckAlerts(rates_total, time):
    global ExtBarsHandle, ExtRepetitionsHandle, ExtSoundHandle
    time_0 = time[rates_total - 1]
    if time_0 != ExtBarsHandle:
        ExtSoundHandle = 0
        ExtRepetitionsHandle = 0
        ExtBarsHandle = time_0
    i = rates_total - 1
    if (((ExtMACDBuffer[i - 1] < ExtSignalBuffer[i - 1] and ExtMACDBuffer[i] > ExtSignalBuffer[i]) or (ExtMACDBuffer[i - 1] > ExtSignalBuffer[i - 1] and ExtMACDBuffer[i] < ExtSignalBuffer[i])) or (ExtMACDBuffer[i - 1] < 0.0 and ExtMACDBuffer[i] > 0.0)) or (ExtMACDBuffer[i - 1] > 0.0 and ExtMACDBuffer[i] < 0.0):
        if ExtRepetitionsHandle >= InpRepetitions:
            return
        time_current = TimeCurrent()
        if (time_current - ExtSoundHandle) > InpPause:
            if ExtMACDBuffer[i - 1] < ExtSignalBuffer[i - 1] and ExtMACDBuffer[i] > ExtSignalBuffer[i]:
                PlaySound(InpSound)
                Alert('COMPRA - MACD cruzou a linha de sinal em ', TimeToString(time[i]))
                ExtSoundHandle = time_current
                ExtRepetitionsHandle += 1
            elif ExtMACDBuffer[i - 1] > ExtSignalBuffer[i - 1] and ExtMACDBuffer[i] < ExtSignalBuffer[i]:
                PlaySound(InpSound)
                Alert('VENDA - MACD cruzou a linha de sinal em ', TimeToString(time[i]))
                ExtSoundHandle = time_current
                ExtRepetitionsHandle += 1
            elif ExtMACDBuffer[i - 1] < 0.0 and ExtMACDBuffer[i] > 0.0:
                PlaySound(InpSound)
                Alert('COMPRA - MACD cruzou a região zero em ', TimeToString(time[i]))
                ExtSoundHandle = time_current
                ExtRepetitionsHandle += 1
            elif ExtMACDBuffer[i - 1] > 0.0 and ExtMACDBuffer[i] < 0.0:
                PlaySound(InpSound)
                Alert('VENDA - MACD cruzou a região zero em ', TimeToString(time[i]))
                ExtSoundHandle = time_current
                ExtRepetitionsHandle += 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDColorHistogram(_MQL5Indicator):
    name = 'MACD_Color_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Período da Média Móvel Curta
        'InpSlowEMA': 26,  # Período da Média Móvel Longa
        'InpSignalSMA': 9,  # Período da Média Móvel do Sinal
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Preço aplicado ao cálculo
        'InpRepetitions': 1,  # Número máximo de repetições do alerta
        'InpPause': 0,  # Pausa entre alertas (em segundos)
    }

