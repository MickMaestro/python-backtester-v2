"""Double_Stochastic_RSI_fl — converted from MQL5: MQL5 Indicators/Double stochastic RSI - fl/Double_Stochastic_RSI_fl.mq5

Copyright: mladen; Link: www.forex-station.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-station.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5, 'indicator_minimum': -1.0, 'indicator_maximum': 101.0}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [6333684, 16748574], 2: [16748574], 3: [12632256], 4: [6333684], 5: [12632256]}, 'widths': {1: 1, 5: 2}, 'styles': {1: 0, 2: 2, 3: 2, 4: 2}, 'labels': {1: 'Stochastic', 2: 'Stochastic level up', 3: 'Stochastic middle level', 4: 'Stochastic level down'}, 'levels': [], 'description': [], 'name': 'Double_Stochastic_RSI_fl', 'source': 'MQL5 Indicators/Double stochastic RSI - fl/Double_Stochastic_RSI_fl.mq5', 'folder': 'Double stochastic RSI - fl', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'RSI applied to price', 'sinput': False}, {'mql': 'StoPeriod1', 'py': 'StoPeriod1', 'param': 'StoPeriod1', 'type': 'int', 'default': 55, 'label': 'Stochastic period 1 (less than 2 - no stochastic)', 'sinput': False}, {'mql': 'StoPeriod2', 'py': 'StoPeriod2', 'param': 'StoPeriod2', 'type': 'int', 'default': 55, 'label': 'Stochastic period 2 (less than 2 - no stochastic)', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'int', 'default': 15, 'label': 'Smoothing period (less than 2 - no smoothing)', 'sinput': False}, {'mql': 'flLookBack', 'py': 'flLookBack', 'param': 'flLookBack', 'type': 'int', 'default': 25, 'label': 'Floating levels look back period', 'sinput': False}, {'mql': 'flLevelUp', 'py': 'flLevelUp', 'param': 'flLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up level %', 'sinput': False}, {'mql': 'flLevelDown', 'py': 'flLevelDown', 'param': 'flLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # RSI period
Price = _input('Price', pr_close)  # RSI applied to price
StoPeriod1 = _input('StoPeriod1', 55)  # Stochastic period 1 (less than 2 - no stochastic)
StoPeriod2 = _input('StoPeriod2', 55)  # Stochastic period 2 (less than 2 - no stochastic)
EMAPeriod = _input('EMAPeriod', 15)  # Smoothing period (less than 2 - no smoothing)
flLookBack = _input('flLookBack', 25)  # Floating levels look back period
flLevelUp = _input('flLevelUp', 90.0)  # Floating levels up level %
flLevelDown = _input('flLevelDown', 10.0)  # Floating levels down level %
RsiBuffer = Arr(0, 0.0)
StoBuffer = Arr(0, 0.0)
StcBuffer = Arr(0, 0.0)
StlBuffer = Arr(0, 0.0)
LevBuffer = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(3,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, LevBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, StlBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, StoBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, RsiBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, StcBuffer, INDICATOR_CALCULATIONS)
    strSmooth = ('smoothed ' if (EMAPeriod > 1) else '')
    strStoch = ('stochastic ' if (StoPeriod1 > 1 or StoPeriod2 > 1) else '')
    strStoch = ('double stochastic ' if (StoPeriod1 > 1 and StoPeriod2 > 1) else strStoch)
    IndicatorSetString(INDICATOR_SHORTNAME, strSmooth + strStoch + 'RSI(' + _str(RSIPeriod) + ',' + _str(StoPeriod1) + ',' + _str(StoPeriod2) + ',' + _str(EMAPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + EMAPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        RsiBuffer[i] = iRsi(getPrice(Price, open, close, high, low, i, rates_total), RSIPeriod, i, rates_total)
        max_ = RsiBuffer[i]
        k = 1
        while k < StoPeriod1 and (i - k) >= 0:
            max_ = MathMax(max_, RsiBuffer[i - k])
            k += 1
        min_ = RsiBuffer[i]
        k = 1
        while k < StoPeriod1 and (i - k) >= 0:
            min_ = MathMin(min_, RsiBuffer[i - k])
            k += 1
        StcBuffer[i] = ((_fdiv(RsiBuffer[i] - min_, max_ - min_) * 100.0) if (max_ != min_) else RsiBuffer[i])
        max_ = StcBuffer[i]
        k = 1
        while k < StoPeriod2 and (i - k) >= 0:
            max_ = MathMax(max_, StcBuffer[i - k])
            k += 1
        min_ = StcBuffer[i]
        k = 1
        while k < StoPeriod2 and (i - k) >= 0:
            min_ = MathMin(min_, StcBuffer[i - k])
            k += 1
        sto = ((_fdiv(StcBuffer[i] - min_, max_ - min_) * 100.0) if (max_ != min_) else StcBuffer[i])
        StoBuffer[i] = ((StoBuffer[i - 1] + (alpha * (sto - StoBuffer[i - 1]))) if (i > 0) else sto)
        start = MathMax(i - flLookBack + 1, 0)
        min_ = StoBuffer[ArrayMinimum(StoBuffer, start, flLookBack)]
        max_ = StoBuffer[ArrayMaximum(StoBuffer, start, flLookBack)]
        range_ = max_ - min_
        levelup[i] = min_ + ((flLevelUp * range_) / 100.0)
        leveldn[i] = min_ + ((flLevelDown * range_) / 100.0)
        levelmi[i] = min_ + (0.5 * range_)
        StlBuffer[i] = StoBuffer[i]
        LevBuffer[i] = StoBuffer[i]
        if StoBuffer[i] > levelup[i]:
            LevBuffer[i] = levelup[i]
        if StoBuffer[i] < leveldn[i]:
            LevBuffer[i] = leveldn[i]
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    if period <= 1:
        return price
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, period)
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleStochasticRSIFl(_MQL5Indicator):
    name = 'Double_Stochastic_RSI_fl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # RSI period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # RSI applied to price
        'StoPeriod1': 55,  # Stochastic period 1 (less than 2 - no stochastic)
        'StoPeriod2': 55,  # Stochastic period 2 (less than 2 - no stochastic)
        'EMAPeriod': 15,  # Smoothing period (less than 2 - no smoothing)
        'flLookBack': 25,  # Floating levels look back period
        'flLevelUp': 90.0,  # Floating levels up level %
        'flLevelDown': 10.0,  # Floating levels down level %
    }
    y_range = (-1.0, 101.0)

