"""nonlagma_v1 — converted from MQL5: MQL5 Indicators/NonLagMA/nonlagma_v1.mq5

Copyright: Copyright © 2012, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 16760576, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'nonlagma_v1', 'source': 'MQL5 Indicators/NonLagMA/nonlagma_v1.mq5', 'folder': 'NonLagMA', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 9, 'label': 'Length in bars', 'sinput': False}, {'mql': 'PointFilter', 'py': 'PointFilter', 'param': 'PointFilter', 'type': 'double', 'default': 0.0, 'label': 'Filter in pips', 'sinput': False}, {'mql': 'PctFilter', 'py': 'PctFilter', 'param': 'PctFilter', 'type': 'double', 'default': 0.0, 'label': 'Dynamic Filter in decimal(ex.0.5)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Shift in bars', 'sinput': False}, {'mql': 'ColorMode', 'py': 'ColorMode', 'param': 'ColorMode', 'type': 'int', 'default': 0, 'label': 'Color Mode(0-off,1-on)', 'sinput': False}, {'mql': 'CountBars', 'py': 'CountBars', 'param': 'CountBars', 'type': 'int', 'default': 0, 'label': 'CountBars(0-full history)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', 0)
Price = _input('Price', PRICE_CLOSE)  # Apply to
Length = _input('Length', 9)  # Length in bars
PointFilter = _input('PointFilter', 0.0)  # Filter in pips
PctFilter = _input('PctFilter', 0.0)  # Dynamic Filter in decimal(ex.0.5)
Shift = _input('Shift', 0)  # Shift in bars
ColorMode = _input('ColorMode', 0)  # Color Mode(0-off,1-on)
CountBars = _input('CountBars', 0)  # CountBars(0-full history)
nlma = Arr(0, 0.0)
trend = Arr(0, 0.0)
tf = 0
Price_handle = 0
mtf_handle = 0
prevBars = 0
Len = 0
alpha = Arr(0, 0.0)
mtf_nlma = Arr(0, 0.0)
mtf_trend = Arr(1, 0.0, dyn=False)
price = Arr(0, 0.0)
Weight = 0.0
point = 0.0

def OnInit():
    global Len, Price_handle, Weight, mtf_handle, point, tf
    if TimeFrame <= Period():
        tf = Period()
    else:
        tf = TimeFrame
    SetIndexBuffer(0, nlma, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    SetIndexBuffer(1, trend, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'NonLagMA_v1[' + timeframeToString(TimeFrame) + '](' + priceToString(Price) + ',' + _str(Length) + ',' + _str(PointFilter) + ',' + _str(PctFilter) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, 'NonLagMA_v1[' + timeframeToString(TimeFrame) + ']')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 2)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    Price_handle = iMA(None, tf, 1, 0, 0, Price)
    if TimeFrame > 0:
        mtf_handle = iCustom(None, TimeFrame, 'NonLagMA_v1', 0, Price, Length, PointFilter, PctFilter, Shift, ColorMode, CountBars)
    else:
        t = 0.0
        coeff = 0.0
        g = 0.0
        phase = 0.0
        cycle = 4.0
        coeff = 3 * 3.1415926535
        phase = Length - 1
        Len = _int((Length * 4) + phase)
        ArrayResize(alpha, Len)
        Weight = 0.0
        for i in range(0, Len):
            if i <= (phase - 1):
                t = _fdiv(1.0 * i, phase - 1)
            else:
                t = 1.0 + _fdiv((i - phase + 1) * ((2 * cycle) - 1.0), (cycle * Length) - 1.0)
            if t <= 0.5:
                g = 1.0
            else:
                g = _fdiv(1, (coeff * t) + 1)
            alpha[i] = g * MathCos(3.1415926535 * t)
            Weight += alpha[i]
    point = Point() * MathPow(10, _imod(Digits(), 2))
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Len)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    x = 0
    y = 0
    shift = 0
    limit = 0
    mtflimit = 0
    copied = 0
    filter_ = 0.0
    sumDel = 0.0
    avgDel = 0.0
    sumPow = 0.0
    stdDev = 0.0
    mtf_time = 0
    if prev_calculated == 0:
        limit = 0
        mtflimit = rates_total - 1
        ArrayInitialize(nlma, EMPTY_VALUE)
    else:
        limit = rates_total - 1
        mtflimit = _idiv(PeriodSeconds(tf), PeriodSeconds(Period()))
    copied = CopyBuffer(Price_handle, 0, _DT(Time[rates_total - 1]), _DT(Time[0]), price)
    if copied < 0:
        Print('not all prices copied. Will try on next tick Error =', GetLastError(), ', copied =', copied)
        return 0
    if tf > Period():
        ArraySetAsSeries(Time, True)
        shift = 0
        y = 0
        while shift < mtflimit:
            if Time[shift] < iTime_u("", TimeFrame, y):
                y += 1
            mtf_time = iTime_u("", TimeFrame, y)
            copied = CopyBuffer(mtf_handle, 0, _DT(mtf_time), _DT(mtf_time), mtf_nlma)
            if copied <= 0:
                return 0
            x = rates_total - shift - 1
            nlma[x] = mtf_nlma[0]
            if ColorMode > 0:
                copied = CopyBuffer(mtf_handle, 1, _DT(mtf_time), _DT(mtf_time), mtf_trend)
                trend[x] = mtf_trend[0]
            else:
                trend[x] = 0.0
            shift += 1
    else:
        shift = limit
        for shift in range(shift, rates_total):
            if (CountBars > 0 and shift < (rates_total - CountBars)) or shift < Len:
                continue
            sum_ = price[shift] * alpha[0]
            i = 1
            for i in range(i, Len):
                sum_ += price[shift - i] * alpha[i]
            else:
                i = _range_end(i, Len, 1)
            if Weight > 0:
                nlma[shift] = _fdiv(sum_, Weight)
            if PctFilter > 0 and ((CountBars > 0 and shift < (rates_total - CountBars + Len + Length)) or (CountBars == 0 and shift < (Len + Length))):
                continue
            if PctFilter > 0 and nlma[shift - 1] > 0:
                sumDel = MathAbs(nlma[shift] - nlma[shift - 1])
                i = 1
                for i in range(i, Length):
                    sumDel += MathAbs(nlma[shift - i] - nlma[shift - i - 1])
                else:
                    i = _range_end(i, Length, 1)
                avgDel = sumDel / Length
                sumPow = MathPow(MathAbs(nlma[shift] - nlma[shift - 1]) - avgDel, 2)
                i = 1
                for i in range(i, Length):
                    sumPow += MathPow(MathAbs(nlma[shift - i] - nlma[shift - i - 1]) - avgDel, 2)
                else:
                    i = _range_end(i, Length, 1)
                stdDev = MathSqrt(sumPow / Length)
                filter_ = PctFilter * stdDev
            elif PointFilter > 0:
                filter_ = PointFilter * point
            else:
                filter_ = 0.0
            if MathAbs(nlma[shift] - nlma[shift - 1]) < filter_:
                nlma[shift] = nlma[shift - 1]
            if shift > 0:
                if ColorMode > 0 and nlma[shift - 1] > 0:
                    trend[shift] = trend[shift - 1]
                    if nlma[shift] > nlma[shift - 1]:
                        trend[shift] = 1.0
                    if nlma[shift] < nlma[shift - 1]:
                        trend[shift] = 2.0
                else:
                    trend[shift] = 0.0
        else:
            shift = _range_end(shift, rates_total, 1)
    return rates_total

def timeframeToString(TF):
    _sw1 = TF
    if _sw1 == PERIOD_CURRENT:
        return 'Current'
    elif _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M2:
        return 'M2'
    elif _sw1 == PERIOD_M3:
        return 'M3'
    elif _sw1 == PERIOD_M4:
        return 'M4'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M6:
        return 'M6'
    elif _sw1 == PERIOD_M10:
        return 'M10'
    elif _sw1 == PERIOD_M12:
        return 'M12'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M20:
        return 'M20'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H2:
        return 'H2'
    elif _sw1 == PERIOD_H3:
        return 'H3'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_H6:
        return 'H6'
    elif _sw1 == PERIOD_H8:
        return 'H8'
    elif _sw1 == PERIOD_H12:
        return 'H12'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'

def priceToString(app_price):
    _sw2 = app_price
    if _sw2 == PRICE_CLOSE:
        return 'Close'
    elif _sw2 == PRICE_HIGH:
        return 'High'
    elif _sw2 == PRICE_LOW:
        return 'Low'
    elif _sw2 == PRICE_MEDIAN:
        return 'Median'
    elif _sw2 == PRICE_OPEN:
        return 'Open'
    elif _sw2 == PRICE_TYPICAL:
        return 'Typical'
    elif _sw2 == PRICE_WEIGHTED:
        return 'Weighted'
    else:
        return ''

def iTime_u(symbol, TF, index):
    if index < 0:
        return -1
    if CopyTime(symbol, TF, index, 1, _s_iTime_timearray) > 0:
        return _s_iTime_timearray[0]
    else:
        return -1

# ---- static local variables
_s_iTime_timearray = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonlagmaV1(_MQL5Indicator):
    name = 'nonlagma_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'Length': 9,  # Length in bars
        'PointFilter': 0.0,  # Filter in pips
        'PctFilter': 0.0,  # Dynamic Filter in decimal(ex.0.5)
        'Shift': 0,  # Shift in bars
        'ColorMode': 0,  # Color Mode(0-off,1-on)
        'CountBars': 0,  # CountBars(0-full history)
    }

