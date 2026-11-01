"""Watermark — converted from MQL5: MQL5 Indicators/Watermark/Watermark.mq5

Copyright: Copyright 2019-2025, Virologista Kerntopf Corp.; Link: https://www.mql5.com/pt/users/virologustavo/news; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019-2025, Virologista Kerntopf Corp.', 'link': 'https://www.mql5.com/pt/users/virologustavo/news', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Watermark', 'source': 'MQL5 Indicators/Watermark/Watermark.mq5', 'folder': 'Watermark', 'inputs': [{'mql': 'InpTextColor', 'py': 'InpTextColor', 'param': None, 'type': 'color', 'default': 0, 'label': "Cor da marca d'água", 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 70, 'label': 'Tamanho base da fonte', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTextColor = _input('InpTextColor', 0x000000)  # Cor da marca d'água
InpFontSize = _input('InpFontSize', 70)  # Tamanho base da fonte
wmSymbolLabel = 'Ticker Symbol Name'  # Rótulo principal (símbolo + período)
wmDescLabel = 'Ticker Symbol Description'  # Descrição do ativo
wmScreenWidth = 0  # Largura atual do gráfico
wmScreenHeight = 0  # Altura atual do gráfico
wmFontSize = 0  # Tamanho da fonte ajustado

def wmCreateLabel(wmName, wmLabel):
    if ObjectFind(0, wmName) != -1:
        ObjectDelete(0, wmName)
    ObjectCreate(0, wmName, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, wmName, OBJPROP_COLOR, InpTextColor)
    ObjectSetInteger(0, wmName, OBJPROP_ANCHOR, ANCHOR_CENTER)
    ObjectSetInteger(0, wmName, OBJPROP_FONTSIZE, InpFontSize)
    ObjectSetInteger(0, wmName, OBJPROP_BACK, True)
    ObjectSetString(0, wmName, OBJPROP_TEXT, wmLabel)

def wmResizeLabel(wmName, wmRatio):
    wmFinalSize = MathMax(10, _int(wmFontSize * wmRatio))
    if ObjectFind(0, wmName) != -1:
        if not ObjectSetInteger(0, wmName, OBJPROP_FONTSIZE, wmFinalSize):
            Print('Erro ao redimensionar fonte do objeto: ', wmName)

def wmPositionLabel(wmName, wmOffset):
    if ObjectFind(0, wmName) == -1:
        return
    x = _int(_idiv(wmScreenWidth, 2))
    y = _int(_idiv(wmScreenHeight, 2) + wmOffset)
    ObjectSetInteger(0, wmName, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, wmName, OBJPROP_YDISTANCE, y)

def wmGetTimeframe(wmPeriod):
    wmResult = EnumToString(wmPeriod, 'ENUM_TIMEFRAMES')
    if StringFind(wmResult, 'PERIOD_', 0) == 0:
        return StringSubstr(wmResult, 7)
    else:
        return 'Unknown'

def OnInit():
    wmCreateLabel(wmSymbolLabel, StringFormat('📈%s :⏱%s', Symbol(), wmGetTimeframe(Period())))
    wmCreateLabel(wmDescLabel, SymbolInfoString(Symbol(), SYMBOL_DESCRIPTION))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global wmFontSize, wmScreenHeight, wmScreenWidth
    wmChartWidth = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0)
    wmChartHeight = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, 0)
    if wmScreenWidth != wmChartWidth or wmScreenHeight != wmChartHeight:
        wmScreenWidth = wmChartWidth
        wmScreenHeight = wmChartHeight
        wmFontSize = _idiv(InpFontSize * wmScreenWidth, 1000)
        wmResizeLabel(wmSymbolLabel, 0.75)
        wmResizeLabel(wmDescLabel, 0.5)
        wmPositionLabel(wmSymbolLabel, 0)
        wmPositionLabel(wmDescLabel, wmFontSize + 5)
        ChartRedraw()
    return rates_total

def OnDeinit(reason):
    for i in range(0, ArraySize(wmLabels)):
        if ObjectFind(0, wmLabels[i]) != -1:
            ObjectDelete(0, wmLabels[i])

# ---- global variables initialised from expressions
wmLabels = Arr.of([wmSymbolLabel, wmDescLabel], fill="")  # Usado para exclusão em lote


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Watermark(_MQL5Indicator):
    name = 'Watermark'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFontSize': 70,  # Tamanho base da fonte
    }

