"""Solar Winds — converted from MQL5: MQL5 Indicators/Solar Wind Indicator for MQ5/Solar Winds.mq5

Solar Winds for MQL5
Demonstrates classic for-loop construction for re-painting and non-repainting
Has choice for using Custom Events or not
Copyright: Copyright © LukeB; Link: https://www.mql5.com/en/users/lukeb; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © LukeB', 'link': 'https://www.mql5.com/en/users/lukeb', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 8, 2: 10}, 'colors': {1: [3329330, 255], 2: [3329330, 255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Solar Winds for MQL5', 'Demonstrates classic for-loop construction for re-painting and non-repainting', 'Has choice for using Custom Events or not'], 'name': 'Solar Winds', 'source': 'MQL5 Indicators/Solar Wind Indicator for MQ5/Solar Winds.mq5', 'folder': 'Solar Wind Indicator for MQ5', 'inputs': [{'mql': 'NRP', 'py': 'NRP', 'param': 'NRP', 'type': 'int', 'default': 0, 'label': 'Non-Repainting (NPR) ON/OFF', 'sinput': False}, {'mql': 'UseEvents', 'py': 'UseEvents', 'param': 'UseEvents', 'type': 'int', 'default': 0, 'label': 'Use Custom Events ON/OFF', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 35, 'label': '', 'sinput': False}, {'mql': 'smooth', 'py': 'smooth', 'param': 'smooth', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'DoAlert', 'py': 'DoAlert', 'param': 'DoAlert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'alertMail', 'py': 'alertMail', 'param': 'alertMail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'lngLineClr', 'py': 'lngLineClr', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Long Side Line Color', 'sinput': False}, {'mql': 'shrtLineClr', 'py': 'shrtLineClr', 'param': None, 'type': 'color', 'default': 255, 'label': 'Short Side Line Color', 'sinput': False}, {'mql': 'lngHistClor', 'py': 'lngHistClor', 'param': None, 'type': 'color', 'default': 9109643, 'label': 'Long Side Histogram Color', 'sinput': False}, {'mql': 'shrtHistClor', 'py': 'shrtHistClor', 'param': None, 'type': 'color', 'default': 2763429, 'label': 'Short Side Histogram Color', 'sinput': False}, {'mql': 'Uniquifier', 'py': 'Uniquifier', 'param': 'Uniquifier', 'type': 'uint', 'default': 176, 'label': 'Make this instance unique', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CUSTOM_EVENT
CUSTOM_EVENT_RUN_INDICATOR = 130
CUSTOM_EVENT_DO_ALERTS = 150
_enum('ENUM_CUSTOM_EVENT', {130: 'CUSTOM_EVENT_RUN_INDICATOR', 150: 'CUSTOM_EVENT_DO_ALERTS'})

# enum ENUM_ON_OFF
ENUM_OFF = 0
ENUM_ON = 1
_enum('ENUM_ON_OFF', {0: 'ENUM_OFF', 1: 'ENUM_ON'})

# enum EnumPlotClrs
ENUM_LONG_CLR = 0
ENUM_SHORT_CLR = 1
_enum('EnumPlotClrs', {0: 'ENUM_LONG_CLR', 1: 'ENUM_SHORT_CLR'})

# ---- inputs and global variables
g_shortName = 'SolarWinds'
g_minBars = 0
g_maxBars = 0
g_msgString = ""
g_strUniquifier = ""
g_isTesting = False
NRP = _input('NRP', ENUM_OFF)  # Non-Repainting (NPR) ON/OFF
UseEvents = _input('UseEvents', ENUM_OFF)  # Use Custom Events ON/OFF
period = _input('period', 35)
smooth = _input('smooth', 15)
DoAlert = _input('DoAlert', True)
alertMail = _input('alertMail', False)
lngLineClr = _input('lngLineClr', clrLimeGreen)  # Long Side Line Color
shrtLineClr = _input('shrtLineClr', clrRed)  # Short Side Line Color
lngHistClor = _input('lngHistClor', clrDarkMagenta)  # Long Side Histogram Color
shrtHistClor = _input('shrtHistClor', clrBrown)  # Short Side Histogram Color
Uniquifier = _input('Uniquifier', 176)  # Make this instance unique
g_windLine = Arr(0, 0.0)
g_windLineClrIdx = Arr(0, 0.0)
g_histogram = Arr(0, 0.0)
g_histogramClrIdx = Arr(0, 0.0)
g_calcZero = Arr(0, 0.0)
g_calcOne = Arr(0, 0.0)
g_calcTwo = Arr(0, 0.0)

def OnInit():
    global g_isTesting, g_maxBars, g_minBars, g_shortName, g_strUniquifier
    retCode = INIT_SUCCEEDED
    g_shortName += IntegerToString(Uniquifier) + ('_RP' if (NRP == ENUM_OFF) else '_NRP')
    IndicatorSetString(INDICATOR_SHORTNAME, g_shortName)
    g_minBars = period
    g_maxBars = 30000 - g_minBars
    g_strUniquifier = IntegerToString(Uniquifier)
    g_isTesting = (MQLInfoInteger(MQL_TESTER) != 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    ArraySetAsSeries(g_windLine, True)
    ArraySetAsSeries(g_windLineClrIdx, True)
    ArraySetAsSeries(g_histogram, True)
    ArraySetAsSeries(g_histogramClrIdx, True)
    ArraySetAsSeries(g_calcZero, True)
    ArraySetAsSeries(g_calcOne, True)
    ArraySetAsSeries(g_calcTwo, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, g_windLine, INDICATOR_DATA)
    SetIndexBuffer(1, g_windLineClrIdx, INDICATOR_COLOR_INDEX)
    PlotIndexSetString(0, PLOT_LABEL, 'WIND_LINE' + g_strUniquifier)
    SetIndexBuffer(2, g_histogram, INDICATOR_DATA)
    SetIndexBuffer(3, g_histogramClrIdx, INDICATOR_COLOR_INDEX)
    PlotIndexSetString(1, PLOT_LABEL, 'HISTO_DECO' + g_strUniquifier)
    SetIndexBuffer(4, g_calcZero, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, g_calcOne, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, g_calcTwo, INDICATOR_CALCULATIONS)
    return retCode

def OnDeinit(reason):
    global g_msgString
    if StringLen(g_msgString) > 0:
        g_msgString = ''
        Comment(g_msgString)

def PostCustomEvent(customEvent, longParm, doubleParm, stringParm):
    global g_msgString
    postSucceeded = True
    if False:
        postSucceeded = False
    elif not EventChartCustom(ChartID(), customEvent, longParm, doubleParm, stringParm):
        errCode = GetLastError()
        g_msgString = 'Post CUSTOM_EVENT ' + IntegerToString(customEvent) + ' Failed with error ' + IntegerToString(errCode) + '.'
        Comment(g_msgString)
        Print(g_msgString)
        postSucceeded = False
    return postSucceeded

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == (CHARTEVENT_CUSTOM + CUSTOM_EVENT_RUN_INDICATOR) and sparam == g_strUniquifier:
        firstWorkBar = _int(lparam)
        RunTheIndicator(firstWorkBar)
    elif id_ == (CHARTEVENT_CUSTOM + CUSTOM_EVENT_DO_ALERTS) and sparam == g_strUniquifier:
        DoTheAlerts(g_windLine)

def GetTheFirstWorkBar(firstWorkBar, rates_total, prev_calculated, maxBars, minBars):
    global _s_GetTheFirstWorkBar_firstRun
    if prev_calculated < 1 or _s_GetTheFirstWorkBar_firstRun == True:
        firstWorkBar.v = rates_total - (minBars + 1)
        if firstWorkBar.v > (maxBars - (minBars + 1)):
            firstWorkBar.v = maxBars - (minBars + 1)
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, firstWorkBar.v)
            PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, firstWorkBar.v)
        elif firstWorkBar.v < (minBars + 1):
            return False
        _s_GetTheFirstWorkBar_firstRun = False
    else:
        firstWorkBar.v = rates_total - prev_calculated
    return True

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global g_msgString
    firstWorkBar = Box(0)
    if True != GetTheFirstWorkBar(firstWorkBar, rates_total, prev_calculated, g_maxBars, g_minBars):
        g_msgString = 'OnCalculate' + ' Failed to calculate the first work bar.  Bars total: ' + IntegerToString(rates_total) + ', Minimum required bars: ' + IntegerToString(g_minBars + 1)
        Comment(g_msgString)
        Print(g_msgString)
        return prev_calculated
    if True == g_isTesting or UseEvents == ENUM_OFF:
        if not RunTheIndicator(firstWorkBar.v):
            return prev_calculated
    else:
        if not PostCustomEvent(CUSTOM_EVENT_RUN_INDICATOR, firstWorkBar.v, 0.0, g_strUniquifier):
            return prev_calculated
    return rates_total

def RunTheIndicator(firstWorkBar):
    run_succeeded = True
    if True:
        SetCrossOverValue(firstWorkBar, g_calcZero, g_calcOne)
        MakeWindLine(firstWorkBar, g_calcOne, g_calcTwo, g_windLine, g_windLineClrIdx, g_histogram, g_histogramClrIdx)
        if True == g_isTesting or UseEvents == ENUM_OFF:
            DoTheAlerts(g_windLine)
        else:
            PostCustomEvent(CUSTOM_EVENT_DO_ALERTS, 0, 0.0, g_strUniquifier)
    else:
        run_succeeded = False
    return run_succeeded

def SetCrossOverValue(firstWorkBar, calcZero, calcOne):
    if NRP == ENUM_ON:
        for i in range(firstWorkBar, 0 - 1, -1):
            DoTheCrossOverCalc(i, calcZero, calcOne)
    else:
        for i in range(0, firstWorkBar + 1):
            DoTheCrossOverCalc(i, calcZero, calcOne)

def DoTheCrossOverCalc(workBar, calcZero, calcOne):
    global _s_DoTheCrossOverCalc_Fish, _s_DoTheCrossOverCalc_Value, _s_DoTheCrossOverCalc_Value1
    price = 0.0
    MinL = 0.0
    MaxH = 0.0
    MaxH = iHigh(Symbol(), 0, iHighest(Symbol(), 0, MODE_HIGH, period, workBar))
    MinL = iLow(Symbol(), 0, iLowest(Symbol(), 0, MODE_LOW, period, workBar))
    price = (iHigh(Symbol(), 0, workBar) + iLow(Symbol(), 0, workBar)) / 2
    _s_DoTheCrossOverCalc_Value = (0.33 * 2 * (_fdiv(price - MinL, MaxH - MinL) - 0.5)) + (0.67 * _s_DoTheCrossOverCalc_Value1)
    _s_DoTheCrossOverCalc_Value = MathMin(MathMax(_s_DoTheCrossOverCalc_Value, -0.999), 0.999)
    calcZero[workBar] = (0.5 * MathLog(_fdiv(1 + _s_DoTheCrossOverCalc_Value, 1 - _s_DoTheCrossOverCalc_Value))) + (0.5 * _s_DoTheCrossOverCalc_Fish)
    _s_DoTheCrossOverCalc_Value1 = _s_DoTheCrossOverCalc_Value
    _s_DoTheCrossOverCalc_Fish = calcZero[workBar]
    if calcZero[workBar] > 0:
        calcOne[workBar] = 10.0
    else:
        calcOne[workBar] = -10.0

def MakeWindLine(firstWorkBar, calcOne, calcTwo, windLine, windClr, histogram, histoClr):
    sum_ = 0.0
    sumw = 0.0
    weight = 0.0
    i = 0
    k = 0
    i = firstWorkBar
    for i in range(i, 0 - 1, -1):
        sum_ = 0.0
        sumw = 0.0
        k = 0
        while k < smooth and g_maxBars:
            weight = smooth - k
            sumw += weight
            sum_ += weight * calcOne[i + k]
            k += 1
        if sumw != 0:
            calcTwo[i] = _fdiv(sum_, sumw)
        else:
            calcTwo[i] = 0.0
    else:
        i = _range_end(i, 0 - 1, -1)
    i = 0
    for i in range(i, firstWorkBar + 1):
        sum_ = 0.0
        sumw = 0.0
        k = 0
        while k < smooth and (i - k) >= 0:
            weight = smooth - k
            sumw += weight
            sum_ += weight * calcTwo[i - k]
            k += 1
        if sumw != 0:
            windLine[i] = _fdiv(sum_, sumw)
            histogram[i] = windLine[i]
            windClr[i] = (ENUM_LONG_CLR if (windLine[i] > 0) else ENUM_SHORT_CLR)
            histoClr[i] = (ENUM_LONG_CLR if (windLine[i] > 0) else ENUM_SHORT_CLR)
        else:
            windLine[i] = 0.0
            histogram[i] = windLine[i]
            windClr[i] = windClr[i + 1]
            histoClr[i] = histoClr[i + 1]
    else:
        i = _range_end(i, firstWorkBar + 1, 1)

def DoTheAlerts(windLine):
    global _s_DoTheAlerts_lastAlertTime
    currentTime = iTime(Symbol(), PERIOD_CURRENT, 0)
    sAlertMsg = ""
    if _s_DoTheAlerts_lastAlertTime != currentTime:
        if windLine[1] <= 0 and windLine[0] > 0:
            if DoAlert:
                sAlertMsg = 'Solar Wind ' + g_strUniquifier + ' MQ5- ' + Symbol() + ' ' + TF2Str(Period()) + ': cross UP'
                if DoAlert:
                    Alert(sAlertMsg)
                if alertMail:
                    SendMail(sAlertMsg, ' Alert!\n' + TimeToString(currentTime, TIME_DATE | TIME_SECONDS) + '\n' + sAlertMsg)
            _s_DoTheAlerts_lastAlertTime = currentTime
        elif windLine[1] >= 0 and windLine[0] < 0:
            if DoAlert:
                sAlertMsg = 'Solar Wind ' + g_strUniquifier + ' MQ5- ' + Symbol() + ' ' + TF2Str(Period()) + ': cross DOWN'
                if DoAlert:
                    Alert(sAlertMsg)
                if alertMail:
                    SendMail(sAlertMsg, ' Alert!\n' + TimeToString(currentTime, TIME_DATE | TIME_SECONDS) + '\n' + sAlertMsg)
            _s_DoTheAlerts_lastAlertTime = currentTime

def TF2Str(iPeriod):
    retStr = ""
    _sw1 = iPeriod
    if _sw1 == PERIOD_M1:
        retStr = 'M1'
    elif _sw1 == PERIOD_M5:
        retStr = 'M5'
    elif _sw1 == PERIOD_M15:
        retStr = 'M15'
    elif _sw1 == PERIOD_M30:
        retStr = 'M30'
    elif _sw1 == PERIOD_H1:
        retStr = 'H1'
    elif _sw1 == PERIOD_H4:
        retStr = 'H4'
    elif _sw1 == PERIOD_D1:
        retStr = 'D1'
    elif _sw1 == PERIOD_W1:
        retStr = 'W1'
    elif _sw1 == PERIOD_MN1:
        retStr = 'MN1'
    else:
        retStr = 'M' + IntegerToString(iPeriod)
    return retStr

# ---- static local variables
_s_GetTheFirstWorkBar_firstRun = True
_s_DoTheCrossOverCalc_Value = 0.0
_s_DoTheCrossOverCalc_Value1 = 0.0
_s_DoTheCrossOverCalc_Fish = 0.0
_s_DoTheAlerts_lastAlertTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SolarWinds(_MQL5Indicator):
    name = 'Solar Winds'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'NRP': _Choice({0: 'ENUM_OFF', 1: 'ENUM_ON'}, default=0),  # Non-Repainting (NPR) ON/OFF
        'UseEvents': _Choice({0: 'ENUM_OFF', 1: 'ENUM_ON'}, default=0),  # Use Custom Events ON/OFF
        'period': 35,
        'smooth': 15,
        'DoAlert': True,
        'alertMail': False,
        'Uniquifier': 176,  # Make this instance unique
    }

