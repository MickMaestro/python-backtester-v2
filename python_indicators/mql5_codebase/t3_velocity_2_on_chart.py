"""t3_velocity_2_on_chart — converted from MQL5: MQL5 Indicators/T3 Velocity on Chart/t3_velocity_2_on_chart.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 16, 2: 8}, 'colors': {1: [16760576, 8894686, 4294967295], 2: [3329330, 6333684, 12632256]}, 'widths': {1: 2, 2: 2}, 'styles': {2: 0}, 'labels': {1: 'T3 velocity', 2: 'T3 velocity'}, 'levels': [], 'description': [], 'name': 't3_velocity_2_on_chart', 'source': 'MQL5 Indicators/T3 Velocity on Chart/t3_velocity_2_on_chart.mq5', 'folder': 'T3 Velocity on Chart', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 32.0, 'label': 'T3 velocity calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'ColorNorm', 'py': 'ColorNorm', 'param': 'ColorNorm', 'type': 'int', 'default': 20, 'label': 'Colors normalization period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 6333684, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 20, 'label': 'Color steps for drawing', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 0, 'label': 'Style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
pr_haclose = 10
pr_haopen = 11
pr_hahigh = 12
pr_halow = 13
pr_hamedian = 14
pr_hatypical = 15
pr_haweighted = 16
pr_haaverage = 17
pr_hamedianb = 18
pr_hatbiased = 19
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_haclose', 11: 'pr_haopen', 12: 'pr_hahigh', 13: 'pr_halow', 14: 'pr_hamedian', 15: 'pr_hatypical', 16: 'pr_haweighted', 17: 'pr_haaverage', 18: 'pr_hamedianb', 19: 'pr_hatbiased'})

# enum enStyles
st_automatic = 0
st_bars = 1
st_candles = 2
st_line = 3
_enum('enStyles', {0: 'st_automatic', 1: 'st_bars', 2: 'st_candles', 3: 'st_line'})

# ---- inputs and global variables
T3Period = _input('T3Period', 32.0)  # T3 velocity calculation period
T3Hot = _input('T3Hot', 0.7)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
Price = _input('Price', pr_close)  # Price to use
ColorNorm = _input('ColorNorm', 20)  # Colors normalization period
ColorFrom = _input('ColorFrom', clrSandyBrown)  # Color down
ColorTo = _input('ColorTo', clrDeepSkyBlue)  # Color Up
ColorSteps = _input('ColorSteps', 20)  # Color steps for drawing
Style = _input('Style', st_automatic)  # Style
vel = Arr(0, 0.0)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
baro = Arr(0, 0.0)
barc = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
line = Arr(0, 0.0)
cololBuffer = Arr(0, 0.0)
cSteps = 0
workT3 = Arr(0, 0.0, dims=(12,))
workT3Coeffs = Arr(0, 0.0, dims=(12,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, line, INDICATOR_DATA)
    SetIndexBuffer(6, cololBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, vel, INDICATOR_CALCULATIONS)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_styleInUse, _s_OnCalculate_styleToUse
    calculated = prev_calculated
    style = _int(ChartGetInteger(0, CHART_MODE, 0))
    if (not _s_OnCalculate_styleSetUp) or (Style == st_automatic and _s_OnCalculate_styleInUse != style):
        if Style == st_automatic:
            _sw1 = style
            if _sw1 == CHART_BARS:
                _s_OnCalculate_styleToUse = DRAW_COLOR_BARS
            elif _sw1 == CHART_CANDLES:
                _s_OnCalculate_styleToUse = DRAW_COLOR_CANDLES
            elif _sw1 == CHART_LINE:
                _s_OnCalculate_styleToUse = DRAW_COLOR_LINE
        else:
            _sw2 = Style
            if _sw2 == st_bars:
                _s_OnCalculate_styleToUse = DRAW_COLOR_BARS
            elif _sw2 == st_candles:
                _s_OnCalculate_styleToUse = DRAW_COLOR_CANDLES
            elif _sw2 == st_line:
                _s_OnCalculate_styleToUse = DRAW_COLOR_LINE
        _s_OnCalculate_styleInUse = style
        if _s_OnCalculate_styleToUse == DRAW_COLOR_LINE:
            PlotIndexSetInteger(1, PLOT_DRAW_TYPE, _s_OnCalculate_styleToUse)
        else:
            PlotIndexSetInteger(0, PLOT_DRAW_TYPE, _s_OnCalculate_styleToUse)
        calculated = 0
    for i in range(MathMax(calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        vel[i] = iT3(price, T3Period, T3Hot, T3Original, i, rates_total, 0) - iT3(price, T3Period, T3Hot / 2.0, T3Original, i, rates_total, 1)
        line[i] = EMPTY_VALUE
        baro[i] = EMPTY_VALUE
        barc[i] = EMPTY_VALUE
        barh[i] = EMPTY_VALUE
        barl[i] = EMPTY_VALUE
        if _s_OnCalculate_styleToUse == DRAW_COLOR_LINE:
            line[i] = close[i]
        else:
            baro[i] = open[i]
            barc[i] = close[i]
            barh[i] = high[i]
            barl[i] = low[i]
        min_ = vel[i]
        max_ = vel[i]
        sto = 50.0
        k = 1
        while k < ColorNorm and (i - k) >= 0:
            min_ = MathMin(min_, vel[i - k])
            max_ = MathMax(max_, vel[i - k])
            k += 1
        if max_ != min_:
            sto = _fdiv(100 * (vel[i] - min_), max_ - min_)
        cololBuffer[i] = MathFloor((sto * cSteps) / 100.0)
        colorBuffer[i] = MathFloor((sto * cSteps) / 100.0)
    return rates_total

def iT3(price, period, hot, original, r, bars, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        a = hot
        workT3Coeffs[instanceNo][1] = (-a) * a * a
        workT3Coeffs[instanceNo][2] = (3 * a * a) + (3 * a * a * a)
        workT3Coeffs[instanceNo][3] = (-6 * a * a) - (3 * a) - (3 * a * a * a)
        workT3Coeffs[instanceNo][4] = 1 + (3 * a) + (a * a * a) + (3 * a * a)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    if r == 0:
        workT3[r][0 + buffer] = price
        workT3[r][1 + buffer] = price
        workT3[r][2 + buffer] = price
        workT3[r][3 + buffer] = price
        workT3[r][4 + buffer] = price
        workT3[r][5 + buffer] = price
    else:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])

def getPrice(price, open, close, high, low, i, bars, instanceNo=0):
    if price >= pr_haclose:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
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
        _sw3 = price
        if _sw3 == pr_haclose:
            return haClose
        elif _sw3 == pr_haopen:
            return haOpen
        elif _sw3 == pr_hahigh:
            return haHigh
        elif _sw3 == pr_halow:
            return haLow
        elif _sw3 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw3 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw3 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw3 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw3 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw3 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
    _sw4 = price
    if _sw4 == pr_close:
        return close[i]
    elif _sw4 == pr_open:
        return open[i]
    elif _sw4 == pr_high:
        return high[i]
    elif _sw4 == pr_low:
        return low[i]
    elif _sw4 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw4 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw4 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw4 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw4 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw4 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
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

# ---- static local variables
_s_OnCalculate_styleSetUp = False
_s_OnCalculate_styleInUse = -1
_s_OnCalculate_styleToUse = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3Velocity2OnChart(_MQL5Indicator):
    name = 't3_velocity_2_on_chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3Period': 32.0,  # T3 velocity calculation period
        'T3Hot': 0.7,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
        'ColorNorm': 20,  # Colors normalization period
        'ColorSteps': 20,  # Color steps for drawing
        'Style': _Choice({0: 'automatically adjust style', 1: 'view as bars', 2: 'view as candles', 3: 'view as line'}, default=0),  # Style
    }

