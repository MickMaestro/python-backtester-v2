"""ROC2_VG — converted from MQL5: MQL5 Indicators/ROC2_VG/ROC2_VG.mq5

Copyright: Copyright © 2006, Vladislav Goshkov (VG); Link: 4vg@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Vladislav Goshkov (VG)', 'link': '4vg@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [2263842, 17919]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ROC2_VG', 'source': 'MQL5 Indicators/ROC2_VG/ROC2_VG.mq5', 'folder': 'ROC2_VG', 'inputs': [{'mql': 'ROCPeriod1', 'py': 'ROCPeriod1', 'param': 'ROCPeriod1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'ROCType1', 'py': 'ROCType1', 'param': 'ROCType1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ROCPeriod2', 'py': 'ROCPeriod2', 'param': 'ROCPeriod2', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ROCType2', 'py': 'ROCType2', 'param': 'ROCType2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Livel1', 'py': 'Livel1', 'param': 'Livel1', 'type': 'double', 'default': 0.005, 'label': '', 'sinput': False}, {'mql': 'Livel2', 'py': 'Livel2', 'param': 'Livel2', 'type': 'double', 'default': 0.002, 'label': '', 'sinput': False}, {'mql': 'Livel3', 'py': 'Livel3', 'param': 'Livel3', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Livel4', 'py': 'Livel4', 'param': 'Livel4', 'type': 'double', 'default': -0.002, 'label': '', 'sinput': False}, {'mql': 'Livel5', 'py': 'Livel5', 'param': 'Livel5', 'type': 'double', 'default': -0.005, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_TYPE
MOM = 1
ROC = 2
ROCP = 3
ROCR = 4
ROCR100 = 5
_enum('ENUM_TYPE', {1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROCR', 5: 'ROCR100'})

# ---- inputs and global variables
ROCPeriod1 = _input('ROCPeriod1', 8)
ROCType1 = _input('ROCType1', MOM)
ROCPeriod2 = _input('ROCPeriod2', 14)
ROCType2 = _input('ROCType2', MOM)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Livel1 = _input('Livel1', 0.005)
Livel2 = _input('Livel2', 0.002)
Livel3 = _input('Livel3', 0.0)
Livel4 = _input('Livel4', -0.002)
Livel5 = _input('Livel5', -0.005)
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
RSI_Handle = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(ROCPeriod1, ROCPeriod2))
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'ROC2_VG( ' + EnumToString(ROCType1, 'ENUM_TYPE') + ' = ' + _str(ROCPeriod1) + ' ,' + EnumToString(ROCType2, 'ENUM_TYPE') + ' = ' + _str(ROCPeriod2) + ')'
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
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = close[bar]
        prevPrice = close[bar - ROCPeriod1]
        _sw1 = ROCType1
        if _sw1 == MOM:
            IndBuffer1[bar] = price - prevPrice
        elif _sw1 == ROC:
            IndBuffer1[bar] = (_fdiv(price, prevPrice) - 1) * 100
        elif _sw1 == ROCP:
            IndBuffer1[bar] = _fdiv(price - prevPrice, prevPrice)
        elif _sw1 == ROCR:
            IndBuffer1[bar] = _fdiv(price, prevPrice)
        elif _sw1 == ROCR100:
            IndBuffer1[bar] = _fdiv(price, prevPrice) * 100
        else:
            IndBuffer1[bar] = _fdiv(price - prevPrice, prevPrice)
        prevPrice = close[bar - ROCPeriod2]
        _sw2 = ROCType2
        if _sw2 == MOM:
            IndBuffer2[bar] = price - prevPrice
        elif _sw2 == ROC:
            IndBuffer2[bar] = (_fdiv(price, prevPrice) - 1) * 100
        elif _sw2 == ROCP:
            IndBuffer2[bar] = _fdiv(price - prevPrice, prevPrice)
        elif _sw2 == ROCR:
            IndBuffer2[bar] = _fdiv(price, prevPrice)
        elif _sw2 == ROCR100:
            IndBuffer2[bar] = _fdiv(price, prevPrice) * 100
        else:
            IndBuffer2[bar] = _fdiv(price - prevPrice, prevPrice)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ROC2VG(_MQL5Indicator):
    name = 'ROC2_VG'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ROCPeriod1': 8,
        'ROCType1': _Choice({1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROC', 5: 'ROCR100'}, default=1),
        'ROCPeriod2': 14,
        'ROCType2': _Choice({1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROC', 5: 'ROCR100'}, default=1),
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Livel1': 0.005,
        'Livel2': 0.002,
        'Livel3': 0.0,
        'Livel4': -0.002,
        'Livel5': -0.005,
    }

