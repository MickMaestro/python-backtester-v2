"""Polynomial_Regression — converted from MQL5: MQL5 Indicators/Polynomial Regression/Polynomial_Regression.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16748574], 3: [3329330]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Regression', 2: 'Band Up', 3: 'Band Down'}, 'levels': [], 'description': [], 'name': 'Polynomial_Regression', 'source': 'MQL5 Indicators/Polynomial Regression/Polynomial_Regression.mq5', 'folder': 'Polynomial Regression', 'inputs': [{'mql': 'InpLength', 'py': 'InpLength', 'param': 'InpLength', 'type': 'uint', 'default': 50, 'label': 'Length', 'sinput': False}, {'mql': 'InpPower', 'py': 'InpPower', 'param': 'InpPower', 'type': 'uint', 'default': 2, 'label': 'Power', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpLength = _input('InpLength', 50)  # Length
InpPower = _input('InpPower', 2)  # Power
InpDeviation = _input('InpDeviation', 1.0)  # Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferRegression = Arr(0, 0.0)
BufferBandUP = Arr(0, 0.0)
BufferBandDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
handle_ma = 0
length = 0
power = 0
deviation = 0.0

def OnInit():
    global deviation, handle_ma, length, power
    length = (5 if (InpLength < 5) else InpLength)
    power = (9 if (InpPower > 9) else InpPower)
    deviation = (0.01 if (InpDeviation < 0.01) else InpDeviation)
    SetIndexBuffer(0, BufferRegression, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBandUP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBandDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BufferRegression, True)
    ArraySetAsSeries(BufferBandUP, True)
    ArraySetAsSeries(BufferBandDN, True)
    ArraySetAsSeries(BufferMA, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Polynomial regression(' + _str(length) + ',' + _str(power) + ',' + DoubleToString(deviation, 2) + ')')
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
        limit = length - 1
        ArrayInitialize(BufferRegression, EMPTY_VALUE)
        ArrayInitialize(BufferBandUP, EMPTY_VALUE)
        ArrayInitialize(BufferBandDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    count = (1 if (limit == 0) else length)
    copied_ma = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied_ma != count:
        return 0
    summ_x_value = Arr(21, 0.0, dyn=False)
    summ_y_value = Arr(11, 0.0, dyn=False)
    constant = Arr(11, 0.0, dyn=False)
    matrix = Arr(11, 0.0, dyn=False, dims=(11,))
    ArrayInitialize(summ_x_value, 0)
    ArrayInitialize(summ_y_value, 0)
    ArrayInitialize(constant, 0)
    ArrayInitialize(matrix, 0)
    summ = 0.0
    summ_x = 0.0
    summ_y = 0.0
    pos = length - 1
    summ_x_value[0] = length
    for exp_n in range(1, 2 * power + 1):
        summ_x = 0.0
        summ_y = 0.0
        for k in range(1, length + 1):
            summ_x += MathPow(k, exp_n)
            if exp_n == 1:
                summ_y += BufferMA[pos - k + 1]
            elif exp_n <= (power + 1):
                summ_y += BufferMA[pos - k + 1] * MathPow(k, exp_n - 1)
        summ_x_value[exp_n] = summ_x
        if summ_y != 0:
            summ_y_value[exp_n - 1] = summ_y
    for row in range(0, power + 1):
        for col in range(0, power + 1):
            matrix[row][col] = summ_x_value[row + col]
    initial_row = 1
    initial_col = 1
    for i in range(1, power + 1):
        for row in range(initial_row, power + 1):
            summ_y_value[row] = summ_y_value[row] - (_fdiv(matrix[row][i - 1], matrix[i - 1][i - 1]) * summ_y_value[i - 1])
            for col in range(initial_col, power + 1):
                matrix[row][col] = matrix[row][col] - (_fdiv(matrix[row][i - 1], matrix[i - 1][i - 1]) * matrix[i - 1][col])
        initial_col += 1
        initial_row += 1
    j = 0
    for i in range(power, 0 - 1, -1):
        if j == 0:
            constant[i] = _fdiv(summ_y_value[i], matrix[i][i])
        else:
            summ = 0.0
            for k in range(j, 1 - 1, -1):
                summ += constant[i + k] * matrix[i][i + k]
            constant[i] = _fdiv(summ_y_value[i] - summ, matrix[i][i])
        j += 1
    k = 1
    for i in range(length - 1, 0 - 1, -1):
        summ = 0.0
        for n in range(0, power + 1):
            summ += constant[n] * MathPow(k, n)
        BufferRegression[i] = summ
        k += 1
    BufferRegression[length] = EMPTY_VALUE
    summ = 0.0
    for i in range(length - 1, 0 - 1, -1):
        summ += MathPow(BufferMA[i] - BufferRegression[i], 2)
    variance = MathSqrt(_fdiv(summ, length))
    for i in range(length - 1, 0 - 1, -1):
        BufferBandUP[i] = BufferRegression[i] + (deviation * variance)
        BufferBandDN[i] = BufferRegression[i] - (deviation * variance)
    BufferBandUP[length] = EMPTY_VALUE
    BufferBandDN[length] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PolynomialRegression(_MQL5Indicator):
    name = 'Polynomial_Regression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpLength': 50,  # Length
        'InpPower': 2,  # Power
        'InpDeviation': 1.0,  # Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

