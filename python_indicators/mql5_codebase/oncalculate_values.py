"""OnCalculate_values — converted from MQL5: MQL5 Indicators/View the Value in OnCalculate Parameters/OnCalculate_values.mq5

Show the values of the OnCalculate Parameters.
Displays Most_Recent_Value / Previous_Value / Start_Up_Value.
Version 1.20 added additional controls for seeing and setting as_series and not_series.
Author: https://www.mql5.com/en/users/lukeb.
Copyright: Copyright © 2018-2019, MetaQuotes Software Corp.; Link: https://www.mql5.com/en/users/lukeb; Version: 1.22

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'copyright': 'Copyright © 2018-2019, MetaQuotes Software Corp.', 'version': '1.22', 'link': 'https://www.mql5.com/en/users/lukeb', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9109504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Line'}, 'levels': [], 'description': ['Show the values of the OnCalculate Parameters.', 'Displays Most_Recent_Value / Previous_Value / Start_Up_Value.', 'Version 1.20 added additional controls for seeing and setting as_series and not_series.', 'Author: https://www.mql5.com/en/users/lukeb.'], 'name': 'OnCalculate_values', 'source': 'MQL5 Indicators/View the Value in OnCalculate Parameters/OnCalculate_values.mq5', 'folder': 'View the Value in OnCalculate Parameters', 'inputs': [{'mql': 'StartWithSeriesSet', 'py': 'StartWithSeriesSet', 'param': 'StartWithSeriesSet', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum SERIES_ONOFF
ON = 0
OFF = 1
_enum('SERIES_ONOFF', {0: 'ON', 1: 'OFF'})

# enum objectIndicies
CALLCOUNTER = 0
BARSCOUNT = 1
WINDBARS = 2
WINDVIS = 3
BARSFUNC = 4
IBARSFUNC = 5
RATESTOTAL = 6
PREVCALCULATED = 7
TIMEZEROCALC = 8
TIMEBARSCALC = 9
IMABARSVAL = 10
IMAZEROVAL = 11
OPENCALC = 12
HIGHCALC = 13
LOWCALC = 14
CLOSECALC = 15
TICKVOLUME = 16
VOLUMECALC = 17
ASKBID = 18
SPREADCALC = 19
SERIESONOFF = 20
OnCalcEnumEnd = 21
_enum('objectIndicies', {0: 'CALLCOUNTER', 1: 'BARSCOUNT', 2: 'WINDBARS', 3: 'WINDVIS', 4: 'BARSFUNC', 5: 'IBARSFUNC', 6: 'RATESTOTAL', 7: 'PREVCALCULATED', 8: 'TIMEZEROCALC', 9: 'TIMEBARSCALC', 10: 'IMABARSVAL', 11: 'IMAZEROVAL', 12: 'OPENCALC', 13: 'HIGHCALC', 14: 'LOWCALC', 15: 'CLOSECALC', 16: 'TICKVOLUME', 17: 'VOLUMECALC', 18: 'ASKBID', 19: 'SPREADCALC', 20: 'SERIESONOFF', 21: 'OnCalcEnumEnd'})

# ---- inputs and global variables
StartWithSeriesSet = _input('StartWithSeriesSet', ON)
LineBuffer = Arr(0, 0.0)  # Buffer to display the moving aveage line and capture iMA values for display.
comment_string = ''  # a global value to use for displaying comments
ary_dispObjType = Arr.of([OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL, OBJ_LABEL], fill=0)
ary_dispObjNames = Arr.of(['Call_Count', 'BarsCount', 'WindowBars', 'WindVisible', 'BarsFunc', 'iBarsFunc', 'RatesTotal', 'Prev_Calc', 'Time_Zero_Calc', 'Time_Bars_Calc', 'IMA_Bars_VAL', 'IMA_ZERO_VAL', 'Open_Calc', 'High_Calc', 'Low_Calc', 'Close_Calc', 'Tick_Vol_Calc', 'Volume_Calc', 'ASK-BID', 'Spread_Calc', 'Series_ONOFF'], fill="")
ary_dispObjXPos = Arr.of([20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], fill=0)
ary_dispObjYPos = Arr.of([20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420], fill=0)
ary_dispObjColor = Arr.of([clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellowGreen, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellow, clrYellowGreen, clrLimeGreen], fill=0)
ary_As_Series = Arr.of(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], fill="")
ary_dispObjText = Arr.of(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], fill="")
DISPALYWINDOWZERO = 0
THECURRENTCHART = 0
ARRAYNEWVAL = 0  # Access the '0' instance of the ary_OnCalcVals array
ARRAYPREVVAL = 1  # Access the '1' instance of the ary_OnCalcVals array
k_notSetVal = 999  # An Initializtion value that is easily recognized
g_seriesSetting = True
g_drawNeedded = True
tick_count = 0
start_ticks = 0
finish_ticks = 0
call_count = 0

class OnCalcValues(MqlObject):
    _q_fields = ('callCount', 'barsCalc', 'winBars', 'winVis', 'barsFunc', 'iBarsFunc', 'ratesTotal', 'prevCalc', 'timeZeroCalc', 'timeBarsCalc', 'IMAZeroVal', 'IMABarsVal', 'openCalc', 'highCalc', 'lowCalc', 'closeCalc', 'tickVolume', 'volume', 'askBidPts', 'spread', 'seriesOnOff')
    def __init__(self, *args):
        self.callCount = 0
        self.barsCalc = 0
        self.winBars = 0
        self.winVis = 0
        self.barsFunc = 0
        self.iBarsFunc = 0
        self.ratesTotal = 0
        self.prevCalc = 0
        self.timeZeroCalc = 0
        self.timeBarsCalc = 0
        self.IMAZeroVal = 0.0
        self.IMABarsVal = 0.0
        self.openCalc = 0.0
        self.highCalc = 0.0
        self.lowCalc = 0.0
        self.closeCalc = 0.0
        self.tickVolume = 0
        self.volume = 0
        self.askBidPts = 0
        self.spread = 0
        self.seriesOnOff = 0

def OnInit():
    global MA_handle, comment_string
    init_return_code = INIT_SUCCEEDED
    IndicatorSetString(INDICATOR_SHORTNAME, 'OnCalculate_Values')
    EventSetTimer(1)
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    ArraySetAsSeries(LineBuffer, True)
    loop_counter = 0
    while True:
        loop_counter += 1
        if MA_handle == 0:
            MA_handle = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_OPEN)
        if MA_handle == INVALID_HANDLE:
            error_code = GetLastError()
            MA_handle = 0
            comment_string = 'OnInit' + ': Failed to Create MA_handle, attempt ' + IntegerToString(loop_counter) + ', Error: ' + IntegerToString(error_code)
            Comment(comment_string)
            Print(comment_string)
            init_return_code = INIT_FAILED
        if not (MA_handle == 0 and loop_counter < 5):
            break
    for i in range(0, ArrayRange(ary_OnCalcVals, 0)):
        ary_OnCalcVals[i].callCount = k_notSetVal
        ary_OnCalcVals[i].barsCalc = k_notSetVal
        ary_OnCalcVals[i].winBars = k_notSetVal
        ary_OnCalcVals[i].winVis = k_notSetVal
        ary_OnCalcVals[i].barsFunc = k_notSetVal
        ary_OnCalcVals[i].iBarsFunc = k_notSetVal
        ary_OnCalcVals[i].ratesTotal = k_notSetVal
        ary_OnCalcVals[i].prevCalc = k_notSetVal
        ary_OnCalcVals[i].timeZeroCalc = k_notSetVal
        ary_OnCalcVals[i].timeBarsCalc = k_notSetVal
        ary_OnCalcVals[i].IMAZeroVal = k_notSetVal
        ary_OnCalcVals[i].IMABarsVal = k_notSetVal
        ary_OnCalcVals[i].openCalc = k_notSetVal
        ary_OnCalcVals[i].highCalc = k_notSetVal
        ary_OnCalcVals[i].lowCalc = k_notSetVal
        ary_OnCalcVals[i].closeCalc = k_notSetVal
        ary_OnCalcVals[i].lowCalc = k_notSetVal
        ary_OnCalcVals[i].closeCalc = k_notSetVal
        ary_OnCalcVals[i].tickVolume = k_notSetVal
        ary_OnCalcVals[i].volume = k_notSetVal
        ary_OnCalcVals[i].askBidPts = k_notSetVal
        ary_OnCalcVals[i].spread = k_notSetVal
    ary_OnCalcVals[ARRAYNEWVAL].callCount = 0
    ary_OnCalcVals[ARRAYNEWVAL].seriesOnOff = StartWithSeriesSet
    return init_return_code

def OnDeinit(reason):
    global comment_string
    EventKillTimer()
    for i in range(0, OnCalcEnumEnd):
        ObjectDelete(THECURRENTCHART, ary_dispObjNames[i])
    if StringLen(comment_string) > 0:
        comment_string = ''
        Comment(comment_string)
    ChartRedraw(ChartID())

def OnChartEvent(id_, lparam, dparam, sparam):
    global g_seriesSetting
    chartRedraw = False
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if sparam == ary_dispObjNames[SERIESONOFF]:
            ary_OnCalcVals[ARRAYNEWVAL].seriesOnOff = (OFF if (ary_OnCalcVals[ARRAYNEWVAL].seriesOnOff == ON) else ON)
            chartRedraw = True
        elif sparam == ary_dispObjNames[SPREADCALC]:
            g_seriesSetting = (False if (g_seriesSetting == True) else True)
            chartRedraw = True
        elif sparam == ary_dispObjNames[IMAZEROVAL]:
            if ArrayGetAsSeries(LineBuffer):
                ArraySetAsSeries(LineBuffer, False)
            else:
                ArraySetAsSeries(LineBuffer, True)
            total_bars = iBars(Symbol(), PERIOD_CURRENT)
            GetTerminalIMAData(total_bars, total_bars)
            chartRedraw = True
    elif id_ == CHARTEVENT_CHART_CHANGE:
        SetChartBarValues()
        chartRedraw = True
    if chartRedraw:
        DisplayOnCalcValues()
        ChartRedraw(ChartID())

def OnTimer():
    global _s_OnTimer_timer_count, g_drawNeedded
    _s_OnTimer_timer_count += 1
    if g_drawNeedded == True or (not MathMod(_s_OnTimer_timer_count, 10.0)):
        DisplayOnCalcValues()
        g_drawNeedded = False

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global g_drawNeedded
    toCopy = Box(0)
    SetToCopyCount(toCopy, rates_total, prev_calculated)
    if ary_OnCalcVals[ARRAYNEWVAL].seriesOnOff == ON:
        SetAsSeries(g_seriesSetting, time, open, high, low, close, tick_volume, volume, spread)
    CopyNewToOld(ary_OnCalcVals[ARRAYNEWVAL].callCount)
    ary_OnCalcVals[ARRAYNEWVAL].callCount += 1
    DetermineSeriesStatus(time, open, high, low, close, tick_volume, volume, spread)
    LoadOnCalculateValues(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread)
    GetTerminalIMAData(rates_total, toCopy.v)
    LoadOtherValues()
    g_drawNeedded = True
    return rates_total

def LoadOnCalculateValues(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ary_OnCalcVals[ARRAYNEWVAL].ratesTotal = rates_total
    ary_OnCalcVals[ARRAYNEWVAL].prevCalc = prev_calculated
    ary_OnCalcVals[ARRAYNEWVAL].timeZeroCalc = time[0]
    ary_OnCalcVals[ARRAYNEWVAL].timeBarsCalc = time[rates_total - 1]
    ary_OnCalcVals[ARRAYNEWVAL].openCalc = open[0]
    ary_OnCalcVals[ARRAYNEWVAL].highCalc = high[0]
    ary_OnCalcVals[ARRAYNEWVAL].lowCalc = low[0]
    ary_OnCalcVals[ARRAYNEWVAL].closeCalc = close[0]
    ary_OnCalcVals[ARRAYNEWVAL].tickVolume = tick_volume[0]
    ary_OnCalcVals[ARRAYNEWVAL].volume = volume[0]
    ary_OnCalcVals[ARRAYNEWVAL].spread = spread[0]

def DetermineSeriesStatus(time, open, high, low, close, tick_volume, volume, spread):
    ary_As_Series[TIMEZEROCALC] = ('As_Series' if ArrayGetAsSeries(time) else 'Not_Series')
    ary_As_Series[TIMEBARSCALC] = ary_As_Series[TIMEZEROCALC]
    ary_As_Series[OPENCALC] = ('As_Series' if ArrayGetAsSeries(open) else 'Not_Series')
    ary_As_Series[HIGHCALC] = ('As_Series' if ArrayGetAsSeries(high) else 'Not_Series')
    ary_As_Series[LOWCALC] = ('As_Series' if ArrayGetAsSeries(low) else 'Not_Series')
    ary_As_Series[CLOSECALC] = ('As_Series' if ArrayGetAsSeries(close) else 'Not_Series')
    ary_As_Series[TICKVOLUME] = ('As_Series' if ArrayGetAsSeries(tick_volume) else 'Not_Series')
    ary_As_Series[VOLUMECALC] = ('As_Series' if ArrayGetAsSeries(volume) else 'Not_Series')
    ary_As_Series[SPREADCALC] = ('As_Series' if ArrayGetAsSeries(spread) else 'Not_Series')

def GetTerminalIMAData(rates_total, toCopy):
    global comment_string
    if CopyBuffer(MA_handle, 0, 0, toCopy, LineBuffer) <= 0:
        err_code = GetLastError()
        comment_string = 'GetTerminalIMAData' + ': Getting MA data failed, asked for ' + IntegerToString(toCopy) + ' bars, Error: ' + IntegerToString(err_code)
        Comment(comment_string)
        Print(comment_string)
        ary_OnCalcVals[ARRAYNEWVAL].IMAZeroVal = k_notSetVal
        ary_OnCalcVals[ARRAYNEWVAL].IMABarsVal = k_notSetVal
    else:
        ary_OnCalcVals[ARRAYNEWVAL].IMAZeroVal = LineBuffer[0]
        ary_OnCalcVals[ARRAYNEWVAL].IMABarsVal = LineBuffer[rates_total - 1]

def LoadOtherValues():
    ary_OnCalcVals[ARRAYNEWVAL].barsCalc = BarsCalculated(MA_handle)
    ary_OnCalcVals[ARRAYNEWVAL].barsFunc = Bars(Symbol(), Period())
    ary_OnCalcVals[ARRAYNEWVAL].iBarsFunc = iBars(Symbol(), Period())
    ary_As_Series[IMAZEROVAL] = ('As_Series' if ArrayGetAsSeries(LineBuffer) else 'Not_Series')
    ary_As_Series[IMABARSVAL] = ary_As_Series[IMAZEROVAL]
    SetChartBarValues()
    SymbolInfoTick(Symbol(), last_tick)
    ask = last_tick.ask
    bid = last_tick.bid
    ary_OnCalcVals[ARRAYNEWVAL].askBidPts = _int(_fdiv(ask - bid, Point()))

def ThereIsANewBar(time):
    global _s_ThereIsANewBar_lastBarTime
    newBar = False
    if time[0] > _s_ThereIsANewBar_lastBarTime or 1 == ary_OnCalcVals[ARRAYNEWVAL].callCount:
        _s_ThereIsANewBar_lastBarTime = time[0]
        newBar = True
    return newBar

def SetChartBarValues():
    ary_OnCalcVals[ARRAYNEWVAL].winBars = ChartGetInteger(ChartID(), CHART_VISIBLE_BARS)
    ary_OnCalcVals[ARRAYNEWVAL].winVis = ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR)

def CopyNewToOld(CallCount):
    if CallCount == 1:
        MoveNewTo(ARRAYONSTARTUP)
    MoveNewTo(ARRAYPREVVAL)

def MoveNewTo(aryIndx):
    ary_OnCalcVals[aryIndx].callCount = ary_OnCalcVals[ARRAYNEWVAL].callCount
    ary_OnCalcVals[aryIndx].barsCalc = ary_OnCalcVals[ARRAYNEWVAL].barsCalc
    ary_OnCalcVals[aryIndx].winBars = ary_OnCalcVals[ARRAYNEWVAL].winBars
    ary_OnCalcVals[aryIndx].winVis = ary_OnCalcVals[ARRAYNEWVAL].winVis
    ary_OnCalcVals[aryIndx].IMAZeroVal = ary_OnCalcVals[ARRAYNEWVAL].IMAZeroVal
    ary_OnCalcVals[aryIndx].IMABarsVal = ary_OnCalcVals[ARRAYNEWVAL].IMABarsVal
    ary_OnCalcVals[aryIndx].barsFunc = ary_OnCalcVals[ARRAYNEWVAL].barsFunc
    ary_OnCalcVals[aryIndx].iBarsFunc = ary_OnCalcVals[ARRAYNEWVAL].iBarsFunc
    ary_OnCalcVals[aryIndx].ratesTotal = ary_OnCalcVals[ARRAYNEWVAL].ratesTotal
    ary_OnCalcVals[aryIndx].prevCalc = ary_OnCalcVals[ARRAYNEWVAL].prevCalc
    ary_OnCalcVals[aryIndx].timeZeroCalc = ary_OnCalcVals[ARRAYNEWVAL].timeZeroCalc
    ary_OnCalcVals[aryIndx].timeBarsCalc = ary_OnCalcVals[ARRAYNEWVAL].timeBarsCalc
    ary_OnCalcVals[aryIndx].openCalc = ary_OnCalcVals[ARRAYNEWVAL].openCalc
    ary_OnCalcVals[aryIndx].highCalc = ary_OnCalcVals[ARRAYNEWVAL].highCalc
    ary_OnCalcVals[aryIndx].lowCalc = ary_OnCalcVals[ARRAYNEWVAL].lowCalc
    ary_OnCalcVals[aryIndx].closeCalc = ary_OnCalcVals[ARRAYNEWVAL].closeCalc
    ary_OnCalcVals[aryIndx].tickVolume = ary_OnCalcVals[ARRAYNEWVAL].tickVolume
    ary_OnCalcVals[aryIndx].volume = ary_OnCalcVals[ARRAYNEWVAL].volume
    ary_OnCalcVals[aryIndx].askBidPts = ary_OnCalcVals[ARRAYNEWVAL].askBidPts
    ary_OnCalcVals[aryIndx].spread = ary_OnCalcVals[ARRAYNEWVAL].spread
    ary_OnCalcVals[aryIndx].seriesOnOff = ary_OnCalcVals[ARRAYNEWVAL].seriesOnOff

def DisplayOnCalcValues():
    for i in range(0, OnCalcEnumEnd):
        SetLabelObjectText(i)

def SetLabelObjectText(ObjectID):
    global comment_string
    barsNumString = IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].barsFunc - 1)
    promptString = ""
    _sw1 = ObjectID
    if _sw1 == CALLCOUNTER:
        ary_dispObjText[ObjectID] = 'OnCalc Calls: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].callCount) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].callCount) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].callCount)
        MakeALabel(ObjectID)
    elif _sw1 == BARSCOUNT:
        ary_dispObjText[ObjectID] = 'Bars Calculated: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].barsCalc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].barsCalc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].barsCalc)
        MakeALabel(ObjectID)
    elif _sw1 == WINDBARS:
        ary_dispObjText[ObjectID] = 'Window Bars: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].winBars) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].winBars) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].winBars)
        MakeALabel(ObjectID)
    elif _sw1 == WINDVIS:
        ary_dispObjText[ObjectID] = 'First Visible Bar #: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].winVis) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].winVis) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].winVis)
        MakeALabel(ObjectID)
    elif _sw1 == IMAZEROVAL:
        ary_dispObjText[ObjectID] = 'iMA_Val[0], ' + ary_As_Series[ObjectID] + ': ' + DoubleToString(ary_OnCalcVals[ARRAYNEWVAL].IMAZeroVal, Digits() + 1) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYPREVVAL].IMAZeroVal, Digits()) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYONSTARTUP].IMAZeroVal, Digits())
        MakeALabel(ObjectID)
    elif _sw1 == IMABARSVAL:
        ary_dispObjText[ObjectID] = 'iMA_Val[' + barsNumString + '], ' + ary_As_Series[ObjectID] + ': ' + DoubleToString(ary_OnCalcVals[ARRAYNEWVAL].IMABarsVal, Digits() + 1) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYPREVVAL].IMABarsVal, Digits()) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYONSTARTUP].IMABarsVal, Digits())
        MakeALabel(ObjectID)
    elif _sw1 == IBARSFUNC:
        ary_dispObjText[ObjectID] = ' iBars Func: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].iBarsFunc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].iBarsFunc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].iBarsFunc)
        MakeALabel(ObjectID)
    elif _sw1 == BARSFUNC:
        ary_dispObjText[ObjectID] = 'Bars Func: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].barsFunc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].barsFunc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].barsFunc)
        MakeALabel(ObjectID)
    elif _sw1 == RATESTOTAL:
        ary_dispObjText[ObjectID] = 'Rates Total: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].ratesTotal) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].ratesTotal) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].ratesTotal)
        MakeALabel(ObjectID)
    elif _sw1 == PREVCALCULATED:
        ary_dispObjText[ObjectID] = 'Previous Calculated: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].prevCalc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].prevCalc) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].prevCalc)
        MakeALabel(ObjectID)
    elif _sw1 == TIMEZEROCALC:
        ary_dispObjText[ObjectID] = 'time[0], ' + ary_As_Series[ObjectID] + ': ' + TimeToString(ary_OnCalcVals[ARRAYNEWVAL].timeZeroCalc) + ' / ' + TimeToString(ary_OnCalcVals[ARRAYPREVVAL].timeZeroCalc) + ' / ' + TimeToString(ary_OnCalcVals[ARRAYONSTARTUP].timeZeroCalc)
        MakeALabel(ObjectID)
    elif _sw1 == TIMEBARSCALC:
        ary_dispObjText[ObjectID] = 'time[' + barsNumString + '], ' + ary_As_Series[ObjectID] + ': ' + TimeToString(ary_OnCalcVals[ARRAYNEWVAL].timeBarsCalc) + ' / ' + TimeToString(ary_OnCalcVals[ARRAYPREVVAL].timeBarsCalc) + ' / ' + TimeToString(ary_OnCalcVals[ARRAYONSTARTUP].timeBarsCalc)
        MakeALabel(ObjectID)
    elif _sw1 == OPENCALC:
        ary_dispObjText[ObjectID] = 'open[0], ' + ary_As_Series[ObjectID] + ': ' + DoubleToString(ary_OnCalcVals[ARRAYNEWVAL].openCalc, Digits() + 1) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYPREVVAL].openCalc, Digits()) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYONSTARTUP].openCalc, Digits())
        MakeALabel(ObjectID)
    elif _sw1 == HIGHCALC:
        ary_dispObjText[ObjectID] = 'high[0], ' + ary_As_Series[ObjectID] + ': ' + DoubleToString(ary_OnCalcVals[ARRAYNEWVAL].highCalc, Digits() + 1) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYPREVVAL].highCalc, Digits()) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYONSTARTUP].highCalc, Digits())
        MakeALabel(ObjectID)
    elif _sw1 == LOWCALC:
        ary_dispObjText[ObjectID] = 'low[0], ' + ary_As_Series[ObjectID] + ': ' + DoubleToString(ary_OnCalcVals[ARRAYNEWVAL].lowCalc, Digits() + 1) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYPREVVAL].lowCalc, Digits()) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYONSTARTUP].lowCalc, Digits())
        MakeALabel(ObjectID)
    elif _sw1 == CLOSECALC:
        ary_dispObjText[ObjectID] = 'close[0], ' + ary_As_Series[ObjectID] + ': ' + DoubleToString(ary_OnCalcVals[ARRAYNEWVAL].closeCalc, Digits() + 1) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYPREVVAL].closeCalc, Digits()) + ' / ' + DoubleToString(ary_OnCalcVals[ARRAYONSTARTUP].closeCalc, Digits())
        MakeALabel(ObjectID)
    elif _sw1 == TICKVOLUME:
        ary_dispObjText[ObjectID] = 'tick_volume[0], ' + ary_As_Series[ObjectID] + ': ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].tickVolume) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].tickVolume) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].tickVolume)
        MakeALabel(ObjectID)
    elif _sw1 == VOLUMECALC:
        ary_dispObjText[ObjectID] = 'volume[0], ' + ary_As_Series[ObjectID] + ': ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].volume) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].volume) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].volume)
        MakeALabel(ObjectID)
    elif _sw1 == ASKBID:
        ary_dispObjText[ObjectID] = 'Ask-Bid pts: ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].askBidPts) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].askBidPts) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].askBidPts)
        MakeALabel(ObjectID)
    elif _sw1 == SPREADCALC:
        ary_dispObjText[ObjectID] = 'spread[0], ' + ary_As_Series[ObjectID] + ': ' + IntegerToString(ary_OnCalcVals[ARRAYNEWVAL].spread) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYPREVVAL].spread) + ' / ' + IntegerToString(ary_OnCalcVals[ARRAYONSTARTUP].spread)
        MakeALabel(ObjectID)
    elif _sw1 == SERIESONOFF:
        promptString = ('Set Arrays to Series: ' if g_seriesSetting else 'Set Arrays to Not_Series: ')
        ary_dispObjText[ObjectID] = promptString + ('ON' if (ary_OnCalcVals[ARRAYNEWVAL].seriesOnOff == ON) else 'OFF') + ' / ' + ('ON' if (ary_OnCalcVals[ARRAYPREVVAL].seriesOnOff == ON) else 'OFF') + ' / ' + ('ON' if (ary_OnCalcVals[ARRAYONSTARTUP].seriesOnOff == ON) else 'OFF')
        MakeALabel(ObjectID)
    else:
        comment_string = 'SetLabelObjectText' + ' error: Got an Undefined Object ID: ' + IntegerToString(ObjectID)

def MakeALabel(displayOjectIndex):
    chartID = ChartID()
    windowIndex = ObjectFind(ChartID(), ary_dispObjNames[displayOjectIndex])
    if windowIndex < 0:
        ObjectCreate(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJ_LABEL, DISPALYWINDOWZERO, 0, 0)
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_HIDDEN, True)
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_SELECTABLE, True)
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_SELECTED, False)
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_CORNER, CORNER_RIGHT_LOWER)
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_FONTSIZE, 11)
        ObjectSetString(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_FONT, 'Arial')
        ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_COLOR, ary_dispObjColor[displayOjectIndex])
    ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_XDISTANCE, ary_dispObjXPos[displayOjectIndex])
    ObjectSetInteger(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_YDISTANCE, ary_dispObjYPos[displayOjectIndex])
    ObjectSetString(THECURRENTCHART, ary_dispObjNames[displayOjectIndex], OBJPROP_TEXT, ary_dispObjText[displayOjectIndex])

def SetToCopyCount(to_copy, rates_total, prev_calculated):
    if prev_calculated < 1 or rates_total < prev_calculated:
        to_copy.v = rates_total
    else:
        to_copy.v = rates_total - prev_calculated + 1

def SetAsSeries(as_series, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, as_series)
    ArraySetAsSeries(open, as_series)
    ArraySetAsSeries(high, as_series)
    ArraySetAsSeries(low, as_series)
    ArraySetAsSeries(close, as_series)
    ArraySetAsSeries(tick_volume, as_series)
    ArraySetAsSeries(volume, as_series)
    ArraySetAsSeries(spread, as_series)

# ---- global variables initialised from expressions
MA_handle = 0  # The handle to us to access terminal iMA data
last_tick = MqlTick()  # a MQL5 built in Structure to hold data from the last tick (quote) processed in OnCalculate
ary_OnCalcVals = Arr(3, 0, dyn=False, factory=OnCalcValues)  # store values passed into OnCalculate; Three instances of values - Newest, Prvious and First
ARRAYONSTARTUP = ArrayRange(ary_OnCalcVals, 0) - 1  # this is the value 2, to access the '2' instance of the ary_OnCalcVals array

# ---- static local variables
_s_OnTimer_timer_count = 0
_s_ThereIsANewBar_lastBarTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OnCalculateValues(_MQL5Indicator):
    name = 'OnCalculate_values'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartWithSeriesSet': _Choice({0: 'On Off enumberation to control if explicitly setting the array series type is on.', 1: 'On Off enumberation to control if explicitly setting the array series type is on.'}, default=0),
    }

