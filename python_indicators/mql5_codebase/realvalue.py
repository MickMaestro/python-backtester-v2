"""realvalue — converted from MQL5: MQL5 Indicators/RealValue/realvalue.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RealValue'}, 'levels': [], 'description': [], 'name': 'realvalue', 'source': 'MQL5 Indicators/RealValue/realvalue.mq5', 'folder': 'RealValue', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Variation', 'py': 'Variation', 'param': 'Variation', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 20, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Alpha = _input('Alpha', 1.0)
Variation = _input('Variation', 3.0)
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 20)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RealValue')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    var = 0.0
    xvar = 0.0
    val = 0.0
    diffB = 0.0
    diff = 0.0
    res = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 2
        IndBuffer[first - 1] = (high[first - 1] + low[first - 1]) / 2.0
        IndBuffer[first - 2] = (high[first - 2] + low[first - 2]) / 2.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        var = MathAbs(high[bar] - low[bar] - (high[bar - 1] - low[bar - 1]))
        xvar = XMA1.XMASeries(2, prev_calculated, rates_total, XMA_Method, XPhase, XLength, var, bar, False)
        val = (high[bar] + low[bar]) / 2.0
        diffB = IndBuffer[bar - 1] - IndBuffer[bar - 2]
        diff = val - ((high[bar - 1] + low[bar - 1]) / 2.0)
        res = Alpha * var
        if diffB > res:
            diffB = res
        if diffB < (-res):
            diffB = -res
        c = var / Variation
        if val > IndBuffer[bar - 1]:
            if diff < 0:
                c = 0.0
                diffB = 0.0
            IndBuffer[bar] = IndBuffer[bar - 1] + diffB + c
        else:
            if diff > 0:
                c = 0.0
                diffB = 0.0
            IndBuffer[bar] = IndBuffer[bar - 1] + diffB - c
        IndBuffer[bar] = (IndBuffer[bar] + IndBuffer[bar - 1]) / 2.0
        IndBuffer[bar] += dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Realvalue(_MQL5Indicator):
    name = 'realvalue'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 1.0,
        'Variation': 3.0,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 20,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

