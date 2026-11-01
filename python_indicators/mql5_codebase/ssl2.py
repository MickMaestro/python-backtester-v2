"""SSL2 — converted from MQL5: MQL5 Indicators/SSL2/SSL2.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13959039, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SSL'}, 'levels': [], 'description': [], 'name': 'SSL2', 'source': 'MQL5 Indicators/SSL2/SSL2.mq5', 'folder': 'SSL2', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания первого мувинга', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 26, 'label': 'глубина сглаживания второго мувинга', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength1 = _input('XLength1', 12)  # глубина сглаживания первого мувинга
XLength2 = _input('XLength2', 26)  # глубина сглаживания второго мувинга
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, MathMax(XLength1, XLength2), XPhase)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = UpXMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'SSL(', XLength1, ', ', XLength2, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    upxma = 0.0
    dnxma = 0.0
    ssl1 = 0.0
    ssl2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        upxma = UpXMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, high[bar], bar, False)
        dnxma = DnXMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, low[bar], bar, False)
        if close[bar] < dnxma:
            ssl1 = upxma
        else:
            ssl1 = dnxma
        upxma = UpXMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, high[bar], bar, False)
        dnxma = DnXMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, low[bar], bar, False)
        if close[bar] < dnxma:
            ssl2 = upxma
        else:
            ssl2 = dnxma
        UpIndBuffer[bar] = ssl1 + dPriceShift
        DnIndBuffer[bar] = ssl2 + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
UpXMA1 = _alloc(CXMA)
UpXMA1.__init__()
DnXMA1 = _alloc(CXMA)
DnXMA1.__init__()
UpXMA2 = _alloc(CXMA)
UpXMA2.__init__()
DnXMA2 = _alloc(CXMA)
DnXMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SSL2(_MQL5Indicator):
    name = 'SSL2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength1': 12,  # глубина сглаживания первого мувинга
        'XLength2': 26,  # глубина сглаживания второго мувинга
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

