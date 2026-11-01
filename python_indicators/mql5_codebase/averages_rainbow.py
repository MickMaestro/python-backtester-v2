"""Averages_rainbow — converted from MQL5: MQL5 Indicators/Averages rainbow/Averages_rainbow.mq5

Copyright: © mladen, 2017, mladenfx@gmail.com; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017, mladenfx@gmail.com', 'link': 'www.forex-station.com', 'window': 'chart', 'indicator_buffers': 512, 'indicator_plots': 256}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Averages_rainbow', 'source': 'MQL5 Indicators/Averages rainbow/Averages_rainbow.mq5', 'folder': 'Averages rainbow', 'inputs': [{'mql': 'AvgMethod', 'py': 'AvgMethod', 'param': 'AvgMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'AvgAverages', 'py': 'AvgAverages', 'param': 'AvgAverages', 'type': 'int', 'default': 50, 'label': 'Averages No.', 'sinput': False}, {'mql': 'AvgPeriodStart', 'py': 'AvgPeriodStart', 'param': 'AvgPeriodStart', 'type': 'int', 'default': 10, 'label': 'Starting average period', 'sinput': False}, {'mql': 'AvgStep', 'py': 'AvgStep', 'param': 'AvgStep', 'type': 'int', 'default': 2, 'label': 'Step to increase consecutive averages', 'sinput': False}, {'mql': 'AvgPrice', 'py': 'AvgPrice', 'param': 'AvgPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'ColorUp', 'py': 'ColorUp', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color for slope up', 'sinput': False}, {'mql': 'ColorDn', 'py': 'ColorDn', 'param': None, 'type': 'color', 'default': 6333684, 'label': 'Color for slope down', 'sinput': False}, {'mql': 'LinesWidth', 'py': 'LinesWidth', 'param': 'LinesWidth', 'type': 'int', 'default': 0, 'label': 'Averages lines width', 'sinput': False}, {'mql': 'LinesStyle', 'py': 'LinesStyle', 'param': 'LinesStyle', 'type': 'int', 'default': 0, 'label': 'Averages lines style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AvgMethod = _input('AvgMethod', ma_ema)  # Average method
AvgAverages = _input('AvgAverages', 50)  # Averages No.
AvgPeriodStart = _input('AvgPeriodStart', 10)  # Starting average period
AvgStep = _input('AvgStep', 2)  # Step to increase consecutive averages
AvgPrice = _input('AvgPrice', pr_close)  # Price
ColorUp = _input('ColorUp', clrDeepSkyBlue)  # Color for slope up
ColorDn = _input('ColorDn', clrSandyBrown)  # Color for slope down
LinesWidth = _input('LinesWidth', 0)  # Averages lines width
LinesStyle = _input('LinesStyle', STYLE_SOLID)  # Averages lines style
totalAvgs = 0
workSma = Arr(0, 0.0, dims=(256,))
workEma = Arr(0, 0.0, dims=(256,))
workSmma = Arr(0, 0.0, dims=(256,))
workLwma = Arr(0, 0.0, dims=(256,))
workHa = Arr(0, 0.0, dims=(4,))

class simpleBuff(MqlObject):
    _q_fields = ('buffer', 'bufferColor')
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)
        self.bufferColor = Arr(0, 0.0)

def OnInit():
    global totalAvgs
    totalAvgs = MathMax(MathMin(AvgAverages, 256), 1)
    for i in range(0, totalAvgs):
        SetIndexBuffer(i * 2, wbuffer[i].buffer, INDICATOR_DATA)
        SetIndexBuffer((i * 2) + 1, wbuffer[i].bufferColor, INDICATOR_COLOR_INDEX)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
        PlotIndexSetInteger(i, PLOT_COLOR_INDEXES, 2)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, 0, ColorUp)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, 1, ColorDn)
        PlotIndexSetInteger(i, PLOT_LINE_WIDTH, LinesWidth)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, LinesStyle)
        PlotIndexSetString(i, PLOT_LABEL, 'Average (' + _str(AvgPeriodStart + (AvgStep * i)) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(AvgPrice, open, close, high, low, i, rates_total)
        k = 0
        while k < totalAvgs:
            wbuffer[k].buffer[i] = iCustomMa(AvgMethod, price, AvgPeriodStart + (k * AvgStep), i, rates_total, k)
            wbuffer[k].bufferColor[i] = ((0 if (wbuffer[k].buffer[i] > wbuffer[k].buffer[i - 1]) else 1 if (wbuffer[k].buffer[i] < wbuffer[k].buffer[i - 1]) else wbuffer[k].bufferColor[i - 1]) if (i > 0) else 0)
            k += 1
        i += 1
    return i

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    k = 1
    workSma[r][instanceNo + 0] = price
    avg = price
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    avg = _fdiv(avg, float(k))
    return avg

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
    if period < 1:
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
        _sw2 = tprice
        if _sw2 == pr_haclose:
            return haClose
        elif _sw2 == pr_haopen:
            return haOpen
        elif _sw2 == pr_hahigh:
            return haHigh
        elif _sw2 == pr_halow:
            return haLow
        elif _sw2 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw2 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw2 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw2 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw2 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw2 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw2 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw3 = tprice
    if _sw3 == pr_close:
        return close[i]
    elif _sw3 == pr_open:
        return open[i]
    elif _sw3 == pr_high:
        return high[i]
    elif _sw3 == pr_low:
        return low[i]
    elif _sw3 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw3 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw3 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw3 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw3 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

# ---- global variables initialised from expressions
wbuffer = Arr(256, 0, dyn=False, factory=simpleBuff)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragesRainbow(_MQL5Indicator):
    name = 'Averages_rainbow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'AvgMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Average method
        'AvgAverages': 50,  # Averages No.
        'AvgPeriodStart': 10,  # Starting average period
        'AvgStep': 2,  # Step to increase consecutive averages
        'AvgPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'LinesWidth': 0,  # Averages lines width
        'LinesStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Averages lines style
    }

