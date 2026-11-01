"""bsi_trend_indicator_v1.1 — converted from MQL5: MQL5 Indicators/BSI Trend Indicator/bsi_trend_indicator_v1.1.mq5

Copyright: Copyright 2015, fxborg; Link: http://fxborg-labo.hateblo.jp/; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2015, fxborg', 'link': 'http://fxborg-labo.hateblo.jp/', 'version': '1.1', 'indicator_buffers': 30, 'indicator_plots': 3, 'window': 'chart'}, 'types': {1: 0, 2: 0, 3: 8}, 'colors': {1: [2139610], 2: [255], 3: [9639167, 12695295, 6908265, 16436871, 16748574]}, 'widths': {1: 2, 2: 2, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'bsi_trend_indicator_v1.1', 'source': 'MQL5 Indicators/BSI Trend Indicator/bsi_trend_indicator_v1.1.mq5', 'folder': 'BSI Trend Indicator', 'inputs': [{'mql': 'InpBSIPeriod', 'py': 'InpBSIPeriod', 'param': 'InpBSIPeriod', 'type': 'int', 'default': 5, 'label': 'BSI_CalcBars', 'sinput': False}, {'mql': 'InpFastPeriod', 'py': 'InpFastPeriod', 'param': 'InpFastPeriod', 'type': 'int', 'default': 10, 'label': 'Fast Period', 'sinput': False}, {'mql': 'InpSlowPeriod', 'py': 'InpSlowPeriod', 'param': 'InpSlowPeriod', 'type': 'int', 'default': 7, 'label': 'Slow Period', 'sinput': False}, {'mql': 'InpUsingVolumeWeight', 'py': 'InpUsingVolumeWeight', 'param': 'InpUsingVolumeWeight', 'type': 'bool', 'default': True, 'label': 'Using TickVolume', 'sinput': False}, {'mql': 'InpLwMaPeriod', 'py': 'InpLwMaPeriod', 'param': 'InpLwMaPeriod', 'type': 'int', 'default': 30, 'label': 'LWMA Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpBSIPeriod = _input('InpBSIPeriod', 5)  # BSI_CalcBars
InpFastPeriod = _input('InpFastPeriod', 10)  # Fast Period
InpSlowPeriod = _input('InpSlowPeriod', 7)  # Slow Period
InpUsingVolumeWeight = _input('InpUsingVolumeWeight', True)  # Using TickVolume
InpLwMaPeriod = _input('InpLwMaPeriod', 30)  # LWMA Period
SmoothPeriod = 3  # Smooth Period
ScaleFactor = 0.75  # Scale factor
VolatilityPeriod = 55  # Volatility Period
Slow_ScaleFactor = 2.25  # Scale factor
Slow_VolatilityPeriod = 70  # Volatility Period
InpMaMethod = MODE_SMMA  # Ma Method
SlowBuffer = Arr(0, 0.0)
LwMaBuffer = Arr(0, 0.0)
MainBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
MainColor_Buffer = Arr(0, 0.0)
SlowColor_Buffer = Arr(0, 0.0)
PriceBuffer = Arr(0, 0.0)
VolBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
StdDevBuffer = Arr(0, 0.0)
StdDevCalcBuffer = Arr(0, 0.0)
Slow_HighBuffer = Arr(0, 0.0)
Slow_LowBuffer = Arr(0, 0.0)
Slow_CloseBuffer = Arr(0, 0.0)
Slow_StdDevBuffer = Arr(0, 0.0)
Slow_StdDevCalcBuffer = Arr(0, 0.0)
MedianBuffer = Arr(0, 0.0)
MedianMaBuffer = Arr(0, 0.0)
Slow_MedianBuffer = Arr(0, 0.0)
Slow_MedianMaBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
LowerMaBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
UpperMaBuffer = Arr(0, 0.0)
Slow_LowerBuffer = Arr(0, 0.0)
Slow_LowerMaBuffer = Arr(0, 0.0)
Slow_UpperBuffer = Arr(0, 0.0)
Slow_UpperMaBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = Slow_StdDevPeriod + Slow_VolatilityPeriod + SmoothPeriod + SmoothPeriod + InpSlowPeriod + InpBSIPeriod + MathMax(InpFastPeriod, InpSlowPeriod)
    idx = 0
    SetIndexBuffer(((idx := idx + 1) - 1), MedianMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_MedianMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(((idx := idx + 1) - 1), MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(((idx := idx + 1) - 1), MainColor_Buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(((idx := idx + 1) - 1), SlowBuffer, INDICATOR_DATA)
    SetIndexBuffer(((idx := idx + 1) - 1), SlowColor_Buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(((idx := idx + 1) - 1), SigBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), PriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), LwMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), MedianBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), HighBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), LowBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), CloseBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), StdDevBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), StdDevCalcBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), VolBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), UpperBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), LowerBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), UpperMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), LowerMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_HighBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_LowBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_CloseBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_StdDevBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_StdDevCalcBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_MedianBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_UpperBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_LowerBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_UpperMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((idx := idx + 1) - 1), Slow_LowerMaBuffer, INDICATOR_CALCULATIONS)
    idx = 0
    for idx in range(idx, 30):
        PlotIndexSetDouble(idx, PLOT_EMPTY_VALUE, 0)
    else:
        idx = _range_end(idx, 30, 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'BSI Trend v1.1'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    j = 0
    first = 0
    if rates_total <= (min_rates_total + 3):
        return 0
    MathSrand(_int(TimeLocal()))
    first = Slow_StdDevPeriod
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
        PriceBuffer[i] = (high[i] + low[i] + close[i]) / 3
        StdDevBuffer[i] = calcStdDev(StdDevCalcBuffer, close, StdDevPeriod, i)
        Slow_StdDevBuffer[i] = calcStdDev(Slow_StdDevCalcBuffer, close, Slow_StdDevPeriod, i)
        second = Slow_StdDevPeriod + Slow_VolatilityPeriod
        if i <= second:
            continue
        volsum = 0
        sd = 0.0
        slow_sd = 0.0
        j = i - Slow_VolatilityPeriod + 1
        for j in range(j, i + 1):
            slow_sd += StdDevBuffer[j]
            if j <= (i - VolatilityPeriod + 1):
                sd += StdDevBuffer[j]
                if InpUsingVolumeWeight:
                    volsum += tick_volume[j]
        else:
            j = _range_end(j, i + 1, 1)
        if InpUsingVolumeWeight:
            VolBuffer[i] = _fdiv(float(volsum), VolatilityPeriod)
        v = _fdiv(sd, VolatilityPeriod)
        slow_v = _fdiv(slow_sd, Slow_VolatilityPeriod)
        third = second + SmoothPeriod + SmoothPeriod
        if i <= third:
            continue
        StepChannel(high, low, close, ScaleFactor, SmoothPeriod, v, i, HighBuffer, LowBuffer, CloseBuffer, UpperBuffer, LowerBuffer, MedianBuffer, UpperMaBuffer, LowerMaBuffer, MedianMaBuffer)
        StepChannel(high, low, close, Slow_ScaleFactor, SmoothPeriod, slow_v, i, Slow_HighBuffer, Slow_LowBuffer, Slow_CloseBuffer, Slow_UpperBuffer, Slow_LowerBuffer, Slow_MedianBuffer, Slow_UpperMaBuffer, Slow_LowerMaBuffer, Slow_MedianMaBuffer)
        LwMaBuffer[i] = LinearWeightedMA(i, InpLwMaPeriod, PriceBuffer)
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
        MainBuffer[i] = LwMaBuffer[i] + (sigsum / InpFastPeriod)
        sixes = fourth + InpSlowPeriod
        if i <= sixes:
            continue
        mainsum = 0.0
        j = 0
        for j in range(j, InpSlowPeriod):
            mainsum += MainBuffer[i - j]
        else:
            j = _range_end(j, InpSlowPeriod, 1)
        SlowBuffer[i] = mainsum / InpSlowPeriod
        if MathMax(LwMaBuffer[i - 1], LwMaBuffer[i]) < MainBuffer[i] and MainBuffer[i - 1] < MainBuffer[i]:
            if MainColor_Buffer[i - 1] == 4.0 or (MainColor_Buffer[i - 1] != 0.0 and (Slow_MedianMaBuffer[i - 3] * 1.0001) < Slow_MedianMaBuffer[i]):
                MainColor_Buffer[i] = 4.0
            else:
                MainColor_Buffer[i] = 3.0
        elif MathMin(LwMaBuffer[i - 1], LwMaBuffer[i]) > MainBuffer[i] and MainBuffer[i - 1] > MainBuffer[i]:
            if MainColor_Buffer[i - 1] == 0.0 or (MainColor_Buffer[i - 1] != 4.0 and (Slow_MedianMaBuffer[i - 3] * 0.9999) > Slow_MedianMaBuffer[i]):
                MainColor_Buffer[i] = 0.0
            else:
                MainColor_Buffer[i] = 1.0
        else:
            MainColor_Buffer[i] = 2.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def calcStdDev(calc_buffer, close, span, i):
    if i < (span - 1):
        return 0.0
    if i == (span - 1):
        calc_buffer[i] = SimpleMA(i, span, close)
    else:
        calc_buffer[i] = SmoothedMA(i, span, calc_buffer[i - 1], close)
    sum_ = 0.0
    for j in range(0, span):
        sum_ += MathPow(close[i - j] - calc_buffer[i], 2)
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

# ---- global variables initialised from expressions
StdDevPeriod = _idiv(VolatilityPeriod, 7)  # Fast Period
Slow_StdDevPeriod = _idiv(Slow_VolatilityPeriod, 7)  # Fast Period


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BsiTrendIndicatorV11(_MQL5Indicator):
    name = 'bsi_trend_indicator_v1.1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpBSIPeriod': 5,  # BSI_CalcBars
        'InpFastPeriod': 10,  # Fast Period
        'InpSlowPeriod': 7,  # Slow Period
        'InpUsingVolumeWeight': True,  # Using TickVolume
        'InpLwMaPeriod': 30,  # LWMA Period
    }

