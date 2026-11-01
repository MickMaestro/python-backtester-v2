"""RVIDiff — converted from MQL5: MQL5 Indicators/RVIDiff/RVIDiff.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 8421376, 8421504, 36095, 55295]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'RVIDiff'}, 'levels': [], 'description': [], 'name': 'RVIDiff', 'source': 'MQL5 Indicators/RVIDiff/RVIDiff.mq5', 'folder': 'RVIDiff', 'inputs': [{'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 13, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RVIPeriod = _input('RVIPeriod', 12)
XMA_Method = _input('XMA_Method', MODE_T3)  # метод сглаживания индикатора
XLength = _input('XLength', 13)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_1 = 0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
RVI_Handle = 0

def OnInit():
    global RVI_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(RVIPeriod) + 1 + 3 + 1
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    RVI_Handle = iRVI(None, 0, RVIPeriod)
    if RVI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RVIDiff(' + _str(RVIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(RVI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    RVI = Arr(0, 0.0)
    Sign = Arr(0, 0.0)
    diff = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    maxbar = rates_total - 1 - min_rates_1
    if CopyBuffer(RVI_Handle, MAIN_LINE, 0, to_copy, RVI) <= 0:
        return 0
    if CopyBuffer(RVI_Handle, SIGNAL_LINE, 0, to_copy, Sign) <= 0:
        return 0
    ArraySetAsSeries(RVI, True)
    ArraySetAsSeries(Sign, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        diff = RVI[bar] - Sign[bar]
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, diff, bar, True)
        clr = 2
        if IndBuffer[bar] >= 0:
            if IndBuffer[bar] >= IndBuffer[bar + 1]:
                clr = 0
            else:
                clr = 1
        else:
            if IndBuffer[bar] <= IndBuffer[bar + 1]:
                clr = 4
            else:
                clr = 3
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RVIDiff(_MQL5Indicator):
    name = 'RVIDiff'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RVIPeriod': 12,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод сглаживания индикатора
        'XLength': 13,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

