"""ICHI_OSC — converted from MQL5: MQL5 Indicators/ICHI_OSC/ICHI_OSC.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16748574, 13458026, 8421504, 8388736, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ColorXWPR_Histogram'}, 'levels': [], 'description': [], 'name': 'ICHI_OSC', 'source': 'MQL5 Indicators/ICHI_OSC/ICHI_OSC.mq5', 'folder': 'ICHI_OSC', 'inputs': [{'mql': 'a_ichi', 'py': 'a_ichi', 'param': 'a_ichi', 'type': 'uint', 'default': 22, 'label': 'период Ишимоку', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'метод сглаживания', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_COLOR_MODE
ENUM_LEVELES = 1
ENUM_DIRECT = 2
_enum('ENUM_COLOR_MODE', {1: 'ENUM_LEVELES', 2: 'ENUM_DIRECT'})

# ---- inputs and global variables
a_ichi = _input('a_ichi', 22)  # период Ишимоку
XMA_Method = _input('XMA_Method', MODE_JJMA)  # метод сглаживания
XLength = _input('XLength', 5)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtIndBuffer = Arr(0, 0.0)
ColorExtIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
ks = 0
Ichi_Handle = 0

def OnInit():
    global Ichi_Handle, ks, min_rates_1, min_rates_total
    ts = _int(a_ichi * 0.5)
    ks = _int(a_ichi * 1.5)
    sb = _int(a_ichi * 3.0)
    min_rates_1 = ks + sb + 1
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    Ichi_Handle = iIchimoku(None, 0, ts, ks, sb)
    if Ichi_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iIchimoku')
        return INIT_FAILED
    SetIndexBuffer(0, ExtIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtIndBuffer, True)
    ArraySetAsSeries(ColorExtIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'ICHI_OSC(' + _str(sb) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ichi_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ICHI_OSC = 0.0
    ICHI_OSC_prev = 0.0
    TS = Arr(0, 0.0)
    KS = Arr(0, 0.0)
    SA = Arr(0, 0.0)
    CS = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    MaxBar = rates_total - min_rates_1 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = MaxBar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ichi_Handle, TENKANSEN_LINE, 0, to_copy, TS) <= 0:
        return 0
    if CopyBuffer(Ichi_Handle, KIJUNSEN_LINE, 0, to_copy, KS) <= 0:
        return 0
    if CopyBuffer(Ichi_Handle, SENKOUSPANA_LINE, ks, to_copy, SA) <= 0:
        return 0
    if CopyBuffer(Ichi_Handle, CHIKOUSPAN_LINE, ks, to_copy, CS) <= 0:
        return 0
    ArraySetAsSeries(TS, True)
    ArraySetAsSeries(KS, True)
    ArraySetAsSeries(SA, True)
    ArraySetAsSeries(CS, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        markt = CS[bar] - SA[bar]
        trend = TS[bar] - KS[bar]
        ICHI_OSC = _fdiv(-(trend - markt), Point())
        ExtIndBuffer[bar] = XMA1.XMASeries(MaxBar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, ICHI_OSC, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        ICHI_OSC = ExtIndBuffer[bar]
        ICHI_OSC_prev = ExtIndBuffer[bar + 1]
        if ICHI_OSC > 0:
            if ICHI_OSC_prev < ICHI_OSC:
                clr = 0
            if ICHI_OSC_prev > ICHI_OSC:
                clr = 1
        elif ICHI_OSC < 0:
            if ICHI_OSC_prev < ICHI_OSC:
                clr = 4
            if ICHI_OSC_prev > ICHI_OSC:
                clr = 3
        ColorExtIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ICHIOSC(_MQL5Indicator):
    name = 'ICHI_OSC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'a_ichi': 22,  # период Ишимоку
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания
        'XLength': 5,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

