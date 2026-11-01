"""Volume Candles — converted from MQL5: MQL5 Indicators/Bar or Volume Colored Candlesticks/Volume Candles.mq5

Volume Colored Candlestick with Bollinger Bands as the Standard Deviation
Copyright: 2021, Mateus Matucuma Teixeira; Link: https://github.com/BRMateus2/; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2021, Mateus Matucuma Teixeira', 'link': 'https://github.com/BRMateus2/', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Volume Colored Candlestick with Bollinger Bands as the Standard Deviation'], 'name': 'Volume Candles', 'source': 'MQL5 Indicators/Bar or Volume Colored Candlesticks/Volume Candles.mq5', 'folder': 'Bar or Volume Colored Candlesticks', 'inputs': [{'mql': 'iPeriodInp', 'py': 'iPeriodInp', 'param': 'iPeriodInp', 'type': 'int', 'default': 1440, 'label': 'Period of Bollinger Bands', 'sinput': False}, {'mql': 'iBandsDev', 'py': 'iBandsDev', 'param': 'iBandsDev', 'type': 'double', 'default': 2.0, 'label': 'Bollinger Bands Standard Deviation', 'sinput': False}, {'mql': 'iSensitivity', 'py': 'iSensitivity', 'param': 'iSensitivity', 'type': 'double', 'default': 1.0, 'label': 'Sensitivity, default 1.0, lower means less sensitive', 'sinput': False}, {'mql': 'iShowIndicators', 'py': 'iShowIndicators', 'param': 'iShowIndicators', 'type': 'bool', 'default': False, 'label': 'Calibration: show calculation indicators in chart', 'sinput': False}, {'mql': 'iShowGradient', 'py': 'iShowGradient', 'param': 'iShowGradient', 'type': 'bool', 'default': False, 'label': 'Calibration: show gradients in chart', 'sinput': False}, {'mql': 'cLow', 'py': 'cLow', 'param': None, 'type': 'color', 'default': 15786048, 'label': 'Low Volume', 'sinput': False}, {'mql': 'cAvg', 'py': 'cAvg', 'param': None, 'type': 'color', 'default': 61664, 'label': 'Average Volume', 'sinput': False}, {'mql': 'cHigh', 'py': 'cHigh', 'param': None, 'type': 'color', 'default': 2105599, 'label': 'High Volume', 'sinput': False}, {'mql': 'ENUM_APPLIED_VOLUMEInp', 'py': 'ENUM_APPLIED_VOLUMEInp', 'param': 'ENUM_APPLIED_VOLUMEInp', 'type': 'int', 'default': 0, 'label': 'Volume by "Ticks" or by "Real"', 'sinput': False}, {'mql': 'adPeriodInp', 'py': 'adPeriodInp', 'param': 'adPeriodInp', 'type': 'bool', 'default': True, 'label': 'Adapt the Period? Overrides Standard Period Settings', 'sinput': False}, {'mql': 'adPeriodMinutesInp', 'py': 'adPeriodMinutesInp', 'param': 'adPeriodMinutesInp', 'type': 'int', 'default': 27600, 'label': 'Period in minutes that all M and H timeframes should adapt to?', 'sinput': False}, {'mql': 'adPeriodD1Inp', 'py': 'adPeriodD1Inp', 'param': 'adPeriodD1Inp', 'type': 'int', 'default': 20, 'label': 'Period for D1 - Daily Timeframe', 'sinput': False}, {'mql': 'adPeriodW1Inp', 'py': 'adPeriodW1Inp', 'param': 'adPeriodW1Inp', 'type': 'int', 'default': 4, 'label': 'Period for W1 - Weekly Timeframe', 'sinput': False}, {'mql': 'adPeriodMN1Inp', 'py': 'adPeriodMN1Inp', 'param': 'adPeriodMN1Inp', 'type': 'int', 'default': 1, 'label': 'Period for MN - Monthly Timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iName = 'VolumeCandles'
iPeriodInp = _input('iPeriodInp', 1440)  # Period of Bollinger Bands
iPeriod = 60  # Backup iPeriod if user inserts wrong value
iBandsDev = _input('iBandsDev', 2.0)  # Bollinger Bands Standard Deviation
iSensitivity = _input('iSensitivity', 1.0)  # Sensitivity, default 1.0, lower means less sensitive
iShowIndicators = _input('iShowIndicators', False)  # Calibration: show calculation indicators in chart
iShowGradient = _input('iShowGradient', False)  # Calibration: show gradients in chart
cLow = _input('cLow', 0xF0E040)  # Low Volume
cAvg = _input('cAvg', 0x00F0E0)  # Average Volume
cHigh = _input('cHigh', 0x2020FF)  # High Volume
cCount = 2  # Counter of gradient variations (cLow->cMean is one, cMean->cHigh is the second)
cGradientSize = 63  # Has a platform limit of 64! There is also some math craziness to make the gradients fit all colors without loss
cGradientParts = _idiv(cGradientSize, cCount)  # Counter of the parts
ENUM_APPLIED_VOLUMEInp = _input('ENUM_APPLIED_VOLUMEInp', VOLUME_TICK)  # Volume by "Ticks" or by "Real"
adPeriodInp = _input('adPeriodInp', True)  # Adapt the Period? Overrides Standard Period Settings
adPeriodMinutesInp = _input('adPeriodMinutesInp', 27600)  # Period in minutes that all M and H timeframes should adapt to?
adPeriodD1Inp = _input('adPeriodD1Inp', 20)  # Period for D1 - Daily Timeframe
adPeriodW1Inp = _input('adPeriodW1Inp', 4)  # Period for W1 - Weekly Timeframe
adPeriodMN1Inp = _input('adPeriodMN1Inp', 1)  # Period for MN - Monthly Timeframe
iVolHandle = 0
iBandsBufUpperI = 5
iBandsBufMiddleI = 6
iBandsBufLowerI = 7
iBandsHandle = 0
iBandsBufUpper = Arr.of([], fill=0.0)
iBandsBufMiddle = Arr.of([], fill=0.0)
iBandsBufLower = Arr.of([], fill=0.0)
iBufOpenI = 0  # Index for Open Buffer values, also this is the first index and is the most important for setting the next plots
iBufOpen = Arr.of([], fill=0.0)  # Open Buffer values
iBufHighI = 1
iBufHigh = Arr.of([], fill=0.0)
iBufLowI = 2
iBufLow = Arr.of([], fill=0.0)
iBufCloseI = 3
iBufClose = Arr.of([], fill=0.0)
iBufColorI = 4
iBufColor = Arr.of([], fill=0.0)
subwindow = 0  # Subwindow which iShowIndicators will be used
iVolName = ''  # Should be released if created
iBandsName = ''  # Should be released if created

def OnInit():
    global iBandsHandle, iBandsName, iName, iPeriod, iVolHandle, iVolName, subwindow
    if adPeriodInp == True:
        if PeriodSeconds(PERIOD_CURRENT) < PeriodSeconds(PERIOD_D1) and PeriodSeconds(PERIOD_CURRENT) >= PeriodSeconds(PERIOD_M1):
            if adPeriodMinutesInp > 0:
                iPeriodCalc = _idiv(adPeriodMinutesInp * 60, PeriodSeconds(PERIOD_CURRENT))
                if iPeriodCalc == 0:
                    iPeriod = iPeriodCalc + 1
                elif iPeriod < 0:
                    Print('ERROR: ' + 'calculation error with "iPeriod = ((adPeriodMinutesInp * 60) / PeriodSeconds(PERIOD_CURRENT))". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(111) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
                    ResetLastError()
                    DebugBreak()
                else:
                    iPeriod = iPeriodCalc
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodMinutesInp" = "' + IntegerToString(adPeriodMinutesInp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(116) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
                ResetLastError()
                DebugBreak()
        elif PeriodSeconds(PERIOD_CURRENT) == PeriodSeconds(PERIOD_D1):
            if adPeriodD1Inp > 0:
                iPeriod = adPeriodD1Inp
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodD1Inp" = "' + IntegerToString(adPeriodD1Inp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(122) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
                ResetLastError()
                DebugBreak()
        elif PeriodSeconds(PERIOD_CURRENT) == PeriodSeconds(PERIOD_W1):
            if adPeriodW1Inp > 0:
                iPeriod = adPeriodW1Inp
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodW1Inp" = "' + IntegerToString(adPeriodW1Inp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(128) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
                ResetLastError()
                DebugBreak()
        elif PeriodSeconds(PERIOD_CURRENT) == PeriodSeconds(PERIOD_MN1):
            if adPeriodMN1Inp > 0:
                iPeriod = adPeriodMN1Inp
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodMN1Inp" = "' + IntegerToString(adPeriodMN1Inp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(134) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
                ResetLastError()
                DebugBreak()
        else:
            Print('ERROR: ' + 'untreated condition. Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(137) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
            ResetLastError()
            DebugBreak()
    elif iPeriodInp <= 0 and adPeriodInp == False:
        Print('ERROR: ' + 'wrong value for "iPeriodInp" = "' + IntegerToString(iPeriodInp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(140) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
    else:
        iPeriod = iPeriodInp
    if iSensitivity < 0.001:
        Print('ERROR: ' + 'Sensitivity cannot be smaller than 0.001' + ' at "' + 'OnInit' + ':' + IntegerToString(146) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_PARAMETERS_INCORRECT
    if _imod(cGradientSize, cCount) != 1:
        Print('ERROR: ' + "cGradientSize is not divisible by cCount without there being one free slot, as for the fact that [cGradients; ...; cGradients] can't be closed correctly" + ' at "' + 'OnInit' + ':' + IntegerToString(151) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_PARAMETERS_INCORRECT
    iVolHandle = iVolumes(Symbol(), Period(), ENUM_APPLIED_VOLUMEInp)
    if iVolHandle == INVALID_HANDLE or iVolHandle < 0:
        Print('ERROR: ' + 'iVolHandle == INVALID_HANDLE || iVolHandle < 0' + ' at "' + 'OnInit' + ':' + IntegerToString(158) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    iBandsHandle = iBands(Symbol(), Period(), iPeriod, 0, iBandsDev, iVolHandle)
    if iBandsHandle == INVALID_HANDLE or iBandsHandle < 0:
        Print('ERROR: ' + 'iBandsHandle == INVALID_HANDLE || iBandsHandle < 0' + ' at "' + 'OnInit' + ':' + IntegerToString(163) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if iShowIndicators:
        subwindow = _int(ChartGetInteger(ChartID(), CHART_WINDOWS_TOTAL))
        if not ChartIndicatorAdd(ChartID(), subwindow, iVolHandle):
            Print('ERROR: ' + '!ChartIndicatorAdd(ChartID(), subwindow, iVolHandle)' + ' at "' + 'OnInit' + ':' + IntegerToString(170) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
            ResetLastError()
            DebugBreak()
            return INIT_FAILED
        iVolName = ChartIndicatorName(ChartID(), subwindow, 0)
        if not ChartIndicatorAdd(ChartID(), subwindow, iBandsHandle):
            Print('ERROR: ' + '!ChartIndicatorAdd(ChartID(), subwindow, iBandsHandle)' + ' at "' + 'OnInit' + ':' + IntegerToString(175) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
            ResetLastError()
            DebugBreak()
            return INIT_FAILED
        iBandsName = ChartIndicatorName(ChartID(), subwindow, 1)
    if not SetIndexBuffer(iBufOpenI, iBufOpen, INDICATOR_DATA):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(182) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBufHighI, iBufHigh, INDICATOR_DATA):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(186) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBufLowI, iBufLow, INDICATOR_DATA):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(190) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBufCloseI, iBufClose, INDICATOR_DATA):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(194) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBufColorI, iBufColor, INDICATOR_COLOR_INDEX):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(198) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not PlotIndexSetInteger(iBufOpenI, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(203) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not PlotIndexSetDouble(iBufOpenI, PLOT_EMPTY_VALUE, DBL_MIN):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(208) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cGradientSize):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(212) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBandsBufUpperI, iBandsBufUpper, INDICATOR_CALCULATIONS):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(216) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBandsBufMiddleI, iBandsBufMiddle, INDICATOR_CALCULATIONS):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(220) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    if not SetIndexBuffer(iBandsBufLowerI, iBandsBufLower, INDICATOR_CALCULATIONS):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(224) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    i = 0
    while i < cGradientParts:
        PlotIndexSetInteger(iBufOpenI, PLOT_LINE_COLOR, i, argbGradient(cLow, cAvg, 1.0 - ((float(cGradientParts) - i) / cGradientParts)))
        PlotIndexSetInteger(iBufOpenI, PLOT_LINE_COLOR, i + cGradientParts, argbGradient(cAvg, cHigh, 1.0 - ((float(cGradientParts) - i) / cGradientParts)))
        i += 1
    PlotIndexSetInteger(iBufOpenI, PLOT_LINE_COLOR, cGradientSize - 1, argbGradient(cAvg, cHigh, 1.0))
    iName = StringFormat('VC(%d)', iPeriod)
    if not IndicatorSetString(INDICATOR_SHORTNAME, iName):
        Print('ERROR: ' + 'IndicatorSetString(INDICATOR_SHORTNAME, iName)' + ' at "' + 'OnInit' + ':' + IntegerToString(237) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    PlotIndexSetString(iBufOpenI, PLOT_LABEL, 'Open;' + 'High;' + 'Low;' + 'Close')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if iShowIndicators:
        ChartIndicatorDelete(ChartID(), subwindow, iVolName)
        ChartIndicatorDelete(ChartID(), subwindow, iBandsName)
    IndicatorRelease(iVolHandle)
    IndicatorRelease(iBandsHandle)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_chartBars, _s_OnCalculate_chartBarsLast, _s_OnCalculate_iShowGradientBars, _s_OnCalculate_iShowGradientColors
    _s_OnCalculate_chartBars = Bars(Symbol(), PERIOD_CURRENT)
    if _s_OnCalculate_chartBars != _s_OnCalculate_chartBarsLast and (not iShowGradient):
        if _s_OnCalculate_chartBars != 0 and _s_OnCalculate_chartBars < iPeriod:
            Print('ERROR: ' + 'not enough past data to calculate, the Indicator has "' + IntegerToString(_s_OnCalculate_chartBars) + '" bars and needs "' + IntegerToString(iPeriod) + '" bars' + ' at "' + 'OnCalculate' + ':' + IntegerToString(278) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
            ResetLastError()
            DebugBreak()
        _s_OnCalculate_chartBarsLast = _s_OnCalculate_chartBars
        i = 0
        while i < iPeriod and i < rates_total:
            iBufOpen[i] = DBL_MIN
            i += 1
    if rates_total < iPeriod:
        return 0
    elif BarsCalculated(iVolHandle) < rates_total or BarsCalculated(iBandsHandle) < rates_total:
        return 0
    if (CopyBuffer(iBandsHandle, 1, 0, rates_total - prev_calculated + 1, iBandsBufUpper) <= 0 or CopyBuffer(iBandsHandle, 0, 0, rates_total - prev_calculated + 1, iBandsBufMiddle) <= 0) or CopyBuffer(iBandsHandle, 2, 0, rates_total - prev_calculated + 1, iBandsBufLower) <= 0:
        Print('ERROR: ' + '' + ' at "' + 'OnCalculate' + ':' + IntegerToString(291) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Volume Candles.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return 0
    i = ((prev_calculated - 1) if ((prev_calculated - 1) > iPeriod) else 0 if iShowGradient else iPeriod)
    while i < rates_total:
        iBufOpen[i] = open[i]
        iBufHigh[i] = high[i]
        iBufLow[i] = low[i]
        iBufClose[i] = close[i]
        if (tick_volume[i] if (ENUM_APPLIED_VOLUMEInp == VOLUME_TICK) else volume[i]) > iBandsBufMiddle[i]:
            indexColor = MathRound(iSensitivity * _fdiv(((tick_volume[i] - iBandsBufMiddle[i]) if (ENUM_APPLIED_VOLUMEInp == VOLUME_TICK) else (volume[i] - iBandsBufMiddle[i])), (1.0 if ((iBandsBufUpper[i] - iBandsBufMiddle[i]) == 0.0) else (iBandsBufUpper[i] - iBandsBufMiddle[i]))) * float(cGradientParts)) + cGradientParts
            if indexColor < cGradientParts:
                indexColor = cGradientParts
            elif indexColor >= cGradientSize:
                indexColor = cGradientSize - 1
            iBufColor[i] = indexColor
        else:
            indexColor = MathRound((1.0 / iSensitivity) * _fdiv(((tick_volume[i] - (0.0 if (iBandsBufLower[i] < 0.0) else iBandsBufLower[i])) if (ENUM_APPLIED_VOLUMEInp == VOLUME_TICK) else (volume[i] - (0.0 if (iBandsBufLower[i] < 0.0) else iBandsBufLower[i]))), (1.0 if ((iBandsBufMiddle[i] - (0.0 if (iBandsBufLower[i] < 0.0) else iBandsBufLower[i])) == 0.0) else (iBandsBufMiddle[i] - (0.0 if (iBandsBufLower[i] < 0.0) else iBandsBufLower[i])))) * float(cGradientParts))
            if indexColor < 0.0:
                indexColor = 0.0
            elif indexColor > cGradientParts:
                indexColor = cGradientParts - 1
            iBufColor[i] = indexColor
        if iShowGradient:
            iBufColor[i] = _s_OnCalculate_iShowGradientColors
            if _s_OnCalculate_iShowGradientBars != Bars(Symbol(), PERIOD_CURRENT):
                _s_OnCalculate_iShowGradientColors += 1
            if _s_OnCalculate_iShowGradientColors >= cGradientSize:
                _s_OnCalculate_iShowGradientColors = 0
        i += 1
    if iShowGradient:
        _s_OnCalculate_iShowGradientBars = Bars(Symbol(), PERIOD_CURRENT)
    return rates_total

def argbGradient(c1, c2, gradient=0.5, alpha=0.0):
    c = 0x00000000
    if gradient > 1.0:
        gradient = 1.0
    elif gradient < 0.0:
        gradient = 0.0
    if alpha > 1.0:
        alpha = 1.0
    elif alpha < 0.0:
        alpha = 0.0
    red1 = c1 & 0xFF
    green1 = (c1 & 0xFF00) >> 8
    blue1 = (c1 & 0xFF0000) >> 16
    alpha1 = (c1 & 0xFF000000) >> 24
    red2 = c2 & 0xFF
    green2 = (c2 & 0xFF00) >> 8
    blue2 = (c2 & 0xFF0000) >> 16
    alpha2 = (c2 & 0xFF000000) >> 24
    if red1 > red2:
        c = (red1 - _uint((red1 - red2) * gradient)) & 0xFF
    else:
        c = (red1 + _uint((red2 - red1) * gradient)) & 0xFF
    if green1 > green2:
        c = _uint(((green1 - _uint((green1 - green2) * gradient)) & 0xFF) << 8) + c
    else:
        c = _uint(((green1 + _uint((green2 - green1) * gradient)) & 0xFF) << 8) + c
    if blue1 > blue2:
        c = _uint(((blue1 - _uint((blue1 - blue2) * gradient)) & 0xFF) << 16) + c
    else:
        c = _uint(((blue1 + _uint((blue2 - blue1) * gradient)) & 0xFF) << 16) + c
    if alpha1 > alpha2:
        c = _uint(((alpha1 - _uint((alpha1 - alpha2) * alpha)) & 0xFF) << 24) + c
    else:
        c = _uint(((alpha1 + _uint((alpha2 - alpha1) * alpha)) & 0xFF) << 24) + c
    return c

# ---- static local variables
_s_OnCalculate_chartBars = 0
_s_OnCalculate_chartBarsLast = 0
_s_OnCalculate_iShowGradientColors = 0
_s_OnCalculate_iShowGradientBars = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeCandles(_MQL5Indicator):
    name = 'Volume Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriodInp': 1440,  # Period of Bollinger Bands
        'iBandsDev': 2.0,  # Bollinger Bands Standard Deviation
        'iSensitivity': 1.0,  # Sensitivity, default 1.0, lower means less sensitive
        'iShowIndicators': False,  # Calibration: show calculation indicators in chart
        'iShowGradient': False,  # Calibration: show gradients in chart
        'ENUM_APPLIED_VOLUMEInp': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume by "Ticks" or by "Real"
        'adPeriodInp': True,  # Adapt the Period? Overrides Standard Period Settings
        'adPeriodMinutesInp': 27600,  # Period in minutes that all M and H timeframes should adapt to?
        'adPeriodD1Inp': 20,  # Period for D1 - Daily Timeframe
        'adPeriodW1Inp': 4,  # Period for W1 - Weekly Timeframe
        'adPeriodMN1Inp': 1,  # Period for MN - Monthly Timeframe
    }

