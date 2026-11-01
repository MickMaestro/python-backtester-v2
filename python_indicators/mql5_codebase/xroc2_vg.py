"""XROC2_VG — converted from MQL5: MQL5 Indicators/XROC2_VG/XROC2_VG.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [11186720, 13850042]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'XROC2_VG', 'source': 'MQL5 Indicators/XROC2_VG/XROC2_VG.mq5', 'folder': 'XROC2_VG', 'inputs': [{'mql': 'ROCPeriod1', 'py': 'ROCPeriod1', 'param': 'ROCPeriod1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 4, 'label': 'метод усреднения первого индикатора', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 5, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'ROCPeriod2', 'py': 'ROCPeriod2', 'param': 'ROCPeriod2', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения второго индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'ROCType', 'py': 'ROCType', 'param': 'ROCType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Livel1', 'py': 'Livel1', 'param': 'Livel1', 'type': 'double', 'default': 0.005, 'label': '', 'sinput': False}, {'mql': 'Livel2', 'py': 'Livel2', 'param': 'Livel2', 'type': 'double', 'default': 0.002, 'label': '', 'sinput': False}, {'mql': 'Livel3', 'py': 'Livel3', 'param': 'Livel3', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Livel4', 'py': 'Livel4', 'param': 'Livel4', 'type': 'double', 'default': -0.002, 'label': '', 'sinput': False}, {'mql': 'Livel5', 'py': 'Livel5', 'param': 'Livel5', 'type': 'double', 'default': -0.005, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_TYPE
MOM = 1
ROC = 2
ROCP = 3
ROCR = 4
ROCR100 = 5
_enum('ENUM_TYPE', {1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROCR', 5: 'ROCR100'})

# ---- inputs and global variables
ROCPeriod1 = _input('ROCPeriod1', 8)
MA_Method1 = _input('MA_Method1', MODE_JJMA)  # метод усреднения первого индикатора
Length1 = _input('Length1', 5)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
ROCPeriod2 = _input('ROCPeriod2', 14)
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод усреднения второго индикатора
Length2 = _input('Length2', 5)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
ROCType = _input('ROCType', MOM)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Livel1 = _input('Livel1', 0.005)
Livel2 = _input('Livel2', 0.002)
Livel3 = _input('Livel3', 0.0)
Livel4 = _input('Livel4', -0.002)
Livel5 = _input('Livel5', -0.005)
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
min_rates_total = 0
RSI_Handle = 0

def OnInit():
    global min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = _int(MathMax(min_rates_1 + ROCPeriod1, min_rates_2 + ROCPeriod2))
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'ROC2_VG( ' + EnumToString(ROCType, 'ENUM_TYPE') + ', ' + _str(ROCPeriod1) + ', ' + _str(ROCPeriod2) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Livel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Livel2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, Livel3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, Livel4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, Livel5)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    prevPrice = 0.0
    res1 = 0.0
    res2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = close[bar]
        prevPrice = close[MathMax(0, bar - _int(ROCPeriod1))]
        _sw1 = ROCType
        if _sw1 == MOM:
            res1 = price - prevPrice
        elif _sw1 == ROC:
            res1 = (_fdiv(price, prevPrice) - 1) * 100
        elif _sw1 == ROCP:
            res1 = _fdiv(price - prevPrice, prevPrice)
        elif _sw1 == ROCR:
            res1 = _fdiv(price, prevPrice)
        elif _sw1 == ROCR100:
            res1 = _fdiv(price, prevPrice) * 100
        else:
            res1 = _fdiv(price - prevPrice, prevPrice)
        IndBuffer1[bar] = XMA1.XMASeries(ROCPeriod1 + 1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, res1, bar, False)
        prevPrice = close[MathMax(0, bar - _int(ROCPeriod2))]
        _sw2 = ROCType
        if _sw2 == MOM:
            res2 = price - prevPrice
        elif _sw2 == ROC:
            res2 = (_fdiv(price, prevPrice) - 1) * 100
        elif _sw2 == ROCP:
            res2 = _fdiv(price - prevPrice, prevPrice)
        elif _sw2 == ROCR:
            res2 = _fdiv(price, prevPrice)
        elif _sw2 == ROCR100:
            res2 = _fdiv(price, prevPrice) * 100
        else:
            res2 = _fdiv(price - prevPrice, prevPrice)
        IndBuffer2[bar] = XMA2.XMASeries(ROCPeriod2 + 1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res2, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XROC2VG(_MQL5Indicator):
    name = 'XROC2_VG'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ROCPeriod1': 8,
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения первого индикатора
        'Length1': 5,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого сглаживания,
        'ROCPeriod2': 14,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения второго индикатора
        'Length2': 5,  # глубина  второго сглаживания
        'Phase2': 15,  # параметр второго сглаживания,
        'ROCType': _Choice({1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROC', 5: 'ROCR100'}, default=1),
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Livel1': 0.005,
        'Livel2': 0.002,
        'Livel3': 0.0,
        'Livel4': -0.002,
        'Livel5': -0.005,
    }

