"""Logarithmic_Regression — converted from MQL5: MQL5 Indicators/Logarithmic Regression/Logarithmic_Regression.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper', 2: 'Middle', 3: 'Lower'}, 'levels': [], 'description': [], 'name': 'Logarithmic_Regression', 'source': 'MQL5 Indicators/Logarithmic Regression/Logarithmic_Regression.mq5', 'folder': 'Logarithmic Regression', 'inputs': [{'mql': 'InpLength', 'py': 'InpLength', 'param': 'InpLength', 'type': 'uint', 'default': 50, 'label': 'Length', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpLength = _input('InpLength', 50)  # Length
InpDeviation = _input('InpDeviation', 1.0)  # Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferUpper = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
handle_ma = 0
length = 0
deviation = 0.0
summ_y_value = Arr(4, 0.0, dyn=False)
constant = Arr(4, 0.0, dyn=False)
matrix = Arr(4, 0.0, dyn=False, dims=(4,))
summ_x_value = Arr(8, 0.0, dyn=False)

def OnInit():
    global deviation, handle_ma, length
    length = (3 if (InpLength < 3) else InpLength)
    deviation = (0.01 if (InpDeviation < 0.01) else InpDeviation)
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferMA, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Logarithmic Regression(' + _str(length) + ',' + DoubleToString(deviation, 2) + ')')
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < length:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    count = (1 if (limit == 0) else rates_total)
    copied_ma = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied_ma != count:
        return 0
    ArrayInitialize(summ_x_value, 0)
    ArrayInitialize(summ_y_value, 0)
    ArrayInitialize(constant, 0)
    ArrayInitialize(matrix, 0)
    summ_x = 0.0
    summ_y = 0.0
    summ = 0.0
    summ_x_value[0] = length
    for exp_n in range(1, 2 + 1):
        summ_x = 0.0
        summ_y = 0.0
        for k in range(1, length + 1):
            lnx = MathLog(k)
            summ_x += MathPow(lnx, exp_n)
            if exp_n == 1:
                summ_y += MathLog(BufferMA[length - k])
            else:
                summ_y += MathLog(BufferMA[length - k]) * MathPow(lnx, exp_n - 1)
        summ_x_value[exp_n] = summ_x
        if summ_y != 0:
            summ_y_value[exp_n - 1] = summ_y
    for row in range(0, 1 + 1):
        for col in range(0, 1 + 1):
            matrix[row][col] = summ_x_value[row + col]
    summ_y_value[1] = summ_y_value[1] - (_fdiv(matrix[1][0], matrix[0][0]) * summ_y_value[0])
    matrix[1][1] = matrix[1][1] - (_fdiv(matrix[1][0], matrix[0][0]) * matrix[0][1])
    constant[1] = _fdiv(summ_y_value[1], matrix[1][1])
    a = _fdiv(summ_y_value[0] - (constant[1] * matrix[0][1]), matrix[0][0])
    constant[0] = MathExp(a)
    k = 1
    summ = 0.0
    for i in range(length - 1, 0 - 1, -1):
        BufferMiddle[i] = constant[0] * MathPow(k, constant[1])
        summ += MathPow(BufferMA[i] - BufferMiddle[i], 2)
        k += 1
    BufferMiddle[length] = EMPTY_VALUE
    variance = MathSqrt(_fdiv(summ, length))
    for i in range(length - 1, 0 - 1, -1):
        BufferUpper[i] = BufferMiddle[i] + (deviation * variance)
        BufferLower[i] = BufferMiddle[i] - (deviation * variance)
    BufferUpper[length] = EMPTY_VALUE
    BufferLower[length] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LogarithmicRegression(_MQL5Indicator):
    name = 'Logarithmic_Regression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpLength': 50,  # Length
        'InpDeviation': 1.0,  # Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

