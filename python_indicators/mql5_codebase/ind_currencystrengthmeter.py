"""IND_CurrencyStrengthMeter — converted from MQL5: MQL5 Indicators/INDICATOR Currency Strength Meter - MT5/IND_CurrencyStrengthMeter.mq5

Copyright: Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com; Link: https://fxweirdos.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com', 'link': 'https://fxweirdos.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'IND_CurrencyStrengthMeter', 'source': 'MQL5 Indicators/INDICATOR Currency Strength Meter - MT5/IND_CurrencyStrengthMeter.mq5', 'folder': 'INDICATOR Currency Strength Meter - MT5', 'inputs': [{'mql': 'cFontClr', 'py': 'cFontClr', 'param': None, 'type': 'color', 'default': 2402047, 'label': 'FONT COLOR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
cFontClr = _input('cFontClr', 0x24A6FF)  # FONT COLOR
dAUD = 0.0
dCAD = 0.0
dCHF = 0.0
dEUR = 0.0
dGBP = 0.0
dJPY = 0.0
dNZD = 0.0
dUSD = 0.0
dArray1 = Arr(8, 0.0, dyn=False)
sArray1 = Arr.of(['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD'], fill="", dyn=False, size=8)
chartid = 0
sCurrency1 = ""
sCurrency2 = ""
iPos = 0
i = 0
j = 0
k = 0
dtemp = 0.0
stemp = ""

class cCandlestick(MqlObject):
    _q_fields = ('dOpenPrice', 'dClosePrice')
    def __init__(self, *args):
        self.dOpenPrice = 0.0
        self.dClosePrice = 0.0
    def mvGetCandleStickCharateristics(self, s, n):
        self.dOpenPrice = iOpen(s, PERIOD_CURRENT, n)
        self.dClosePrice = iClose(s, PERIOD_CURRENT, n)

def vSetLabel(sName, sub_window, xx, yy, cFontColor, iFontSize, sText):
    ObjectCreate(0, sName, OBJ_LABEL, sub_window, 0, 0)
    ObjectSetInteger(0, sName, OBJPROP_YDISTANCE, xx)
    ObjectSetInteger(0, sName, OBJPROP_XDISTANCE, yy)
    ObjectSetInteger(0, sName, OBJPROP_COLOR, cFontColor)
    ObjectSetInteger(0, sName, OBJPROP_WIDTH, FW_BOLD)
    ObjectSetInteger(0, sName, OBJPROP_FONTSIZE, iFontSize)
    ObjectSetString(0, sName, OBJPROP_TEXT, 0, sText)

def vfunction(sCountry, dPrice1, dPricen, iSwitch):
    global dAUD, dCAD, dCHF, dEUR, dGBP, dJPY, dNZD, dUSD
    if sCountry == 'AUD':
        dAUD = dAUD + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'CAD':
        dCAD = dCAD + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'CHF':
        dCHF = dCHF + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'EUR':
        dEUR = dEUR + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'GBP':
        dGBP = dGBP + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'JPY':
        dJPY = dJPY + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'NZD':
        dNZD = dNZD + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)
    elif sCountry == 'USD':
        dUSD = dUSD + (_fdiv(dPrice1 - dPricen, dPrice1) * 100 * iSwitch)

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
    global chartid, dAUD, dCAD, dCHF, dEUR, dGBP, dJPY, dNZD, dUSD, dtemp, iPos, k, sCurrency1, sCurrency2, stemp
    ObjectsDeleteAll(0)
    k = 0
    while k < SymbolsTotal(True):
        chartid = ChartOpen(SymbolName(k, True), PERIOD_CURRENT)
        ChartClose(chartid)
        k += 1
    dAUD = 0.0
    dCAD = 0.0
    dCHF = 0.0
    dEUR = 0.0
    dGBP = 0.0
    dJPY = 0.0
    dNZD = 0.0
    dUSD = 0.0
    iPos = 0
    sCurrency1 = ''
    sCurrency2 = ''
    dtemp = 0.0
    stemp = ''
    dArray1[0] = dAUD
    dArray1[1] = dCAD
    dArray1[2] = dCHF
    dArray1[3] = dEUR
    dArray1[4] = dGBP
    dArray1[5] = dJPY
    dArray1[6] = dNZD
    dArray1[7] = dUSD
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
    global dAUD, dCAD, dCHF, dEUR, dGBP, dJPY, dNZD, dUSD, dtemp, i, iPos, j, k, sCurrency1, sCurrency2, stemp
    dAUD = 0.0
    dCAD = 0.0
    dCHF = 0.0
    dEUR = 0.0
    dGBP = 0.0
    dJPY = 0.0
    dNZD = 0.0
    dUSD = 0.0
    iPos = 0
    sCurrency1 = ''
    sCurrency2 = ''
    dtemp = 0.0
    stemp = ''
    vSetLabel('CSMBorderUp', 0, 25, 20, cFontClr, 8, '==============')
    vSetLabel('CSMTimeFrame', 0, 45, 20, cFontClr, 8, 'Currency Strength Meter | Timeframe is ' + GetTimeFrame(Period()))
    vSetLabel('CSMBorderDown', 0, 65, 20, cFontClr, 8, '==============')
    k = 0
    while k < SymbolsTotal(True):
        cCS1.mvGetCandleStickCharateristics(SymbolName(k, True), 1)
        cCS2.mvGetCandleStickCharateristics(SymbolName(k, True), 12)
        if StringLen(SymbolName(k, True)) == 7:
            iPos = 1
        sCurrency1 = StringSubstr(SymbolName(k, True), 0, 3)
        sCurrency2 = StringSubstr(SymbolName(k, True), 3 + iPos, 3)
        vfunction(sCurrency1, cCS1.dClosePrice, cCS2.dOpenPrice, 1)
        vfunction(sCurrency2, cCS1.dClosePrice, cCS2.dOpenPrice, -1)
        k += 1
    dArray1[0] = dAUD
    dArray1[1] = dCAD
    dArray1[2] = dCHF
    dArray1[3] = dEUR
    dArray1[4] = dGBP
    dArray1[5] = dJPY
    dArray1[6] = dNZD
    dArray1[7] = dUSD
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
            if dArray1[i] > dArray1[j]:
                dtemp = dArray1[i]
                stemp = sArray1[i]
                dArray1[i] = dArray1[j]
                sArray1[i] = sArray1[j]
                dArray1[j] = dtemp
                sArray1[j] = stemp
            j += 1
        i += 1
    i = 0
    while i < 8:
        vSetLabel('CSM' + IntegerToString(i) + GetTimeFrame(Period()), 0, 85 + (i * 20), 20, cFontClr, 8, sArray1[i] + ' = ' + DoubleToString(dArray1[i], 2))
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


class INDCurrencyStrengthMeter(_MQL5Indicator):
    name = 'IND_CurrencyStrengthMeter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

