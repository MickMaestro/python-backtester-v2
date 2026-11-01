"""Tendência Diária — converted from MQL5: MQL5 Indicators/Daily Trend/Tendência Diária.mq5

Este indicador exibe a tendência do dia em qualquer tempo gráfico
Copyright: Emanuel Kowalczuk; Link: e.kwk@hotmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Emanuel Kowalczuk', 'link': 'e.kwk@hotmail.com', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Este indicador exibe a tendência do dia em qualquer tempo gráfico'], 'name': 'Tendência Diária', 'source': 'MQL5 Indicators/Daily Trend/Tendência Diária.mq5', 'folder': 'Daily Trend', 'inputs': [{'mql': 'TamanhoFonte', 'py': 'TamanhoFonte', 'param': 'TamanhoFonte', 'type': 'int', 'default': 12, 'label': 'Tamanho da fonte do texto', 'sinput': False}, {'mql': 'PosicaoTexto', 'py': 'PosicaoTexto', 'param': 'PosicaoTexto', 'type': 'int', 'default': 2, 'label': 'Posição do texto', 'sinput': False}, {'mql': 'MargemHorizontal', 'py': 'MargemHorizontal', 'param': 'MargemHorizontal', 'type': 'int', 'default': 100, 'label': 'Margem horizontal (espaçamento da borda)', 'sinput': False}, {'mql': 'MargemVertical', 'py': 'MargemVertical', 'param': 'MargemVertical', 'type': 'int', 'default': 20, 'label': 'Margem vertical (espaçamento da borda)', 'sinput': False}, {'mql': 'CorAlta', 'py': 'CorAlta', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Cor tendência de alta', 'sinput': False}, {'mql': 'CorBaixa', 'py': 'CorBaixa', 'param': None, 'type': 'color', 'default': 255, 'label': 'Cor tendência de baixa', 'sinput': False}, {'mql': 'CorNeutra', 'py': 'CorNeutra', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Cor tendência neutra', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_POSICAO_TEXTO
SUPERIOR_ESQUERDO = 1
SUPERIOR_DIREITO = 2
INFERIOR_ESQUERDO = 3
INFERIOR_DIREITO = 4
_enum('ENUM_POSICAO_TEXTO', {1: 'SUPERIOR_ESQUERDO', 2: 'SUPERIOR_DIREITO', 3: 'INFERIOR_ESQUERDO', 4: 'INFERIOR_DIREITO'})

# ---- inputs and global variables
TamanhoFonte = _input('TamanhoFonte', 12)  # Tamanho da fonte do texto
PosicaoTexto = _input('PosicaoTexto', SUPERIOR_DIREITO)  # Posição do texto
MargemHorizontal = _input('MargemHorizontal', 100)  # Margem horizontal (espaçamento da borda)
MargemVertical = _input('MargemVertical', 20)  # Margem vertical (espaçamento da borda)
CorAlta = _input('CorAlta', clrGreen)  # Cor tendência de alta
CorBaixa = _input('CorBaixa', clrRed)  # Cor tendência de baixa
CorNeutra = _input('CorNeutra', clrGray)  # Cor tendência neutra

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'TendenciaLabel')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    precoAbertura = iOpen(None, PERIOD_D1, 0)
    precoAtual = iClose(None, PERIOD_D1, 0)
    variacaoPercentual = _fdiv(precoAtual - precoAbertura, precoAbertura) * 100
    textoVariacao = DoubleToString(variacaoPercentual, 2) + '%'
    ObjectDelete(0, 'TendenciaLabel')
    xDistance = MargemHorizontal
    yDistance = MargemVertical
    _sw1 = PosicaoTexto
    if _sw1 == SUPERIOR_ESQUERDO:
        xDistance = MargemHorizontal
        yDistance = MargemVertical
    elif _sw1 == SUPERIOR_DIREITO:
        xDistance = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)) - MargemHorizontal - 150
        yDistance = MargemVertical
    elif _sw1 == INFERIOR_ESQUERDO:
        xDistance = MargemHorizontal
        yDistance = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)) - MargemVertical - 40
    elif _sw1 == INFERIOR_DIREITO:
        xDistance = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)) - MargemHorizontal - 150
        yDistance = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)) - MargemVertical - 40
    else:
        pass
    if variacaoPercentual >= 0.1:
        ObjectCreate(0, 'TendenciaLabel', OBJ_LABEL, 0, 0, 0)
        ObjectSetString(0, 'TendenciaLabel', OBJPROP_TEXT, 'Tendência Diária: Alta (' + textoVariacao + ')')
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_COLOR, CorAlta)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_XDISTANCE, xDistance)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_YDISTANCE, yDistance)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_FONTSIZE, TamanhoFonte)
    elif variacaoPercentual <= -0.1:
        ObjectCreate(0, 'TendenciaLabel', OBJ_LABEL, 0, 0, 0)
        ObjectSetString(0, 'TendenciaLabel', OBJPROP_TEXT, 'Tendência Diária: Baixa (' + textoVariacao + ')')
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_COLOR, CorBaixa)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_XDISTANCE, xDistance)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_YDISTANCE, yDistance)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_FONTSIZE, TamanhoFonte)
    else:
        ObjectCreate(0, 'TendenciaLabel', OBJ_LABEL, 0, 0, 0)
        ObjectSetString(0, 'TendenciaLabel', OBJPROP_TEXT, 'Tendência Diária: Neutra (' + textoVariacao + ')')
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_COLOR, CorNeutra)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_XDISTANCE, xDistance)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_YDISTANCE, yDistance)
        ObjectSetInteger(0, 'TendenciaLabel', OBJPROP_FONTSIZE, TamanhoFonte)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TendênciaDiária(_MQL5Indicator):
    name = 'Tendência Diária'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TamanhoFonte': 12,  # Tamanho da fonte do texto
        'PosicaoTexto': _Choice({1: 'Canto Superior Esquerdo', 2: 'Canto Superior Direito', 3: 'Canto Inferior Esquerdo', 4: 'Canto Inferior Direito'}, default=2),  # Posição do texto
        'MargemHorizontal': 100,  # Margem horizontal (espaçamento da borda)
        'MargemVertical': 20,  # Margem vertical (espaçamento da borda)
    }

