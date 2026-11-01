"""LRMA — converted from MQL5: MQL5 Indicators/Linear Regression/LRMA.mq5

Линейная регрессия является статистическим инструментом, используемым для
прогнозирования будущих цен исходя из прошлых данных. Используется метод 
наименьших квадратов для построения «наиболее подходящей» прямой линии 
через ряд точек ценовых значений. В качестве входных параметров используется 
количество расчетных баров (свечей). Данный индикатор хорошо использовать для автоматической торговли
Copyright: Copyright 2014, Vinin; Link: http:\\\\vinin.ucoz.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Vinin', 'link': 'http:\\\\vinin.ucoz.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LRMA'}, 'levels': [], 'description': ['Линейная регрессия является статистическим инструментом, используемым для', 'прогнозирования будущих цен исходя из прошлых данных. Используется метод ', 'наименьших квадратов для построения «наиболее подходящей» прямой линии ', 'через ряд точек ценовых значений. В качестве входных параметров используется ', 'количество расчетных баров (свечей). Данный индикатор хорошо использовать для автоматической торговли'], 'name': 'LRMA', 'source': 'MQL5 Indicators/Linear Regression/LRMA.mq5', 'folder': 'Linear Regression', 'inputs': [{'mql': 'LRMAPeriod', 'py': 'LRMAPeriod', 'param': 'LRMAPeriod', 'type': 'int', 'default': 14, 'label': 'Period LRMA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LRMAPeriod = _input('LRMAPeriod', 14)  # Period LRMA
LRMABuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LRMABuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(LRMABuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total <= LRMAPeriod:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        ArrayInitialize(LRMABuffer, 0.0)
        limit = rates_total - LRMAPeriod - 1
    for pos in range(limit, 0 - 1, -1):
        LRMABuffer[pos] = LRMA(pos, LRMAPeriod, close)
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


class LRMAIndicator(_MQL5Indicator):
    name = 'LRMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LRMAPeriod': 14,  # Period LRMA
    }

