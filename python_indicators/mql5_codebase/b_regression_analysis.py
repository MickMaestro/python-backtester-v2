"""b_regression_analysis — converted from MQL5: MQL5 Indicators/Regression Analysis/b_regression_analysis.mq5

This indicator compares four types of regression (linear, quadratic,
logarithmic and exponential) and chooses the one that best fits the
data analyzed.
Copyright: Copyright © 2011, barmenteros; Link: barmenteros.fx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, barmenteros', 'link': 'barmenteros.fx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711935], 2: [16711680], 3: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Regression', 2: 'Upper Band', 3: 'Lower Band'}, 'levels': [], 'description': ['This indicator compares four types of regression (linear, quadratic,', 'logarithmic and exponential) and chooses the one that best fits the', 'data analyzed.'], 'name': 'b_regression_analysis', 'source': 'MQL5 Indicators/Regression Analysis/b_regression_analysis.mq5', 'folder': 'Regression Analysis', 'inputs': [{'mql': 'dp_limiter', 'py': 'dp_limiter', 'param': 'dp_limiter', 'type': 'ushort', 'default': 100, 'label': 'Number of data points', 'sinput': False}, {'mql': 'endpos', 'py': 'endpos', 'param': 'endpos', 'type': 'uint', 'default': 0, 'label': 'Last value position', 'sinput': False}, {'mql': 'multStdDev', 'py': 'multStdDev', 'param': 'multStdDev', 'type': 'double', 'default': 1.96, 'label': 'Bands separation', 'sinput': False}, {'mql': 'comments', 'py': 'comments', 'param': 'comments', 'type': 'int', 'default': 0, 'label': 'Comments switch', 'sinput': False}, {'mql': 'record', 'py': 'record', 'param': 'record', 'type': 'int', 'default': 1, 'label': 'Record info into a file text', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum inputs_switch
On = 0
Off = 1
_enum('inputs_switch', {0: 'On', 1: 'Off'})

# ---- inputs and global variables
dp_limiter = _input('dp_limiter', 100)  # Number of data points
endpos = _input('endpos', 0)  # Last value position
multStdDev = _input('multStdDev', 1.96)  # Bands separation
comments = _input('comments', On)  # Comments switch
record = _input('record', Off)  # Record info into a file text
Extdp_limiter = 0
RegBfr = Arr(0, 0.0)
BandUpBfr = Arr(0, 0.0)
BandDwBfr = Arr(0, 0.0)

def TimeDayMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day

def TimeYearMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.year

def TimeMonthMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.mon

def TimeHourMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.hour

def TimeMinuteMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.min

def TimeSecondsMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.sec

def iPolReg(datapoints, grade, array1, array2):
    pos = 0
    expon = 0
    k = 0
    row = 0
    col = 0
    initialrow = 0
    initialcol = 0
    loop = 0
    i = 0
    j = 0
    sumx = 0.0
    sumyx = 0.0
    sum_ = 0.0
    sumxvalues = Arr(0, 0.0)
    sumyxvalues = Arr(0, 0.0)
    matrix = Arr(0, 0.0, dims=(10,))
    constant = Arr(0, 0.0)
    pos = datapoints - 1
    ArrayResize(sumxvalues, (2 * grade) + 1)
    ArrayResize(sumyxvalues, grade + 1)
    ArrayInitialize(sumxvalues, 0.0)
    ArrayInitialize(sumyxvalues, 0.0)
    sumxvalues[0] = datapoints
    expon = 1
    for expon in range(expon, 2 * grade + 1):
        sumx = 0.0
        sumyx = 0.0
        k = 1
        for k in range(k, datapoints + 1):
            sumx += MathPow(k, expon)
            if expon == 1:
                sumyx += array1[pos - k + 1]
            elif expon <= (grade + 1):
                sumyx += array1[pos - k + 1] * MathPow(k, expon - 1)
        else:
            k = _range_end(k, datapoints + 1, 1)
        sumxvalues[expon] = sumx
        if sumyx != 0.0:
            sumyxvalues[expon - 1] = sumyx
    else:
        expon = _range_end(expon, 2 * grade + 1, 1)
    ArrayResize(matrix, grade + 1)
    ArrayInitialize(matrix, 0.0)
    row = 0
    for row in range(row, grade + 1):
        col = 0
        for col in range(col, grade + 1):
            matrix[row][col] = sumxvalues[row + col]
        else:
            col = _range_end(col, grade + 1, 1)
    else:
        row = _range_end(row, grade + 1, 1)
    initialrow = 1
    initialcol = 1
    loop = 1
    for loop in range(loop, grade + 1):
        row = initialrow
        for row in range(row, grade + 1):
            sumyxvalues[row] = sumyxvalues[row] - (_fdiv(matrix[row][loop - 1], matrix[loop - 1][loop - 1]) * sumyxvalues[loop - 1])
            col = initialcol
            for col in range(col, grade + 1):
                matrix[row][col] = matrix[row][col] - (_fdiv(matrix[row][loop - 1], matrix[loop - 1][loop - 1]) * matrix[loop - 1][col])
            else:
                col = _range_end(col, grade + 1, 1)
        else:
            row = _range_end(row, grade + 1, 1)
        initialrow += 1
        initialcol += 1
    else:
        loop = _range_end(loop, grade + 1, 1)
    ArrayResize(constant, grade + 1)
    ArrayInitialize(constant, 0.0)
    j = 0
    i = grade
    for i in range(i, 0 - 1, -1):
        if j == 0:
            constant[i] = _fdiv(sumyxvalues[i], matrix[i][i])
        else:
            sum_ = 0.0
            k = j
            for k in range(k, 0, -1):
                sum_ += constant[i + k] * matrix[i][i + k]
            else:
                k = _range_end(k, 0, -1)
            constant[i] = _fdiv(sumyxvalues[i] - sum_, matrix[i][i])
        j += 1
    else:
        i = _range_end(i, 0 - 1, -1)
    ArrayResize(array2, datapoints)
    ArrayInitialize(array2, EMPTY_VALUE)
    k = 1
    i = datapoints - 1
    for i in range(i, 0 - 1, -1):
        sum_ = 0.0
        j = 0
        for j in range(j, grade + 1):
            sum_ += constant[j] * MathPow(k, j)
        else:
            j = _range_end(j, grade + 1, 1)
        array2[i] = sum_
        k += 1
    else:
        i = _range_end(i, 0 - 1, -1)

def iLogReg(datapoints, array1, array2):
    pos = 0
    expon = 0
    k = 0
    row = 0
    col = 0
    i = 0
    sumx = 0.0
    sumyx = 0.0
    lnx = 0.0
    a = 0.0
    sumxvalues = Arr(0, 0.0)
    sumyxvalues = Arr(0, 0.0)
    matrix = Arr(0, 0.0, dims=(10,))
    constant = Arr(0, 0.0)
    pos = datapoints - 1
    ArrayResize(sumxvalues, 3)
    ArrayResize(sumyxvalues, 2)
    ArrayInitialize(sumxvalues, 0.0)
    ArrayInitialize(sumyxvalues, 0.0)
    sumxvalues[0] = datapoints
    expon = 1
    for expon in range(expon, 2 + 1):
        sumx = 0.0
        sumyx = 0.0
        k = 1
        for k in range(k, datapoints + 1):
            lnx = MathLog(k)
            sumx += MathPow(lnx, expon)
            if expon == 1:
                sumyx += MathLog(array1[pos - k + 1])
            else:
                sumyx += MathLog(array1[pos - k + 1]) * MathPow(lnx, expon - 1)
        else:
            k = _range_end(k, datapoints + 1, 1)
        sumxvalues[expon] = sumx
        if sumyx != 0.0:
            sumyxvalues[expon - 1] = sumyx
    else:
        expon = _range_end(expon, 2 + 1, 1)
    ArrayResize(matrix, 2)
    ArrayInitialize(matrix, 0.0)
    row = 0
    for row in range(row, 1 + 1):
        col = 0
        for col in range(col, 1 + 1):
            matrix[row][col] = sumxvalues[row + col]
        else:
            col = _range_end(col, 1 + 1, 1)
    else:
        row = _range_end(row, 1 + 1, 1)
    sumyxvalues[1] = sumyxvalues[1] - (_fdiv(matrix[1][0], matrix[0][0]) * sumyxvalues[0])
    matrix[1][1] = matrix[1][1] - (_fdiv(matrix[1][0], matrix[0][0]) * matrix[0][1])
    ArrayResize(constant, 2)
    ArrayInitialize(constant, 0.0)
    constant[1] = _fdiv(sumyxvalues[1], matrix[1][1])
    a = _fdiv(sumyxvalues[0] - (constant[1] * matrix[0][1]), matrix[0][0])
    constant[0] = MathExp(a)
    ArrayResize(array2, datapoints)
    ArrayInitialize(array2, EMPTY_VALUE)
    k = 1
    i = datapoints - 1
    for i in range(i, 0 - 1, -1):
        array2[i] = constant[0] * MathPow(k, constant[1])
        k += 1
    else:
        i = _range_end(i, 0 - 1, -1)

def iExpReg(datapoints, array1, array2):
    pos = 0
    expon = 0
    k = 0
    row = 0
    col = 0
    i = 0
    sumx = 0.0
    sumyx = 0.0
    a = 0.0
    sumxvalues = Arr(0, 0.0)
    sumyxvalues = Arr(0, 0.0)
    matrix = Arr(0, 0.0, dims=(10,))
    constant = Arr(0, 0.0)
    pos = datapoints - 1
    ArrayResize(sumxvalues, 3)
    ArrayResize(sumyxvalues, 2)
    ArrayInitialize(sumxvalues, 0.0)
    ArrayInitialize(sumyxvalues, 0.0)
    sumxvalues[0] = datapoints
    expon = 1
    for expon in range(expon, 2 + 1):
        sumx = 0.0
        sumyx = 0.0
        k = 1
        for k in range(k, datapoints + 1):
            sumx += MathPow(k, expon)
            if expon == 1:
                sumyx += MathLog(array1[pos - k + 1])
            else:
                sumyx += MathLog(array1[pos - k + 1]) * MathPow(k, expon - 1)
        else:
            k = _range_end(k, datapoints + 1, 1)
        sumxvalues[expon] = sumx
        if sumyx != 0.0:
            sumyxvalues[expon - 1] = sumyx
    else:
        expon = _range_end(expon, 2 + 1, 1)
    ArrayResize(matrix, 2)
    ArrayInitialize(matrix, 0.0)
    row = 0
    for row in range(row, 1 + 1):
        col = 0
        for col in range(col, 1 + 1):
            matrix[row][col] = sumxvalues[row + col]
        else:
            col = _range_end(col, 1 + 1, 1)
    else:
        row = _range_end(row, 1 + 1, 1)
    sumyxvalues[1] = sumyxvalues[1] - (_fdiv(matrix[1][0], matrix[0][0]) * sumyxvalues[0])
    matrix[1][1] = matrix[1][1] - (_fdiv(matrix[1][0], matrix[0][0]) * matrix[0][1])
    ArrayResize(constant, 2)
    ArrayInitialize(constant, 0.0)
    constant[1] = _fdiv(sumyxvalues[1], matrix[1][1])
    a = _fdiv(sumyxvalues[0] - (constant[1] * matrix[0][1]), matrix[0][0])
    constant[0] = MathExp(a)
    ArrayResize(array2, datapoints)
    ArrayInitialize(array2, EMPTY_VALUE)
    k = 1
    i = datapoints - 1
    for i in range(i, 0 - 1, -1):
        array2[i] = constant[0] * MathExp(k * constant[1])
        k += 1
    else:
        i = _range_end(i, 0 - 1, -1)

def iStdDevOnArray(array1, datapoints):
    i = 0
    sum_ = 0.0
    arithmean = 0.0
    stddev = 0.0
    sum_ = 0.0
    i = datapoints - 1
    for i in range(i, 0 - 1, -1):
        sum_ += array1[i]
    else:
        i = _range_end(i, 0 - 1, -1)
    if datapoints <= 0:
        datapoints = 1
    arithmean = _fdiv(sum_, datapoints)
    sum_ = 0.0
    i = datapoints - 1
    for i in range(i, 0 - 1, -1):
        sum_ += (array1[i] - arithmean) * (array1[i] - arithmean)
    else:
        i = _range_end(i, 0 - 1, -1)
    if datapoints <= 0:
        datapoints = 1
    stddev = MathSqrt(_fdiv(sum_, datapoints))
    return stddev

def BestReg(rates_total, array1, array2, array3):
    short_name = ""
    currentstddev = 0.0
    c_stddevindex = 0
    i = 0
    if comments == On:
        Comment('LinReg=', DoubleToString(array1[0], Digits()), ' || QuadReg=', DoubleToString(array1[1], Digits()), ' || LogReg=', DoubleToString(array1[2], Digits()), ' || ExpReg=', DoubleToString(array1[3], Digits()))
    currentstddev = array1[0]
    c_stddevindex = 0
    i = 1
    for i in range(i, 3 + 1):
        if array1[i] < currentstddev:
            currentstddev = array1[i]
            c_stddevindex = i
    else:
        i = _range_end(i, 3 + 1, 1)
    _sw1 = c_stddevindex
    if _sw1 == 0:
        iPolReg(dp_limiter, 1, array2, array3)
        short_name = 'LinReg('
    elif _sw1 == 1:
        iPolReg(dp_limiter, 2, array2, array3)
        short_name = 'QuadReg('
    elif _sw1 == 2:
        iLogReg(dp_limiter, array2, array3)
        short_name = 'LogReg('
    elif _sw1 == 3:
        iExpReg(dp_limiter, array2, array3)
        short_name = 'ExpReg('
    else:
        iPolReg(dp_limiter, 1, array2, array3)
        short_name = 'LinReg('
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + _str(dp_limiter) + ')')
    PlotIndexSetString(0, PLOT_LABEL, short_name + _str(dp_limiter) + ')')
    ArrayInitialize(RegBfr, EMPTY_VALUE)
    i = dp_limiter - 1
    for i in range(i, 0 - 1, -1):
        RegBfr[rates_total - 1 - endpos - i] = array3[i]
    else:
        i = _range_end(i, 0 - 1, -1)

def ConfidenceBands(rates_total, array1):
    i = 0
    sum_ = 0.0
    variance = 0.0
    sum_ = 0.0
    i = dp_limiter - 1
    for i in range(i, 0 - 1, -1):
        sum_ += (array1[i] - RegBfr[rates_total - 1 - endpos - i]) * (array1[i] - RegBfr[rates_total - 1 - endpos - i])
    else:
        i = _range_end(i, 0 - 1, -1)
    variance = MathSqrt(sum_ / dp_limiter)
    ArrayInitialize(BandUpBfr, EMPTY_VALUE)
    ArrayInitialize(BandDwBfr, EMPTY_VALUE)
    i = dp_limiter - 1
    for i in range(i, 0 - 1, -1):
        BandUpBfr[rates_total - 1 - endpos - i] = RegBfr[rates_total - 1 - endpos - i] + (multStdDev * variance)
        BandDwBfr[rates_total - 1 - endpos - i] = RegBfr[rates_total - 1 - endpos - i] - (multStdDev * variance)
    else:
        i = _range_end(i, 0 - 1, -1)

def OnInit():
    global Extdp_limiter
    if dp_limiter <= 2:
        Extdp_limiter = 3
        printf('Incorrect value for input variable dp_limiter=%d. Indicator will use value=%d for calculations.', dp_limiter, Extdp_limiter)
    else:
        Extdp_limiter = dp_limiter
    SetIndexBuffer(0, RegBfr)
    SetIndexBuffer(1, BandUpBfr)
    SetIndexBuffer(2, BandDwBfr)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetString(1, PLOT_LABEL, 'UpperBand')
    PlotIndexSetString(2, PLOT_LABEL, 'LowerBand')

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_c_filehandle, _s_OnCalculate_current_day, _s_OnCalculate_p_filehandle, _s_OnCalculate_previous_day
    filename = Box("")
    timetext = Box("")
    i = 0
    errorstddev = Arr(4, 0.0, dyn=False)
    data = Arr(0, 0.0)
    regression = Arr(0, 0.0)
    regressionerror = Arr(0, 0.0)
    if record == On:
        _s_OnCalculate_previous_day = _s_OnCalculate_current_day
        _s_OnCalculate_current_day = TimeDayMQL4(TimeCurrent())
        if _s_OnCalculate_current_day != _s_OnCalculate_previous_day:
            StringConcatenate(filename, TimeYearMQL4(TimeCurrent()), '-', TimeMonthMQL4(TimeCurrent()), '-', _s_OnCalculate_current_day, '-', Symbol(), '-b_Regression_Analysis.txt')
            _s_OnCalculate_p_filehandle = _s_OnCalculate_c_filehandle
            ResetLastError()
            _s_OnCalculate_c_filehandle = FileOpen(filename.v, (FILE_CSV | FILE_READ) | FILE_WRITE, 59)
            if _s_OnCalculate_c_filehandle != INVALID_HANDLE and _s_OnCalculate_c_filehandle != _s_OnCalculate_p_filehandle:
                FileWrite(_s_OnCalculate_c_filehandle, 'time', 'error[LinReg]', 'error[QuadReg]', 'error[LogReg]', 'error[ExpReg]')
            else:
                Print('Operation FileOpen failed, error ', GetLastError())
    ArrayResize(data, Extdp_limiter)
    ArrayResize(regression, Extdp_limiter)
    ArrayResize(regressionerror, Extdp_limiter)
    ArrayInitialize(data, EMPTY_VALUE)
    i = 0
    for i in range(i, dp_limiter):
        data[i] = price[rates_total - 1 - endpos - i]
    else:
        i = _range_end(i, dp_limiter, 1)
    ArrayInitialize(regression, EMPTY_VALUE)
    iPolReg(dp_limiter, 1, data, regression)
    ArrayInitialize(regressionerror, EMPTY_VALUE)
    i = 0
    for i in range(i, dp_limiter):
        regressionerror[i] = MathAbs(data[i] - regression[i])
    else:
        i = _range_end(i, dp_limiter, 1)
    errorstddev[0] = iStdDevOnArray(regressionerror, dp_limiter)
    ArrayInitialize(regression, EMPTY_VALUE)
    iPolReg(dp_limiter, 2, data, regression)
    i = 0
    for i in range(i, dp_limiter):
        regressionerror[i] = MathAbs(data[i] - regression[i])
    else:
        i = _range_end(i, dp_limiter, 1)
    errorstddev[1] = iStdDevOnArray(regressionerror, dp_limiter)
    ArrayInitialize(regression, EMPTY_VALUE)
    iLogReg(dp_limiter, data, regression)
    i = 0
    for i in range(i, dp_limiter):
        regressionerror[i] = MathAbs(data[i] - regression[i])
    else:
        i = _range_end(i, dp_limiter, 1)
    errorstddev[2] = iStdDevOnArray(regressionerror, dp_limiter)
    ArrayInitialize(regression, EMPTY_VALUE)
    iExpReg(dp_limiter, data, regression)
    i = 0
    for i in range(i, dp_limiter):
        regressionerror[i] = MathAbs(data[i] - regression[i])
    else:
        i = _range_end(i, dp_limiter, 1)
    errorstddev[3] = iStdDevOnArray(regressionerror, dp_limiter)
    if record == On:
        if _s_OnCalculate_c_filehandle != INVALID_HANDLE:
            StringConcatenate(timetext, TimeHourMQL4(TimeCurrent()), ':', TimeMinuteMQL4(TimeCurrent()), ':', TimeSecondsMQL4(TimeCurrent()))
            FileWrite(_s_OnCalculate_c_filehandle, timetext.v, DoubleToString(errorstddev[0], Digits()), DoubleToString(errorstddev[1], Digits()), DoubleToString(errorstddev[2], Digits()), DoubleToString(errorstddev[3], Digits()))
    BestReg(rates_total, errorstddev, data, regression)
    ConfidenceBands(rates_total, data)
    return rates_total

# ---- static local variables
_s_OnCalculate_current_day = 0
_s_OnCalculate_previous_day = 0
_s_OnCalculate_c_filehandle = 0
_s_OnCalculate_p_filehandle = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BRegressionAnalysis(_MQL5Indicator):
    name = 'b_regression_analysis'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'dp_limiter': 100,  # Number of data points
        'endpos': 0,  # Last value position
        'multStdDev': 1.96,  # Bands separation
        'comments': _Choice({0: 'On', 1: 'Off'}, default=0),  # Comments switch
        'record': _Choice({0: 'On', 1: 'Off'}, default=1),  # Record info into a file text
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

