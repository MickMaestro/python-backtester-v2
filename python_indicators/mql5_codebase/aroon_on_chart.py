"""aroon_on_chart — converted from MQL5: MQL5 Indicators/Aroon on chart/aroon_on_chart.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 16, 2: 8}, 'colors': {1: [16760576, 8894686], 2: [3329330, 9662683]}, 'widths': {1: 2, 2: 2}, 'styles': {2: 0}, 'labels': {1: 'Aroon trend', 2: 'Aroon trend'}, 'levels': [], 'description': [], 'name': 'aroon_on_chart', 'source': 'MQL5 Indicators/Aroon on chart/aroon_on_chart.mq5', 'folder': 'Aroon on chart', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 25, 'label': 'calculation period', 'sinput': False}, {'mql': 'PriceHigh', 'py': 'PriceHigh', 'param': 'PriceHigh', 'type': 'int', 'default': 2, 'label': 'Price to use for high', 'sinput': False}, {'mql': 'PriceLow', 'py': 'PriceLow', 'param': 'PriceLow', 'type': 'int', 'default': 3, 'label': 'Price to use for low', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 0, 'label': 'Style', 'sinput': False}, {'mql': 'ColorUp', 'py': 'ColorUp', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Up color', 'sinput': False}, {'mql': 'ColorDown', 'py': 'ColorDown', 'param': None, 'type': 'color', 'default': 8894686, 'label': 'Up color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AroonPeriod = _input('AroonPeriod', 25)  # calculation period
PriceHigh = _input('PriceHigh', pr_high)  # Price to use for high
PriceLow = _input('PriceLow', pr_low)  # Price to use for low
Style = _input('Style', st_automatic)  # Style
ColorUp = _input('ColorUp', clrDeepSkyBlue)  # Up color
ColorDown = _input('ColorDown', clrBurlyWood)  # Up color
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
baro = Arr(0, 0.0)
barc = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
line = Arr(0, 0.0)
cololBuffer = Arr(0, 0.0)
prh = Arr(0, 0.0)
prl = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, line, INDICATOR_DATA)
    SetIndexBuffer(6, cololBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, prh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, prl, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Aroon (' + DoubleToString(AroonPeriod, 0) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    global _s_OnCalculate_styleInUse, _s_OnCalculate_styleToUse
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
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, clrNONE)
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clrNONE)
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, ColorUp)
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, ColorDown)
        else:
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, ColorUp)
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, ColorDown)
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, clrNONE)
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, clrNONE)
            PlotIndexSetInteger(0, PLOT_DRAW_TYPE, _s_OnCalculate_styleToUse)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prh[i] = getPrice(PriceHigh, open, close, high, low, rates_total, i)
        prl[i] = getPrice(PriceLow, open, close, high, low, rates_total, i)
        max_ = 0.0
        maxv = prh[i]
        min_ = 0.0
        minv = prl[i]
        k = 1
        while k <= AroonPeriod and (i - k) >= 0:
            if prh[i - k] > maxv:
                max_ = k
                maxv = prh[i - k]
            if prl[i - k] < minv:
                min_ = k
                minv = prl[i - k]
            k += 1
        valueup = (100 * (AroonPeriod - max_)) / AroonPeriod
        valuedn = (100 * (AroonPeriod - min_)) / AroonPeriod
        baro[i] = open[i]
        barc[i] = close[i]
        barh[i] = high[i]
        barl[i] = low[i]
        line[i] = close[i]
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            if valueup > valuedn:
                cololBuffer[i] = 0.0
                colorBuffer[i] = 0.0
            if valueup < valuedn:
                cololBuffer[i] = 1.0
                colorBuffer[i] = 1.0
    return rates_total

def getPrice(price, open, close, high, low, bars, i, instanceNo=0):
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

# ---- static local variables
_s_OnCalculate_styleSetUp = False
_s_OnCalculate_styleInUse = -1
_s_OnCalculate_styleToUse = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonOnChart(_MQL5Indicator):
    name = 'aroon_on_chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 25,  # calculation period
        'PriceHigh': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=2),  # Price to use for high
        'PriceLow': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=3),  # Price to use for low
        'Style': _Choice({0: 'automatically adjust style', 1: 'view as bars', 2: 'view as candles', 3: 'view as line'}, default=0),  # Style
    }

