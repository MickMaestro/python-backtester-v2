"""xlineregression — converted from MQL5: MQL5 Indicators/XLineRegression/xlineregression.mq5

Copyright: Copyright © 2012, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [5197615], 2: [8388736], 3: [255], 4: [16711680], 5: [16711680], 6: [255], 7: [8388736], 8: [5197615]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4}, 'labels': {2: '+4Sigma', 3: '+3Sigma', 4: '+2Sigma', 5: '+1Sigma', 6: '-1Sigma', 7: '-2Sigma', 8: '-3Sigma', 9: '-4Sigma'}, 'levels': [], 'description': [''], 'name': 'xlineregression', 'source': 'MQL5 Indicators/XLineRegression/xlineregression.mq5', 'folder': 'XLineRegression', 'inputs': [{'mql': 'days', 'py': 'days', 'param': 'days', 'type': 'int', 'default': 90, 'label': 'number of days for average', 'sinput': False}, {'mql': 'period1', 'py': 'period1', 'param': 'period1', 'type': 'int', 'default': 40, 'label': 'period of the linear regression', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'double', 'default': 0.3, 'label': 'step between the lines', 'sinput': False}, {'mql': 'degree', 'py': 'degree', 'param': 'degree', 'type': 'int', 'default': 1, 'label': 'regression degree', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
days = _input('days', 90)  # number of days for average
period1 = _input('period1', 40)  # period of the linear regression
step = _input('step', 0.3)  # step between the lines
degree = _input('degree', 1)  # regression degree
price = _input('price', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
myPeriod = PERIOD_D1
a = Arr(10, 0.0, dyn=False, dims=(10,))
b = Arr(10, 0.0, dyn=False)
x = Arr(10, 0.0, dyn=False)
sx = Arr(20, 0.0, dyn=False)
period = 0
avgDayRange = 0.0
min_rates_total = 0
SMA_Handle = 0
LWMA_Handle = 0

def OnInit():
    global LWMA_Handle, SMA_Handle, min_rates_total, period
    period = _idiv(period1 * 50 * 5 * 60, PeriodSeconds())
    min_rates_total = period + 1
    LWMA_Handle = iMA(None, 0, period, 0, MODE_LWMA, price)
    if LWMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the LWMA indicator')
    SMA_Handle = iMA(None, 0, period, 0, MODE_SMA, price)
    if SMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SMA indicator')
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer8, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    shortname = Box("")
    StringConcatenate(shortname, 'XLinesReg(', days, ', ', period1, ', ', step, ', ', EnumToString(price, 'Applied_price_'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global avgDayRange
    if (BarsCalculated(SMA_Handle) < rates_total or BarsCalculated(LWMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    PP = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        summ = 0.0
        for i in range(days - 1, 0 - 1, -1):
            O = Arr(1, 0.0, dyn=False)
            C = Arr(1, 0.0, dyn=False)
            if CopyOpen(Symbol(), myPeriod, i, 1, O) <= 0:
                return 0
            if CopyClose(Symbol(), myPeriod, i, 1, C) <= 0:
                return 0
            summ += MathAbs(C[0] - O[0])
        avgDayRange = summ / days
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if degree == 1:
            PP = regression_LRMA(bar)
        elif degree == 2:
            PP = regression_QRMA(bar, open, low, high, close)
        else:
            PP = regressionPolynomial(bar, open, low, high, close)
        if PP == EMPTY_VALUE:
            return 0
        ExtLineBuffer1[bar] = PP + (avgDayRange * step * 4)
        ExtLineBuffer2[bar] = PP + (avgDayRange * step * 3)
        ExtLineBuffer3[bar] = PP + (avgDayRange * step * 2)
        ExtLineBuffer4[bar] = PP + (avgDayRange * step * 1)
        ExtLineBuffer5[bar] = PP - (avgDayRange * step * 1)
        ExtLineBuffer6[bar] = PP - (avgDayRange * step * 2)
        ExtLineBuffer7[bar] = PP - (avgDayRange * step * 3)
        ExtLineBuffer8[bar] = PP - (avgDayRange * step * 4)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]

def ma_qwma(shift, Open, Low, High, Close):
    sum_ = 0.0
    j = 0
    i = 0
    j = shift
    i = 1
    while j < (shift + period):
        sum_ += PriceSeries(price, j, Open, Low, High, Close) * MathPow(period - i + 1, 2)
        j += 1
        i += 1
    value = _fdiv(6.0, period * (period + 1) * ((2 * period) + 1))
    return value * sum_

def regression_QRMA(shift, Open, Low, High, Close):
    sma = Arr(1, 0.0, dyn=False)
    lwma = Arr(1, 0.0, dyn=False)
    if CopyBuffer(SMA_Handle, 0, shift, 1, sma) <= 0:
        return EMPTY_VALUE
    if CopyBuffer(LWMA_Handle, 0, shift, 1, lwma) <= 0:
        return EMPTY_VALUE
    qwma = ma_qwma(shift, Open, Low, High, Close)
    value = (3.0 * sma[0]) + (qwma * (10 - _idiv(15, period + 2))) - (lwma[0] * (12 - _idiv(15, period + 2)))
    return value

def regressionPolynomial(shift, Open, Low, High, Close):
    sx[1] = period + 1
    degree1 = degree + 1
    max_ = (degree1 * 2) - 2
    for i in range(1, max_ + 1):
        sx[i + 1] = 0.0
        for n in range(0, period + 1):
            sx[i + 1] += MathPow(n, i)
    t = 0.0
    for i in range(1, degree1 + 1):
        b[i] = 0.0
        n = 0
        while n <= period:
            if i == 1:
                b[i] += PriceSeries(price, n + shift, Open, Low, High, Close)
            else:
                b[i] += PriceSeries(price, n + shift, Open, Low, High, Close) * MathPow(n, i - 1)
            n += 1
    for j in range(1, degree1 + 1):
        for i in range(1, degree1 + 1):
            k = i + j - 1
            a[i][j] = sx[k]
    for k in range(1, degree1 - 1 + 1):
        l = 0
        mm = 0.0
        for i in range(k, degree1 + 1):
            if MathAbs(a[i][k]) > mm:
                mm = MathAbs(a[i][k])
                l = i
        if l == 0:
            return 0.0
        if l != k:
            for j in range(1, degree1 + 1):
                t = a[k][j]
                a[k][j] = a[l][j]
                a[l][j] = t
            t = b[k]
            b[k] = b[l]
            b[l] = t
        div = 0.0
        for i in range(k + 1, degree1 + 1):
            div = _fdiv(a[i][k], a[k][k])
            for j in range(1, degree1 + 1):
                if j == k:
                    a[i][j] = 0.0
                else:
                    a[i][j] = a[i][j] - (div * a[k][j])
            b[i] = b[i] - (div * b[k])
    x[degree1] = _fdiv(b[degree1], a[degree1][degree1])
    for i in range(degree, 1 - 1, -1):
        t = 0.0
        for j in range(1, degree1 - i + 1):
            t += a[i][i + j] * x[i + j]
            x[i] = _fdiv(1, a[i][i]) * (b[i] - t)
    value = x[1]
    for i in range(1, degree + 1):
        value += x[i + 1] * MathPow(period, i)
    return value

def regression_LRMA(shift):
    sma = Arr(1, 0.0, dyn=False)
    lwma = Arr(1, 0.0, dyn=False)
    if CopyBuffer(SMA_Handle, 0, shift, 1, sma) <= 0:
        return EMPTY_VALUE
    if CopyBuffer(LWMA_Handle, 0, shift, 1, lwma) <= 0:
        return EMPTY_VALUE
    return (3 * lwma[0]) - (2 * sma[0])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xlineregression(_MQL5Indicator):
    name = 'xlineregression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'days': 90,  # number of days for average
        'period1': 40,  # period of the linear regression
        'step': 0.3,  # step between the lines
        'degree': 1,  # regression degree
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

