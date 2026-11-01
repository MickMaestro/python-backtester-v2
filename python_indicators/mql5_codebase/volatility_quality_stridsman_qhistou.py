"""Volatility_quality_Stridsman_qhistou — converted from MQL5: MQL5 Indicators/Volatility Quality Stridsman (histo)/Volatility_quality_Stridsman_qhistou.mq5

Copyright: © mladen, 2017; Link: mladenfx@gmail.com www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'mladenfx@gmail.com www.forex-station.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'vq histogram'}, 'levels': [], 'description': [], 'name': 'Volatility_quality_Stridsman_qhistou', 'source': 'MQL5 Indicators/Volatility Quality Stridsman (histo)/Volatility_quality_Stridsman_qhistou.mq5', 'folder': 'Volatility Quality Stridsman (histo)', 'inputs': [{'mql': 'PriceSmoothing', 'py': 'PriceSmoothing', 'param': 'PriceSmoothing', 'type': 'int', 'default': 5, 'label': 'Price smoothing period', 'sinput': False}, {'mql': 'PriceSmoothingMethod', 'py': 'PriceSmoothingMethod', 'param': 'PriceSmoothingMethod', 'type': 'int', 'default': 3, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'FilterInPips', 'py': 'FilterInPips', 'param': 'FilterInPips', 'type': 'double', 'default': 2.0, 'label': 'Filter (in pips)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_medianb = 8
pr_tbiased = 9
pr_tbiased2 = 10
pr_haclose = 11
pr_haopen = 12
pr_hahigh = 13
pr_halow = 14
pr_hamedian = 15
pr_hatypical = 16
pr_haweighted = 17
pr_haaverage = 18
pr_hamedianb = 19
pr_hatbiased = 20
pr_hatbiased2 = 21
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_tbiased2', 11: 'pr_haclose', 12: 'pr_haopen', 13: 'pr_hahigh', 14: 'pr_halow', 15: 'pr_hamedian', 16: 'pr_hatypical', 17: 'pr_haweighted', 18: 'pr_haaverage', 19: 'pr_hamedianb', 20: 'pr_hatbiased', 21: 'pr_hatbiased2'})

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
PriceSmoothing = _input('PriceSmoothing', 5)  # Price smoothing period
PriceSmoothingMethod = _input('PriceSmoothingMethod', ma_lwma)  # Price smoothing method
FilterInPips = _input('FilterInPips', 2.0)  # Filter (in pips)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
histo = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))
workSma = Arr(0, 0.0, dims=(5,))
workEma = Arr(0, 0.0, dims=(5,))
workSmma = Arr(0, 0.0, dims=(5,))
workLwma = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, histo, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility quality Stridsman (' + _str(PriceSmoothing) + ')')
    return 0

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    pipMultiplier = MathPow(10, _imod(Digits(), 2))
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        cHigh = iCustomMa(PriceSmoothingMethod, high[i], PriceSmoothing, i, rates_total, 0)
        cLow = iCustomMa(PriceSmoothingMethod, low[i], PriceSmoothing, i, rates_total, 1)
        cOpen = iCustomMa(PriceSmoothingMethod, open[i], PriceSmoothing, i, rates_total, 2)
        cClose = iCustomMa(PriceSmoothingMethod, close[i], PriceSmoothing, i, rates_total, 3)
        pClose = (iCustomMa(PriceSmoothingMethod, close[i - 1], PriceSmoothing, i, rates_total, 4) if (i > 0) else cClose)
        trueRange = MathMax(cHigh, pClose) - MathMin(cLow, pClose)
        range_ = cHigh - cLow
        vqi = (((_fdiv(cClose - pClose, trueRange) + _fdiv(cClose - cOpen, range_)) * 0.5) if (range_ != 0 and trueRange != 0) else val[i - 1] if (i > 0) else 0)
        val[i] = ((val[i - 1] + (MathAbs(vqi) * (cClose - pClose + cClose - cOpen) * 0.5)) if (i > 0) else 0)
        if FilterInPips > 0 and i > 0:
            if MathAbs(val[i] - val[i - 1]) < (FilterInPips * pipMultiplier * Point()):
                val[i] = val[i - 1]
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        histo[i] = 1.0
    return rates_total

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
        instanceNo *= 4
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][instanceNo + 2] + workHa[i - 1][instanceNo + 3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][instanceNo + 0] = haLow
            workHa[i][instanceNo + 1] = haHigh
        else:
            workHa[i][instanceNo + 0] = haHigh
            workHa[i][instanceNo + 1] = haLow
        workHa[i][instanceNo + 2] = haOpen
        workHa[i][instanceNo + 3] = haClose
        _sw1 = tprice
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw1 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw1 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw2 = tprice
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw2 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw2 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw3 = mode
    if _sw3 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw3 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    k = 0
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, k)

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period <= 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityQualityStridsmanQhistou(_MQL5Indicator):
    name = 'Volatility_quality_Stridsman_qhistou'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PriceSmoothing': 5,  # Price smoothing period
        'PriceSmoothingMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Price smoothing method
        'FilterInPips': 2.0,  # Filter (in pips)
    }
    y_range = (0.0, 1.0)

