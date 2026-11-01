"""spectrometr_separate — converted from MQL5: MQL5 Indicators/Spectrometr_Separate/spectrometr_separate.mq5

Copyright: Copyright © 2009, Yuriy Tokman; Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [42495], 3: [65535], 4: [65280], 5: [16711680], 6: [16748574], 7: [13828244], 8: [6908265]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'Wave 1', 2: 'Wave 2', 3: 'Wave 3', 4: 'Wave 4', 5: 'Wave 5', 6: 'Wave 6', 7: 'Wave 7', 8: 'Wave 8'}, 'levels': [], 'description': [], 'name': 'spectrometr_separate', 'source': 'MQL5 Indicators/Spectrometr_Separate/spectrometr_separate.mq5', 'folder': 'Spectrometr_Separate', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'int', 'default': 16388, 'label': 'indicator time frame', 'sinput': False}, {'mql': 'iStartFrom', 'py': 'iStartFrom', 'param': 'iStartFrom', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AddToObjName', 'py': 'AddToObjName', 'param': None, 'type': 'string', 'default': '1', 'label': '', 'sinput': False}, {'mql': 'HandlerColor', 'py': 'HandlerColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': '', 'sinput': False}, {'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 14822282, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', PERIOD_H4)  # indicator time frame
iStartFrom = _input('iStartFrom', 0)
AddToObjName = _input('AddToObjName', '1')
HandlerColor = _input('HandlerColor', clrGray)
TextColor = _input('TextColor', clrBlueViolet)
min_rates_total = 0
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
ExtMapBuffer5 = Arr(0, 0.0)
ExtMapBuffer6 = Arr(0, 0.0)
ExtMapBuffer7 = Arr(0, 0.0)
ExtMapBuffer8 = Arr(0, 0.0)
LastLeftBar = 0
LastRightBar = 0
ObjNPref = ""
ShortName = ""
Wind = 0
nPeriod = 0
nStartFrom = 0
A = Arr(0, 0.0)
B = Arr(0, 0.0)
R = Arr(0, 0.0)
F = Arr(0, 0.0)

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
    global ObjNPref, ShortName, Wind, min_rates_total, nPeriod, nStartFrom
    ShortName = 'Spectrometr' + '_' + AddToObjName
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    ObjNPref = ShortName + '_'
    nStartFrom = iStartFrom
    min_rates_total = nStartFrom + nPeriod - 1
    Wind = ChartWindowFind(0, ShortName)
    nPeriod = _idiv(PeriodSeconds(iPeriod), 60)
    IndicatorInit(0, ExtMapBuffer1, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(1, ExtMapBuffer2, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(2, ExtMapBuffer3, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(3, ExtMapBuffer4, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(4, ExtMapBuffer5, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(5, ExtMapBuffer6, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(6, ExtMapBuffer7, min_rates_total, EMPTY_VALUE, 0)
    IndicatorInit(7, ExtMapBuffer8, min_rates_total, EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjDeleteByPrefix(ObjNPref)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global LastLeftBar, LastRightBar
    if rates_total < (min_rates_total + begin):
        return 0
    Time0 = Arr(1, 0, dyn=False)
    TimeL = Arr(1, 0, dyn=False)
    TimeR = Arr(1, 0, dyn=False)
    ObjName = ""
    Arr_ = Arr(0, 0.0)
    N = 0
    bar = 0
    Per60 = 0
    ArraySetAsSeries(price, True)
    if CopyTime(Symbol(), PERIOD_CURRENT, 0, 1, Time0) <= 0:
        return 0
    ObjName = ObjNPref + 'Null line'
    LastLeftBar = nStartFrom + nPeriod - 1
    LastRightBar = nStartFrom
    if CopyTime(Symbol(), PERIOD_CURRENT, LastLeftBar, 1, TimeL) <= 0:
        return 0
    if CopyTime(Symbol(), PERIOD_CURRENT, LastRightBar, 1, TimeR) <= 0:
        return 0
    SetTline(0, ObjName, Wind, TimeR[0], 0.0, TimeL[0], 0.0, HandlerColor, STYLE_SOLID, 1, True)
    fLinearRegressionAll2(nStartFrom, nStartFrom + nPeriod - 1, Arr_, price)
    fFurie(Arr_, A, B, R, F)
    N = MathMax(ArraySize(Arr_), 2)
    IndicatorsDrawBegin(rates_total - N + 1)
    for i in range(0, N):
        bar = i + iStartFrom
        ExtMapBuffer1[bar] = (A[0] * MathSin(_fdiv(1 * 6.28 * i, N - 1))) + (B[0] * MathCos(_fdiv(1 * 6.28 * i, N - 1)))
        ExtMapBuffer2[bar] = (A[1] * MathSin(_fdiv(2 * 6.28 * i, N - 1))) + (B[1] * MathCos(_fdiv(2 * 6.28 * i, N - 1)))
        ExtMapBuffer3[bar] = (A[2] * MathSin(_fdiv(3 * 6.28 * i, N - 1))) + (B[2] * MathCos(_fdiv(3 * 6.28 * i, N - 1)))
        ExtMapBuffer4[bar] = (A[3] * MathSin(_fdiv(4 * 6.28 * i, N - 1))) + (B[3] * MathCos(_fdiv(4 * 6.28 * i, N - 1)))
        ExtMapBuffer5[bar] = (A[4] * MathSin(_fdiv(5 * 6.28 * i, N - 1))) + (B[4] * MathCos(_fdiv(5 * 6.28 * i, N - 1)))
        ExtMapBuffer6[bar] = (A[5] * MathSin(_fdiv(6 * 6.28 * i, N - 1))) + (B[5] * MathCos(_fdiv(6 * 6.28 * i, N - 1)))
        ExtMapBuffer7[bar] = (A[6] * MathSin(_fdiv(7 * 6.28 * i, N - 1))) + (B[6] * MathCos(_fdiv(7 * 6.28 * i, N - 1)))
        ExtMapBuffer8[bar] = (A[7] * MathSin(_fdiv(8 * 6.28 * i, N - 1))) + (B[7] * MathCos(_fdiv(8 * 6.28 * i, N - 1)))
    bar = 0
    for bar in range(bar, iStartFrom):
        ExtMapBuffer1[bar] = EMPTY_VALUE
        ExtMapBuffer2[bar] = EMPTY_VALUE
        ExtMapBuffer3[bar] = EMPTY_VALUE
        ExtMapBuffer4[bar] = EMPTY_VALUE
        ExtMapBuffer5[bar] = EMPTY_VALUE
        ExtMapBuffer6[bar] = EMPTY_VALUE
        ExtMapBuffer7[bar] = EMPTY_VALUE
        ExtMapBuffer8[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, iStartFrom, 1)
    Per60 = PeriodSeconds()
    timeX1 = Time0[0] + (Per60 * 3)
    Color1 = _uint(PlotIndexGetInteger(1, PLOT_LINE_COLOR, 0))
    timeX2 = Time0[0] + (Per60 * 5)
    Color2 = _uint(PlotIndexGetInteger(2, PLOT_LINE_COLOR, 0))
    timeX3 = Time0[0] + (Per60 * 7)
    Color3 = _uint(PlotIndexGetInteger(3, PLOT_LINE_COLOR, 0))
    timeX4 = Time0[0] + (Per60 * 9)
    Color4 = _uint(PlotIndexGetInteger(4, PLOT_LINE_COLOR, 0))
    timeX5 = Time0[0] + (Per60 * 11)
    Color5 = _uint(PlotIndexGetInteger(5, PLOT_LINE_COLOR, 0))
    timeX6 = Time0[0] + (Per60 * 13)
    Color6 = _uint(PlotIndexGetInteger(6, PLOT_LINE_COLOR, 0))
    timeX7 = Time0[0] + (Per60 * 15)
    Color7 = _uint(PlotIndexGetInteger(7, PLOT_LINE_COLOR, 0))
    timeX8 = Time0[0] + (Per60 * 17)
    Color8 = _uint(PlotIndexGetInteger(8, PLOT_LINE_COLOR, 0))
    SetTline(0, ObjNPref + '1', Wind, timeX1, R[1], timeX1, -R[1], Color1, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '2', Wind, timeX2, R[2], timeX2, -R[2], Color2, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '3', Wind, timeX3, R[3], timeX3, -R[3], Color3, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '4', Wind, timeX4, R[4], timeX4, -R[4], Color4, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '5', Wind, timeX5, R[5], timeX5, -R[5], Color5, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '6', Wind, timeX6, R[6], timeX6, -R[6], Color6, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '7', Wind, timeX7, R[7], timeX7, -R[7], Color7, STYLE_SOLID, 8, False)
    SetTline(0, ObjNPref + '8', Wind, timeX8, R[8], timeX8, -R[8], Color8, STYLE_SOLID, 8, False)
    return rates_total

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, back):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, back)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, back):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, back)
    else:
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_BACK, back)

def ObjDeleteByPrefix(aPrefix):
    for i in range(ObjectsTotal(0, Wind) - 1, 0 - 1, -1):
        if StringFind(ObjectName(0, i, Wind, -1), aPrefix, 0) == 0:
            ObjectDelete(0, ObjectName(0, i, Wind, -1))

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


class SpectrometrSeparate(_MQL5Indicator):
    name = 'spectrometr_separate'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'iPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # indicator time frame
        'iStartFrom': 0,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

