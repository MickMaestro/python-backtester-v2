"""Arbitrage — converted from MQL5: MQL5 Indicators/Arbitrage II/Arbitrage.mq5

Arbitrage
Copyright: Copyright 2018, pipPod.; Link: https://www.mql5.com/en/users/pippod; Version: 2.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, pipPod.', 'link': 'https://www.mql5.com/en/users/pippod', 'version': '2.10', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {}, 'colors': {1: [3329330, 2237106], 2: [2237106]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Arbitrage'], 'name': 'Arbitrage', 'source': 'MQL5 Indicators/Arbitrage II/Arbitrage.mq5', 'folder': 'Arbitrage II', 'inputs': [{'mql': 'Indicator', 'py': 'Indicator', 'param': 'Indicator', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MA', 'py': 'MA', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'ushort', 'default': 14, 'label': 'MA Period', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'MA Price', 'sinput': False}, {'mql': 'MACD', 'py': 'MACD', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'ushort', 'default': 12, 'label': 'Fast EMA Period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'ushort', 'default': 26, 'label': 'Slow EMA Period', 'sinput': False}, {'mql': 'SignalSMA', 'py': 'SignalSMA', 'param': 'SignalSMA', 'type': 'ushort', 'default': 9, 'label': 'Signal SMA Period', 'sinput': False}, {'mql': 'MACDPrice', 'py': 'MACDPrice', 'param': 'MACDPrice', 'type': 'int', 'default': 1, 'label': 'MACD Price', 'sinput': False}, {'mql': 'Stochastic', 'py': 'Stochastic', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'ushort', 'default': 7, 'label': 'K Period', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'ushort', 'default': 3, 'label': 'D Period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'ushort', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Price Field', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'ushort', 'default': 14, 'label': 'RSI Period', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'RSI Price', 'sinput': False}, {'mql': 'CCI', 'py': 'CCI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'ushort', 'default': 14, 'label': 'CCI Period', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 1, 'label': 'CCI Price', 'sinput': False}, {'mql': 'RVI', 'py': 'RVI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'ushort', 'default': 14, 'label': 'RVI Period', 'sinput': False}, {'mql': 'DeMarker', 'py': 'DeMarker', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'DeMarkerPeriod', 'py': 'DeMarkerPeriod', 'param': 'DeMarkerPeriod', 'type': 'ushort', 'default': 14, 'label': 'DeMarker Period', 'sinput': False}, {'mql': 'TriX', 'py': 'TriX', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'TrixPeriod', 'py': 'TrixPeriod', 'param': 'TrixPeriod', 'type': 'ushort', 'default': 14, 'label': 'TriX Period', 'sinput': False}, {'mql': 'TrixPrice', 'py': 'TrixPrice', 'param': 'TrixPrice', 'type': 'int', 'default': 1, 'label': 'TriX Price', 'sinput': False}, {'mql': '_', 'py': '_', 'param': None, 'type': 'string', 'default': '', 'label': '---', 'sinput': False}, {'mql': 'ColorBars', 'py': 'ColorBars', 'param': 'ColorBars', 'type': 'bool', 'default': True, 'label': 'Color Bars', 'sinput': False}, {'mql': 'FillBuffers', 'py': 'FillBuffers', 'param': 'FillBuffers', 'type': 'bool', 'default': True, 'label': 'Fill Buffers', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 3329330  # #property indicator_color1
indicator_color2 = 2237106  # #property indicator_color2

# enum indicators
INDICATOR_MA = 0
INDICATOR_MACD = 1
INDICATOR_STOCHASTIC = 2
INDICATOR_RSI = 3
INDICATOR_CCI = 4
INDICATOR_RVI = 5
INDICATOR_DEMARK = 6
INDICATOR_TRIX = 7
_enum('indicators', {0: 'INDICATOR_MA', 1: 'INDICATOR_MACD', 2: 'INDICATOR_STOCHASTIC', 3: 'INDICATOR_RSI', 4: 'INDICATOR_CCI', 5: 'INDICATOR_RVI', 6: 'INDICATOR_DEMARK', 7: 'INDICATOR_TRIX'})

# ---- inputs and global variables
indicator_level1 = 0.0
indicator_level2 = 0.2
indicator_level4 = 20.0
indicator_level6 = 30.0
indicator_level8 = 100.0
Indicator = _input('Indicator', INDICATOR_MA)
MA = _input('MA', "")
MAPeriod = _input('MAPeriod', 14)  # MA Period
MAMethod = _input('MAMethod', MODE_SMA)  # MA Method
MAPrice = _input('MAPrice', PRICE_CLOSE)  # MA Price
MACD = _input('MACD', "")
FastEMA = _input('FastEMA', 12)  # Fast EMA Period
SlowEMA = _input('SlowEMA', 26)  # Slow EMA Period
SignalSMA = _input('SignalSMA', 9)  # Signal SMA Period
MACDPrice = _input('MACDPrice', PRICE_CLOSE)  # MACD Price
Stochastic = _input('Stochastic', "")
Kperiod = _input('Kperiod', 7)  # K Period
Dperiod = _input('Dperiod', 3)  # D Period
Slowing = _input('Slowing', 3)
PriceField = _input('PriceField', STO_LOWHIGH)  # Price Field
RSI = _input('RSI', "")
RSIPeriod = _input('RSIPeriod', 14)  # RSI Period
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # RSI Price
CCI = _input('CCI', "")
CCIPeriod = _input('CCIPeriod', 14)  # CCI Period
CCIPrice = _input('CCIPrice', PRICE_CLOSE)  # CCI Price
RVI = _input('RVI', "")
RVIPeriod = _input('RVIPeriod', 14)  # RVI Period
DeMarker = _input('DeMarker', "")
DeMarkerPeriod = _input('DeMarkerPeriod', 14)  # DeMarker Period
TriX = _input('TriX', "")
TrixPeriod = _input('TrixPeriod', 14)  # TriX Period
TrixPrice = _input('TrixPrice', PRICE_CLOSE)  # TriX Price
_ = _input('_', "")  # ---
ColorBars = _input('ColorBars', True)  # Color Bars
FillBuffers = _input('FillBuffers', True)  # Fill Buffers
BaseBuffer = Arr(0, 0.0)
QuotBuffer = Arr(0, 0.0)
base = ""
quot = ""
symbol1 = ""
symbol2 = ""
symbol3 = ""
Index1 = Arr(0, 0.0)
Index2 = Arr(0, 0.0)
Index3 = Arr(0, 0.0)
index1 = 0.0
index2 = 0.0
index3 = 0.0
baseIndex = 0.0
quotIndex = 0.0
baseUSD = False
quotUSD = False
quotJPY = False
quotJPY1 = False
quotJPY2 = False
quotJPY3 = False
shortName = ""
chartID = 0
window = 0
indHandle1 = 0
indHandle2 = 0
indHandle3 = 0

def OnInit():
    global base, baseUSD, chartID, indHandle1, indHandle2, indHandle3, quot, quotJPY, quotJPY1, quotJPY2, quotJPY3, quotUSD, shortName, symbol1, symbol2, symbol3, window
    colorBase = _uint(indicator_color1)
    colorQuot = _uint(indicator_color2)
    base = StringSubstr(Symbol(), 0, 3)
    quot = StringSubstr(Symbol(), 3, 3)
    if Symbol() == 'EURUSD':
        if (not SymbolSelect('EURJPY', True)) or (not SymbolSelect('USDJPY', True)):
            return INIT_FAILED
        colorBase = clrRoyalBlue
        colorQuot = clrLimeGreen
        quotUSD = True
        symbol1 = Symbol()
        symbol2 = 'EURJPY'
        quotJPY2 = True
        symbol3 = 'USDJPY'
        quotJPY3 = True
    if Symbol() == 'EURJPY':
        if (not SymbolSelect('EURUSD', True)) or (not SymbolSelect('USDJPY', True)):
            return INIT_FAILED
        colorBase = clrRoyalBlue
        colorQuot = clrYellow
        quotJPY = True
        symbol1 = Symbol()
        quotJPY1 = True
        symbol2 = 'EURUSD'
        symbol3 = 'USDJPY'
        quotJPY3 = True
    if Symbol() == 'GBPUSD':
        if (not SymbolSelect('GBPJPY', True)) or (not SymbolSelect('USDJPY', True)):
            return INIT_FAILED
        colorBase = clrSilver
        colorQuot = clrLimeGreen
        quotUSD = True
        symbol1 = Symbol()
        symbol2 = 'GBPJPY'
        quotJPY2 = True
        symbol3 = 'USDJPY'
        quotJPY3 = True
    if Symbol() == 'GBPJPY':
        if (not SymbolSelect('GBPUSD', True)) or (not SymbolSelect('USDJPY', True)):
            return INIT_FAILED
        colorBase = clrSilver
        colorQuot = clrYellow
        quotJPY = True
        symbol1 = Symbol()
        quotJPY1 = True
        symbol2 = 'GBPUSD'
        symbol3 = 'USDJPY'
        quotJPY3 = True
    if Symbol() == 'USDCAD':
        if (not SymbolSelect('CADJPY', True)) or (not SymbolSelect('USDJPY', True)):
            return INIT_FAILED
        colorBase = clrLimeGreen
        colorQuot = clrWhiteSmoke
        baseUSD = True
        symbol1 = Symbol()
        symbol2 = 'CADJPY'
        quotJPY2 = True
        symbol3 = 'USDJPY'
        quotJPY3 = True
    if Symbol() == 'USDCHF':
        if (not SymbolSelect('CHFJPY', True)) or (not SymbolSelect('USDJPY', True)):
            return INIT_FAILED
        colorBase = clrLimeGreen
        colorQuot = clrFireBrick
        baseUSD = True
        symbol1 = Symbol()
        symbol2 = 'CHFJPY'
        quotJPY2 = True
        symbol3 = 'USDJPY'
        quotJPY3 = True
    if Symbol() == 'USDJPY':
        if (not SymbolSelect('EURUSD', True)) or (not SymbolSelect('EURJPY', True)):
            return INIT_FAILED
        colorBase = clrLimeGreen
        colorQuot = clrYellow
        quotJPY = True
        symbol1 = Symbol()
        quotJPY1 = True
        symbol2 = 'EURUSD'
        symbol3 = 'EURJPY'
        quotJPY3 = True
    indHandle1 = INVALID_HANDLE
    indHandle2 = INVALID_HANDLE
    indHandle3 = INVALID_HANDLE
    _sw1 = Indicator
    if _sw1 == INDICATOR_MA:
        indHandle1 = iMA(symbol1, Period(), MAPeriod, MAMethod, 0, MACDPrice)
        indHandle2 = iMA(symbol2, Period(), MAPeriod, MAMethod, 0, MACDPrice)
        indHandle3 = iMA(symbol3, Period(), MAPeriod, MAMethod, 0, MACDPrice)
        shortName = StringFormat('Arbitrage %s(%d)', StringSubstr(EnumToString(MAMethod, 'ENUM_MA_METHOD'), 5), MAPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 5)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    elif _sw1 == INDICATOR_MACD:
        indHandle1 = iMACD(symbol1, Period(), FastEMA, SlowEMA, SignalSMA, MACDPrice)
        indHandle2 = iMACD(symbol2, Period(), FastEMA, SlowEMA, SignalSMA, MACDPrice)
        indHandle3 = iMACD(symbol3, Period(), FastEMA, SlowEMA, SignalSMA, MACDPrice)
        shortName = StringFormat('Arbitrage MACD(%d,%d,%d)', FastEMA, SlowEMA, SignalSMA)
        IndicatorSetInteger(INDICATOR_DIGITS, 5)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    elif _sw1 == INDICATOR_STOCHASTIC:
        indHandle1 = iStochastic(symbol1, Period(), Kperiod, Dperiod, Slowing, MODE_SMA, PriceField)
        indHandle2 = iStochastic(symbol2, Period(), Kperiod, Dperiod, Slowing, MODE_SMA, PriceField)
        indHandle3 = iStochastic(symbol3, Period(), Kperiod, Dperiod, Slowing, MODE_SMA, PriceField)
        shortName = StringFormat('Arbitrage Stochastic(%d,%d,%d)', Kperiod, Dperiod, Slowing)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level6)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level6)
    elif _sw1 == INDICATOR_RSI:
        indHandle1 = iRSI(symbol1, Period(), RSIPeriod, RSIPrice)
        indHandle2 = iRSI(symbol2, Period(), RSIPeriod, RSIPrice)
        indHandle3 = iRSI(symbol3, Period(), RSIPeriod, RSIPrice)
        shortName = StringFormat('Arbitrage RSI(%d)', RSIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level4)
    elif _sw1 == INDICATOR_CCI:
        indHandle1 = iCCI(symbol1, Period(), CCIPeriod, CCIPrice)
        indHandle2 = iCCI(symbol2, Period(), CCIPeriod, CCIPrice)
        indHandle3 = iCCI(symbol3, Period(), CCIPeriod, CCIPrice)
        shortName = StringFormat('Arbitrage CCI(%d)', CCIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level8)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level8)
    elif _sw1 == INDICATOR_RVI:
        indHandle1 = iRVI(symbol1, Period(), RVIPeriod)
        indHandle2 = iRVI(symbol2, Period(), RVIPeriod)
        indHandle3 = iRVI(symbol3, Period(), RVIPeriod)
        shortName = StringFormat('Arbitrage RVI(%d)', RVIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 3)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level2)
    elif _sw1 == INDICATOR_DEMARK:
        indHandle1 = iDeMarker(symbol1, Period(), DeMarkerPeriod)
        indHandle2 = iDeMarker(symbol2, Period(), DeMarkerPeriod)
        indHandle3 = iDeMarker(symbol3, Period(), DeMarkerPeriod)
        shortName = StringFormat('Arbitrage DeMarker(%d)', DeMarkerPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 3)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level2)
    elif _sw1 == INDICATOR_TRIX:
        indHandle1 = iTriX(symbol1, Period(), TrixPeriod, TrixPrice)
        indHandle2 = iTriX(symbol2, Period(), TrixPeriod, TrixPrice)
        indHandle3 = iTriX(symbol3, Period(), TrixPeriod, TrixPrice)
        shortName = StringFormat('Arbitrage TriX(%d)', TrixPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 5)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    if (indHandle1 == INVALID_HANDLE or indHandle2 == INVALID_HANDLE) or indHandle3 == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    chartID = ChartID()
    window = _short(ChartWindowFind(chartID, shortName))
    xStart = 4
    xIncrement = 25
    yStart = 16
    ObjectCreate_u(base, xStart, yStart, colorBase)
    xStart += xIncrement
    ObjectCreate_u(quot, xStart, yStart, colorQuot)
    ArraySetAsSeries(Index1, True)
    ArraySetAsSeries(Index2, True)
    ArraySetAsSeries(Index3, True)
    SetIndexBuffer(0, BaseBuffer)
    ArraySetAsSeries(BaseBuffer, True)
    SetIndexBuffer(1, QuotBuffer)
    ArraySetAsSeries(QuotBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    if FillBuffers:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_FILLING)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, colorBase)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, colorQuot)
        PlotIndexSetString(0, PLOT_LABEL, base + ';' + quot)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, colorBase)
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, colorQuot)
        PlotIndexSetString(0, PLOT_LABEL, base)
        PlotIndexSetString(1, PLOT_LABEL, quot)
    if ColorBars:
        if ChartGetInteger(0, CHART_COLOR_CANDLE_BULL) != colorBase:
            ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, colorBase)
            ChartSetInteger(0, CHART_COLOR_CHART_UP, colorBase)
        if ChartGetInteger(0, CHART_COLOR_CANDLE_BEAR) != colorQuot:
            ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, colorQuot)
            ChartSetInteger(0, CHART_COLOR_CHART_DOWN, colorQuot)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global baseIndex, index1, index2, index3, quotIndex
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if prev_calculated > rates_total or prev_calculated <= 0:
        barsWindow = _int(ChartGetInteger(chartID, CHART_VISIBLE_BARS)) + 20
        if ((((iBars(symbol1, Period()) <= barsWindow or BarsCalculated(indHandle1) < barsWindow) or iBars(symbol2, Period()) <= barsWindow) or BarsCalculated(indHandle2) < barsWindow) or iBars(symbol3, Period()) <= barsWindow) or BarsCalculated(indHandle3) < barsWindow:
            return 0
        ArrayInitialize(BaseBuffer, EMPTY_VALUE)
        ArrayInitialize(QuotBuffer, EMPTY_VALUE)
        limit = barsWindow - 2
    toCopy = limit + 2
    copied = 0
    if ((copied := CopyBuffer(indHandle1, 0, _DT(time[0]), toCopy, Index1)) != toCopy or (copied := CopyBuffer(indHandle2, 0, _DT(time[0]), toCopy, Index2)) != toCopy) or (copied := CopyBuffer(indHandle3, 0, _DT(time[0]), toCopy, Index3)) != toCopy:
        printf('Error: %d', GetLastError())
        return (0 if (not prev_calculated) else (rates_total - 1))
    for i in range(limit, 0 - 1, -1):
        index1 = Index1[i]
        index2 = Index2[i]
        index3 = Index3[i]
        _sw2 = Indicator
        if _sw2 == INDICATOR_MA:
            index1 -= Index1[i + 1]
            if quotJPY1:
                index1 = index1 / 100
            index2 -= Index2[i + 1]
            if quotJPY2:
                index2 = index2 / 100
            index3 -= Index3[i + 1]
            if quotJPY3:
                index3 = index3 / 100
        elif _sw2 == INDICATOR_MACD:
            if quotJPY1:
                index1 = index1 / 100
            if quotJPY2:
                index2 = index2 / 100
            if quotJPY3:
                index3 = index3 / 100
        elif _sw2 in (INDICATOR_STOCHASTIC, INDICATOR_RSI):
            index1 -= 50
            index2 -= 50
            index3 -= 50
        elif _sw2 == INDICATOR_DEMARK:
            index1 -= 0.5
            index2 -= 0.5
            index3 -= 0.5
        else:
            pass
        if quotUSD:
            baseIndex = (index1 + index2) / 2
            index1 *= -1
            quotIndex = (index1 + index3) / 2
        if quotJPY:
            if Symbol() == 'USDJPY':
                index2 *= -1
            baseIndex = (index1 + index2) / 2
            index1 *= -1
            index3 *= -1
            quotIndex = (index1 + index3) / 2
        if baseUSD:
            baseIndex = (index1 + index3) / 2
            index1 *= -1
            quotIndex = (index1 + index2) / 2
        BaseBuffer[i] = baseIndex
        QuotBuffer[i] = quotIndex
    return rates_total

def OnDeinit(reason):
    ObjectDelete(chartID, base + _str(window))
    ObjectDelete(chartID, quot + _str(window))
    IndicatorRelease(indHandle1)
    IndicatorRelease(indHandle2)
    IndicatorRelease(indHandle3)
    return

def ObjectCreate_u(currency, x, y, clr):
    name = currency + _str(window)
    ObjectCreate(chartID, name, OBJ_LABEL, window, 0, 0)
    ObjectSetString(chartID, name, OBJPROP_TEXT, currency)
    ObjectSetString(chartID, name, OBJPROP_FONT, 'Arial Bold')
    ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chartID, name, OBJPROP_YDISTANCE, y)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Arbitrage(_MQL5Indicator):
    name = 'Arbitrage'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Indicator': _Choice({0: 'Moving Average', 1: 'Moving Average Convergence/Divergence', 2: 'Stochastic Oscillator', 3: 'Relative Strength Index', 4: 'Commodity Channel Index', 5: 'Relative Vigor Index', 6: 'DeMarker Oscillator', 7: 'Triple Exponential Average'}, default=0),
        'MAPeriod': 14,  # MA Period
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Price
        'FastEMA': 12,  # Fast EMA Period
        'SlowEMA': 26,  # Slow EMA Period
        'SignalSMA': 9,  # Signal SMA Period
        'MACDPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD Price
        'Kperiod': 7,  # K Period
        'Dperiod': 3,  # D Period
        'Slowing': 3,
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Price Field
        'RSIPeriod': 14,  # RSI Period
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI Price
        'CCIPeriod': 14,  # CCI Period
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # CCI Price
        'RVIPeriod': 14,  # RVI Period
        'DeMarkerPeriod': 14,  # DeMarker Period
        'TrixPeriod': 14,  # TriX Period
        'TrixPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # TriX Price
        'ColorBars': True,  # Color Bars
        'FillBuffers': True,  # Fill Buffers
    }

