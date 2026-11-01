"""Detrended_Synthetic_Price_zoscillatoru — converted from MQL5: MQL5 Indicators/Detrended Synthetic Price (oscillator)/Detrended_Synthetic_Price_zoscillatoru.mq5

Copyright: © mladen, 2017; Link: www.forex-station.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'www.forex-station.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'value'}, 'levels': [], 'description': [], 'name': 'Detrended_Synthetic_Price_zoscillatoru', 'source': 'MQL5 Indicators/Detrended Synthetic Price (oscillator)/Detrended_Synthetic_Price_zoscillatoru.mq5', 'folder': 'Detrended Synthetic Price (oscillator)', 'inputs': [{'mql': 'DspPeriod', 'py': 'DspPeriod', 'param': 'DspPeriod', 'type': 'int', 'default': 14, 'label': 'DSP period', 'sinput': False}, {'mql': 'DspPrice', 'py': 'DspPrice', 'param': 'DspPrice', 'type': 'int', 'default': 4, 'label': 'DSP price', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'double', 'default': 9.0, 'label': 'Signal period', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 1, 'label': 'Change color on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enColorOn
chg_onZero = 0
chg_onOuter = 1
chg_onOuter2 = 2
chg_onSlope = 3
_enum('enColorOn', {0: 'chg_onZero', 1: 'chg_onOuter', 2: 'chg_onOuter2', 3: 'chg_onSlope'})

# ---- inputs and global variables
DspPeriod = _input('DspPeriod', 14)  # DSP period
DspPrice = _input('DspPrice', pr_median)  # DSP price
SignalPeriod = _input('SignalPeriod', 9.0)  # Signal period
ColorOn = _input('ColorOn', chg_onOuter)  # Change color on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelu = Arr(0, 0.0)
leveld = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, levelu, INDICATOR_DATA)
    SetIndexBuffer(1, leveld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, ' (dsl) DSP oscillator  (' + _str(DspPeriod) + ',' + _str(SignalPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alphas = _fdiv(2.0, 1.0 + SignalPeriod)
    alpham = _fdiv(2.0, 1.0 + DspPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(DspPrice, open, close, high, low, i, rates_total)
        val[i] = iEma(price, alpham, i, rates_total, 0) - iEma(price, alpham / 2.0, i, rates_total, 1)
        levelu[i] = (((levelu[i - 1] + (alphas * (val[i] - levelu[i - 1]))) if (val[i] > 0) else levelu[i - 1]) if (i > 0) else 0)
        leveld[i] = (((leveld[i - 1] + (alphas * (val[i] - leveld[i - 1]))) if (val[i] < 0) else leveld[i - 1]) if (i > 0) else 0)
        _sw1 = ColorOn
        if _sw1 == chg_onOuter:
            valc[i] = (1 if (val[i] > levelu[i]) else 2 if (val[i] < leveld[i]) else 0)
        elif _sw1 == chg_onOuter2:
            valc[i] = (1 if (val[i] > levelu[i]) else 2 if (val[i] < leveld[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw1 == chg_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iEma(price, alpha, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DetrendedSyntheticPriceZoscillatoru(_MQL5Indicator):
    name = 'Detrended_Synthetic_Price_zoscillatoru'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DspPeriod': 14,  # DSP period
        'DspPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=4),  # DSP price
        'SignalPeriod': 9.0,  # Signal period
        'ColorOn': _Choice({0: 'Change color on zero cross', 1: 'Change color on levels cross', 2: 'Change color on opposite levels cross', 3: 'Change color on slope change'}, default=1),  # Change color on :
    }

