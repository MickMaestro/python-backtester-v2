"""averageofatr_histogram — converted from MQL5: MQL5 Indicators/AverageOfATR_Histogram/averageofatr_histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 10, 2: 5, 3: 5}, 'colors': {1: [65535, 9109504], 2: [16711935], 3: [16748574]}, 'widths': {1: 3, 2: 4, 3: 2}, 'styles': {1: 0}, 'labels': {1: 'AverageOfATR_Histogram', 2: 'AverageOfATR Trend', 3: 'AverageOfATR Flat'}, 'levels': [], 'description': [''], 'name': 'averageofatr_histogram', 'source': 'MQL5 Indicators/AverageOfATR_Histogram/averageofatr_histogram.mq5', 'folder': 'AverageOfATR_Histogram', 'inputs': [{'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 3, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
ATRPeriod = _input('ATRPeriod', 7)
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 3)  # Глубина  сглаживания
XPhase = _input('XPhase', 15)  # Параметр усреднения
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
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
    min_rates_total = min_rates_ATR + GetStartBars(XMA_Method, XLength, XPhase) + 2
    XMA.XMALengthCheck('XLength', XLength)
    XMA.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    SetIndexBuffer(2, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(3, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 163)
    ArraySetAsSeries(DnIndBuffer, True)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'AverageOfATR_Histogram(', ATRPeriod, ' ', XLength, ' ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_diff_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    clr = 0
    ATR = Arr(0, 0.0)
    diff = 0.0
    xatr = 0.0
    maxbar = rates_total - 1 - min_rates_ATR - 2
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        _s_OnCalculate_diff_prev = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    ArraySetAsSeries(ATR, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        xatr = XMA.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, ATR[bar], bar, True)
        IndBuffer[bar] = ATR[bar] - xatr
        diff = IndBuffer[bar]
        if diff > 0:
            clr = 0
        else:
            clr = 1
        ColorBuffer[bar] = clr
        UpIndBuffer[bar] = EMPTY_VALUE
        DnIndBuffer[bar] = EMPTY_VALUE
        if diff > 0 and _s_OnCalculate_diff_prev <= 0:
            UpIndBuffer[bar] = 0.0
        if diff < 0 and _s_OnCalculate_diff_prev >= 0:
            DnIndBuffer[bar] = 0.0
        if bar:
            _s_OnCalculate_diff_prev = diff
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()

# ---- static local variables
_s_OnCalculate_diff_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageofatrHistogram(_MQL5Indicator):
    name = 'averageofatr_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATRPeriod': 7,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 3,  # Глубина  сглаживания
        'XPhase': 15,  # Параметр усреднения
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

