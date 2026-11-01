"""MHL_average_-_alertsl1v — converted from MQL5: MQL5 Indicators/MHL Average/MHL_average_-_alertsl1v.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [12632256], 2: [16760576, 6333684]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Average', 2: 'MHL average'}, 'levels': [], 'description': [], 'name': 'MHL_average_-_alertsl1v', 'source': 'MQL5 Indicators/MHL Average/MHL_average_-_alertsl1v.mq5', 'folder': 'MHL Average', 'inputs': [{'mql': 'CalcPeriod', 'py': 'CalcPeriod', 'param': 'CalcPeriod', 'type': 'int', 'default': 10, 'label': 'Calculation period', 'sinput': False}, {'mql': 'AverPeriod', 'py': 'AverPeriod', 'param': 'AverPeriod', 'type': 'int', 'default': 50, 'label': 'Average period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'MaMethodToUse', 'py': 'MaMethodToUse', 'param': 'MaMethodToUse', 'type': 'int', 'default': 0, 'label': 'What ma method to use in average calculation', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Alert on trend change?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enMaMethod
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaMethod', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
CalcPeriod = _input('CalcPeriod', 10)  # Calculation period
AverPeriod = _input('AverPeriod', 50)  # Average period
Price = _input('Price', pr_close)  # Price to use
MaMethodToUse = _input('MaMethodToUse', ma_sma)  # What ma method to use in average calculation
alertsOn = _input('alertsOn', False)  # Alert on trend change?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
MaBuffer = Arr(0, 0.0)
AvgBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, AvgBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MHL average (' + _str(CalcPeriod) + ',' + _str(AverPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        _sw1 = MaMethodToUse
        if _sw1 == ma_sma:
            AvgBuffer[i] = iSma(price, AverPeriod, i, rates_total, 0)
        elif _sw1 == ma_ema:
            AvgBuffer[i] = iEma(price, AverPeriod, i, rates_total, 0)
        elif _sw1 == ma_smma:
            AvgBuffer[i] = iSmma(price, AverPeriod, i, rates_total, 0)
        elif _sw1 == ma_lwma:
            AvgBuffer[i] = iLwma(price, AverPeriod, i, rates_total, 0)
        min_ = low[i]
        max_ = high[i]
        k = 1
        while k < CalcPeriod and (i - k) >= 0:
            min_ = MathMin(min_, low[i - k])
            max_ = MathMax(max_, high[i - k])
            k += 1
        price = (max_ + min_) / 2.0
        _sw2 = MaMethodToUse
        if _sw2 == ma_sma:
            MaBuffer[i] = iSma(price, AverPeriod, i, rates_total, 1)
        elif _sw2 == ma_ema:
            MaBuffer[i] = iEma(price, AverPeriod, i, rates_total, 1)
        elif _sw2 == ma_smma:
            MaBuffer[i] = iSmma(price, AverPeriod, i, rates_total, 1)
        elif _sw2 == ma_lwma:
            MaBuffer[i] = iLwma(price, AverPeriod, i, rates_total, 1)
        if i > 0:
            ColorBuffer[i] = ColorBuffer[i - 1]
            if MaBuffer[i] < AvgBuffer[i]:
                ColorBuffer[i] = 0.0
            if MaBuffer[i] > AvgBuffer[i]:
                ColorBuffer[i] = 1.0
        else:
            ColorBuffer[i] = 0.0
    manageAlerts(time, ColorBuffer, rates_total)
    return rates_total

def manageAlerts(time, trend, bars):
    if alertsOn:
        whichBar = bars - 1
        if not alertsOnCurrent:
            whichBar = bars - 2
        time1 = time[whichBar]
        if trend[whichBar] != trend[whichBar - 1]:
            if trend[whichBar] == 0:
                doAlert(time1, 'up')
            if trend[whichBar] == 1:
                doAlert(time1, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' MHL average trend changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' MHL average', message)
        if alertsSound:
            PlaySound('alert2.wav')

def iSma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo + 0] = price
    workSma[r][instanceNo + 1] = price
    k = 1
    while k < period and (r - k) >= 0:
        workSma[r][instanceNo + 1] += workSma[r - k][instanceNo + 0]
        k += 1
    workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], 1.0 * k)
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _tbars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _tbars:
            ArrayResize(workHa, _tbars)
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


class MHLAverageAlertsl1v(_MQL5Indicator):
    name = 'MHL_average_-_alertsl1v'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalcPeriod': 10,  # Calculation period
        'AverPeriod': 50,  # Average period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'MaMethodToUse': _Choice({0: 'Calculate average using SMA', 1: 'Calculate average using EMA', 2: 'Calculate average using SMMA', 3: 'Calculate average using LWMA'}, default=0),  # What ma method to use in average calculation
        'alertsOn': False,  # Alert on trend change?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
    }

