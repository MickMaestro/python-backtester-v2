"""double_smoothed_stochastic_1_1t17 — converted from MQL5: MQL5 Indicators/Double smoothed stochastic/double_smoothed_stochastic_1_1t17.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 2, 'indicator_minimum': -1.0, 'indicator_maximum': 101.0}, 'types': {1: 7, 2: 1}, 'colors': {1: [3329330, 42495], 2: [6908265]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Stochastic levels', 2: 'Stochastic'}, 'levels': [], 'description': [], 'name': 'double_smoothed_stochastic_1_1t17', 'source': 'MQL5 Indicators/Double smoothed stochastic/double_smoothed_stochastic_1_1t17.mq5', 'folder': 'Double smoothed stochastic', 'inputs': [{'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 55, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'int', 'default': 15, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'EMAPeriod2', 'py': 'EMAPeriod2', 'param': 'EMAPeriod2', 'type': 'int', 'default': 7, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'PriceForHigh', 'py': 'PriceForHigh', 'param': 'PriceForHigh', 'type': 'int', 'default': 2, 'label': 'Price to use for high', 'sinput': False}, {'mql': 'PriceForLow', 'py': 'PriceForLow', 'param': 'PriceForLow', 'type': 'int', 'default': 3, 'label': 'Price to use for low', 'sinput': False}, {'mql': 'PriceForClose', 'py': 'PriceForClose', 'param': 'PriceForClose', 'type': 'int', 'default': 0, 'label': 'Price to use for close', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'double', 'default': 80.0, 'label': 'Overbought level', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'double', 'default': 20.0, 'label': 'Oversold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DimGray = 0x696969  # MQL4 colour name

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

# ---- inputs and global variables
StochasticPeriod = _input('StochasticPeriod', 55)  # Stochastic period
EMAPeriod = _input('EMAPeriod', 15)  # Smoothing period
EMAPeriod2 = _input('EMAPeriod2', 7)  # Smoothing period
PriceForHigh = _input('PriceForHigh', pr_high)  # Price to use for high
PriceForLow = _input('PriceForLow', pr_low)  # Price to use for low
PriceForClose = _input('PriceForClose', pr_close)  # Price to use for close
UpLevel = _input('UpLevel', 80.0)  # Overbought level
DnLevel = _input('DnLevel', 20.0)  # Oversold level
StochasticBuffer = Arr(0, 0.0)
LevelsBuffer = Arr(0, 0.0)
StochasticLine = Arr(0, 0.0)
calcBuffer = Arr(0, 0.0)
calcBuffer1 = Arr(0, 0.0)
prh = Arr(0, 0.0)
prl = Arr(0, 0.0)
prc = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(12,))

def OnInit():
    SetIndexBuffer(0, StochasticBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LevelsBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, StochasticLine, INDICATOR_DATA)
    SetIndexBuffer(3, calcBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, calcBuffer1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, prh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, prl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, prc, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, DimGray)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Double smoothe stochastic (' + _str(StochasticPeriod) + ',' + _str(EMAPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    alpha = _fdiv(2.0, 1.0 + EMAPeriod)
    alpha1 = _fdiv(2.0, 1.0 + EMAPeriod2)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        prh[i] = getPrice(PriceForHigh, open, close, high, low, rates_total, i, 0)
        prl[i] = getPrice(PriceForLow, open, close, high, low, rates_total, i, 1)
        prc[i] = getPrice(PriceForClose, open, close, high, low, rates_total, i, 2)
        max_ = prh[i]
        k = 1
        while k < StochasticPeriod and (i - k) >= 0:
            max_ = MathMax(max_, prh[i - k])
            k += 1
        min_ = prl[i]
        k = 1
        while k < StochasticPeriod and (i - k) >= 0:
            min_ = MathMin(min_, prl[i - k])
            k += 1
        sto = 0.0
        if max_ != min_:
            sto = _fdiv(prc[i] - min_, max_ - min_) * 100.0
        calcBuffer[i] = calcBuffer[i - 1] + (alpha * (sto - calcBuffer[i - 1]))
        max_ = calcBuffer[i]
        k = 1
        while k < StochasticPeriod and (i - k) >= 0:
            max_ = MathMax(max_, calcBuffer[i - k])
            k += 1
        min_ = calcBuffer[i]
        k = 1
        while k < StochasticPeriod and (i - k) >= 0:
            min_ = MathMin(min_, calcBuffer[i - k])
            k += 1
        if max_ != min_:
            sto = _fdiv(calcBuffer[i] - min_, max_ - min_) * 100.0
        else:
            sto = 0.0
        calcBuffer1[i] = calcBuffer1[i - 1] + (alpha * (sto - calcBuffer1[i - 1]))
        StochasticBuffer[i] = StochasticBuffer[i - 1] + (alpha1 * (calcBuffer1[i] - StochasticBuffer[i - 1]))
        StochasticLine[i] = StochasticBuffer[i]
        LevelsBuffer[i] = StochasticBuffer[i]
        if StochasticBuffer[i] > UpLevel:
            LevelsBuffer[i] = UpLevel
        if StochasticBuffer[i] < DnLevel:
            LevelsBuffer[i] = DnLevel
    return rates_total

def getPrice(price, open, close, high, low, bars, i, instanceNo=0):
    if price >= pr_haclose:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
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
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleSmoothedStochastic11t17(_MQL5Indicator):
    name = 'double_smoothed_stochastic_1_1t17'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StochasticPeriod': 55,  # Stochastic period
        'EMAPeriod': 15,  # Smoothing period
        'EMAPeriod2': 7,  # Smoothing period
        'PriceForHigh': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=2),  # Price to use for high
        'PriceForLow': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=3),  # Price to use for low
        'PriceForClose': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use for close
        'UpLevel': 80.0,  # Overbought level
        'DnLevel': 20.0,  # Oversold level
    }
    y_range = (-1.0, 101.0)

