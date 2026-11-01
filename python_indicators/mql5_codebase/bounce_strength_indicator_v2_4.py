"""bounce_strength_indicator_v2.4 — converted from MQL5: MQL5 Indicators/BSI Trend Indicator/bounce_strength_indicator_v2.4.mq5

Copyright: Copyright 2015, fxborg; Link: http://fxborg-labo.hateblo.jp/; Version: 2.4

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2015, fxborg', 'link': 'http://fxborg-labo.hateblo.jp/', 'version': '2.4', 'indicator_buffers': 20, 'indicator_plots': 3, 'window': 'separate'}, 'types': {1: 0, 2: 10, 3: 1}, 'colors': {1: [6908265], 2: [55295, 16748574, 9639167], 3: [3329330]}, 'widths': {1: 1, 2: 3, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {2: 'BSI Main', 3: 'BSI Slow'}, 'levels': [], 'description': [], 'name': 'bounce_strength_indicator_v2.4', 'source': 'MQL5 Indicators/BSI Trend Indicator/bounce_strength_indicator_v2.4.mq5', 'folder': 'BSI Trend Indicator', 'inputs': [{'mql': 'InpScaleFactor', 'py': 'InpScaleFactor', 'param': 'InpScaleFactor', 'type': 'double', 'default': 0.75, 'label': 'Scale factor', 'sinput': False}, {'mql': 'InpMaPeriod', 'py': 'InpMaPeriod', 'param': 'InpMaPeriod', 'type': 'int', 'default': 3, 'label': 'Smooth Period', 'sinput': False}, {'mql': 'InpVolatilityPeriod', 'py': 'InpVolatilityPeriod', 'param': 'InpVolatilityPeriod', 'type': 'int', 'default': 55, 'label': 'Volatility Period', 'sinput': False}, {'mql': 'InpBSIPeriod', 'py': 'InpBSIPeriod', 'param': 'InpBSIPeriod', 'type': 'int', 'default': 5, 'label': 'BSI_CalcBars', 'sinput': False}, {'mql': 'InpFastPeriod', 'py': 'InpFastPeriod', 'param': 'InpFastPeriod', 'type': 'int', 'default': 10, 'label': 'Fast Period', 'sinput': False}, {'mql': 'InpSlowPeriod', 'py': 'InpSlowPeriod', 'param': 'InpSlowPeriod', 'type': 'int', 'default': 7, 'label': 'Slow Period', 'sinput': False}, {'mql': 'InpUsingVolumeWeight', 'py': 'InpUsingVolumeWeight', 'param': 'InpUsingVolumeWeight', 'type': 'bool', 'default': True, 'label': 'Using TickVolume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpScaleFactor = _input('InpScaleFactor', 0.75)  # Scale factor
InpMaPeriod = _input('InpMaPeriod', 3)  # Smooth Period
InpVolatilityPeriod = _input('InpVolatilityPeriod', 55)  # Volatility Period
InpBSIPeriod = _input('InpBSIPeriod', 5)  # BSI_CalcBars
InpFastPeriod = _input('InpFastPeriod', 10)  # Fast Period
InpSlowPeriod = _input('InpSlowPeriod', 7)  # Slow Period
InpUsingVolumeWeight = _input('InpUsingVolumeWeight', True)  # Using TickVolume
StdDevPeriod = _idiv(InpVolatilityPeriod, 7)  # Fast Period
InpMaMethod = MODE_SMMA  # Ma Method
UpperBuffer = Arr(0, 0.0)
MedianBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
TrendBuffer = Arr(0, 0.0)
UpperMaBuffer = Arr(0, 0.0)
MedianMaBuffer = Arr(0, 0.0)
LowerMaBuffer = Arr(0, 0.0)
MainBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
MainColor_Buffer = Arr(0, 0.0)
TrendColor_Buffer = Arr(0, 0.0)
PosBuffer = Arr(0, 0.0)
NegBuffer = Arr(0, 0.0)
BaseBuffer = Arr(0, 0.0)
VolBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
StdDevBuffer = Arr(0, 0.0)
StdDevCalcBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = StdDevPeriod + InpVolatilityPeriod + InpMaPeriod + InpMaPeriod + InpSlowPeriod + InpBSIPeriod + MathMax(InpFastPeriod, InpSlowPeriod)
    SetIndexBuffer(0, SigBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, MainColor_Buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, TrendBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, TrendColor_Buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, PosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, NegBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, MedianMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, BaseBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, UpperMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, LowerMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, UpperBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, MedianBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, LowerBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, HighBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, LowBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, CloseBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, StdDevBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, StdDevCalcBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(19, VolBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(11, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(12, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(13, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(14, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(15, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(16, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(17, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(18, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(19, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'BSI v2.4'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    j = 0
    first = 0
    if rates_total <= (min_rates_total + 3):
        return 0
    MathSrand(_int(TimeLocal()))
    first = StdDevPeriod
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    else:
        i = 0
        for i in range(i, first):
            MedianBuffer[i] = close[i]
            HighBuffer[i] = high[i]
            LowBuffer[i] = low[i]
        else:
            i = _range_end(i, first, 1)
    i = first
    for i in range(i, rates_total):
        StdDevBuffer[i] = calcStdDev(close, StdDevPeriod, i)
        second = StdDevPeriod + InpVolatilityPeriod
        if i <= second:
            continue
        volsum = 0
        sd = 0.0
        j = i - InpVolatilityPeriod + 1
        for j in range(j, i + 1):
            sd += StdDevBuffer[j]
            if InpUsingVolumeWeight:
                volsum += tick_volume[j]
        else:
            j = _range_end(j, i + 1, 1)
        if InpUsingVolumeWeight:
            VolBuffer[i] = float(volsum) / InpVolatilityPeriod
        v = sd / InpVolatilityPeriod
        BaseBuffer[i] = v
        third = second + InpMaPeriod + InpMaPeriod
        if i <= third:
            continue
        StepChannel(high, low, close, InpScaleFactor, InpMaPeriod, v, i, HighBuffer, LowBuffer, CloseBuffer, UpperBuffer, LowerBuffer, MedianBuffer, UpperMaBuffer, LowerMaBuffer, MedianMaBuffer)
        fourth = third + InpBSIPeriod
        if i <= fourth:
            continue
        SigBuffer[i] = calc_BSI(high, low, close, tick_volume, i)
        fifth = fourth + InpFastPeriod
        if i <= fifth:
            continue
        sigsum = 0.0
        j = 0
        for j in range(j, InpFastPeriod):
            sigsum += SigBuffer[i - j]
        else:
            j = _range_end(j, InpFastPeriod, 1)
        MainBuffer[i] = sigsum / InpFastPeriod
        sixes = fourth + InpSlowPeriod
        if i <= sixes:
            continue
        mainsum = 0.0
        j = 0
        for j in range(j, InpSlowPeriod):
            mainsum += MainBuffer[i - j]
        else:
            j = _range_end(j, InpSlowPeriod, 1)
        TrendBuffer[i] = mainsum / InpSlowPeriod
        if TrendBuffer[i] > 0:
            TrendColor_Buffer[i] = 1.0
        elif TrendBuffer[i] < 0:
            TrendColor_Buffer[i] = 2.0
        else:
            TrendColor_Buffer[i] = 0.0
        if 0 < MainBuffer[i] and TrendBuffer[i] < MainBuffer[i]:
            MainColor_Buffer[i] = 1.0
        elif 0 > MainBuffer[i] and TrendBuffer[i] > MainBuffer[i]:
            MainColor_Buffer[i] = 2.0
        else:
            MainColor_Buffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def calcStdDev(close, span, i):
    if i < (span - 1):
        return 0.0
    if i == (span - 1):
        StdDevCalcBuffer[i] = SimpleMA(i, span, close)
    else:
        StdDevCalcBuffer[i] = SmoothedMA(i, span, StdDevCalcBuffer[i - 1], close)
    sum_ = 0.0
    for j in range(0, span):
        sum_ += MathPow(close[i - j] - StdDevCalcBuffer[i], 2)
    return MathSqrt(_fdiv(sum_, span))

def calcMaxVol(tick_volume, span, i):
    if i < (span - 1):
        return 0
    volmax = 0
    for j in range(0, span):
        if volmax < tick_volume[i - j]:
            volmax = tick_volume[i - j]
    return volmax

def calc_BSI(high, low, close, tick_volume, i):
    if i <= min_rates_total:
        return 0.0
    if MedianMaBuffer[i - InpBSIPeriod + 1] == 0:
        return 0.0
    sumpos2 = 0.0
    sumneg2 = 0.0
    sumpos = 0.0
    sumneg = 0.0
    sumhigh = 0.0
    sumpvol = 0.0
    sumnvol = 0.0
    sum_ = 0.0
    for k in range(i - InpBSIPeriod + 1, i + 1):
        vol = 1.0
        if InpUsingVolumeWeight and VolBuffer[k] > 0:
            if tick_volume[k] > 0:
                vol = MathMin(1.0, MathSqrt(_fdiv(tick_volume[k], VolBuffer[k])))
            elif tick_volume[k - 1] > 0 and tick_volume[k] == 0:
                vol = MathMin(1.0, MathSqrt(_fdiv(tick_volume[k - 1], VolBuffer[k - 1])))
        range_ = _fdiv(UpperMaBuffer[i] - LowerMaBuffer[i], Point())
        sp = high[k] - low[k]
        if not ((close[k - 1] - (sp * 0.2)) > close[k]):
            ratio = _fdiv(GompertzRatio(_fdiv(MedianMaBuffer[k] - low[k], Point()), range_), range_)
            sumpos += (close[k] - low[k]) * ratio * vol
            sumpos2 += close[k] - low[k]
        if not ((close[k - 1] + (sp * 0.2)) < close[k]):
            ratio = _fdiv(GompertzRatio(_fdiv(high[k] - MedianMaBuffer[k], Point()), range_), range_)
            sumneg += (high[k] - close[k]) * ratio * vol
            sumneg2 += high[k] - close[k]
    tmppos = 0.0
    tmpneg = 0.0
    tmppos = sumpos
    tmpneg = sumneg
    PosBuffer[i] = tmppos
    NegBuffer[i] = -tmpneg
    if (tmppos + tmpneg) != 0:
        return (tmppos - tmpneg) * MathAbs(_fdiv(tmppos - tmpneg, tmppos + tmpneg))
    return 0.0

def GompertzRatio(x, a):
    if a == 0.0 or x == 0.0:
        return 0.0
    b = 0.15
    c = 0.99
    y = 0.0
    y = a * MathExp((-b) * MathPow(c, x))
    return y

def StepChannel(high, low, close, scale_factor, ma_period, volatility, i, high_buffer, low_buffer, close_buffer, upper_buffer, lower_buffer, median_buffer, upper_ma_buffer, lower_ma_buffer, median_ma_buffer):
    j = 0
    h = 0.0
    l = 0.0
    c = 0.0
    hsum = 0.0
    lsum = 0.0
    csum = 0.0
    j = 0
    for j in range(j, ma_period):
        hsum += high[i - j]
        lsum += low[i - j]
        csum += close[i - j]
    else:
        j = _range_end(j, ma_period, 1)
    h = _fdiv(hsum, ma_period)
    l = _fdiv(lsum, ma_period)
    c = _fdiv(csum, ma_period)
    base = volatility * scale_factor
    if (h - base) > high_buffer[i - 1]:
        high_buffer[i] = h
    elif (h + base) < high_buffer[i - 1]:
        high_buffer[i] = h + base
    else:
        high_buffer[i] = high_buffer[i - 1]
    if (l + base) < low_buffer[i - 1]:
        low_buffer[i] = l
    elif (l - base) > low_buffer[i - 1]:
        low_buffer[i] = l - base
    else:
        low_buffer[i] = low_buffer[i - 1]
    if (c - (base / 2)) > close_buffer[i - 1]:
        close_buffer[i] = c - (base / 2)
    elif (c + (base / 2)) < close_buffer[i - 1]:
        close_buffer[i] = c + (base / 2)
    else:
        close_buffer[i] = close_buffer[i - 1]
    upper_buffer[i] = high_buffer[i] + (base / 2)
    lower_buffer[i] = low_buffer[i] - (base / 2)
    median_buffer[i] = (high_buffer[i] + low_buffer[i] + (close_buffer[i] * 2)) / 4
    hsum = 0.0
    lsum = 0.0
    csum = 0.0
    j = 0
    for j in range(j, ma_period):
        hsum += upper_buffer[i - j]
        lsum += lower_buffer[i - j]
        csum += median_buffer[i - j]
    else:
        j = _range_end(j, ma_period, 1)
    upper_ma_buffer[i] = _fdiv(hsum, ma_period)
    lower_ma_buffer[i] = _fdiv(lsum, ma_period)
    median_ma_buffer[i] = _fdiv(csum, ma_period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BounceStrengthIndicatorV24(_MQL5Indicator):
    name = 'bounce_strength_indicator_v2.4'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpScaleFactor': 0.75,  # Scale factor
        'InpMaPeriod': 3,  # Smooth Period
        'InpVolatilityPeriod': 55,  # Volatility Period
        'InpBSIPeriod': 5,  # BSI_CalcBars
        'InpFastPeriod': 10,  # Fast Period
        'InpSlowPeriod': 7,  # Slow Period
        'InpUsingVolumeWeight': True,  # Using TickVolume
    }

