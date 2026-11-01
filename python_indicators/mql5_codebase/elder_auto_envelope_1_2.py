"""elder_auto_envelope_1_2 — converted from MQL5: MQL5 Indicators/Elder Auto Envelopes/elder_auto_envelope_1_2.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 8, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16760576, 6333684], 2: [16760576, 6333684], 3: [8421504], 5: [6908265]}, 'widths': {2: 2}, 'styles': {4: 4, 5: 4}, 'labels': {1: 'Envelope fill', 2: 'Ema', 3: 'Fast ema', 4: 'Upper band', 5: 'Lower band'}, 'levels': [], 'description': [], 'name': 'elder_auto_envelope_1_2', 'source': 'MQL5 Indicators/Elder Auto Envelopes/elder_auto_envelope_1_2.mq5', 'folder': 'Elder Auto Envelopes', 'inputs': [{'mql': 'EmaPeriod', 'py': 'EmaPeriod', 'param': 'EmaPeriod', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'FastEmaPeriod', 'py': 'FastEmaPeriod', 'param': 'FastEmaPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DeviationsFactor', 'py': 'DeviationsFactor', 'param': 'DeviationsFactor', 'type': 'double', 'default': 2.7, 'label': 'Original was 2.7 best for stock markets', 'sinput': False}, {'mql': 'DeviationsPeriod', 'py': 'DeviationsPeriod', 'param': 'DeviationsPeriod', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_haclose = 7
pr_haopen = 8
pr_hahigh = 9
pr_halow = 10
pr_hamedian = 11
pr_hatypical = 12
pr_haweighted = 13
pr_haaverage = 14
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_haclose', 8: 'pr_haopen', 9: 'pr_hahigh', 10: 'pr_halow', 11: 'pr_hamedian', 12: 'pr_hatypical', 13: 'pr_haweighted', 14: 'pr_haaverage'})

# ---- inputs and global variables
EmaPeriod = _input('EmaPeriod', 21)
FastEmaPeriod = _input('FastEmaPeriod', 13)
Price = _input('Price', pr_close)
DeviationsFactor = _input('DeviationsFactor', 2.7)  # Original was 2.7 best for stock markets
DeviationsPeriod = _input('DeviationsPeriod', 100)
slowEma = Arr(0, 0.0)
slowEmaColor = Arr(0, 0.0)
fastEma = Arr(0, 0.0)
envelopeUp = Arr(0, 0.0)
envelopeDn = Arr(0, 0.0)
fillup = Arr(0, 0.0)
filldn = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, fillup, INDICATOR_DATA)
    SetIndexBuffer(1, filldn, INDICATOR_DATA)
    SetIndexBuffer(2, slowEma, INDICATOR_DATA)
    SetIndexBuffer(3, slowEmaColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, fastEma, INDICATOR_DATA)
    SetIndexBuffer(5, envelopeUp, INDICATOR_DATA)
    SetIndexBuffer(6, envelopeDn, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        ema = iEma(price, EmaPeriod, i, rates_total, 0)
        bullp = MathAbs(high[i] - ema)
        bearp = MathAbs(low[i] - ema)
        maxp = MathMax(bullp, bearp)
        work[i][0] = _fdiv(maxp, ema)
        work[i][1] = work[MathMax(i - 1, 0)][1]
        curTime = MqlDateTime()
        prevTime = MqlDateTime()
        TimeToStruct(time[i], curTime)
        TimeToStruct(MathMax(i - 1, 0), prevTime)
        if curTime.day_of_week < prevTime.day_of_week or Period() > PERIOD_W1:
            avg = 0.0
            sum_ = 0.0
            k = 0
            while k < DeviationsPeriod and (i - k - 1) >= 0:
                avg += work[i - k - 1][0]
                k += 1
            avg = avg / DeviationsPeriod
            k = 0
            while k < DeviationsPeriod and (i - k - 1) >= 0:
                sum_ += (work[i - k - 1][0] - avg) * (work[i - k - 1][0] - avg)
                k += 1
            work[i][1] = MathSqrt(sum_ / DeviationsPeriod)
        slowEma[i] = ema
        envelopeUp[i] = ema * (1 + (DeviationsFactor * work[i][1]))
        envelopeDn[i] = ema * (1 - (DeviationsFactor * work[i][1]))
        if FastEmaPeriod > 0:
            fastEma[i] = iEma(price, FastEmaPeriod, i, rates_total, 1)
            if fastEma[i] > slowEma[i]:
                slowEmaColor[i] = 0.0
            if fastEma[i] < slowEma[i]:
                slowEmaColor[i] = 1.0
            fillup[i] = fastEma[i]
            filldn[i] = slowEma[i]
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
    return 0.0

def iEma(price, period, r, totalBars, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    if r < 1:
        workEma[r][instanceNo] = price
    else:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ElderAutoEnvelope12(_MQL5Indicator):
    name = 'elder_auto_envelope_1_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EmaPeriod': 21,
        'FastEmaPeriod': 13,
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Heiken ashi close', 8: 'Heiken ashi open', 9: 'Heiken ashi high', 10: 'Heiken ashi low', 11: 'Heiken ashi median', 12: 'Heiken ashi typical', 13: 'Heiken ashi weighted', 14: 'Heiken ashi average'}, default=0),
        'DeviationsFactor': 2.7,  # Original was 2.7 best for stock markets
        'DeviationsPeriod': 100,
    }

