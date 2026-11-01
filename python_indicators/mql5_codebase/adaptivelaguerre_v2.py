"""adaptivelaguerre_v2 — converted from MQL5: MQL5 Indicators/Adaptive Laguerre Filter/adaptivelaguerre_v2.mq5

Copyright: Copyright © 2012, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 16760576, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'adaptivelaguerre_v2', 'source': 'MQL5 Indicators/Adaptive Laguerre Filter/adaptivelaguerre_v2.mq5', 'folder': 'Adaptive Laguerre Filter', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Length', 'sinput': False}, {'mql': 'Order', 'py': 'Order', 'param': 'Order', 'type': 'int', 'default': 4, 'label': 'Laguerre Filter Order', 'sinput': False}, {'mql': 'AdaptiveMode', 'py': 'AdaptiveMode', 'param': 'AdaptiveMode', 'type': 'int', 'default': 1, 'label': 'Adaptive Mode:0-off,1-on', 'sinput': False}, {'mql': 'AdaptiveSmooth', 'py': 'AdaptiveSmooth', 'param': 'AdaptiveSmooth', 'type': 'int', 'default': 5, 'label': 'Adaptive Factor Smoothing Period', 'sinput': False}, {'mql': 'AdaptiveSmoothMode', 'py': 'AdaptiveSmoothMode', 'param': 'AdaptiveSmoothMode', 'type': 'int', 'default': 4, 'label': 'Adaptive Factor Smoothing Mode', 'sinput': False}, {'mql': 'ColorMode', 'py': 'ColorMode', 'param': 'ColorMode', 'type': 'int', 'default': 1, 'label': 'Color Mode(0-off,1-on)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_SMOOTH_MODE
sma = 0
ema = 1
wilder = 2
lwma = 3
median = 4
_enum('ENUM_SMOOTH_MODE', {0: 'sma', 1: 'ema', 2: 'wilder', 3: 'lwma', 4: 'median'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', 0)
Price = _input('Price', PRICE_CLOSE)  # Apply to
Length = _input('Length', 10)  # Length
Order = _input('Order', 4)  # Laguerre Filter Order
AdaptiveMode = _input('AdaptiveMode', 1)  # Adaptive Mode:0-off,1-on
AdaptiveSmooth = _input('AdaptiveSmooth', 5)  # Adaptive Factor Smoothing Period
AdaptiveSmoothMode = _input('AdaptiveSmoothMode', 4)  # Adaptive Factor Smoothing Mode
ColorMode = _input('ColorMode', 1)  # Color Mode(0-off,1-on)
laguerre = Arr(0, 0.0)
trend = Arr(0, 0.0)
price = Arr(0, 0.0)
diff = Arr(0, 0.0)
gamma = Arr(0, 0.0)
tf = 0
mtf_handle = 0
Price_handle = 0
L = Arr(0, 0.0, dims=(2,))
mtf_laguerre = Arr(1, 0.0, dyn=False)
mtf_trend = Arr(1, 0.0, dyn=False)
ema = Arr(2, 0.0, dyn=False)
prevtime = 0
ptime = 0
ftime = True

def OnInit():
    global Price_handle, mtf_handle, tf
    if TimeFrame <= Period():
        tf = Period()
    else:
        tf = TimeFrame
    SetIndexBuffer(0, laguerre, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    SetIndexBuffer(1, trend, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, price, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, diff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, gamma, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Length + 1)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'AdaptiveLaguerre_v2[' + timeframeToString(TimeFrame) + '](' + priceToString(Price) + ',' + _str(Length) + ',' + _str(Order) + ',' + _str(AdaptiveMode) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, 'AdaptiveLaguerre_v2[' + timeframeToString(TimeFrame) + ']')
    Price_handle = iMA(None, TimeFrame, 1, 0, 0, Price)
    if TimeFrame > 0:
        mtf_handle = iCustom(None, TimeFrame, 'AdaptiveLaguerre_v2', 0, Price, Length, Order, AdaptiveMode, AdaptiveSmooth, AdaptiveSmoothMode, ColorMode)
    else:
        ArrayResize(L, Order)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    x = 0
    y = 0
    shift = 0
    limit = 0
    mtflimit = 0
    copied = 0
    sgamma = 0.0
    mtf_time = 0
    if prev_calculated == 0:
        limit = 0
        mtflimit = rates_total - 1
        ArrayInitialize(laguerre, EMPTY_VALUE)
    else:
        limit = rates_total - 1
        mtflimit = rates_total - prev_calculated + _idiv(PeriodSeconds(tf), PeriodSeconds(Period()))
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
            copied = CopyBuffer(mtf_handle, 0, _DT(mtf_time), _DT(mtf_time), mtf_laguerre)
            if copied <= 0:
                return 0
            x = rates_total - shift - 1
            laguerre[x] = mtf_laguerre[0]
            if ColorMode > 0:
                copied = CopyBuffer(mtf_handle, 1, _DT(mtf_time), _DT(mtf_time), mtf_trend)
                if copied <= 0:
                    return 0
                trend[x] = mtf_trend[0]
            else:
                trend[x] = 0.0
            shift += 1
    else:
        shift = limit
        for shift in range(shift, rates_total):
            if shift < Length:
                continue
            diff[shift] = MathAbs(price[shift] - laguerre[shift - 1])
            if shift < (2 * Length):
                continue
            if AdaptiveMode > 0:
                gamma[shift] = AdaptiveGamma(diff, Length, shift)
                _sw1 = AdaptiveSmoothMode
                if _sw1 == 1:
                    sgamma = EMA(gamma[shift], AdaptiveSmooth, Time[shift], shift)
                elif _sw1 == 2:
                    sgamma = EMA(gamma[shift], (2 * AdaptiveSmooth) - 1, Time[shift], shift)
                elif _sw1 == 3:
                    sgamma = LWMA(gamma, AdaptiveSmooth, shift)
                elif _sw1 == 4:
                    sgamma = Median(gamma, AdaptiveSmooth, shift)
                else:
                    sgamma = SMA(gamma, AdaptiveSmooth, shift)
            else:
                sgamma = 10.0 / (Length + 9)
            laguerre[shift] = Laguerre(price[shift], sgamma, Order, Time[shift], shift)
            if shift < (Length + 2):
                continue
            if shift > 0:
                if ColorMode > 0 and laguerre[shift - 1] > 0:
                    trend[shift] = trend[shift - 1]
                    if laguerre[shift] > laguerre[shift - 1]:
                        trend[shift] = 1.0
                    if laguerre[shift] < laguerre[shift - 1]:
                        trend[shift] = 2.0
                else:
                    trend[shift] = 0.0
        else:
            shift = _range_end(shift, rates_total, 1)
    return rates_total

def Laguerre(_price, _gamma, order, time, bar):
    global prevtime
    gam = 1 - _gamma
    array = Arr(0, 0.0)
    ArrayResize(array, order)
    if time != prevtime:
        for i in range(0, order):
            L[i][1] = L[i][0]
        prevtime = time
    for i in range(0, order):
        if bar <= order:
            L[i][0] = _price
        else:
            if i == 0:
                L[i][0] = ((1 - gam) * _price) + (gam * L[i][1])
            else:
                L[i][0] = ((-gam) * L[i - 1][0]) + L[i - 1][1] + (gam * L[i][1])
            array[i] = L[i][0]
    return TriMA_gen(array, order, order - 1)

def SMA(array, per, bar):
    Sum = 0.0
    for i in range(0, per):
        Sum += array[bar - i]
    return _fdiv(Sum, per)

def EMA(_price, per, time, bar):
    global ftime, ptime
    if ptime != time:
        ema[1] = ema[0]
        ptime = time
    if ftime:
        ema[0] = _price
        ftime = False
    else:
        ema[0] = ema[1] + (_fdiv(2.0, 1 + per) * (_price - ema[1]))
    return ema[0]

def LWMA(array, per, bar):
    lwma_ = 0.0
    Sum = 0.0
    Weight = 0.0
    for i in range(0, per):
        Weight += per - i
        Sum += array[bar - i] * (per - i)
    if Weight > 0:
        lwma_ = _fdiv(Sum, Weight)
    else:
        lwma_ = 0.0
    return lwma_

def TriMA_gen(array, per, bar):
    len1 = _int(MathFloor((per + 1) * 0.5))
    len2 = _int(MathCeil((per + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len2):
        sum_ += SMA(array, len1, bar - i)
    trimagen = _fdiv(sum_, len2)
    return trimagen

def Median(_price, per, bar):
    median_ = 0.0
    array = Arr(0, 0.0)
    ArrayResize(array, per)
    for i in range(0, per):
        array[i] = _price[bar - i]
    ArraySort(array)
    num = _int(MathRound(_idiv(per - 1, 2)))
    if MathMod(per, 2) > 0:
        median_ = array[num]
    else:
        median_ = 0.5 * (array[num] + array[num + 1])
    return median_

def AdaptiveGamma(array, per, bar):
    eff = 0.0
    sum_ = 0.0
    max_ = 0.0
    min_ = 1000000000.0
    for i in range(0, per):
        if array[bar - i] > max_:
            max_ = array[bar - i]
        if array[bar - i] < min_:
            min_ = array[bar - i]
    if (max_ - min_) != 0:
        eff = _fdiv(array[bar] - min_, max_ - min_)
    else:
        eff = 0.0
    return eff

def timeframeToString(TF):
    _sw2 = TF
    if _sw2 == PERIOD_CURRENT:
        return 'Current'
    elif _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M2:
        return 'M2'
    elif _sw2 == PERIOD_M3:
        return 'M3'
    elif _sw2 == PERIOD_M4:
        return 'M4'
    elif _sw2 == PERIOD_M5:
        return 'M5'
    elif _sw2 == PERIOD_M6:
        return 'M6'
    elif _sw2 == PERIOD_M10:
        return 'M10'
    elif _sw2 == PERIOD_M12:
        return 'M12'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M20:
        return 'M20'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H2:
        return 'H2'
    elif _sw2 == PERIOD_H3:
        return 'H3'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_H6:
        return 'H6'
    elif _sw2 == PERIOD_H8:
        return 'H8'
    elif _sw2 == PERIOD_H12:
        return 'H12'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'

def priceToString(app_price):
    _sw3 = app_price
    if _sw3 == PRICE_CLOSE:
        return 'Close'
    elif _sw3 == PRICE_HIGH:
        return 'High'
    elif _sw3 == PRICE_LOW:
        return 'Low'
    elif _sw3 == PRICE_MEDIAN:
        return 'Median'
    elif _sw3 == PRICE_OPEN:
        return 'Open'
    elif _sw3 == PRICE_TYPICAL:
        return 'Typical'
    elif _sw3 == PRICE_WEIGHTED:
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


class AdaptivelaguerreV2(_MQL5Indicator):
    name = 'adaptivelaguerre_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'Length': 10,  # Length
        'Order': 4,  # Laguerre Filter Order
        'AdaptiveMode': 1,  # Adaptive Mode:0-off,1-on
        'AdaptiveSmooth': 5,  # Adaptive Factor Smoothing Period
        'AdaptiveSmoothMode': _Choice({0: 'SMA', 1: 'EMA', 2: 'Wilder', 3: 'LWMA', 4: 'Median'}, default=4),  # Adaptive Factor Smoothing Mode
        'ColorMode': 1,  # Color Mode(0-off,1-on)
    }

