"""spectr — converted from MQL5: MQL5 Indicators/Spectr/spectr.mq5

Copyright: Copyright © 2009, Yuriy Tokman; Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [42495], 3: [65535], 4: [65280], 5: [16711680], 6: [16748574], 7: [13828244], 8: [6908265]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'Wave 1', 2: 'Wave 2', 3: 'Wave 3', 4: 'Wave 4', 5: 'Wave 5', 6: 'Wave 6', 7: 'Wave 7', 8: 'Wave 8'}, 'levels': [], 'description': [], 'name': 'spectr', 'source': 'MQL5 Indicators/Spectr/spectr.mq5', 'folder': 'Spectr', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'int', 'default': 16388, 'label': 'indicator time frame', 'sinput': False}, {'mql': 'iStartFrom', 'py': 'iStartFrom', 'param': 'iStartFrom', 'type': 'uint', 'default': 0, 'label': 'Bar index for the calculation start', 'sinput': False}, {'mql': 'VV', 'py': 'VV', 'param': 'VV', 'type': 'uint', 'default': 1, 'label': 'Wave height', 'sinput': False}, {'mql': 'pm', 'py': 'pm', 'param': 'pm', 'type': 'uint', 'default': 20, 'label': 'Smoothing period to the calculation of moving average', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'type of averaging', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', PERIOD_H4)  # indicator time frame
iStartFrom = _input('iStartFrom', 0)  # Bar index for the calculation start
VV = _input('VV', 1)  # Wave height
pm = _input('pm', 20)  # Smoothing period to the calculation of moving average
ma_method = _input('ma_method', MODE_SMA)  # type of averaging
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
min_rates_total = 0
min_rates_ = 0
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
ExtMapBuffer5 = Arr(0, 0.0)
ExtMapBuffer6 = Arr(0, 0.0)
ExtMapBuffer7 = Arr(0, 0.0)
ExtMapBuffer8 = Arr(0, 0.0)
nPeriod = 0
nStartFrom = 0
A = Arr(0, 0.0)
B = Arr(0, 0.0)
R = Arr(0, 0.0)
F = Arr(0, 0.0)
MA_Handle = 0

def IndicatorInit(Number, IndArray, DrawBegin, EmptyValue, Shift):
    SetIndexBuffer(Number, IndArray, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, EmptyValue)
    ArraySetAsSeries(IndArray, True)

def IndicatorsDrawBegin(DrawBegin):
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, DrawBegin)

def OnInit():
    global MA_Handle, min_rates_, min_rates_total, nPeriod, nStartFrom
    ShortName = 'Spectr'
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    MA_Handle = iMA(Symbol(), PERIOD_CURRENT, pm, 0, ma_method, applied_price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return
    nPeriod = _idiv(PeriodSeconds(iPeriod), 60)
    nStartFrom = _int(iStartFrom)
    min_rates_ = nStartFrom + nPeriod
    min_rates_total = _int(pm + min_rates_)
    IndicatorInit(0, ExtMapBuffer1, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(1, ExtMapBuffer2, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(2, ExtMapBuffer3, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(3, ExtMapBuffer4, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(4, ExtMapBuffer5, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(5, ExtMapBuffer6, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(6, ExtMapBuffer7, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(7, ExtMapBuffer8, min_rates_total, EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < (min_rates_total + begin):
        return 0
    Arr_ = Arr(0, 0.0)
    MA = Arr(0, 0.0)
    N = 0
    bar = 0
    to_copy = 0
    to_copy = min_rates_
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    ArraySetAsSeries(price, True)
    ArraySetAsSeries(MA, True)
    fLinearRegressionAll2(nStartFrom, nStartFrom + nPeriod - 1, Arr_, price)
    fFurie(Arr_, A, B, R, F)
    N = MathMax(ArraySize(Arr_), 2)
    IndicatorsDrawBegin(rates_total - N + 1)
    for i in range(0, N):
        bar = i + _int(iStartFrom)
        ExtMapBuffer1[bar] = MA[bar] + (((A[0] * MathSin(_fdiv(1 * 6.28 * i, N - 1))) + (B[0] * MathCos(_fdiv(1 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer2[bar] = MA[bar] + (((A[1] * MathSin(_fdiv(2 * 6.28 * i, N - 1))) + (B[1] * MathCos(_fdiv(2 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer3[bar] = MA[bar] + (((A[2] * MathSin(_fdiv(3 * 6.28 * i, N - 1))) + (B[2] * MathCos(_fdiv(3 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer4[bar] = MA[bar] + (((A[3] * MathSin(_fdiv(4 * 6.28 * i, N - 1))) + (B[3] * MathCos(_fdiv(4 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer5[bar] = MA[bar] + (((A[4] * MathSin(_fdiv(5 * 6.28 * i, N - 1))) + (B[4] * MathCos(_fdiv(5 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer6[bar] = MA[bar] + (((A[5] * MathSin(_fdiv(6 * 6.28 * i, N - 1))) + (B[5] * MathCos(_fdiv(6 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer7[bar] = MA[bar] + (((A[6] * MathSin(_fdiv(7 * 6.28 * i, N - 1))) + (B[6] * MathCos(_fdiv(7 * 6.28 * i, N - 1)))) * VV)
        ExtMapBuffer8[bar] = MA[bar] + (((A[7] * MathSin(_fdiv(8 * 6.28 * i, N - 1))) + (B[7] * MathCos(_fdiv(8 * 6.28 * i, N - 1)))) * VV)
    bar = 0
    for bar in range(bar, _int(iStartFrom)):
        ExtMapBuffer1[bar] = EMPTY_VALUE
        ExtMapBuffer2[bar] = EMPTY_VALUE
        ExtMapBuffer3[bar] = EMPTY_VALUE
        ExtMapBuffer4[bar] = EMPTY_VALUE
        ExtMapBuffer5[bar] = EMPTY_VALUE
        ExtMapBuffer6[bar] = EMPTY_VALUE
        ExtMapBuffer7[bar] = EMPTY_VALUE
        ExtMapBuffer8[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, _int(iStartFrom), 1)
    return rates_total

def fMyArcTan(aS, aC):
    if not aS:
        return 0.0
    if not aC:
        if aS > 0:
            return MathArctan(1) * 2
        elif aS < 0:
            return MathArctan(1) * 6
    else:
        if aS > 0:
            if aC > 0:
                return MathArctan(_fdiv(aS, aC))
            else:
                return MathArctan(_fdiv(aS, aC)) + (MathArctan(1) * 4)
        else:
            if aC > 0:
                return MathArctan(_fdiv(aS, aC)) + (MathArctan(1) * 8)
            else:
                return MathArctan(_fdiv(aS, aC)) + (MathArctan(1) * 4)
    return 0.0

def fFurie(aArr, aA, aB, aR, aF):
    tN = ArraySize(aArr)
    tM = MathMax(_idiv(tN, 2), 1)
    ArrayResize(aA, tM)
    ArrayResize(aB, tM)
    ArrayResize(aR, tM)
    ArrayResize(aF, tM)
    for ti in range(1, tM):
        aA[ti] = 0.0
        aB[ti] = 0.0
        for tj in range(0, tN):
            aA[ti] += aArr[tj] * MathSin(_fdiv(ti * 6.28 * tj, tN))
            aB[ti] += aArr[tj] * MathCos(_fdiv(ti * 6.28 * tj, tN))
        aA[ti] = _fdiv(2 * aA[ti], tN)
        aB[ti] = _fdiv(2 * aB[ti], tN)
        aR[ti] = MathSqrt(MathPow(aA[ti], 2) + MathPow(aB[ti], 2))
        aF[ti] = fMyArcTan(aB[ti], aA[ti])

def fLinearRegressionAll2(i0, i1, aArr, Price):
    aPeriod = 0
    rRetError = 0
    aVal_0 = 0.0
    aVal_1 = 0.0
    aB = 0.0
    aMaxDev = 0.0
    aStdError = 0.0
    aRSquared = 0.0
    x = 0.0
    y = 0.0
    y1 = 0.0
    y2 = 0.0
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    sumy2 = 0.0
    sumx22 = 0.0
    sumy22 = 0.0
    div1 = 0.0
    div2 = 0.0
    rRetError = 0
    aPeriod = i1 - i0 + 1
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    sumy2 = 0.0
    aB = 0.0
    aVal_0 = 0.0
    aVal_1 = 0.0
    for i in range(0, aPeriod):
        y = Price[i0 + i]
        x = i
        sumy += y
        sumxy += y * i
        sumx += x
        sumx2 += MathPow(x, 2)
        sumy2 += MathPow(y, 2)
    sumx22 = MathPow(sumx, 2)
    sumy22 = MathPow(sumy, 2)
    div1 = (sumx2 * aPeriod) - sumx22
    div2 = MathSqrt(((aPeriod * sumx2) - sumx22) * ((aPeriod * sumy2) - sumy22))
    if div1:
        aB = _fdiv((sumxy * aPeriod) - (sumx * sumy), div1)
        aVal_0 = _fdiv(sumy - (sumx * aB), aPeriod)
        aVal_1 = aVal_0 + (aB * (aPeriod - 1))
        rRetError += -1
    else:
        rRetError += -1
    aMaxDev = 0.0
    aStdError = 0.0
    for i in range(0, aPeriod):
        y1 = Price[i0 + i]
        y2 = aVal_0 + (aB * i)
        aMaxDev = MathMax(MathAbs(y1 - y2), aMaxDev)
        aStdError += MathPow(y1 - y2, 2)
    aStdError = MathSqrt(_fdiv(aStdError, aPeriod))
    if div2 != 0:
        aRSquared = MathPow(_fdiv((aPeriod * sumxy) - (sumx * sumy), div2), 2)
    else:
        rRetError += -2
    ArrayResize(aArr, aPeriod)
    for i in range(0, aPeriod):
        y = Price[i0 + i]
        x = aVal_0 + _fdiv(i * (aVal_1 - aVal_0), aPeriod)
        aArr[i] = y - x
    return rRetError


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spectr(_MQL5Indicator):
    name = 'spectr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'iPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # indicator time frame
        'iStartFrom': 0,  # Bar index for the calculation start
        'VV': 1,  # Wave height
        'pm': 20,  # Smoothing period to the calculation of moving average
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # type of averaging
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

