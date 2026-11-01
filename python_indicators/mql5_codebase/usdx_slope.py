"""USDX_Slope — converted from MQL5: MQL5 Indicators/USDX_Slope/USDX_Slope.mq5

USDX vs Slope Direction Line indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [32768], 2: [255], 3: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Neutral'}, 'levels': [], 'description': ['USDX vs Slope Direction Line indicator'], 'name': 'USDX_Slope', 'source': 'MQL5 Indicators/USDX_Slope/USDX_Slope.mq5', 'folder': 'USDX_Slope', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 80, 'label': 'SDL Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'SDL Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'SDL Applied price', 'sinput': False}, {'mql': 'InpShiftX', 'py': 'InpShiftX', 'param': 'InpShiftX', 'type': 'uint', 'default': 1, 'label': 'USDX slope shift', 'sinput': False}, {'mql': 'InpReverceX', 'py': 'InpReverceX', 'param': 'InpReverceX', 'type': 'int', 'default': 0, 'label': 'USDX reverce', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

indicator_color1 = 32768  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 11119017  # #property indicator_color3

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 80)  # SDL Period
InpMethod = _input('InpMethod', MODE_SMA)  # SDL Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # SDL Applied price
InpShiftX = _input('InpShiftX', 1)  # USDX slope shift
InpReverceX = _input('InpReverceX', INPUT_NO)  # USDX reverce
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferSDL = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferMAP2 = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferUSDX = Arr(0, 0.0)
prefix = ""
wnd = 0
shiftX = 0
period_ma = 0
period2 = 0
periodSqrt = 0
handle_maP = 0
handle_maP2 = 0
weight_sum = 0

def OnInit():
    global handle_maP, handle_maP2, period2, periodSqrt, period_ma, prefix, shiftX, wnd
    EventSetTimer(90)
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    shiftX = (1 if (InpShiftX < 1) else InpShiftX)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period2 = _int(floor(period_ma / 2.0))
    periodSqrt = _int(floor(sqrt(period_ma)))
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSDL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAP2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferUSDX, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, ('Reverce ' if InpReverceX else '') + 'USDX (' + _str(shiftX) + ') vs SDL(' + _str(period_ma) + ') Bar')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferSDL, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferMAP2, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferUSDX, True)
    ResetLastError()
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP2 = iMA(None, PERIOD_CURRENT, period2, 0, InpMethod, InpAppliedPrice)
    if handle_maP2 == INVALID_HANDLE:
        Print('The iMA(', _str(period2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    if not SymbolCheck('EURUSD'):
        return INIT_FAILED
    if not SymbolCheck('USDJPY'):
        return INIT_FAILED
    if not SymbolCheck('GBPUSD'):
        return INIT_FAILED
    if not SymbolCheck('USDCAD'):
        return INIT_FAILED
    if not SymbolCheck('USDSEK'):
        return INIT_FAILED
    if not SymbolCheck('USDCHF'):
        return INIT_FAILED
    Time('EURUSD', PERIOD_CURRENT, 1)
    Time('USDJPY', PERIOD_CURRENT, 1)
    Time('GBPUSD', PERIOD_CURRENT, 1)
    Time('USDCAD', PERIOD_CURRENT, 1)
    Time('USDSEK', PERIOD_CURRENT, 1)
    Time('USDCHF', PERIOD_CURRENT, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(4, fmax(shiftX, period_ma)):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - shiftX - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferSDL, 0)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferMAP2, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferUSDX, 0)
    if Time('EURUSD', PERIOD_CURRENT, 1) == 0:
        return 0
    if Time('USDJPY', PERIOD_CURRENT, 1) == 0:
        return 0
    if Time('GBPUSD', PERIOD_CURRENT, 1) == 0:
        return 0
    if Time('USDCAD', PERIOD_CURRENT, 1) == 0:
        return 0
    if Time('USDSEK', PERIOD_CURRENT, 1) == 0:
        return 0
    if Time('USDCHF', PERIOD_CURRENT, 1) == 0:
        return 0
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP2, 0, 0, count, BufferMAP2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        clEU = Close('EURUSD', PERIOD_CURRENT, i)
        clUJ = Close('USDJPY', PERIOD_CURRENT, i)
        clGU = Close('GBPUSD', PERIOD_CURRENT, i)
        clUC = Close('USDCAD', PERIOD_CURRENT, i)
        clUS = Close('USDSEK', PERIOD_CURRENT, i)
        clUCH = Close('USDCHF', PERIOD_CURRENT, i)
        if ((((clEU == 0 or clUJ == 0) or clGU == 0) or clUC == 0) or clUS == 0) or clUCH == 0:
            continue
        EU = pow(clEU, -0.576)
        UJ = pow(clUJ, 0.136)
        GU = pow(clGU, -0.119)
        UC = pow(clUC, 0.091)
        US = pow(clUS, 0.042)
        UCH = pow(clUCH, 0.036)
        x = 50.14348112 * EU * UJ * GU * UC * US * UCH
        BufferUSDX[i] = (_fdiv(1.0, x) if InpReverceX else x)
        BufferRAW[i] = (2.0 * BufferMAP2[i]) - BufferMAP[i]
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        SetNeutral(i)
        if BufferSDL[i] > BufferSDL[i + 1] and BufferUSDX[i] > BufferUSDX[i + shiftX]:
            SetUp(i)
        elif BufferSDL[i] < BufferSDL[i + 1] and BufferUSDX[i] < BufferUSDX[i + shiftX]:
            SetDown(i)
        else:
            SetNeutral(i)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        for i in range(0, 3):
            PlotIndexSetInteger(i, PLOT_LINE_WIDTH, SizeByScale())
        Descriptions()
        ChartRedraw()

def OnTimer():
    Time('EURUSD', PERIOD_CURRENT, 1)
    Time('USDJPY', PERIOD_CURRENT, 1)
    Time('GBPUSD', PERIOD_CURRENT, 1)
    Time('USDCAD', PERIOD_CURRENT, 1)
    Time('USDSEK', PERIOD_CURRENT, 1)
    Time('USDCHF', PERIOD_CURRENT, 1)

def SizeByScale():
    scale = _uchar(ChartGetInteger(0, CHART_SCALE))
    size = (1 if (scale < 3) else 2 if (scale == 3) else 5 if (scale == 4) else 8)
    return size

def Descriptions():
    x = 4
    y = 1
    arr_colors = Arr.of([_int(indicator_color1), _int(indicator_color2), _int(indicator_color3)], fill=0)
    arr_texts = Arr.of(['Up direction', 'Down direction', 'Neutral'], fill="")
    arr_names = Arr(3, "", dyn=False)
    for i in range(0, 3):
        arr_names[i] = prefix + 'label' + _str(i)
        arr_colors[i] = PlotIndexGetInteger(i, PLOT_LINE_COLOR)
        shift = (i * (90 if (i < 2) else 96)) - (x if (i > 0) else 0)
        x += shift
        Label(arr_names[i], x, y, CharToString(167), 16, arr_colors[i], 'Wingdings')
        Label(arr_names[i] + '_txt', x + 10, y + 5, arr_texts[i], 10, clrGray, 'Calibri')

def Label(name, x, y, text, size, clr, font):
    if ObjectFind(0, name) != wnd:
        ObjectCreate(0, name, OBJ_LABEL, wnd, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetString(0, name, OBJPROP_FONT, font)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, '\n')

def SetUp(index):
    BufferUP[index] = 0.5
    BufferNL[index] = EMPTY_VALUE
    BufferDN[index] = BufferNL[index]

def SetDown(index):
    BufferDN[index] = 0.5
    BufferNL[index] = EMPTY_VALUE
    BufferUP[index] = BufferNL[index]

def SetNeutral(index):
    BufferNL[index] = 0.5
    BufferUP[index] = EMPTY_VALUE
    BufferDN[index] = BufferUP[index]

def SymbolCheck(symbol_name):
    select = Box(0)
    ResetLastError()
    if not SymbolInfoInteger(symbol_name, SYMBOL_SELECT, select):
        err = GetLastError()
        Print('Error: ', err, ' Symbol ', symbol_name, ' does not exist')
        return False
    else:
        if select.v:
            return True
        ResetLastError()
        if not SymbolSelect(symbol_name, True):
            err = GetLastError()
            Print('Error selected ', symbol_name, ': ', err)
    return False

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Close(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyClose(symbol_name, timeframe, shift, 1, array) == 1) else 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class USDXSlope(_MQL5Indicator):
    name = 'USDX_Slope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 80,  # SDL Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # SDL Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # SDL Applied price
        'InpShiftX': 1,  # USDX slope shift
        'InpReverceX': _Choice({1: 'Yes', 0: 'No'}, default=0),  # USDX reverce
    }

