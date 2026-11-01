"""rsx_variation — converted from MQL5: MQL5 Indicators/RSX Variation/rsx_variation.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3329330, 17919]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'rsi'}, 'levels': [], 'description': [], 'name': 'rsx_variation', 'source': 'MQL5 Indicators/RSX Variation/rsx_variation.mq5', 'folder': 'RSX Variation', 'inputs': [{'mql': 'RsxPeriod', 'py': 'RsxPeriod', 'param': 'RsxPeriod', 'type': 'int', 'default': 32, 'label': 'RSX period', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'int', 'default': 4, 'label': 'Momentum period (1 for original rsx)', 'sinput': False}, {'mql': 'RsxPrice', 'py': 'RsxPrice', 'param': 'RsxPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
RsxPeriod = _input('RsxPeriod', 32)  # RSX period
MomPeriod = _input('MomPeriod', 4)  # Momentum period (1 for original rsx)
RsxPrice = _input('RsxPrice', pr_close)  # Price
rsi = Arr(0, 0.0)
rsic = Arr(0, 0.0)
wrkBuffer = Arr(0, 0.0, dims=(13,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, rsi, INDICATOR_DATA)
    SetIndexBuffer(1, rsic, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSX variation (' + _str(RsxPeriod) + ',' + _str(MomPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(wrkBuffer, 0) != rates_total:
        ArrayResize(wrkBuffer, rates_total)
    Kg = _fdiv(3.0, 2.0 + RsxPeriod)
    Hg = 1.0 - Kg
    momPeriod = MathMax(MomPeriod, 1)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        for c in range(0, 12):
            wrkBuffer[i][c] = 0.0
        wrkBuffer[i][12] = getPrice(RsxPrice, open, close, high, low, i, rates_total)
        roc = ((wrkBuffer[i][12] - wrkBuffer[i - momPeriod][12]) if (i > momPeriod) else 0)
        roa = MathAbs(roc)
        if i > 0:
            for k in range(0, 3):
                kk = k * 2
                wrkBuffer[i][kk + 0] = (Kg * roc) + (Hg * wrkBuffer[i - 1][kk + 0])
                wrkBuffer[i][kk + 1] = (Kg * wrkBuffer[i][kk + 0]) + (Hg * wrkBuffer[i - 1][kk + 1])
                roc = (1.5 * wrkBuffer[i][kk + 0]) - (0.5 * wrkBuffer[i][kk + 1])
                wrkBuffer[i][kk + 6] = (Kg * roa) + (Hg * wrkBuffer[i - 1][kk + 6])
                wrkBuffer[i][kk + 7] = (Kg * wrkBuffer[i][kk + 6]) + (Hg * wrkBuffer[i - 1][kk + 7])
                roa = (1.5 * wrkBuffer[i][kk + 6]) - (0.5 * wrkBuffer[i][kk + 7])
        rsi[i] = (MathMax(MathMin((_fdiv(roc, roa) + 1.0) * 50.0, 100.0), 0.0) if (roa != 0) else 0)
        rsic[i] = ((1 if (rsi[i] > rsi[i - 1]) else 2 if (rsi[i] < rsi[i - 1]) else rsic[i - 1]) if (i > 0) else 0)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsxVariation(_MQL5Indicator):
    name = 'rsx_variation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'RsxPeriod': 32,  # RSX period
        'MomPeriod': 4,  # Momentum period (1 for original rsx)
        'RsxPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
    }

