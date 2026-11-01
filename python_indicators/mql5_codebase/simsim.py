"""SimSim — converted from MQL5: MQL5 Indicators/SimSim (Simple Simulator v1.0)/SimSim.mq5

Simple Simulator
Copyright: Mokara; Link: https://www.mql5.com/en/users/mokara; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mokara', 'link': 'https://www.mql5.com/en/users/mokara', 'version': '1.0', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Simple Simulator'], 'name': 'SimSim', 'source': 'MQL5 Indicators/SimSim (Simple Simulator v1.0)/SimSim.mq5', 'folder': 'SimSim (Simple Simulator v1.0)', 'inputs': [{'mql': 'barBegin', 'py': 'barBegin', 'param': 'barBegin', 'type': 'uint', 'default': 1000, 'label': 'Beginning Bar', 'sinput': False}, {'mql': 'timeSpeed', 'py': 'timeSpeed', 'param': 'timeSpeed', 'type': 'uint', 'default': 2, 'label': 'Speed (Seconds)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
barBegin = _input('barBegin', 1000)  # Beginning Bar
timeSpeed = _input('timeSpeed', 2)  # Speed (Seconds)
endProgram = False
firstRun = True
chWidth = 0
c = 0
tOpen = 0.0
tPrice = 0.0
tResult = 0.0
tProfit = 0.0
tType = 'NONE'
infoNames = Arr.of(['INFO_TRADE', 'INFO_OPEN', 'INFO_PRICE', 'INFO_RESULT', 'INFO_PROFIT'], fill="", dyn=False, size=5)
infoTitles = Arr.of(['Trade Type: ', 'Trade Open: ', 'Trade Price: ', 'Trade Result: ', 'Total Profit: '], fill="", dyn=False, size=5)
infoValues = Arr.of(['', '', '', '', ''], fill="", dyn=False, size=5)
btnNames = Arr.of(['LONG', 'SHORT', 'CLOSE', 'PAUSE', 'END'], fill="", dyn=False, size=5)

def MakeButton(name, index):
    ObjectCreate(0, name, OBJ_BUTTON, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, _idiv(chWidth, 2) + (index * 70))
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, 10)
    ObjectSetString(0, name, OBJPROP_TEXT, name)

def MakeLabel(name, text, index):
    ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, _idiv(chWidth, 2) - 140)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, (index * 20) + 30)
    ObjectSetString(0, name, OBJPROP_FONT, 'Arial Black')

def EditLabels():
    infoValues[0] = tType
    infoValues[1] = DoubleToString(tOpen, 5)
    infoValues[2] = DoubleToString(tPrice, 5)
    infoValues[3] = DoubleToString(tResult, 0)
    infoValues[4] = DoubleToString(tProfit, 0)
    for i in range(0, ArraySize(infoNames)):
        ObjectSetString(0, infoNames[i], OBJPROP_TEXT, infoTitles[i] + infoValues[i])

def DisableButtons():
    for i in range(0, ArraySize(btnNames)):
        ObjectSetInteger(0, btnNames[i], OBJPROP_STATE, False)

def OnInit():
    EventSetTimer(timeSpeed)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SimSim')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Alert('Net Profit/Loss: ' + DoubleToString(NormalizeDouble(tProfit, 0), 0) + ' pips.')
    EventKillTimer()
    ObjectsDeleteAll(0)

def OnTimer():
    global c, chWidth, endProgram, firstRun, tPrice, tResult
    if firstRun == True:
        if barBegin > Bars(Symbol(), Period()):
            Alert('ERROR: not enough bars.')
            endProgram = True
            firstRun = False
            return
        c = -1 * barBegin
        ChartNavigate(0, CHART_BEGIN, c)
        chWidth = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
        ChartSetInteger(0, CHART_AUTOSCROLL, False)
        ChartSetInteger(0, CHART_SHIFT, False)
        ChartNavigate(0, CHART_END, (-1 * barBegin) - 1)
        ArraySetAsSeries(Rates, True)
        ArrayResize(Rates, barBegin + 10)
        CopyRates(Symbol(), Period(), 0, barBegin + 10, Rates)
        i = 0
        while i < ArraySize(btnNames):
            MakeButton(btnNames[i], i - 2)
            i += 1
        i = 0
        while i < ArraySize(infoNames):
            MakeLabel(infoNames[i], infoTitles[i], i)
            i += 1
        tPrice = Rates[barBegin - 1].close
        EditLabels()
        ChartRedraw()
        firstRun = False
    if c == 0 or endProgram == True:
        Alert('The End.')
        ChartIndicatorDelete(0, 0, 'SimSim')
    if ObjectGetInteger(0, 'PAUSE', OBJPROP_STATE) == True:
        return
    ChartNavigate(0, CHART_END, c)
    c += 1
    tPrice = Rates[-1 * c].close
    if tType == 'LONG':
        tResult = _fdiv(tPrice - tOpen, Point())
    if tType == 'SHORT':
        tResult = _fdiv(tOpen - tPrice, Point())
    EditLabels()
    ChartRedraw()

def OnChartEvent(id_, lparam, dparam, sparam):
    global tOpen, tProfit, tResult, tType
    if ObjectGetInteger(0, 'END', OBJPROP_STATE) == True:
        Alert('Simulation manually terminated.')
        ChartIndicatorDelete(0, 0, 'SimSim')
    if ObjectGetInteger(0, 'LONG', OBJPROP_STATE) == True:
        ObjectSetInteger(0, 'LONG', OBJPROP_STATE, False)
        if tType == 'NONE':
            tOpen = tPrice
            tType = 'LONG'
    if ObjectGetInteger(0, 'SHORT', OBJPROP_STATE) == True:
        ObjectSetInteger(0, 'SHORT', OBJPROP_STATE, False)
        if tType == 'NONE':
            tOpen = tPrice
            tType = 'SHORT'
    if ObjectGetInteger(0, 'CLOSE', OBJPROP_STATE) == True and tType != 'NONE':
        ObjectSetInteger(0, 'CLOSE', OBJPROP_STATE, False)
        if tType != 'NONE':
            tOpen = 0.0
            tProfit += tResult
            tResult = 0.0
            tType = 'NONE'
    if ObjectGetInteger(0, 'CLOSE', OBJPROP_STATE) == True and tType == 'NONE':
        ObjectSetInteger(0, 'CLOSE', OBJPROP_STATE, False)
    EditLabels()
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

# ---- global variables initialised from expressions
Rates = Arr(0, 0, factory=MqlRates)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimSim(_MQL5Indicator):
    name = 'SimSim'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'barBegin': 1000,  # Beginning Bar
        'timeSpeed': 2,  # Speed (Seconds)
    }

