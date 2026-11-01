"""SSL — converted from MQL5: MQL5 Indicators/SSL/SSL.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16748574, 9639167]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'SSL'}, 'levels': [], 'description': [], 'name': 'SSL', 'source': 'MQL5 Indicators/SSL/SSL.mq5', 'folder': 'SSL', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
ExtIndBuffer = Arr(0, 0.0)
ColorExtIndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    UpXMA.XMALengthCheck('XLength', XLength)
    DnXMA.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, ExtIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = UpXMA.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'SSL(', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    upxma = 0.0
    dnxma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        upxma = UpXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False)
        dnxma = DnXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False)
        if close[bar] < dnxma:
            ExtIndBuffer[bar] = upxma + dPriceShift
            ColorExtIndBuffer[bar] = 1.0
        else:
            ExtIndBuffer[bar] = dnxma + dPriceShift
            ColorExtIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
UpXMA = _alloc(CXMA)
UpXMA.__init__()
DnXMA = _alloc(CXMA)
DnXMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SSL(_MQL5Indicator):
    name = 'SSL'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

