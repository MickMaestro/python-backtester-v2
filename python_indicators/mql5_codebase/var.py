"""VAR — converted from MQL5: MQL5 Indicators/Value Area Retracement Volume Indicator/VAR.mq5

Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.20', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'VAR', 'source': 'MQL5 Indicators/Value Area Retracement Volume Indicator/VAR.mq5', 'folder': 'Value Area Retracement Volume Indicator', 'inputs': [{'mql': 'ValueAreaPercentage', 'py': 'ValueAreaPercentage', 'param': 'ValueAreaPercentage', 'type': 'int', 'default': 70, 'label': 'Value area percentage (typically 70%)', 'sinput': False}, {'mql': 'ProfileResolution', 'py': 'ProfileResolution', 'param': 'ProfileResolution', 'type': 'int', 'default': 50, 'label': 'Number of price levels for volume profile', 'sinput': False}, {'mql': 'ProfileTimeframe', 'py': 'ProfileTimeframe', 'param': 'ProfileTimeframe', 'type': 'int', 'default': 16408, 'label': 'Timeframe for volume profile', 'sinput': False}, {'mql': 'ShowVisualElements', 'py': 'ShowVisualElements', 'param': 'ShowVisualElements', 'type': 'bool', 'default': True, 'label': 'Show visual elements on chart', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ValueAreaPercentage = _input('ValueAreaPercentage', 70)  # Value area percentage (typically 70%)
ProfileResolution = _input('ProfileResolution', 50)  # Number of price levels for volume profile
ProfileTimeframe = _input('ProfileTimeframe', PERIOD_D1)  # Timeframe for volume profile
ShowVisualElements = _input('ShowVisualElements', True)  # Show visual elements on chart
POCBuffer = Arr(0, 0.0)
VAHighBuffer = Arr(0, 0.0)
VALowBuffer = Arr(0, 0.0)
ProfileHighBuffer = Arr(0, 0.0)
ProfileLowBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
poc = 0.0
vaHigh = 0.0
vaLow = 0.0
profileHigh = 0.0
profileLow = 0.0
lastCalculationTime = 0
profileBarsToCalculate = 1  # Number of bars to calculate profile for

def OnInit():
    global lastCalculationTime, profileBarsToCalculate
    SetIndexBuffer(0, POCBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, VAHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, VALowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ProfileHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ProfileLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, SignalBuffer, INDICATOR_DATA)
    ArraySetAsSeries(POCBuffer, True)
    ArraySetAsSeries(VAHighBuffer, True)
    ArraySetAsSeries(VALowBuffer, True)
    ArraySetAsSeries(ProfileHighBuffer, True)
    ArraySetAsSeries(ProfileLowBuffer, True)
    ArraySetAsSeries(SignalBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, (DRAW_LINE if ShowVisualElements else DRAW_NONE))
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, clrBlue)
    PlotIndexSetString(0, PLOT_LABEL, 'POC')
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (DRAW_LINE if ShowVisualElements else DRAW_NONE))
    PlotIndexSetInteger(1, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, clrGreen)
    PlotIndexSetString(1, PLOT_LABEL, 'VA High')
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, (DRAW_LINE if ShowVisualElements else DRAW_NONE))
    PlotIndexSetInteger(2, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, clrGreen)
    PlotIndexSetString(2, PLOT_LABEL, 'VA Low')
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, (DRAW_LINE if ShowVisualElements else DRAW_NONE))
    PlotIndexSetInteger(3, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, clrRed)
    PlotIndexSetString(3, PLOT_LABEL, 'Profile High')
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, (DRAW_LINE if ShowVisualElements else DRAW_NONE))
    PlotIndexSetInteger(4, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, clrRed)
    PlotIndexSetString(4, PLOT_LABEL, 'Profile Low')
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, (DRAW_ARROW if ShowVisualElements else DRAW_NONE))
    PlotIndexSetInteger(5, PLOT_ARROW, 233)
    PlotIndexSetInteger(5, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, clrGold)
    PlotIndexSetString(5, PLOT_LABEL, 'Signal')
    lastCalculationTime = 0
    if ProfileTimeframe == PERIOD_MN1:
        profileBarsToCalculate = 12
    elif ProfileTimeframe == PERIOD_W1:
        profileBarsToCalculate = 4
    else:
        profileBarsToCalculate = 1
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastCalculationTime
    if rates_total < 2:
        return 0
    currentProfileTime = iTime(Symbol(), ProfileTimeframe, 0)
    if currentProfileTime == lastCalculationTime:
        return rates_total
    lastCalculationTime = currentProfileTime
    profileStart = iTime(Symbol(), ProfileTimeframe, 1)
    profileEnd = profileStart + PeriodSeconds(ProfileTimeframe) - 1
    CalculateVolumeProfile(profileStart, profileEnd)
    currentOpen = iOpen(Symbol(), Period(), 0)
    ArrayInitialize(POCBuffer, EMPTY_VALUE)
    ArrayInitialize(VAHighBuffer, EMPTY_VALUE)
    ArrayInitialize(VALowBuffer, EMPTY_VALUE)
    ArrayInitialize(ProfileHighBuffer, EMPTY_VALUE)
    ArrayInitialize(ProfileLowBuffer, EMPTY_VALUE)
    ArrayInitialize(SignalBuffer, EMPTY_VALUE)
    for i in range(0, rates_total):
        POCBuffer[i] = poc
        VAHighBuffer[i] = vaHigh
        VALowBuffer[i] = vaLow
        ProfileHighBuffer[i] = profileHigh
        ProfileLowBuffer[i] = profileLow
    timeframeStr = Box(EnumToString(ProfileTimeframe, 'ENUM_TIMEFRAMES'))
    StringReplace(timeframeStr, 'PERIOD_', '')
    if currentOpen > vaLow and currentOpen < vaHigh:
        Comment(timeframeStr.v + ' Profile: Open within Value Area. No clear signal.\n' + 'POC: ', poc, ' | VA High: ', vaHigh, ' | VA Low: ', vaLow)
    elif currentOpen > vaHigh and currentOpen < profileHigh:
        Comment(timeframeStr.v + ' Profile: Buy opportunity on retracement to POC: ', poc, '\n' + 'VA High: ', vaHigh, ' | Profile High: ', profileHigh)
        if ShowVisualElements:
            for i in range(0, rates_total):
                if MathAbs(close[i] - poc) < (0.5 * Point()):
                    SignalBuffer[i] = poc
    elif currentOpen < vaLow and currentOpen > profileLow:
        Comment(timeframeStr.v + ' Profile: Sell opportunity on retracement to POC: ', poc, '\n' + 'VA Low: ', vaLow, ' | Profile Low: ', profileLow)
        if ShowVisualElements:
            for i in range(0, rates_total):
                if MathAbs(close[i] - poc) < (0.5 * Point()):
                    SignalBuffer[i] = poc
    elif currentOpen > profileHigh:
        Comment(timeframeStr.v + ' Profile: Potential upside breakout - open above profile high: ', profileHigh)
    elif currentOpen < profileLow:
        Comment(timeframeStr.v + ' Profile: Potential downside breakout - open below profile low: ', profileLow)
    return rates_total

def CalculateVolumeProfile(startTime, endTime):
    global poc, profileHigh, profileLow, vaHigh, vaLow
    priceLevels = Arr(0, 0.0)
    volumes = Arr(0, 0)
    ArrayResize(priceLevels, ProfileResolution)
    ArrayResize(volumes, ProfileResolution)
    ArrayInitialize(volumes, 0)
    periodHigh = iHigh(Symbol(), ProfileTimeframe, 1)
    periodLow = iLow(Symbol(), ProfileTimeframe, 1)
    range_ = periodHigh - periodLow
    step = range_ / ProfileResolution
    for i in range(0, ProfileResolution):
        priceLevels[i] = periodLow + (i * step)
    m1Bars = iBars(Symbol(), PERIOD_M1)
    for i in range(0, m1Bars):
        time = iTime(Symbol(), PERIOD_M1, i)
        if time >= startTime and time <= endTime:
            high = iHigh(Symbol(), PERIOD_M1, i)
            low = iLow(Symbol(), PERIOD_M1, i)
            volume = iVolume(Symbol(), PERIOD_M1, i)
            for j in range(0, ProfileResolution):
                if priceLevels[j] >= low and priceLevels[j] <= high:
                    volumes[j] += volume
    maxVolume = 0
    pocIndex = 0
    for i in range(0, ProfileResolution):
        if volumes[i] > maxVolume:
            maxVolume = volumes[i]
            pocIndex = i
    poc = priceLevels[pocIndex]
    profileHigh = periodHigh
    profileLow = periodLow
    totalVolume = 0
    for i in range(0, ProfileResolution):
        totalVolume += volumes[i]
    valueAreaVolume = _idiv(totalVolume * ValueAreaPercentage, 100)
    currentVAVolume = 0
    vaHighIndex = pocIndex
    vaLowIndex = pocIndex
    while currentVAVolume < valueAreaVolume:
        if vaHighIndex < (ProfileResolution - 1):
            vaHighIndex += 1
            currentVAVolume += volumes[vaHighIndex]
            if currentVAVolume >= valueAreaVolume:
                break
        if vaLowIndex > 0:
            vaLowIndex -= 1
            currentVAVolume += volumes[vaLowIndex]
        if vaHighIndex >= (ProfileResolution - 1) and vaLowIndex <= 0:
            break
    vaHigh = priceLevels[vaHighIndex]
    vaLow = priceLevels[vaLowIndex]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VAR(_MQL5Indicator):
    name = 'VAR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ValueAreaPercentage': 70,  # Value area percentage (typically 70%)
        'ProfileResolution': 50,  # Number of price levels for volume profile
        'ProfileTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Timeframe for volume profile
        'ShowVisualElements': True,  # Show visual elements on chart
    }

