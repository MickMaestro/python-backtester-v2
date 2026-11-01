"""atrsmoothed — converted from MQL5: MQL5 Indicators/ATRSmoothed_3HTF/atrsmoothed.mq5

ATR Channels
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [14822282]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ATRSmoothed'}, 'levels': [], 'description': ['ATR Channels'], 'name': 'atrsmoothed', 'source': 'MQL5 Indicators/ATRSmoothed_3HTF/atrsmoothed.mq5', 'folder': 'ATRSmoothed_3HTF', 'inputs': [{'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
ATRPeriod = _input('ATRPeriod', 14)
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Метод усреднения
XLength = _input('XLength', 5)  # Глубина  сглаживания
XPhase = _input('XPhase', 15)  # Параметр усреднения
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_ATR = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_ATR, min_rates_total
    ATR_Handle = iATR(None, PERIOD_CURRENT, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_ATR = ATRPeriod
    min_rates_total = min_rates_ATR + GetStartBars(XMA_Method, XLength, XPhase) + 1
    XMA.XMALengthCheck('XLength', XLength)
    XMA.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ExtLineBuffer, True)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'ATRSmoothed(', ATRPeriod, ' ', XLength, ' ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    Range = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    maxbar = rates_total - 1 - min_rates_ATR
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer[bar] = XMA.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, Range[bar], bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atrsmoothed(_MQL5Indicator):
    name = 'atrsmoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATRPeriod': 14,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'XLength': 5,  # Глубина  сглаживания
        'XPhase': 15,  # Параметр усреднения
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

