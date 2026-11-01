"""Corr_momentum — converted from MQL5: MQL5 Indicators/Corr momentum/Corr_momentum.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 6}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8, 6: 8}, 'colors': {1: [3329330, 42495], 2: [3329330], 3: [12632256], 4: [42495], 5: [11119017, 3329330, 6333684], 6: [11119017, 3329330, 6333684]}, 'widths': {6: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 2}, 'labels': {1: 'corrected momentum levels', 2: 'corrected momentum up level', 3: 'corrected momentum middle level', 4: 'corrected momentum down level', 5: 'momentum', 6: 'corrected momentum'}, 'levels': [], 'description': [], 'name': 'Corr_momentum', 'source': 'MQL5 Indicators/Corr momentum/Corr_momentum.mq5', 'folder': 'Corr momentum', 'inputs': [{'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'int', 'default': 32, 'label': 'Momentum period', 'sinput': False}, {'mql': 'CorrectionPeriod', 'py': 'CorrectionPeriod', 'param': 'CorrectionPeriod', 'type': 'int', 'default': 0, 'label': 'Correction period (<0 no correction =0 same as momentum period)', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'LevelsPeriod', 'py': 'LevelsPeriod', 'param': 'LevelsPeriod', 'type': 'int', 'default': 25, 'label': 'Levels period', 'sinput': False}, {'mql': 'LevelsUp', 'py': 'LevelsUp', 'param': 'LevelsUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'LevelsDown', 'py': 'LevelsDown', 'param': 'LevelsDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
chg_onOrig = 3
_enum('enColorOn', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle', 3: 'chg_onOrig'})

# ---- inputs and global variables
MomPeriod = _input('MomPeriod', 32)  # Momentum period
CorrectionPeriod = _input('CorrectionPeriod', 0)  # Correction period (<0 no correction =0 same as momentum period)
Price = _input('Price', pr_close)  # Price
ColorOn = _input('ColorOn', chg_onLevel)  # Color change on :
LevelsPeriod = _input('LevelsPeriod', 25)  # Levels period
LevelsUp = _input('LevelsUp', 90.0)  # Upper level %
LevelsDown = _input('LevelsDown', 10.0)  # Lower level %
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
cor = Arr(0, 0.0)
corc = Arr(0, 0.0)
prices = Arr(0, 0.0)
workDev = Arr(0, 0.0)
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
    SetIndexBuffer(9, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" momentum (' + _str(MomPeriod) + ',' + _str(CorrectionPeriod) + ',' + _str(LevelsPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    deviationsPeriod = (CorrectionPeriod if (CorrectionPeriod > 0) else 0 if (CorrectionPeriod < 0) else MomPeriod)
    colorOn = (ColorOn if (deviationsPeriod > 0) else ColorOn if (ColorOn != chg_onOrig) else chg_onSlope)
    levelPeriod = (LevelsPeriod if (LevelsPeriod > 1) else MomPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        val[i] = prices[i] - prices[MathMax(i - MomPeriod, 0)]
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
    manageAlerts(time, corc, colorOn, rates_total)
    return i

def manageAlerts(_time, _trend, colorOn, bars):
    if AlertsOn:
        whichBar = bars - 1
        if not AlertsOnCurrent:
            whichBar = bars - 2
        time1 = _time[whichBar]
        if _trend[whichBar] != _trend[whichBar - 1]:
            add = 'slope changed to'
            _sw2 = colorOn
            if _sw2 == chg_onLevel:
                add = 'outer level crossed'
            elif _sw2 == chg_onMiddle:
                add = 'middle level crossed'
            elif _sw2 == chg_onOrig:
                add = 'momentum value crossed'
            if _trend[whichBar] == 1:
                doAlert(time1, add + ' up')
            if _trend[whichBar] == 2:
                doAlert(time1, add + ' down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' corrected momentum ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' corrected momentum', message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

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
        _sw3 = tprice
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
        elif _sw3 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw4 = tprice
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
    elif _sw4 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrMomentum(_MQL5Indicator):
    name = 'Corr_momentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MomPeriod': 32,  # Momentum period
        'CorrectionPeriod': 0,  # Correction period (<0 no correction =0 same as momentum period)
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on momentum value cross'}, default=1),  # Color change on :
        'LevelsPeriod': 25,  # Levels period
        'LevelsUp': 90.0,  # Upper level %
        'LevelsDown': 10.0,  # Lower level %
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
    }

