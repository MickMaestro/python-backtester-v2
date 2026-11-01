"""Strong_Levels_V1 — converted from MQL5: MQL5 Indicators/Strong Historical Levels/Strong_Levels_V1.mq5

Rule 1(bull candle on sup. level): if close - low > Jump Factor
Rule 2(bull candle on res. level): if close - low > Jump Factor & (close-low)/(high-low)>ratio
Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.pipcrop.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Missing include files: ..\\include\\Math\\Alglib\\dataanalysis.mqh
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.pipcrop.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Rule 1(bull candle on sup. level): if close - low > Jump Factor', 'Rule 2(bull candle on res. level): if close - low > Jump Factor & (close-low)/(high-low)>ratio'], 'name': 'Strong_Levels_V1', 'source': 'MQL5 Indicators/Strong Historical Levels/Strong_Levels_V1.mq5', 'folder': 'Strong Historical Levels', 'inputs': [{'mql': 'myfilters', 'py': 'myfilters', 'param': 'myfilters', 'type': 'int', 'default': 1, 'label': 'Rule(s) for data gather', 'sinput': False}, {'mql': 'LNo', 'py': 'LNo', 'param': 'LNo', 'type': 'int', 'default': 15, 'label': 'Number of Levels to extract', 'sinput': False}, {'mql': 'tf0', 'py': 'tf0', 'param': 'tf0', 'type': 'int', 'default': 1, 'label': 'Analysing TF', 'sinput': False}, {'mql': 'Jumpmulti', 'py': 'Jumpmulti', 'param': 'Jumpmulti', 'type': 'double', 'default': 100.0, 'label': 'Min. Jump after touch (Percent of ATR)', 'sinput': False}, {'mql': 'ratio', 'py': 'ratio', 'param': 'ratio', 'type': 'double', 'default': 0.6667, 'label': 'Ratio', 'sinput': False}, {'mql': 'ATRPer', 'py': 'ATRPer', 'param': 'ATRPer', 'type': 'int', 'default': 55, 'label': 'ATR Period', 'sinput': False}, {'mql': 'ResColor', 'py': 'ResColor', 'param': None, 'type': 'color', 'default': 13353215, 'label': 'Resistance color for Panel', 'sinput': False}, {'mql': 'SupColor', 'py': 'SupColor', 'param': None, 'type': 'color', 'default': 15130800, 'label': 'Support color for Panel', 'sinput': False}, {'mql': 'BGColor', 'py': 'BGColor', 'param': None, 'type': 'color', 'default': 2497303, 'label': 'Back-ground', 'sinput': False}, {'mql': 'ResColor0', 'py': 'ResColor0', 'param': None, 'type': 'color', 'default': 255, 'label': 'Resistance Levels color', 'sinput': False}, {'mql': 'SupColor0', 'py': 'SupColor0', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Support Levels color', 'sinput': False}, {'mql': 'LevelsInt', 'py': 'LevelsInt', 'param': 'LevelsInt', 'type': 'int', 'default': 2, 'label': 'Levels Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': ['..\\include\\Math\\Alglib\\dataanalysis.mqh'], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter

# enum filterrules
rule1 = 0
rule12 = 1
rule2 = 2
_enum('filterrules', {0: 'rule1', 1: 'rule12', 2: 'rule2'})

# ---- inputs and global variables
Cclustering = None
myfilters = _input('myfilters', 1)  # Rule(s) for data gather
LNo = _input('LNo', 15)  # Number of Levels to extract
tf0 = _input('tf0', PERIOD_M1)  # Analysing TF
Jumpmulti = _input('Jumpmulti', 100.0)  # Min. Jump after touch (Percent of ATR)
ratio = _input('ratio', 0.6667)  # Ratio
ATRPer = _input('ATRPer', 55)  # ATR Period
ResColor = _input('ResColor', clrPink)  # Resistance color for Panel
SupColor = _input('SupColor', clrPowderBlue)  # Support color for Panel
BGColor = _input('BGColor', 0x261B17)  # Back-ground
ResColor0 = _input('ResColor0', clrRed)  # Resistance Levels color
SupColor0 = _input('SupColor0', clrBlue)  # Support Levels color
LevelsInt = _input('LevelsInt', 2)  # Levels Width
ATRHndler = 0
size0 = 0
xini = 5
yini = 20
maxbar = 0
minbar = 10
Ysize = 30
dyy = 5
xdis = 0
lastbars = 0
LastLNo = 0
minLN = 3
sup_xyz = Arr(0, 0)
res_xyz = Arr(0, 0)
NextChart = 0
ToolName = 'SH_Levels_'
OBJName = ""
atr = Arr(0, 0.0)
Jmulti = 0.0
startCluster = False

def OnInit():
    global ATRHndler, Jmulti, LastLNo, OBJName, lastbars, maxbar, xdis, yini
    ObjectsDeleteAll(0, ToolName)
    Jmulti = Jumpmulti / 100.0
    ATRHndler = iATR(Symbol(), tf0, ATRPer)
    SetScreen()
    maxbar = 100000
    OBJName = ToolName + 'Analyse'
    xdis = xini
    ObjectCreate(0, OBJName, OBJ_BUTTON, 0, 0, 0)
    OBJSet(OBJName, 'Analyse Sup./Res.', xini, yini, 180, (2 * Ysize) + dyy, 12, 0xF0F0F0, clrNONE, clrBlack, ALIGN_CENTER, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + ' Loadbar'
    xdis += _int(ObjectGetInteger(ChartID(), ToolName + 'Analyse', OBJPROP_XSIZE)) + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, '0.0 %', xdis, yini, 50, Ysize, 10, clrGold, clrGold, BGColor, ALIGN_LEFT, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + 'clusterLoadbar'
    xdis = xini + _int(ObjectGetInteger(ChartID(), ToolName + 'Analyse', OBJPROP_XSIZE)) + dyy
    yini += Ysize + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, '0.0 %', xdis, yini, 50, Ysize, 10, clrGold, clrGold, BGColor, ALIGN_LEFT, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + ' LN'
    yini += Ysize + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, 'Level No.', xini, yini, 80, Ysize, 10, clrGold, clrGold, BGColor, ALIGN_LEFT, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + ' LN.e'
    xdis = xini + 80 + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, IntegerToString(LNo), xdis, yini, 100 - dyy, Ysize, 10, BGColor, clrGold, clrGold, ALIGN_RIGHT, CORNER_LEFT_UPPER, False)
    LastLNo = LNo
    OBJName = ToolName + ' bars'
    xdis = xini
    yini += Ysize + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, 'Bar count', xdis, yini, 80, Ysize, 10, clrGold, clrGold, BGColor, ALIGN_LEFT, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + ' bars.e'
    xdis += 80 + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, IntegerToString(maxbar), xdis, yini, 100 - dyy, Ysize, 10, BGColor, clrGold, clrGold, ALIGN_RIGHT, CORNER_LEFT_UPPER, False)
    lastbars = maxbar
    OBJName = ToolName + ' TotalRes'
    yini += Ysize + (3 * dyy)
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, 'Res. Count: ', xini, yini, 180, Ysize, 12, ResColor, ResColor, BGColor, ALIGN_LEFT, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + ' TotalSup'
    yini += Ysize + dyy
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, 'Sup. Count: ', xini, yini, 180, Ysize, 12, SupColor, SupColor, BGColor, ALIGN_LEFT, CORNER_LEFT_UPPER, True)
    EventSetMillisecondTimer(5)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnDeinit(reason):
    if reason == 1 or reason == 4:
        ObjectsDeleteAll(0, ToolName)
        EventKillTimer()

def Analyse():
    global NextChart, OBJName, Ysize, startCluster
    OBJName = ToolName + 'Zone_'
    ObjectsDeleteAll(ChartID(), OBJName)
    ChartRedraw()
    OBJName = ToolName + ' Loadbar'
    ObjectSetString(0, OBJName, OBJPROP_TEXT, '0.0 %')
    ObjectSetInteger(0, OBJName, OBJPROP_XSIZE, 50)
    OBJName = ToolName + 'clusterLoadbar'
    ObjectSetInteger(0, OBJName, OBJPROP_XSIZE, 50)
    ObjectSetString(0, OBJName, OBJPROP_TEXT, '0.0 %')
    Ysize = 30
    bars = lastbars
    ctype = Arr(0, 0)
    low = Arr(0, 0.0)
    high = Arr(0, 0.0)
    close = Arr(0, 0.0)
    open = Arr(0, 0.0)
    total = Arr(0, 0.0)
    ArrayResize(ctype, bars)
    ArrayInitialize(ctype, 0)
    resi = _int(bars / 1000.0) - 1
    if resi <= 0:
        resi = 2
    if CopyBuffer(ATRHndler, 0, 0, bars, atr) <= 0:
        return
    if CopyLow(Symbol(), tf0, 0, bars, low) <= 0:
        return
    if CopyHigh(Symbol(), tf0, 0, bars, high) <= 0:
        return
    if CopyClose(Symbol(), tf0, 0, bars, close) <= 0:
        return
    if CopyOpen(Symbol(), tf0, 0, bars, open) <= 0:
        return
    bars = _int(MathMin(ArraySize(open), MathMin(float(bars), ArraySize(close))))
    for i in range(bars - ATRPer - 1, 0 - 1, -1):
        Print(i, '  ', ArraySize(close))
        if close[i] > open[i]:
            ctype[i] = 1
        elif close[i] < open[i]:
            ctype[i] = -1
    sup_mat.Resize(0, 0)
    supclusters.Resize(0, 0)
    res_mat.Resize(0, 0)
    resclusters.Resize(0, 0)
    for i in range(bars - ATRPer - 1, 0 - 1, -1):
        if (myfilters <= 1 and ctype[i] == 1) and (close[i] - low[i]) >= (atr[i] * Jmulti):
            Addsup(low[i])
        if ((myfilters >= 1 and ctype[i] == -1) and (close[i] - low[i]) >= (atr[i] * Jmulti)) and _fdiv(close[i] - low[i], high[i] - low[i]) >= ratio:
            Addsup(low[i])
        if (myfilters <= 1 and ctype[i] == -1) and (high[i] - close[i]) >= (atr[i] * Jmulti):
            Addres(high[i])
        if ((myfilters >= 1 and ctype[i] == 1) and (high[i] - close[i]) >= (atr[i] * Jmulti)) and _fdiv(high[i] - close[i], high[i] - low[i]) >= ratio:
            Addres(high[i])
        if MathMod(float(i), resi) == 0:
            ObjectSetString(0, ToolName + ' Loadbar', OBJPROP_TEXT, DoubleToString(_fdiv(100 * float(bars - ATRPer - 1 - i), bars - ATRPer - 1), 1) + ' %')
            ObjectSetInteger(0, ToolName + ' Loadbar', OBJPROP_XSIZE, 50 + _int(300 * _fdiv(float(bars - ATRPer - i + 1), bars - ATRPer - 1)))
            ObjectSetString(0, ToolName + ' TotalRes', OBJPROP_TEXT, 'Res. Count: ' + IntegerToString(res_mat.Rows()))
            ObjectSetString(0, ToolName + ' TotalSup', OBJPROP_TEXT, 'Sup. Count: ' + IntegerToString(sup_mat.Rows()))
            ChartRedraw()
    startCluster = True
    OBJName = ToolName + 'clusterLoadbar'
    ObjectSetInteger(0, OBJName, OBJPROP_XSIZE, 350)
    ObjectSetString(0, OBJName, OBJPROP_TEXT, 'Wait for Cluster Calculation...')
    supinfo = 0
    resinfo = 0
    Restarts = 5
    Cclustering.KMeansGenerate(sup_mat, sup_mat.Rows(), sup_mat.Cols(), LastLNo, Restarts, supinfo, supclusters, sup_xyz)
    Cclustering.KMeansGenerate(res_mat, res_mat.Rows(), res_mat.Cols(), LastLNo, Restarts, resinfo, resclusters, res_xyz)
    startCluster = False
    ObjectSetString(0, OBJName, OBJPROP_TEXT, 'Cluster Calculation done!')
    LevelRes = Arr(0, 0.0)
    LevelSup = Arr(0, 0.0)
    LevelTotal = Arr(0, 0.0)
    ArrayResize(LevelRes, LastLNo)
    ArrayResize(LevelSup, LastLNo)
    ArrayResize(LevelTotal, LastLNo)
    OBJName = ToolName + 'clusterLoadbar'
    stat_x = _int(ObjectGetInteger(ChartID(), OBJName, OBJPROP_XDISTANCE))
    OBJName = ToolName + ' Loadbar'
    stat_x += _int(ObjectGetInteger(ChartID(), OBJName, OBJPROP_XSIZE)) + dyy
    OBJName = ToolName + 'Analyse'
    stat_y = _int(ObjectGetInteger(ChartID(), OBJName, OBJPROP_YDISTANCE))
    OBJName = ToolName + 'Zone_Res_Header'
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    OBJSet(OBJName, 'Res. Levels', stat_x, stat_y, 135, Ysize, 12, ResColor, ResColor, BGColor, ALIGN_CENTER, CORNER_LEFT_UPPER, True)
    OBJName = ToolName + 'Zone_Sup_Header'
    ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
    stat_x += 135 + dyy
    OBJSet(OBJName, 'Sup. Levels', stat_x, stat_y, 135, Ysize, 12, SupColor, SupColor, BGColor, ALIGN_CENTER, CORNER_LEFT_UPPER, True)
    stat_y += Ysize + dyy
    Ysize = _idiv(Ysize, 2)
    i = 0
    while i < LastLNo:
        stat_x -= 135 + dyy
        OBJName = ToolName + 'Zone_Res_' + IntegerToString(i)
        ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
        OBJSet(OBJName, DoubleToString(resclusters.Get(0, i), Digits()), stat_x, stat_y, 135, Ysize, 12, ResColor, ResColor, BGColor, ALIGN_CENTER, CORNER_LEFT_UPPER, True)
        stat_x += 135 + dyy
        OBJName = ToolName + 'Zone_Sup_' + IntegerToString(i)
        ObjectCreate(0, OBJName, OBJ_EDIT, 0, 0, 0)
        OBJSet(OBJName, DoubleToString(supclusters.Get(0, i), Digits()), stat_x, stat_y, 135, Ysize, 12, SupColor, SupColor, BGColor, ALIGN_CENTER, CORNER_LEFT_UPPER, True)
        stat_y += Ysize + dyy
        i += 1
    NextChart = ChartOpen(Symbol(), Period())
    future = TimeCurrent() + (PeriodSeconds(PERIOD_MN1) * 100)
    price = 0.0
    i = 0
    while i < LastLNo:
        price = NormalizeDouble(resclusters.Get(0, i), Digits())
        OBJName = ToolName + 'Zone_Res_' + IntegerToString(i + LastLNo + 1)
        ObjectCreate(NextChart, OBJName, OBJ_HLINE, 0, 0, 0)
        TrendSet(OBJName, 0, NextChart, price, price, ResColor0, LevelsInt, STYLE_SOLID, True)
        price = NormalizeDouble(supclusters.Get(0, i), Digits())
        OBJName = ToolName + 'Zone_Sup_' + IntegerToString(i + LastLNo + 1)
        ObjectCreate(NextChart, OBJName, OBJ_HLINE, 0, 0, 0)
        TrendSet(OBJName, 0, NextChart, price, price, SupColor0, LevelsInt, STYLE_SOLID, True)
        i += 1
    ChartRedraw(NextChart)
    _delete(Cclustering)
    ArrayFree(sup_xyz)
    ArrayFree(res_xyz)
    ArrayFree(atr)
    Ysize = 30

def OnTimer():
    global OBJName
    if startCluster:
        OBJName = ToolName + 'clusterLoadbar'
        if ObjectGetString(0, OBJName, OBJPROP_TEXT) == 'Wait for Cluster Calculation':
            ObjectSetString(0, OBJName, OBJPROP_TEXT, 'Wait for Cluster Calculation.')
        elif ObjectGetString(0, OBJName, OBJPROP_TEXT) == 'Wait for Cluster Calculation.':
            ObjectSetString(0, OBJName, OBJPROP_TEXT, 'Wait for Cluster Calculation..')
        elif ObjectGetString(0, OBJName, OBJPROP_TEXT) == 'Wait for Cluster Calculation..':
            ObjectSetString(0, OBJName, OBJPROP_TEXT, 'Wait for Cluster Calculation...')
        elif ObjectGetString(0, OBJName, OBJPROP_TEXT) == 'Wait for Cluster Calculation..':
            ObjectSetString(0, OBJName, OBJPROP_TEXT, 'Wait for Cluster Calculation')
        ChartRedraw()

def MeanNormalization_1(mat):
    v = Box(0)
    i = 0
    while i < mat.v.Cols():
        v.v = mat.v.Col(i)
        MeanNormalization_1(v)
        mat.v.Col(v.v, i)
        i += 1

def MeanNormalization_2(v):
    mean = v.v.Mean()
    max_ = v.v.Max()
    min_ = v.v.Min()
    i = 0
    while i < v.v.Size():
        v.v[i] = _fdiv(v.v[i] - mean, max_ - min_)
        i += 1

def Addsup(price):
    msize = _int(sup_mat.Rows())
    sup_mat.Resize(msize + 1, 1)
    sup_mat.Set(msize, 0, price)

def Addres(price):
    msize = _int(res_mat.Rows())
    res_mat.Resize(msize + 1, 1)
    res_mat.Set(msize, 0, price)

def OnChartEvent(id_, lparam, dparam, sparam):
    global LastLNo, OBJName, lastbars
    if id_ == CHARTEVENT_OBJECT_CLICK and sparam == (ToolName + 'Analyse'):
        Sleep(100)
        ObjectSetInteger(ChartID(), sparam, OBJPROP_STATE, False)
        ChartRedraw()
        Analyse()
    if id_ == CHARTEVENT_OBJECT_ENDEDIT and sparam == (ToolName + ' bars.e'):
        OBJName = sparam
        bar = _int(StringToInteger(ObjectGetString(ChartID(), OBJName, OBJPROP_TEXT)))
        if bar < 0:
            bar = iBars(Symbol(), tf0) + 1
        if bar < minbar:
            MessageBox('Min. bar to analyse is ' + IntegerToString(minbar) + '!', 'Min. bar limit', 0)
            ObjectSetString(0, OBJName, OBJPROP_TEXT, IntegerToString(minbar))
        elif bar > iBars(Symbol(), tf0):
            MessageBox('Max. bar to analyse is ' + IntegerToString(iBars(Symbol(), tf0)) + '!', 'Max. bar limit', 0)
            ObjectSetString(0, OBJName, OBJPROP_TEXT, IntegerToString(iBars(Symbol(), tf0)))
        elif bar > 900000:
            mes = MessageBox(IntegerToString(bar) + ' bars to analyse is so much and will take time more than 1 minute! Are you sure?', 'Max. bar warning', 1)
            if mes == 2:
                ObjectSetString(0, OBJName, OBJPROP_TEXT, IntegerToString(lastbars))
        lastbars = _int(StringToInteger(ObjectGetString(ChartID(), OBJName, OBJPROP_TEXT)))
    if id_ == CHARTEVENT_OBJECT_ENDEDIT and sparam == (ToolName + ' LN.e'):
        OBJName = sparam
        bar = _int(StringToInteger(ObjectGetString(ChartID(), OBJName, OBJPROP_TEXT)))
        if bar < 0:
            bar = LNo
        if bar < minLN:
            MessageBox('Min. Level No. to analyse is ' + IntegerToString(minLN) + '!', 'Min. Level No. limit', 0)
            ObjectSetString(0, OBJName, OBJPROP_TEXT, IntegerToString(minLN))
        elif bar > 500:
            MessageBox('Max. Level No. to analyse is 500' + '!', 'Max. bar limit', 0)
            ObjectSetString(0, OBJName, OBJPROP_TEXT, IntegerToString(500))
        elif bar > 100:
            mes = MessageBox(IntegerToString(bar) + ' Level No. analyse is so much and will take time more than 1 minute! Are you sure?', 'Max. Level No. warning', 1)
            if mes == 2:
                ObjectSetString(0, OBJName, OBJPROP_TEXT, IntegerToString(LastLNo))
        LastLNo = _int(StringToInteger(ObjectGetString(ChartID(), OBJName, OBJPROP_TEXT)))
    ChartRedraw()

def SetScreen():
    ChartSetInteger(ChartID(), CHART_FOREGROUND, False)
    ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, BGColor)
    ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, BGColor)
    ChartSetInteger(0, CHART_COLOR_CHART_LINE, BGColor)
    ChartSetInteger(0, CHART_COLOR_CHART_DOWN, BGColor)
    ChartSetInteger(0, CHART_COLOR_CHART_UP, BGColor)
    ChartSetInteger(0, CHART_COLOR_ASK, BGColor)
    ChartSetInteger(0, CHART_COLOR_BID, BGColor)
    ChartSetInteger(0, CHART_COLOR_GRID, BGColor)
    ChartSetInteger(0, CHART_COLOR_BACKGROUND, BGColor)
    ChartSetInteger(0, CHART_COLOR_FOREGROUND, BGColor)

def OBJSet(OBJNameSet, txt, XDis, YDis, XSize, YSize, FSize, Fill, Border, TColor, myAlign, mycorner, myread):
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_CORNER, mycorner)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_XDISTANCE, XDis)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_YDISTANCE, YDis)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_XSIZE, XSize)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_YSIZE, YSize)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_FONTSIZE, FSize)
    ObjectSetString(ChartID(), OBJNameSet, OBJPROP_TEXT, txt)
    ObjectSetString(ChartID(), OBJNameSet, OBJPROP_FONT, 'Calibri')
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_BGCOLOR, Fill)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_BORDER_COLOR, Border)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_COLOR, TColor)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_ALIGN, myAlign)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_BACK, False)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_ZORDER, 5)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_HIDDEN, True)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_READONLY, myread)
    ObjectSetInteger(ChartID(), OBJNameSet, OBJPROP_SELECTABLE, False)

def TrendSet(TrendName, time0, time1, price1, price2, Tcolor, Twidth, Tstyle, b):
    ObjectSetInteger(NextChart, TrendName, OBJPROP_TIME, 0, time0)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_TIME, 1, time1)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_COLOR, Tcolor)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_RAY, False)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_WIDTH, Twidth)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_STYLE, Tstyle)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_BACK, True)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(NextChart, TrendName, OBJPROP_TIMEFRAMES, (OBJ_ALL_PERIODS if b else OBJ_NO_PERIODS))
    ObjectSetDouble(NextChart, TrendName, OBJPROP_PRICE, 0, price1)
    ObjectSetDouble(NextChart, TrendName, OBJPROP_PRICE, 1, price2)

# ---- global variables initialised from expressions
res_mat = CMatrixDouble()
sup_mat = CMatrixDouble()
supclusters = CMatrixDouble()
resclusters = CMatrixDouble()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StrongLevelsV1(_MQL5Indicator):
    name = 'Strong_Levels_V1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'myfilters': _Choice({0: 'Rule 1', 1: 'Rule 1+2', 2: 'Rule 2'}, default=1),  # Rule(s) for data gather
        'LNo': 15,  # Number of Levels to extract
        'tf0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=1),  # Analysing TF
        'Jumpmulti': 100.0,  # Min. Jump after touch (Percent of ATR)
        'ratio': 0.6667,  # Ratio
        'ATRPer': 55,  # ATR Period
        'LevelsInt': 2,  # Levels Width
    }

