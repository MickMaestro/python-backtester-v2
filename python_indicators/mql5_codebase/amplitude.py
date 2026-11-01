"""Amplitude — converted from MQL5: MQL5 Indicators/Amplitude (Minimum Maximum) Indicator/Amplitude.mq5

This Indicator will show the Amplitude [Minimum; Maximum] of a given period and can act as a substitute of the ATR indicator.\\n
The indicator can be used to observe volatility and the force of past swings, useful to determine excesses that will possibly be reversed or repeated, given that the user has knowledge to complement with volume or standard-deviation strategies.\\n
It is suggested a period of 55200 at M1 or 2400 at H1 (meaning 40 sessions of 23hs each), or any period that complements your strategy.
Copyright: 2021, Mateus Matucuma Teixeira; Link: https://github.com/BRMateus2/Amplitude-Indicator/; Version: 1.05

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2021, Mateus Matucuma Teixeira', 'link': 'https://github.com/BRMateus2/Amplitude-Indicator/', 'version': '1.05', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['This Indicator will show the Amplitude [Minimum; Maximum] of a given period and can act as a substitute of the ATR indicator.\\n', 'The indicator can be used to observe volatility and the force of past swings, useful to determine excesses that will possibly be reversed or repeated, given that the user has knowledge to complement with volume or standard-deviation strategies.\\n', 'It is suggested a period of 55200 at M1 or 2400 at H1 (meaning 40 sessions of 23hs each), or any period that complements your strategy.'], 'name': 'Amplitude', 'source': 'MQL5 Indicators/Amplitude (Minimum Maximum) Indicator/Amplitude.mq5', 'folder': 'Amplitude (Minimum Maximum) Indicator', 'inputs': [{'mql': 'iPeriodInp', 'py': 'iPeriodInp', 'param': 'iPeriodInp', 'type': 'int', 'default': 2400, 'label': 'Amplitude of last N candles', 'sinput': False}, {'mql': 'iIgnoreGapsInp', 'py': 'iIgnoreGapsInp', 'param': 'iIgnoreGapsInp', 'type': 'bool', 'default': False, 'label': 'Ignore gaps between candles? (Not include last close?)', 'sinput': False}, {'mql': 'iShowPercentageInp', 'py': 'iShowPercentageInp', 'param': 'iShowPercentageInp', 'type': 'bool', 'default': True, 'label': 'Show percentage instead of absolute values? (V*100 / (H+L)/2)', 'sinput': False}, {'mql': 'adPeriodInp', 'py': 'adPeriodInp', 'param': 'adPeriodInp', 'type': 'bool', 'default': True, 'label': 'Adapt the Period? Overrides Standard Period Settings', 'sinput': False}, {'mql': 'adPeriodMinutesInp', 'py': 'adPeriodMinutesInp', 'param': 'adPeriodMinutesInp', 'type': 'int', 'default': 55200, 'label': 'Period in minutes that all M and H timeframes should adapt to?', 'sinput': False}, {'mql': 'adPeriodD1Inp', 'py': 'adPeriodD1Inp', 'param': 'adPeriodD1Inp', 'type': 'int', 'default': 40, 'label': 'Period for D1 - Daily Timeframe', 'sinput': False}, {'mql': 'adPeriodW1Inp', 'py': 'adPeriodW1Inp', 'param': 'adPeriodW1Inp', 'type': 'int', 'default': 8, 'label': 'Period for W1 - Weekly Timeframe', 'sinput': False}, {'mql': 'adPeriodMN1Inp', 'py': 'adPeriodMN1Inp', 'param': 'adPeriodMN1Inp', 'type': 'int', 'default': 2, 'label': 'Period for MN - Monthly Timeframe', 'sinput': False}, {'mql': 'iBufColor', 'py': 'iBufColor', 'param': None, 'type': 'color', 'default': 13688896, 'label': 'Drawing Color', 'sinput': False}, {'mql': 'iBufStyle', 'py': 'iBufStyle', 'param': 'iBufStyle', 'type': 'int', 'default': 0, 'label': 'Drawing Style', 'sinput': False}, {'mql': 'iBufWidth', 'py': 'iBufWidth', 'param': 'iBufWidth', 'type': 'int', 'default': 1, 'label': 'Drawing Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iName = ""  # Defined at OnInit()
iPeriodInp = _input('iPeriodInp', 2400)  # Amplitude of last N candles
iPeriod = 60  # Backup iPeriod if user inserts wrong value
iIgnoreGapsInp = _input('iIgnoreGapsInp', False)  # Ignore gaps between candles? (Not include last close?)
iShowPercentageInp = _input('iShowPercentageInp', True)  # Show percentage instead of absolute values? (V*100 / (H+L)/2)
iShift = 0  # Shift data
adPeriodInp = _input('adPeriodInp', True)  # Adapt the Period? Overrides Standard Period Settings
adPeriodMinutesInp = _input('adPeriodMinutesInp', 55200)  # Period in minutes that all M and H timeframes should adapt to?
adPeriodD1Inp = _input('adPeriodD1Inp', 40)  # Period for D1 - Daily Timeframe
adPeriodW1Inp = _input('adPeriodW1Inp', 8)  # Period for W1 - Weekly Timeframe
adPeriodMN1Inp = _input('adPeriodMN1Inp', 2)  # Period for MN - Monthly Timeframe
iBufIndex = 0
iBuf = Arr(0, 0.0)
iBufLabel = 'Amplitude'
iBufColor = _input('iBufColor', clrTurquoise)  # Drawing Color
iBufDraw = DRAW_LINE  # Drawing Type
iBufStyle = _input('iBufStyle', STYLE_SOLID)  # Drawing Style
iBufWidth = _input('iBufWidth', 1)  # Drawing Width
last = 0

def OnInit():
    global iName, iPeriod
    if adPeriodInp == True:
        if PeriodSeconds(PERIOD_CURRENT) < PeriodSeconds(PERIOD_D1) and PeriodSeconds(PERIOD_CURRENT) >= PeriodSeconds(PERIOD_M1):
            if adPeriodMinutesInp > 0:
                iPeriodCalc = _idiv(adPeriodMinutesInp * 60, PeriodSeconds(PERIOD_CURRENT))
                if iPeriodCalc == 0:
                    iPeriod = iPeriodCalc + 1
                elif iPeriod < 0:
                    Print('ERROR: ' + 'calculation error with "iPeriod = ((adPeriodMinutesInp * 60) / PeriodSeconds(PERIOD_CURRENT))". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(86) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                    ResetLastError()
                    DebugBreak()
                else:
                    iPeriod = iPeriodCalc
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodMinutesInp" = "' + IntegerToString(adPeriodMinutesInp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(91) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                ResetLastError()
                DebugBreak()
        elif PeriodSeconds(PERIOD_CURRENT) == PeriodSeconds(PERIOD_D1):
            if adPeriodD1Inp > 0:
                iPeriod = adPeriodD1Inp
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodD1Inp" = "' + IntegerToString(adPeriodD1Inp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(97) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                ResetLastError()
                DebugBreak()
        elif PeriodSeconds(PERIOD_CURRENT) == PeriodSeconds(PERIOD_W1):
            if adPeriodW1Inp > 0:
                iPeriod = adPeriodW1Inp
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodW1Inp" = "' + IntegerToString(adPeriodW1Inp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(103) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                ResetLastError()
                DebugBreak()
        elif PeriodSeconds(PERIOD_CURRENT) == PeriodSeconds(PERIOD_MN1):
            if adPeriodMN1Inp > 0:
                iPeriod = adPeriodMN1Inp
            else:
                Print('ERROR: ' + 'wrong value for "adPeriodMN1Inp" = "' + IntegerToString(adPeriodMN1Inp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(109) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                ResetLastError()
                DebugBreak()
        else:
            Print('ERROR: ' + 'untreated condition. Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(112) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
    elif iPeriodInp <= 0 and adPeriodInp == False:
        Print('ERROR: ' + 'wrong value for "iPeriodInp" = "' + IntegerToString(iPeriodInp) + '". Indicator will use value "' + IntegerToString(iPeriod) + '" for calculations.' + ' at "' + 'OnInit' + ':' + IntegerToString(115) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    else:
        iPeriod = iPeriodInp
    if iShowPercentageInp:
        if not IndicatorSetInteger(INDICATOR_DIGITS, 2):
            Print('ERROR: ' + 'IndicatorSetInteger(INDICATOR_DIGITS, 2)' + ' at "' + 'OnInit' + ':' + IntegerToString(122) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
            return INIT_FAILED
    else:
        if not IndicatorSetInteger(INDICATOR_DIGITS, iDigits):
            Print('ERROR: ' + 'IndicatorSetInteger(INDICATOR_DIGITS, iDigits)' + ' at "' + 'OnInit' + ':' + IntegerToString(127) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
            return INIT_FAILED
    if not PlotIndexConstruct(iBufIndex, iBufLabel, iBufColor, iBuf, INDICATOR_DATA, iBufDraw, iShift, iBufStyle, iBufWidth, iPeriod):
        Print('ERROR: ' + '' + ' at "' + 'OnInit' + ':' + IntegerToString(133) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    iName = StringFormat('A(%d)', iPeriod)
    if not IndicatorSetString(INDICATOR_SHORTNAME, iName):
        Print('ERROR: ' + 'IndicatorSetString(INDICATOR_SHORTNAME, iName)' + ' at "' + 'OnInit' + ':' + IntegerToString(138) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global last
    if rates_total < iPeriod:
        return 0
    i = prev_calculated - 1
    while i < rates_total:
        if i < 0:
            i += 1
            continue
        highest = DBL_MIN
        lowest = DBL_MAX
        for j in range(i - iPeriod + 1, i + 1):
            if j < 0:
                continue
            if highest < (high[j] if iIgnoreGapsInp else high[j] if (j == 0) else MathMax(high[j], close[j - 1])):
                highest = (high[j] if iIgnoreGapsInp else high[j] if (j == 0) else MathMax(high[j], close[j - 1]))
            if lowest > (low[j] if iIgnoreGapsInp else low[j] if (j == 0) else MathMin(low[j], close[j - 1])):
                lowest = (low[j] if iIgnoreGapsInp else low[j] if (j == 0) else MathMin(low[j], close[j - 1]))
        iBuf[i] = (_fdiv((highest - lowest) * 100.0, MathAbs(highest + lowest) / 2.0) if iShowPercentageInp else (highest - lowest))
        i += 1
    if i == rates_total and last < TimeCurrent():
        last = TimeCurrent()
        if iShowPercentageInp:
            if not PlotIndexSetString(iBufIndex, PLOT_LABEL, 'Relative Amplitude (' + DoubleToString(iBuf[i - 1], 2) + '%)'):
                Print('ERROR: ' + '!PlotIndexSetString(iBufIndex, PLOT_LABEL, "Relative Amplitude (" + DoubleToString(iBuf[i - 1], 2) + "%)")' + ' at "' + 'OnCalculate' + ':' + IntegerToString(197) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                ResetLastError()
                DebugBreak()
        else:
            if not PlotIndexSetString(iBufIndex, PLOT_LABEL, 'Absolute Amplitude (' + DoubleToString(iBuf[i - 1], iDigits) + ')'):
                Print('ERROR: ' + '!PlotIndexSetString(iBufIndex, PLOT_LABEL, "Absolute Amplitude (" + DoubleToString(iBuf[i - 1], iDigits) + ")")' + ' at "' + 'OnCalculate' + ':' + IntegerToString(201) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
                ResetLastError()
                DebugBreak()
    return rates_total

def OnDeinit(reason):
    return

def PlotIndexConstruct(plotIndex, plotLabel, plotColor, plotBuffer, plotIndexType=INDICATOR_DATA, plotDraw=DRAW_LINE, plotShift=0, plotStyle=STYLE_SOLID, plotWidth=1, plotBegin=0, plotShowOnDatawindow=True, plotEmptyValue=0.0):
    success = True
    if not SetIndexBuffer(plotIndex, plotBuffer, plotIndexType):
        Print('ERROR: ' + '!SetIndexBuffer(plotIndex, plotBuffer, plotIndexType)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(236) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if not PlotIndexSetString(plotIndex, PLOT_LABEL, plotLabel):
        Print('ERROR: ' + '!PlotIndexSetString(plotIndex, PLOT_LABEL, plotLabel)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(240) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if not PlotIndexSetInteger(plotIndex, PLOT_LINE_COLOR, plotColor):
        Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_LINE_COLOR, plotColor)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(244) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if plotDraw != DRAW_ARROW:
        if not PlotIndexSetInteger(plotIndex, PLOT_DRAW_TYPE, plotDraw):
            Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_DRAW_TYPE, plotDraw)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(249) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
            success = False
        if not PlotIndexSetInteger(plotIndex, PLOT_SHIFT, plotShift):
            Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_SHIFT, plotShift)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(253) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
            success = False
    else:
        if not PlotIndexSetInteger(plotIndex, PLOT_DRAW_TYPE, plotDraw):
            Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_DRAW_TYPE, plotDraw)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(258) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
            success = False
        if not PlotIndexSetInteger(plotIndex, PLOT_ARROW_SHIFT, plotShift):
            Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_ARROW_SHIFT, plotShift)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(262) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
            ResetLastError()
            DebugBreak()
            success = False
    if not PlotIndexSetInteger(plotIndex, PLOT_LINE_STYLE, plotStyle):
        Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_LINE_STYLE, plotStyle)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(267) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if not PlotIndexSetInteger(plotIndex, PLOT_LINE_WIDTH, plotWidth):
        Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_LINE_WIDTH, plotWidth)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(271) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if not PlotIndexSetInteger(plotIndex, PLOT_DRAW_BEGIN, plotBegin):
        Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_DRAW_BEGIN, plotBegin)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(275) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if not PlotIndexSetInteger(plotIndex, PLOT_SHOW_DATA, plotShowOnDatawindow):
        Print('ERROR: ' + '!PlotIndexSetInteger(plotIndex, PLOT_SHOW_DATA, plotShowOnDatawindow)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(279) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    if not PlotIndexSetDouble(plotIndex, PLOT_EMPTY_VALUE, plotEmptyValue):
        Print('ERROR: ' + '!PlotIndexSetDouble(plotIndex, PLOT_EMPTY_VALUE, plotEmptyValue)' + ' at "' + 'PlotIndexConstruct' + ':' + IntegerToString(283) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        success = False
    return success

def ObjectChartCreate(symbol, chart_ID=0, sub_window=0, name='Chart', period=PERIOD_H1, x=0, y=0, width=300, height=200, corner=CORNER_LEFT_UPPER, scale=2, date_scale=True, price_scale=True, clr=clrRed, style=STYLE_SOLID, point_width=1, back=False, selection=False, hidden=True, z_order=0):
    if not ObjectCreate(chart_ID, name, OBJ_CHART, sub_window, 0, 0):
        Print('ERROR: ' + '!ObjectCreate(chart_ID, name, OBJ_CHART, sub_window, 0, 0)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(313) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return False
    if not ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(317) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(320) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(323) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(326) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(329) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetString(chart_ID, name, OBJPROP_SYMBOL, symbol):
        Print('ERROR: ' + '!ObjectSetString(chart_ID, name, OBJPROP_SYMBOL, symbol)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(332) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_PERIOD, period):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_PERIOD, period)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(335) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_CHART_SCALE, scale):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_CHART_SCALE, scale)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(338) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_DATE_SCALE, date_scale):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_DATE_SCALE, date_scale)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(341) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_PRICE_SCALE, price_scale):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_PRICE_SCALE, price_scale)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(344) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(347) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(350) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, point_width):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, point_width)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(353) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(356) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(359) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(362) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(365) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if not ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order):
        Print('ERROR: ' + '!ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)' + ' at "' + 'ObjectChartCreate' + ':' + IntegerToString(368) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Amplitude.mq5' + ')')
        ResetLastError()
        DebugBreak()
    return True

# ---- global variables initialised from expressions
iDigits = Digits()  # Subdigits on data


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Amplitude(_MQL5Indicator):
    name = 'Amplitude'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriodInp': 2400,  # Amplitude of last N candles
        'iIgnoreGapsInp': False,  # Ignore gaps between candles? (Not include last close?)
        'iShowPercentageInp': True,  # Show percentage instead of absolute values? (V*100 / (H+L)/2)
        'adPeriodInp': True,  # Adapt the Period? Overrides Standard Period Settings
        'adPeriodMinutesInp': 55200,  # Period in minutes that all M and H timeframes should adapt to?
        'adPeriodD1Inp': 40,  # Period for D1 - Daily Timeframe
        'adPeriodW1Inp': 8,  # Period for W1 - Weekly Timeframe
        'adPeriodMN1Inp': 2,  # Period for MN - Monthly Timeframe
        'iBufStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Drawing Style
        'iBufWidth': 1,  # Drawing Width
    }

