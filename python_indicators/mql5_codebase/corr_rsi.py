"""Corr_RSI — converted from MQL5: MQL5 Indicators/Corr RSI/Corr_RSI.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 6}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8, 6: 8}, 'colors': {1: [3329330, 42495], 2: [3329330], 3: [12632256], 4: [42495], 5: [11119017, 3329330, 6333684], 6: [11119017, 3329330, 6333684]}, 'widths': {6: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 2}, 'labels': {1: 'corrected rsi levels', 2: 'corrected rsi up level', 3: 'corrected rsi middle level', 4: 'corrected rsi down level', 5: 'Rsi', 6: 'corrected rsi'}, 'levels': [], 'description': [], 'name': 'Corr_RSI', 'source': 'MQL5 Indicators/Corr RSI/Corr_RSI.mq5', 'folder': 'Corr RSI', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 32, 'label': 'Rsi period', 'sinput': False}, {'mql': 'RsiType', 'py': 'RsiType', 'param': 'RsiType', 'type': 'int', 'default': 5, 'label': 'Rsi type', 'sinput': False}, {'mql': 'CorrectionPeriod', 'py': 'CorrectionPeriod', 'param': 'CorrectionPeriod', 'type': 'int', 'default': 0, 'label': 'Correction period (<0 no correction =0 same as rsi period)', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'LevelsPeriod', 'py': 'LevelsPeriod', 'param': 'LevelsPeriod', 'type': 'int', 'default': 50, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'LevelsUp', 'py': 'LevelsUp', 'param': 'LevelsUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'LevelsDown', 'py': 'LevelsDown', 'param': 'LevelsDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enRsiTypes
rsi_cut = 0
rsi_ehl = 1
rsi_har = 2
rsi_rap = 3
rsi_rsi = 4
rsi_rsx = 5
rsi_slo = 6
_enum('enRsiTypes', {0: 'rsi_cut', 1: 'rsi_ehl', 2: 'rsi_har', 3: 'rsi_rap', 4: 'rsi_rsi', 5: 'rsi_rsx', 6: 'rsi_slo'})

# enum enColorOn
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
chg_onOrig = 3
_enum('enColorOn', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle', 3: 'chg_onOrig'})

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 32)  # Rsi period
RsiType = _input('RsiType', rsi_rsx)  # Rsi type
CorrectionPeriod = _input('CorrectionPeriod', 0)  # Correction period (<0 no correction =0 same as rsi period)
Price = _input('Price', pr_close)  # Price
ColorOn = _input('ColorOn', chg_onLevel)  # Color change on :
LevelsPeriod = _input('LevelsPeriod', 50)  # Floating levels period
LevelsUp = _input('LevelsUp', 90.0)  # Upper level %
LevelsDown = _input('LevelsDown', 10.0)  # Lower level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
cor = Arr(0, 0.0)
corc = Arr(0, 0.0)
workDev = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(39,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelMi, INDICATOR_DATA)
    SetIndexBuffer(4, levelDn, INDICATOR_DATA)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, cor, INDICATOR_DATA)
    SetIndexBuffer(8, corc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" ' + getRsiName(RsiType) + ' (' + _str(RsiPeriod) + ',' + _str(CorrectionPeriod) + ',' + _str(LevelsPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    deviationsPeriod = (CorrectionPeriod if (CorrectionPeriod > 0) else 0 if (CorrectionPeriod < 0) else RsiPeriod)
    colorOn = (ColorOn if (deviationsPeriod > 0) else ColorOn if (ColorOn != chg_onOrig) else chg_onSlope)
    levelPeriod = (LevelsPeriod if (LevelsPeriod > 1) else RsiPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iRsi(RsiType, getPrice(Price, open, close, high, low, i, rates_total), RsiPeriod, i, rates_total)
        v1 = MathPow(iDeviation(val[i], deviationsPeriod, False, i, rates_total), 2)
        v2 = (MathPow(cor[i - 1] - val[i], 2) if (i > 0) else 0)
        c = (0 if (v2 < v1 or v2 == 0) else (1 - _fdiv(v1, v2)))
        cor[i] = ((cor[i - 1] + (c * (val[i] - cor[i - 1]))) if (i > 0) else val[i])
        start = MathMax(i - levelPeriod + 1, 0)
        min_ = cor[ArrayMinimum(cor, start, levelPeriod)]
        max_ = cor[ArrayMaximum(cor, start, levelPeriod)]
        range_ = max_ - min_
        levelUp[i] = min_ + ((LevelsUp * range_) / 100.0)
        levelDn[i] = min_ + ((LevelsDown * range_) / 100.0)
        levelMi[i] = (levelUp[i] + levelDn[i]) * 0.5
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        _sw1 = colorOn
        if _sw1 == chg_onOrig:
            corc[i] = (1 if (cor[i] < val[i]) else 2 if (cor[i] > val[i]) else corc[i - 1] if (i > 0) else 0)
        elif _sw1 == chg_onMiddle:
            corc[i] = (1 if (cor[i] > levelMi[i]) else 2 if (cor[i] < levelMi[i]) else corc[i - 1] if (i > 0) else 0)
        elif _sw1 == chg_onLevel:
            corc[i] = (1 if (cor[i] > levelUp[i]) else 2 if (cor[i] < levelDn[i]) else (corc[i - 1] if (cor[i] == cor[i - 1]) else 0) if (i > 0) else 0)
        else:
            corc[i] = ((1 if (cor[i] > cor[i - 1]) else 2 if (cor[i] < cor[i - 1]) else corc[i - 1]) if (i > 0) else 0)
        fill2[i] = (levelUp[i] if (cor[i] > levelUp[i]) else levelDn[i] if (cor[i] < levelDn[i]) else cor[i])
        fill1[i] = cor[i]
        i += 1
    return rates_total

def iDeviation(value, length, isSample, i, bars):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    oldMean = value
    newMean = value
    squares = 0.0
    k = 0
    k = 1
    while k < length and (i - k) >= 0:
        newMean = _fdiv(workDev[i - k] - oldMean, k + 1) + oldMean
        squares += (workDev[i - k] - oldMean) * (workDev[i - k] - newMean)
        oldMean = newMean
        k += 1
    return MathSqrt(_fdiv(squares, MathMax(k - isSample, 1)))

def getRsiName(method):
    _sw2 = method
    if _sw2 == rsi_rsi:
        return 'RSI'
    elif _sw2 == rsi_rsx:
        return 'RSX'
    elif _sw2 == rsi_cut:
        return "Cuttler's RSI"
    elif _sw2 == rsi_har:
        return "Haris' RSI"
    elif _sw2 == rsi_rap:
        return 'Rapid RSI'
    elif _sw2 == rsi_slo:
        return 'Slow RSI'
    elif _sw2 == rsi_ehl:
        return "Ehlers' smoothed RSI"
    else:
        return ''

def iRsi(rsiMode, price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 13
    workRsi[r][z + 0] = price
    _sw3 = rsiMode
    if _sw3 == rsi_rsi:
        alpha = _fdiv(1.0, MathMax(period, 1))
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
    elif _sw3 == rsi_slo:
        up = 0.0
        dn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                up += diff
            else:
                dn -= diff
            k += 1
        if r < 1:
            workRsi[r][z + 1] = 50.0
        else:
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (_fdiv(1, MathMax(period, 1)) * (_fdiv(100 * up, MathMax(up + dn, DBL_MIN)) - workRsi[r - 1][z + 1]))
        return workRsi[r][z + 1]
    elif _sw3 == rsi_rap:
        up = 0.0
        dn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                up += diff
            else:
                dn -= diff
            k += 1
        return _fdiv(100 * up, MathMax(up + dn, DBL_MIN))
    elif _sw3 == rsi_ehl:
        up = 0.0
        dn = 0.0
        workRsi[r][z + 3] = (((workRsi[r][z + 0] + (2.0 * workRsi[r - 1][z + 0]) + workRsi[r - 2][z + 0]) / 4.0) if (r > 2) else price)
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 3] - workRsi[r - k - 1][z + 3]
            if diff > 0:
                up += diff
            else:
                dn -= diff
            k += 1
        return _fdiv(50 * (up - dn), MathMax(up + dn, DBL_MIN)) + 50
    elif _sw3 == rsi_cut:
        sump = 0.0
        sumn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                sump += diff
            else:
                sumn -= diff
            k += 1
        workRsi[r][instanceNo + 1] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(sump, MathMax(sumn, DBL_MIN)))
        return workRsi[r][instanceNo + 1]
    elif _sw3 == rsi_har:
        avgUp = 0.0
        avgDn = 0.0
        up = 0.0
        dn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][instanceNo + 0] - workRsi[r - k - 1][instanceNo + 0]
            if diff > 0:
                avgUp += diff
                up += 1
            else:
                avgDn -= diff
                dn += 1
            k += 1
        if up != 0:
            avgUp = _fdiv(avgUp, up)
        if dn != 0:
            avgDn = _fdiv(avgDn, dn)
        workRsi[r][instanceNo + 1] = 100 - _fdiv(100, 1.0 + _fdiv(avgUp, MathMax(avgDn, DBL_MIN)))
        return workRsi[r][instanceNo + 1]
    elif _sw3 == rsi_rsx:
        Kg = _fdiv(3.0, 2.0 + period)
        Hg = 1.0 - Kg
        if r < period:
            for k in range(1, 13):
                workRsi[r][k + z] = 0.0
            return 50.0
        mom = workRsi[r][0 + z] - workRsi[r - 1][0 + z]
        moa = MathAbs(mom)
        for k in range(0, 3):
            kk = k * 2
            workRsi[r][z + kk + 1] = (Kg * mom) + (Hg * workRsi[r - 1][z + kk + 1])
            workRsi[r][z + kk + 2] = (Kg * workRsi[r][z + kk + 1]) + (Hg * workRsi[r - 1][z + kk + 2])
            mom = (1.5 * workRsi[r][z + kk + 1]) - (0.5 * workRsi[r][z + kk + 2])
            workRsi[r][z + kk + 7] = (Kg * moa) + (Hg * workRsi[r - 1][z + kk + 7])
            workRsi[r][z + kk + 8] = (Kg * workRsi[r][z + kk + 7]) + (Hg * workRsi[r - 1][z + kk + 8])
            moa = (1.5 * workRsi[r][z + kk + 7]) - (0.5 * workRsi[r][z + kk + 8])
        return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)
    return 0.0

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
        _sw4 = tprice
        if _sw4 == pr_haclose:
            return haClose
        elif _sw4 == pr_haopen:
            return haOpen
        elif _sw4 == pr_hahigh:
            return haHigh
        elif _sw4 == pr_halow:
            return haLow
        elif _sw4 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw4 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw4 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw4 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw4 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw4 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw4 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw5 = tprice
    if _sw5 == pr_close:
        return close[i]
    elif _sw5 == pr_open:
        return open[i]
    elif _sw5 == pr_high:
        return high[i]
    elif _sw5 == pr_low:
        return low[i]
    elif _sw5 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw5 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw5 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw5 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw5 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw5 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw5 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrRSI(_MQL5Indicator):
    name = 'Corr_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 32,  # Rsi period
        'RsiType': _Choice({0: "Cuttler's RSI", 1: "Ehlers' smoothed RSI", 2: "Harris' RSI", 3: 'Rapid RSI', 4: 'RSI', 5: 'RSX', 6: 'Slow RSI'}, default=5),  # Rsi type
        'CorrectionPeriod': 0,  # Correction period (<0 no correction =0 same as rsi period)
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on rsi value cross'}, default=1),  # Color change on :
        'LevelsPeriod': 50,  # Floating levels period
        'LevelsUp': 90.0,  # Upper level %
        'LevelsDown': 10.0,  # Lower level %
    }

