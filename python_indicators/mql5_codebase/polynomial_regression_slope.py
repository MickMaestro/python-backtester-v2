"""Polynomial_Regression_Slope — converted from MQL5: MQL5 Indicators/Polynomial_Regression_Slope/Polynomial_Regression_Slope.mq5

Polynomial Regression Slope indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'PRS'}, 'levels': [], 'description': ['Polynomial Regression Slope indicator'], 'name': 'Polynomial_Regression_Slope', 'source': 'MQL5 Indicators/Polynomial_Regression_Slope/Polynomial_Regression_Slope.mq5', 'folder': 'Polynomial_Regression_Slope', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'InpPower', 'py': 'InpPower', 'param': 'InpPower', 'type': 'uint', 'default': 2, 'label': 'Power', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 50)  # Period
InpPower = _input('InpPower', 2)  # Power
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferPRS = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
sumxvalue = Arr(0, 0.0)
sumyvalue = Arr(0, 0.0)
constant = Arr(0, 0.0)
matrix = Arr(0, 0.0)
period = 0
power = 0
handle_ma = 0

def OnInit():
    global handle_ma, period, power
    period = (3 if (InpPeriod < 3) else InpPeriod)
    power = (1 if (InpPower < 1) else InpPower)
    ArrayResize(sumxvalue, (2 * power) + 2)
    ArrayResize(sumyvalue, power * 2)
    ArrayResize(constant, power + 2)
    ArrayResize(matrix, (power + 2) * (power + 2))
    ArrayInitialize(sumxvalue, 0)
    ArrayInitialize(sumyvalue, 0)
    ArrayInitialize(constant, 0)
    ArrayInitialize(matrix, 0)
    SetIndexBuffer(0, BufferPRS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Polynomial Regression Slope (' + _str(period) + ',' + _str(power) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPRS, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferPRS, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    sumx = 0.0
    sumy = 0.0
    sum_ = 0.0
    Start = 0.0
    End = 0.0
    k = 0
    initCol = 0
    initRow = 0
    j = 0
    for i in range(limit, 0 - 1, -1):
        ArrayInitialize(sumxvalue, 0)
        ArrayInitialize(sumyvalue, 0)
        ArrayInitialize(constant, 0)
        ArrayInitialize(matrix, 0)
        p = i + period - 1
        sumxvalue[0] = period
        for n in range(1, 2 * power + 1):
            sumx = 0.0
            sumy = 0.0
            k = 1
            for k in range(k, period + 1):
                sumx += pow(k, n)
                sumy = ((sumy + BufferMA[p - k + 1]) if (n == 1) else (sumy + (BufferMA[p - k + 1] * pow(k, n - 1))))
            else:
                k = _range_end(k, period + 1, 1)
            sumxvalue[n] = sumx
            if sumy != 0:
                sumyvalue[n - 1] = sumy
        row = 0
        while row <= power:
            col = 0
            while col <= power:
                SetM(row, col, sumxvalue[row + col])
                col += 1
            row += 1
        initRow = 1
        initCol = initRow
        n = 1
        while n <= power:
            row = initRow
            while row <= power:
                sumyvalue[row] = sumyvalue[row] - _fdiv(GetM(row, n - 1) * sumyvalue[n - 1], GetM(n - 1, n - 1))
                col = initCol
                while col <= power:
                    SetM(row, col, GetM(row, col) - _fdiv(GetM(row, n - 1) * GetM(n - 1, col), GetM(n - 1, n - 1)))
                    col += 1
                row += 1
            initCol += 1
            initRow += 1
            n += 1
        j = 0
        for n in range(power, 0 - 1, -1):
            if j == 0:
                constant[n] = _fdiv(sumyvalue[n], GetM(n, n))
            else:
                sum_ = 0.0
                k = j
                for k in range(k, 1 - 1, -1):
                    sum_ = sum_ + (constant[n + k] * GetM(n, n + k))
                else:
                    k = _range_end(k, 1 - 1, -1)
                constant[n] = _fdiv(sumyvalue[n] - sum_, GetM(n, n))
            j += 1
        k = 1
        for n in range(i + period - 1, i - 1, -1):
            sum_ = 0.0
            j = 0
            for j in range(j, power + 1):
                sum_ = sum_ + (constant[j] * pow(k, j))
            else:
                j = _range_end(j, power + 1, 1)
            if n == (i + period - 1):
                Start = sum_
            k += 1
        End = sum_
        BufferPRS[i] = _fdiv(End - Start, Point())
        BufferColors[i] = (1 if (BufferPRS[i] < BufferPRS[i + 1]) else 0)
    return rates_total

def GetM(col, row):
    return matrix[(col * (power + 1)) + row]

def SetM(col, row, val):
    matrix[(col * (power + 1)) + row] = val


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PolynomialRegressionSlope(_MQL5Indicator):
    name = 'Polynomial_Regression_Slope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 50,  # Period
        'InpPower': 2,  # Power
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

