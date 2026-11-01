"""normalized_macd — converted from MQL5: MQL5 Indicators/Normalized MACD/normalized_macd.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MACD'}, 'levels': [], 'description': [], 'name': 'normalized_macd', 'source': 'MQL5 Indicators/Normalized MACD/normalized_macd.mq5', 'folder': 'Normalized MACD', 'inputs': [{'mql': 'FastEma', 'py': 'FastEma', 'param': 'FastEma', 'type': 'int', 'default': 24, 'label': 'Fast ema', 'sinput': False}, {'mql': 'SlowEma', 'py': 'SlowEma', 'param': 'SlowEma', 'type': 'int', 'default': 52, 'label': 'Slow ema', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 4, 'label': 'Price to use', 'sinput': False}, {'mql': 'NormPeriod', 'py': 'NormPeriod', 'param': 'NormPeriod', 'type': 'int', 'default': 14, 'label': 'Normalization period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 50, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_haclose = 8
pr_haopen = 9
pr_hahigh = 10
pr_halow = 11
pr_hamedian = 12
pr_hatypical = 13
pr_haweighted = 14
pr_haaverage = 15
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_haclose', 9: 'pr_haopen', 10: 'pr_hahigh', 11: 'pr_halow', 12: 'pr_hamedian', 13: 'pr_hatypical', 14: 'pr_haweighted', 15: 'pr_haaverage'})

# ---- inputs and global variables
FastEma = _input('FastEma', 24)  # Fast ema
SlowEma = _input('SlowEma', 52)  # Slow ema
Price = _input('Price', pr_median)  # Price to use
NormPeriod = _input('NormPeriod', 14)  # Normalization period
ColorFrom = _input('ColorFrom', clrOrange)  # Color down
ColorTo = _input('ColorTo', clrLime)  # Color Up
ColorSteps = _input('ColorSteps', 50)  # Color steps for drawing
macd = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
cSteps = 0
totalBars = 0
workHa = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))
workRsi = Arr(0, 0.0, dims=(3,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, macd, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    IndicatorSetString(INDICATOR_SHORTNAME, ' normalized MACD (' + _str(FastEma) + ',' + _str(SlowEma) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global totalBars
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        macd[i] = iRsi(iEma(price, FastEma, i, 0) - iEma(price, SlowEma, i, 1), NormPeriod, rates_total, i)
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            min_ = macd[i]
            max_ = macd[i]
            col = 0.0
            k = 1
            while k < ColorSteps and (i - k) >= 0:
                min_ = (macd[i - k] if (macd[i - k] < min_) else min_)
                max_ = (macd[i - k] if (macd[i - k] > max_) else max_)
                k += 1
            if (max_ - min_) == 0:
                col = 50.0
            else:
                col = _fdiv(100 * (macd[i] - min_), max_ - min_)
            colorBuffer[i] = MathFloor((col * cSteps) / 100.0)
    return rates_total

def getPrice(price, open, close, high, low, i, bars):
    if price >= pr_haclose and price <= pr_haaverage:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][2] + workHa[i - 1][3]) / 2.0
        else:
            haOpen = open[i] + close[i]
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        _sw1 = price
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
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
    _sw2 = price
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
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    return 0.0

def iEma(price, period, r, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iRsi(price, period, bars, i, forInstance=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = forInstance * 3
    alpha = _fdiv(1.0, period)
    workRsi[i][0 + z] = price
    if i < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (i - k - 1) >= 0:
            sum_ += MathAbs(workRsi[i - k][0 + z] - workRsi[i - k - 1][0 + z])
            k += 1
        workRsi[i][1 + z] = _fdiv(workRsi[i][0 + z] - workRsi[0][0 + z], MathMax(k, 1))
        workRsi[i][2 + z] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[i][0 + z] - workRsi[i - 1][0 + z]
        workRsi[i][1 + z] = workRsi[i - 1][1 + z] + (alpha * (change - workRsi[i - 1][1 + z]))
        workRsi[i][2 + z] = workRsi[i - 1][2 + z] + (alpha * (MathAbs(change) - workRsi[i - 1][2 + z]))
    if workRsi[i][2 + z] != 0:
        return 50.0 * (_fdiv(workRsi[i][1 + z], workRsi[i][2 + z]) + 1)
    else:
        return 0.0

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedMacd(_MQL5Indicator):
    name = 'normalized_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'FastEma': 24,  # Fast ema
        'SlowEma': 52,  # Slow ema
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4', 8: 'Heiken ashi close', 9: 'Heiken ashi open', 10: 'Heiken ashi high', 11: 'Heiken ashi low', 12: 'Heiken ashi median', 13: 'Heiken ashi typical', 14: 'Heiken ashi weighted', 15: 'Heiken ashi average'}, default=4),  # Price to use
        'NormPeriod': 14,  # Normalization period
        'ColorSteps': 50,  # Color steps for drawing
    }

