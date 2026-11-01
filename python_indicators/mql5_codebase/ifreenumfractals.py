"""iFreeNumFractals — converted from MQL5: MQL5 Indicators/iFreeNumFractals/iFreeNumFractals.mq5

Copyright: Copyright © 2017, Artem A. Trishkin, Skype artmedia70; Link: https://login.mql5.com/ru/users/artmedia70/; Version: 3.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Artem A. Trishkin, Skype artmedia70', 'link': 'https://login.mql5.com/ru/users/artmedia70/', 'version': '3.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [14822282]}, 'widths': {1: 3, 2: 3}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': [], 'name': 'iFreeNumFractals', 'source': 'MQL5 Indicators/iFreeNumFractals/iFreeNumFractals.mq5', 'folder': 'iFreeNumFractals', 'inputs': [{'mql': 'TypeFractals', 'py': 'TypeFractals', 'param': 'TypeFractals', 'type': 'int', 'default': 0, 'label': 'Type of fractal', 'sinput': False}, {'mql': 'LeftNumUp', 'py': 'LeftNumUp', 'param': 'LeftNumUp', 'type': 'uint', 'default': 2, 'label': 'The number of bars on the left for upper fractals', 'sinput': False}, {'mql': 'RightNumUp', 'py': 'RightNumUp', 'param': 'RightNumUp', 'type': 'uint', 'default': 2, 'label': 'The number of bars on the right for upper fractals', 'sinput': False}, {'mql': 'LeftNumDn', 'py': 'LeftNumDn', 'param': 'LeftNumDn', 'type': 'uint', 'default': 2, 'label': 'The number of bars on the left for lower fractals', 'sinput': False}, {'mql': 'RightNumDn', 'py': 'RightNumDn', 'param': 'RightNumDn', 'type': 'uint', 'default': 2, 'label': 'The number of bars on the right for lower fractals', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 217, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 218, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_TYPE_FRACTAL
TYPE_FRACTAL_ACCURATE = 0
TYPE_FRACTAL_INACCURATE = 1
_enum('ENUM_TYPE_FRACTAL', {0: 'TYPE_FRACTAL_ACCURATE', 1: 'TYPE_FRACTAL_INACCURATE'})

# ---- inputs and global variables
TypeFractals = _input('TypeFractals', TYPE_FRACTAL_ACCURATE)  # Type of fractal
LeftNumUp = _input('LeftNumUp', 2)  # The number of bars on the left for upper fractals
leftNumUp = 0  # Количество баров слева для верхнего фрактала
RightNumUp = _input('RightNumUp', 2)  # The number of bars on the right for upper fractals
rightNumUp = 0  # Количество баров справа для верхнего фрактала
LeftNumDn = _input('LeftNumDn', 2)  # The number of bars on the left for lower fractals
leftNumDn = 0  # Количество баров слева для нижнего фрактала
RightNumDn = _input('RightNumDn', 2)  # The number of bars on the right for lower fractals
rightNumDn = 0  # Количество баров справа для нижнего фрактала
UpLable = _input('UpLable', 217)  # лейба верхнего фрактала
DnLable = _input('DnLable', 218)  # лейба нижнего фрактала
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global leftNumDn, leftNumUp, min_rates_total, rightNumDn, rightNumUp
    min_rates_total = _int(MathMax(LeftNumUp + RightNumUp, LeftNumDn + RightNumDn))
    leftNumUp = (1 if (_int(LeftNumUp) < 1) else _int(LeftNumUp))
    rightNumUp = (1 if (_int(RightNumUp) < 1) else _int(RightNumUp))
    leftNumDn = (1 if (_int(LeftNumDn) < 1) else _int(LeftNumDn))
    rightNumDn = (1 if (_int(RightNumDn) < 1) else _int(RightNumDn))
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Up Fractal')
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'Down Fractal')
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = MQLInfoString(MQL_PROGRAM_NAME) + '(' + _str(leftNumUp) + ',' + _str(rightNumUp) + ')(' + _str(leftNumDn) + ',' + _str(rightNumDn) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    while bar > fmin(rightNumUp, rightNumDn):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        if GetFreeUpperFractal(rates_total, high, bar, leftNumUp, rightNumUp) > 0:
            UpBuffer[bar] = high[bar]
        if GetFreeLowerFractal(rates_total, low, bar, leftNumDn, rightNumDn) > 0:
            DnBuffer[bar] = low[bar]
        bar -= 1
    return rates_total

def GetFreeUpperFractal(Rates_Total, High, shift, left_dimension=2, right_dimension=2):
    if left_dimension < 1:
        left_dimension = 1
    if right_dimension < 1:
        right_dimension = 1
    if (shift - right_dimension) < 1 or (shift + left_dimension) > (Rates_Total - 1):
        return -1.0
    if TypeFractals == TYPE_FRACTAL_ACCURATE:
        for iii in range(shift - 1, shift - right_dimension - 1, -1):
            if High[iii] > High[iii + 1]:
                return -1.0
        for iii in range(shift + 1, shift + left_dimension + 1):
            if High[iii] > High[iii - 1]:
                return -1.0
    else:
        for iii in range(shift - 1, shift - right_dimension - 1, -1):
            if High[iii] > High[shift]:
                return -1.0
        for iii in range(shift + 1, shift + left_dimension + 1):
            if High[iii] > High[shift]:
                return -1.0
    return High[shift]

def GetFreeLowerFractal(Rates_Total, Low, shift, left_dimension=2, right_dimension=2):
    if left_dimension < 1:
        left_dimension = 1
    if right_dimension < 1:
        right_dimension = 1
    if (shift - right_dimension) < 1 or (shift + left_dimension) > (Rates_Total - 1):
        return -1.0
    if TypeFractals == TYPE_FRACTAL_ACCURATE:
        for iii in range(shift - 1, shift - right_dimension - 1, -1):
            if Low[iii] < Low[iii + 1]:
                return -1.0
        for iii in range(shift + 1, shift + left_dimension + 1):
            if Low[iii] < Low[iii - 1]:
                return -1.0
    else:
        for iii in range(shift - 1, shift - right_dimension - 1, -1):
            if Low[iii] < Low[shift]:
                return -1.0
        for iii in range(shift + 1, shift + left_dimension + 1):
            if Low[iii] < Low[shift]:
                return -1.0
    return Low[shift]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IFreeNumFractals(_MQL5Indicator):
    name = 'iFreeNumFractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TypeFractals': _Choice({0: 'Accurate fractal', 1: 'Inaccurate fractal'}, default=0),  # Type of fractal
        'LeftNumUp': 2,  # The number of bars on the left for upper fractals
        'RightNumUp': 2,  # The number of bars on the right for upper fractals
        'LeftNumDn': 2,  # The number of bars on the left for lower fractals
        'RightNumDn': 2,  # The number of bars on the right for lower fractals
        'UpLable': 217,  # лейба верхнего фрактала
        'DnLable': 218,  # лейба нижнего фрактала
    }

