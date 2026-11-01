"""XIBS_Histogram — converted from MQL5: MQL5 Indicators/XIBS_Histogram/XIBS_Histogram.mq5

Internal Bar Strength
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [13959039, 16711680, 8421504, 8388736, 9639167]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Internal Bar Strength'}, 'levels': [], 'description': ['Internal Bar Strength'], 'name': 'XIBS_Histogram', 'source': 'MQL5 Indicators/XIBS_Histogram/XIBS_Histogram.mq5', 'folder': 'XIBS_Histogram', 'inputs': [{'mql': 'IMA_Method', 'py': 'IMA_Method', 'param': 'IMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'ILength', 'py': 'ILength', 'param': 'ILength', 'type': 'int', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPhase', 'py': 'IPhase', 'param': 'IPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Direct', 'py': 'Direct', 'param': 'Direct', 'type': 'bool', 'default': True, 'label': 'переворот индикатора по вертикали', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_LOW = 0
PRICE_HIGH_CLOSE = 1
_enum('Applied_price_', {0: 'PRICE_CLOSE_LOW', 1: 'PRICE_HIGH_CLOSE'})

# ---- inputs and global variables
IMA_Method = _input('IMA_Method', MODE_SMA_)  # метод усреднения
ILength = _input('ILength', 12)  # глубина сглаживания
IPhase = _input('IPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_HIGH_CLOSE)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Direct = _input('Direct', True)  # переворот индикатора по вертикали
HighLevel = _input('HighLevel', 60)  # уровень перезакупа
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
UpExtLineBuffer = Arr(0, 0.0)
DnExtLineBuffer = Arr(0, 0.0)
ExtColorLineBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(IMA_Method, ILength, IPhase)
    XMA1.XMALengthCheck('ILength', ILength)
    XMA1.XMAPhaseCheck('IPhase', IPhase, IMA_Method)
    SetIndexBuffer(0, UpExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtColorLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(IMA_Method)
    StringConcatenate(shortname, 'Internal Bar Strength(', Smooth1, ', ', ILength, ', ', IPhase, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    range_ = 0.0
    dprice = 0.0
    ibs = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if IPC:
            dprice = close[bar] - low[bar]
        else:
            dprice = high[bar] - close[bar]
        range_ = high[bar] - low[bar]
        if range_:
            ibs = _fdiv(dprice, range_)
        else:
            ibs = 0.0
        UpExtLineBuffer[bar] = 100 * XMA1.XMASeries(0, prev_calculated, rates_total, IMA_Method, IPhase, ILength, ibs, bar, False)
        if not Direct:
            UpExtLineBuffer[bar] *= -1
        DnExtLineBuffer[bar] = 50.0
        clr = _int(2.0)
        if UpExtLineBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif UpExtLineBuffer[bar] > 50.0:
            clr = _int(1.0)
        elif UpExtLineBuffer[bar] < LowLevel:
            clr = _int(4.0)
        elif UpExtLineBuffer[bar] < 50.0:
            clr = _int(3.0)
        ExtColorLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XIBSHistogram(_MQL5Indicator):
    name = 'XIBS_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'ILength': 12,  # глубина сглаживания
        'IPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({0: 'Close-Low', 1: 'High-Close'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Direct': True,  # переворот индикатора по вертикали
        'HighLevel': 60,  # уровень перезакупа
        'LowLevel': 40,  # уровень перепроданности
    }

