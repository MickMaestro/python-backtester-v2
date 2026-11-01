"""Holts_double_exponential_smoothing — converted from MQL5: MQL5 Indicators/Holt's  double exponential smoothing/Holts_double_exponential_smoothing.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [8421504, 3329330, 6333684], 2: [8421504, 3329330, 6333684]}, 'widths': {1: 3}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Holt DS', 2: 'Holt DS forecast'}, 'levels': [], 'description': [], 'name': 'Holts_double_exponential_smoothing', 'source': "MQL5 Indicators/Holt's  double exponential smoothing/Holts_double_exponential_smoothing.mq5", 'folder': "Holt's  double exponential smoothing", 'inputs': [{'mql': 'EstimatePeriod', 'py': 'EstimatePeriod', 'param': 'EstimatePeriod', 'type': 'double', 'default': 14.33, 'label': 'Estimation component period', 'sinput': False}, {'mql': 'TrendPeriod', 'py': 'TrendPeriod', 'param': 'TrendPeriod', 'type': 'double', 'default': 10.0, 'label': 'Trend component period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'ForecastHorizon', 'py': 'ForecastHorizon', 'param': 'ForecastHorizon', 'type': 'int', 'default': 25, 'label': 'Forecasted bars', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
EstimatePeriod = _input('EstimatePeriod', 14.33)  # Estimation component period
TrendPeriod = _input('TrendPeriod', 10.0)  # Trend component period
Price = _input('Price', pr_close)  # Price
ForecastHorizon = _input('ForecastHorizon', 25)  # Forecasted bars
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
work = Arr(0, 0.0)
forecast = Arr(0, 0.0)
forecastc = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, forecast, INDICATOR_DATA)
    SetIndexBuffer(3, forecastc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, work, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Holt's double exponential smoothing (" + _str(EstimatePeriod) + ',' + _str(TrendPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + EstimatePeriod)
    gamma = _fdiv(2.0, 1.0 + TrendPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        avg[i] = (((alpha * price) + ((1 - alpha) * (avg[i - 1] + work[i - 1]))) if (i > 0) else price)
        work[i] = (((gamma * (avg[i] - avg[i - 1])) + ((1 - gamma) * work[i - 1])) if (i > 0) else 0)
        avgc[i] = ((1 if (avg[i] > avg[i - 1]) else 2 if (avg[i] < avg[i - 1]) else avgc[i - 1]) if (i > 0) else 0)
        forecast[i] = EMPTY_VALUE
        if i == (rates_total - 1):
            forecast[i - ForecastHorizon] = avg[i]
            forecastc[i - ForecastHorizon] = (1 if (work[i] > 0) else 2)
            for f in range(ForecastHorizon - 1, 0 - 1, -1):
                forecast[i - f] = avg[i] + ((ForecastHorizon - f) * work[i])
                forecastc[i - f] = (1 if (work[i] > 0) else 2)
        i += 1
    PlotIndexSetInteger(1, PLOT_SHIFT, ForecastHorizon)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - ForecastHorizon - 1)
    manageAlerts(time, avgc, rates_total)
    return i

def manageAlerts(time, trend, bars):
    if not AlertsOn:
        return
    whichBar = bars - 1
    if not AlertsOnCurrent:
        whichBar = bars - 2
    time1 = time[whichBar]
    if trend[whichBar] != trend[whichBar - 1]:
        if trend[whichBar] == 1:
            doAlert(time1, 'up')
        if trend[whichBar] == 2:
            doAlert(time1, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + " Holt's double exponential smoothing state changed to " + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + " Holt's double exponential smoothing", message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

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

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HoltsDoubleExponentialSmoothing(_MQL5Indicator):
    name = 'Holts_double_exponential_smoothing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'EstimatePeriod': 14.33,  # Estimation component period
        'TrendPeriod': 10.0,  # Trend component period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'ForecastHorizon': 25,  # Forecasted bars
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
    }

