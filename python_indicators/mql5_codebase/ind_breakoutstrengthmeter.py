"""IND_BreakoutStrengthMeter — converted from MQL5: MQL5 Indicators/INDICATOR Breakout Strength Meter - MT5/IND_BreakoutStrengthMeter.mq5

Copyright: Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com; Link: https://fxweirdos.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com', 'link': 'https://fxweirdos.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'IND_BreakoutStrengthMeter', 'source': 'MQL5 Indicators/INDICATOR Breakout Strength Meter - MT5/IND_BreakoutStrengthMeter.mq5', 'folder': 'INDICATOR Breakout Strength Meter - MT5', 'inputs': [{'mql': 'cFontClr', 'py': 'cFontClr', 'param': None, 'type': 'color', 'default': 2402047, 'label': 'FONT COLOR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
cFontClr = _input('cFontClr', 0x24A6FF)  # FONT COLOR
iAUD = 0
iCAD = 0
iCHF = 0
iEUR = 0
iGBP = 0
iJPY = 0
iNZD = 0
iUSD = 0
iArray1 = Arr(8, 0, dyn=False)
sArray1 = Arr.of(['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD'], fill="", dyn=False, size=8)
chartid = 0
sCurrency1 = ""
sCurrency2 = ""
iPos = 0
i = 0
j = 0
k = 0
itemp = 0
stemp = ""

class cCandlestick(MqlObject):
    _q_fields = ('dHighPrice', 'dLowPrice', 'dClosePrice')
    def __init__(self, *args):
        self.dHighPrice = 0.0
        self.dLowPrice = 0.0
        self.dClosePrice = 0.0
    def mvGetCandleStickCharateristics(self, s, n):
        self.dHighPrice = iHigh(s, PERIOD_CURRENT, n)
        self.dLowPrice = iLow(s, PERIOD_CURRENT, n)
        self.dClosePrice = iClose(s, PERIOD_CURRENT, n)

def vSetLabel(sName, sub_window, xx, yy, cFontColor, iFontSize, sText):
    ObjectCreate(0, sName, OBJ_LABEL, sub_window, 0, 0)
    ObjectSetInteger(0, sName, OBJPROP_YDISTANCE, xx)
    ObjectSetInteger(0, sName, OBJPROP_XDISTANCE, yy)
    ObjectSetInteger(0, sName, OBJPROP_COLOR, cFontColor)
    ObjectSetInteger(0, sName, OBJPROP_WIDTH, FW_BOLD)
    ObjectSetInteger(0, sName, OBJPROP_FONTSIZE, iFontSize)
    ObjectSetString(0, sName, OBJPROP_TEXT, 0, sText)

def vfunction(sCountry, iVal):
    global iAUD, iCAD, iCHF, iEUR, iGBP, iJPY, iNZD, iUSD
    if sCountry == 'AUD':
        if iVal == 1:
            iAUD += 1
        elif iVal == 0:
            iAUD -= 1
    elif sCountry == 'CAD':
        if iVal == 1:
            iCAD += 1
        elif iVal == 0:
            iCAD -= 1
    elif sCountry == 'CHF':
        if iVal == 1:
            iCHF += 1
        elif iVal == 0:
            iCHF -= 1
    elif sCountry == 'EUR':
        if iVal == 1:
            iEUR += 1
        elif iVal == 0:
            iEUR -= 1
    elif sCountry == 'GBP':
        if iVal == 1:
            iGBP += 1
        elif iVal == 0:
            iGBP -= 1
    elif sCountry == 'JPY':
        if iVal == 1:
            iJPY += 1
        elif iVal == 0:
            iJPY -= 1
    elif sCountry == 'NZD':
        if iVal == 1:
            iNZD += 1
        elif iVal == 0:
            iNZD -= 1
    elif sCountry == 'USD':
        if iVal == 1:
            iUSD += 1
        elif iVal == 0:
            iUSD -= 1

def GetTimeFrame(lPeriod):
    _sw1 = lPeriod
    if _sw1 == 0:
        return 'PERIOD_CURRENT'
    elif _sw1 == 1:
        return 'M1'
    elif _sw1 == 5:
        return 'M5'
    elif _sw1 == 15:
        return 'M15'
    elif _sw1 == 30:
        return 'M30'
    elif _sw1 == 60:
        return 'H1'
    elif _sw1 == 240:
        return 'H4'
    elif _sw1 == 1440:
        return 'D1'
    elif _sw1 == 10080:
        return 'W1'
    elif _sw1 == 43200:
        return 'MN1'
    elif _sw1 == 2:
        return 'M2'
    elif _sw1 == 3:
        return 'M3'
    elif _sw1 == 4:
        return 'M4'
    elif _sw1 == 6:
        return 'M6'
    elif _sw1 == 10:
        return 'M10'
    elif _sw1 == 12:
        return 'M12'
    elif _sw1 == 16385:
        return 'H1'
    elif _sw1 == 16386:
        return 'H2'
    elif _sw1 == 16387:
        return 'H3'
    elif _sw1 == 16388:
        return 'H4'
    elif _sw1 == 16390:
        return 'H6'
    elif _sw1 == 16392:
        return 'H8'
    elif _sw1 == 16396:
        return 'H12'
    elif _sw1 == 16408:
        return 'D1'
    elif _sw1 == 32769:
        return 'W1'
    elif _sw1 == 49153:
        return 'MN1'
    else:
        return 'PERIOD_CURRENT'

def OnInit():
    global chartid, iAUD, iCAD, iCHF, iEUR, iGBP, iJPY, iNZD, iPos, iUSD, itemp, k, sCurrency1, sCurrency2, stemp
    ObjectsDeleteAll(0)
    k = 0
    while k < SymbolsTotal(True):
        chartid = ChartOpen(SymbolName(k, True), PERIOD_CURRENT)
        ChartClose(chartid)
        k += 1
    iAUD = 0
    iCAD = 0
    iCHF = 0
    iEUR = 0
    iGBP = 0
    iJPY = 0
    iNZD = 0
    iUSD = 0
    iPos = 0
    sCurrency1 = ''
    sCurrency2 = ''
    itemp = 0
    stemp = ''
    iArray1[0] = iAUD
    iArray1[1] = iCAD
    iArray1[2] = iCHF
    iArray1[3] = iEUR
    iArray1[4] = iGBP
    iArray1[5] = iJPY
    iArray1[6] = iNZD
    iArray1[7] = iUSD
    sArray1[0] = 'AUD'
    sArray1[1] = 'CAD'
    sArray1[2] = 'CHF'
    sArray1[3] = 'EUR'
    sArray1[4] = 'GBP'
    sArray1[5] = 'JPY'
    sArray1[6] = 'NZD'
    sArray1[7] = 'USD'
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global i, iAUD, iCAD, iCHF, iEUR, iGBP, iJPY, iNZD, iPos, iUSD, itemp, j, k, sCurrency1, sCurrency2, stemp
    iAUD = 0
    iCAD = 0
    iCHF = 0
    iEUR = 0
    iGBP = 0
    iJPY = 0
    iNZD = 0
    iUSD = 0
    iPos = 0
    sCurrency1 = ''
    sCurrency2 = ''
    itemp = 0
    stemp = ''
    vSetLabel('CSMBorderUp', 0, 25, 20, cFontClr, 8, '==============')
    vSetLabel('CSMTimeFrame', 0, 45, 20, cFontClr, 8, 'Timeframe is ' + GetTimeFrame(Period()))
    vSetLabel('CSMBorderDown', 0, 65, 20, cFontClr, 8, '==============')
    k = 0
    while k < SymbolsTotal(True):
        cCS1.mvGetCandleStickCharateristics(SymbolName(k, True), 1)
        cCS2.mvGetCandleStickCharateristics(SymbolName(k, True), 2)
        if StringLen(SymbolName(k, True)) == 7:
            iPos = 1
        sCurrency1 = StringSubstr(SymbolName(k, True), 0, 3)
        sCurrency2 = StringSubstr(SymbolName(k, True), 3 + iPos, 3)
        if cCS1.dClosePrice > cCS2.dHighPrice:
            vfunction(sCurrency1, 1)
            vfunction(sCurrency2, 0)
        if cCS1.dClosePrice < cCS2.dLowPrice:
            vfunction(sCurrency1, 0)
            vfunction(sCurrency2, 1)
        k += 1
    iArray1[0] = iAUD
    iArray1[1] = iCAD
    iArray1[2] = iCHF
    iArray1[3] = iEUR
    iArray1[4] = iGBP
    iArray1[5] = iJPY
    iArray1[6] = iNZD
    iArray1[7] = iUSD
    sArray1[0] = 'AUD'
    sArray1[1] = 'CAD'
    sArray1[2] = 'CHF'
    sArray1[3] = 'EUR'
    sArray1[4] = 'GBP'
    sArray1[5] = 'JPY'
    sArray1[6] = 'NZD'
    sArray1[7] = 'USD'
    i = 0
    while i < 8:
        j = i + 1
        while j < 8:
            if iArray1[i] > iArray1[j]:
                itemp = iArray1[i]
                stemp = sArray1[i]
                iArray1[i] = iArray1[j]
                sArray1[i] = sArray1[j]
                iArray1[j] = itemp
                sArray1[j] = stemp
            j += 1
        i += 1
    i = 0
    while i < 8:
        vSetLabel('BSM' + IntegerToString(i) + GetTimeFrame(Period()), 0, 85 + (i * 20), 20, cFontClr, 8, sArray1[i] + ' = ' + IntegerToString(iArray1[i]))
        i += 1
    return rates_total

# ---- global variables initialised from expressions
cCS1 = _alloc(cCandlestick)
cCS1.__init__()
cCS2 = _alloc(cCandlestick)
cCS2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class INDBreakoutStrengthMeter(_MQL5Indicator):
    name = 'IND_BreakoutStrengthMeter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

