"""LRMA_Color — converted from MQL5: MQL5 Indicators/Color Linear Regression/LRMA_Color.mq5

Линейная регрессия является статистическим инструментом, используемым для
прогнозирования будущих цен исходя из прошлых данных. Используется метод 
наименьших квадратов для построения «наиболее подходящей» прямой линии 
через ряд точек ценовых значений. В качестве входных параметров используется 
количество расчетных баров (свечей). Данный индикатор хорошо использовать для ручной торговли
Copyright: Copyright 2014, Vinin; Link: vinin@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Vinin', 'link': 'vinin@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [65535, 65280, 255, 0, 0, 0, 0, 0]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LRMA'}, 'levels': [], 'description': ['Линейная регрессия является статистическим инструментом, используемым для', 'прогнозирования будущих цен исходя из прошлых данных. Используется метод ', 'наименьших квадратов для построения «наиболее подходящей» прямой линии ', 'через ряд точек ценовых значений. В качестве входных параметров используется ', 'количество расчетных баров (свечей). Данный индикатор хорошо использовать для ручной торговли'], 'name': 'LRMA_Color', 'source': 'MQL5 Indicators/Color Linear Regression/LRMA_Color.mq5', 'folder': 'Color Linear Regression', 'inputs': [{'mql': 'LRMAPeriod', 'py': 'LRMAPeriod', 'param': 'LRMAPeriod', 'type': 'int', 'default': 14, 'label': 'Period LRMA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LRMAPeriod = _input('LRMAPeriod', 14)  # Period LRMA
LRMABuffer = Arr(0, 0.0)
LRMAColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LRMABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LRMAColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(LRMABuffer, True)
    ArraySetAsSeries(LRMAColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= LRMAPeriod:
        return 0
    ArraySetAsSeries(close, True)
    limit1 = rates_total - prev_calculated
    limit2 = limit1
    if limit1 > 1:
        limit1 = rates_total - LRMAPeriod - 1
        limit2 = limit1 - 1
    for pos in range(limit1, 0 - 1, -1):
        LRMABuffer[pos] = LRMA(pos, LRMAPeriod, close)
        LRMAColors[pos] = 0.0
    for pos in range(limit2, 0 - 1, -1):
        if LRMABuffer[pos] > LRMABuffer[pos + 1]:
            LRMAColors[pos] = 1.0
            LRMAColors[pos + 1] = 1.0
        elif LRMABuffer[pos] < LRMABuffer[pos + 1]:
            LRMAColors[pos] = 2.0
            LRMAColors[pos + 1] = 2.0
    return rates_total

def LRMA(pos, period, price):
    Res = 0.0
    tmpS = 0.0
    tmpW = 0.0
    wsum = 0.0
    for i in range(0, period):
        tmpS += price[pos + i]
        tmpW += price[pos + i] * (period - i)
        wsum += period - i
    tmpS = _fdiv(tmpS, period)
    tmpW = _fdiv(tmpW, wsum)
    Res = (3.0 * tmpW) - (2.0 * tmpS)
    return Res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LRMAColor(_MQL5Indicator):
    name = 'LRMA_Color'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LRMAPeriod': 14,  # Period LRMA
    }

