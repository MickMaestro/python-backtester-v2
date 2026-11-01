"""dailydata — converted from MQL5: MQL5 Indicators/Daily Data/dailydata.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [11829830, 9662683, 6908265]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Daily data'}, 'levels': [], 'description': [], 'name': 'dailydata', 'source': 'MQL5 Indicators/Daily Data/dailydata.mq5', 'folder': 'Daily Data', 'inputs': [{'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Text color', 'sinput': False}, {'mql': 'ButtonColor', 'py': 'ButtonColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Background color', 'sinput': False}, {'mql': 'AreaColor', 'py': 'AreaColor', 'param': None, 'type': 'color', 'default': 4737096, 'label': 'Area color', 'sinput': False}, {'mql': 'SymbolColor', 'py': 'SymbolColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Symbol color', 'sinput': False}, {'mql': 'LabelsColor', 'py': 'LabelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Labels color', 'sinput': False}, {'mql': 'ValuesNeutralColor', 'py': 'ValuesNeutralColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color for unchanged values', 'sinput': False}, {'mql': 'ValuesPositiveColor', 'py': 'ValuesPositiveColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color for positive values', 'sinput': False}, {'mql': 'ValuesNegativeColor', 'py': 'ValuesNegativeColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color for negative values', 'sinput': False}, {'mql': 'XPosition', 'py': 'XPosition', 'param': 'XPosition', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'YPosition', 'py': 'YPosition', 'param': 'YPosition', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'CandleShift', 'py': 'CandleShift', 'param': 'CandleShift', 'type': 'int', 'default': 5, 'label': 'Candle shift', 'sinput': False}, {'mql': 'TimeFontSize', 'py': 'TimeFontSize', 'param': 'TimeFontSize', 'type': 'int', 'default': 10, 'label': 'Font size for timer', 'sinput': False}, {'mql': 'TimerShift', 'py': 'TimerShift', 'param': 'TimerShift', 'type': 'int', 'default': 7, 'label': 'Timer shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkGray = 0xA9A9A9  # MQL4 colour name
DimGray = 0x696969  # MQL4 colour name
MediumSeaGreen = 0x71B33C  # MQL4 colour name
OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter
PaleVioletRed = 0x9370DB  # MQL4 colour name
SteelBlue = 0xB48246  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
AreaColor = _input('AreaColor', 0x484848)  # Area color
XPosition = _input('XPosition', 10)
YPosition = _input('YPosition', 10)
Corner = _input('Corner', CORNER_RIGHT_UPPER)
CandleShift = _input('CandleShift', 5)  # Candle shift
TimeFontSize = _input('TimeFontSize', 10)  # Font size for timer
TimerShift = _input('TimerShift', 7)  # Timer shift
candleOpen = Arr(0, 0.0)
candleHigh = Arr(0, 0.0)
candleLow = Arr(0, 0.0)
candleClose = Arr(0, 0.0)
candleColor = Arr(0, 0.0)
atrHandle = 0
heightTotal = 0

def OnInit():
    global atrHandle
    SetIndexBuffer(0, candleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, candleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, candleLow, INDICATOR_DATA)
    SetIndexBuffer(3, candleClose, INDICATOR_DATA)
    SetIndexBuffer(4, candleColor, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, CandleShift)
    createObjects()
    setControls()
    atrHandle = iATR(None, 0, 30)
    return 0

def OnDeinit(reason):
    _sw1 = reason
    if _sw1 == REASON_REMOVE:
        for i in range(ObjectsTotal(0), 0 - 1, -1):
            name = ObjectName(ChartID(), i)
            if StringSubstr(name, 0, 9) == 'DailyData':
                ObjectDelete(ChartID(), name)
        ChartRedraw()
    if not getState('DailyDataShowTimer'):
        EventKillTimer()

def OnTimer():
    refreshData()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    refreshData()
    return rates_total

def refreshData():
    global _s_refreshData_inRefresh
    if _s_refreshData_inRefresh:
        return
    _s_refreshData_inRefresh = True
    bars = ArraySize(candleClose)
    period = PERIOD_D1
    if Period() >= PERIOD_D1:
        period = PERIOD_W1
    if Period() >= PERIOD_W1:
        period = PERIOD_MN1
    CopyTime(Symbol(), 0, 0, 1, _s_refreshData_times)
    if CopyRates(Symbol(), period, 0, 1, _s_refreshData_rates) < 1:
        _s_refreshData_inRefresh = False
        return
    candleOpen[bars - 1] = _s_refreshData_rates[0].open
    candleClose[bars - 1] = _s_refreshData_rates[0].close
    candleHigh[bars - 1] = _s_refreshData_rates[0].high
    candleLow[bars - 1] = _s_refreshData_rates[0].low
    candleColor[bars - 1] = 2.0
    if candleOpen[bars - 1] < candleClose[bars - 1]:
        candleColor[bars - 1] = 0.0
    if candleOpen[bars - 1] > candleClose[bars - 1]:
        candleColor[bars - 1] = 1.0
    ObjectSetDouble(0, 'DailyDataArea', OBJPROP_PRICE, 0, _s_refreshData_rates[0].high)
    ObjectSetDouble(0, 'DailyDataArea', OBJPROP_PRICE, 1, _s_refreshData_rates[0].low)
    ObjectSetInteger(0, 'DailyDataArea', OBJPROP_TIME, 0, _s_refreshData_rates[0].time)
    ObjectSetInteger(0, 'DailyDataArea', OBJPROP_TIME, 1, _s_refreshData_times[0])
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, bars - 1)
    pipModifier = 1.0
    if Digits() == 3 or Digits() == 5:
        pipModifier = 10.0
    setBasicValue('DailyDataSymbol', DoubleToString(_s_refreshData_rates[0].close, Digits()), XPosition, YPosition + 20, Corner)
    setBasicValue('DailyDataClock', DoubleToString(_fdiv(_fdiv(_s_refreshData_rates[0].high - _s_refreshData_rates[0].low, Point()), pipModifier), 1), XPosition, YPosition + 38, Corner)
    setBasicValue('DailyDataRange', DoubleToString(_fdiv(_fdiv(_s_refreshData_rates[0].close - _s_refreshData_rates[0].open, Point()), pipModifier), 1), XPosition, YPosition + 56, Corner)
    setBasicValue('DailyDataChange', DoubleToString(_fdiv(_fdiv(_s_refreshData_rates[0].high - _s_refreshData_rates[0].close, Point()), pipModifier), 1), XPosition, YPosition + 74, Corner)
    setBasicValue('DailyDataDistH', DoubleToString(_fdiv(_fdiv(_s_refreshData_rates[0].close - _s_refreshData_rates[0].low, Point()), pipModifier), 1), XPosition, YPosition + 92, Corner)
    setSwapValue('DailyDataSwapShort', DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_SHORT), 1), XPosition, YPosition + 20, Corner)
    setSwapValue('DailyDataSwapLong', DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_SWAP_LONG), 1), XPosition, YPosition + 38, Corner)
    if not getState('DailyDataShowTimer'):
        ShowClock()
    ChartRedraw()
    _s_refreshData_inRefresh = False

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if sparam == 'DailyDataShowBasic':
            setControls()
        if sparam == 'DailyDataShowSwaps':
            setControls()
        if sparam == 'DailyDataShowCandle':
            setControls()
        if sparam == 'DailyDataShowArea':
            setControls()
        if sparam == 'DailyDataShowTimer':
            setControls()

def createObjects():
    if ObjectFind(0, 'DailyDataShowBasic') < 0:
        ObjectCreate(0, 'DailyDataShowBasic', OBJ_BUTTON, 0, 0, 0, 0, 0)
    if ObjectFind(0, 'DailyDataShowSwaps') < 0:
        ObjectCreate(0, 'DailyDataShowSwaps', OBJ_BUTTON, 0, 0, 0, 0, 0)
    if ObjectFind(0, 'DailyDataShowCandle') < 0:
        ObjectCreate(0, 'DailyDataShowCandle', OBJ_BUTTON, 0, 0, 0, 0, 0)
    if ObjectFind(0, 'DailyDataShowArea') < 0:
        ObjectCreate(0, 'DailyDataShowArea', OBJ_BUTTON, 0, 0, 0, 0, 0)
    if ObjectFind(0, 'DailyDataShowTimer') < 0:
        ObjectCreate(0, 'DailyDataShowTimer', OBJ_BUTTON, 0, 0, 0, 0, 0)
    if ObjectFind(0, 'DailyDataArea') < 0:
        ObjectCreate(0, 'DailyDataArea', OBJ_RECTANGLE, 0, 0, 0, 0, 0)

def getState(name):
    ans = (_int(ObjectGetInteger(0, name, OBJPROP_STATE)) != 0)
    return ans

def setVisibleState(control, state):
    if state:
        ObjectSetInteger(0, control, OBJPROP_TIMEFRAMES, OBJ_ALL_PERIODS)
    else:
        ObjectSetInteger(0, control, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)

def setControls():
    global heightTotal
    heightBasic = 20
    if not getState('DailyDataShowBasic'):
        heightBasic = 110
    heightSwap = 20
    if not getState('DailyDataShowSwaps'):
        heightSwap = 56
    heightCandle = 20
    heightArea = 20
    heightTimer = 20
    heightTotal = YPosition + heightArea + heightBasic + heightCandle + heightSwap + heightTimer
    pos = YPosition
    caption = ""
    if not getState('DailyDataShowBasic'):
        caption = 'Hide basic data'
    else:
        caption = 'Show basic data'
    setButton('DailyDataShowBasic', caption, XPosition, pos, TextColor, ButtonColor, Corner)
    pos += heightBasic
    if not getState('DailyDataShowSwaps'):
        caption = 'Hide swaps'
    else:
        caption = 'Show swaps'
    setButton('DailyDataShowSwaps', caption, XPosition, pos, TextColor, ButtonColor, Corner)
    pos += heightSwap
    if not getState('DailyDataShowCandle'):
        caption = 'Hide candle'
    else:
        caption = 'Show candle'
    setButton('DailyDataShowCandle', caption, XPosition, pos, TextColor, ButtonColor, Corner)
    pos += heightCandle
    if not getState('DailyDataShowArea'):
        caption = 'Hide area'
    else:
        caption = 'Show area'
    setButton('DailyDataShowArea', caption, XPosition, pos, TextColor, ButtonColor, Corner)
    pos += heightArea
    if not getState('DailyDataShowTimer'):
        caption = 'Hide timer'
    else:
        caption = 'Show timer'
    setButton('DailyDataShowTimer', caption, XPosition, pos, TextColor, ButtonColor, Corner)
    setVisibleState('DailyDataTimer', not getState('DailyDataShowTimer'))
    if not getState('DailyDataShowTimer'):
        EventSetTimer(1)
    else:
        EventKillTimer()
    ObjectSetInteger(0, 'DailyDataArea', OBJPROP_COLOR, AreaColor)
    ObjectSetInteger(0, 'DailyDataArea', OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, 'DailyDataArea', OBJPROP_BACK, True)
    setVisibleState('DailyDataArea', not getState('DailyDataShowArea'))
    setBasicLabel('DailyDataSymbol', Symbol(), XPosition, YPosition + 20, Corner, SymbolColor, 13)
    setBasicLabel('DailyDataClock', 'range', XPosition, YPosition + 38, Corner, LabelsColor)
    setBasicLabel('DailyDataRange', 'change', XPosition, YPosition + 56, Corner, LabelsColor)
    setBasicLabel('DailyDataChange', 'distance from high', XPosition, YPosition + 74, Corner, LabelsColor)
    setBasicLabel('DailyDataDistH', 'distance from low', XPosition, YPosition + 92, Corner, LabelsColor)
    setVisibleState('DailyDataSymbol' + 'v', not getState('DailyDataShowBasic'))
    setVisibleState('DailyDataClock' + 'v', not getState('DailyDataShowBasic'))
    setVisibleState('DailyDataRange' + 'v', not getState('DailyDataShowBasic'))
    setVisibleState('DailyDataChange' + 'v', not getState('DailyDataShowBasic'))
    setVisibleState('DailyDataDistH' + 'v', not getState('DailyDataShowBasic'))
    ObjectSetInteger(0, 'DailyDataSymbol' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataSymbol', OBJPROP_YDISTANCE))
    ObjectSetInteger(0, 'DailyDataClock' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataClock', OBJPROP_YDISTANCE))
    ObjectSetInteger(0, 'DailyDataRange' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataRange', OBJPROP_YDISTANCE))
    ObjectSetInteger(0, 'DailyDataChange' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataChange', OBJPROP_YDISTANCE))
    ObjectSetInteger(0, 'DailyDataDistH' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataDistH', OBJPROP_YDISTANCE))
    setSwapLabel('DailyDataSwapShort', 'swap short', XPosition, YPosition + 20, Corner, LabelsColor)
    setSwapLabel('DailyDataSwapLong', 'swap long', XPosition, YPosition + 38, Corner, LabelsColor)
    setVisibleState('DailyDataSwapShort' + 'v', not getState('DailyDataShowSwaps'))
    setVisibleState('DailyDataSwapLong' + 'v', not getState('DailyDataShowSwaps'))
    ObjectSetInteger(0, 'DailyDataSwapShort' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataSwapShort', OBJPROP_YDISTANCE))
    ObjectSetInteger(0, 'DailyDataSwapLong' + 'v', OBJPROP_YDISTANCE, ObjectGetInteger(0, 'DailyDataSwapLong', OBJPROP_YDISTANCE))
    if getState('DailyDataShowCandle'):
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
    ChartRedraw()

def setButton(name, caption, xposition, yposition, textColor, backColor, corner):
    relXPosition = xposition
    if corner == 2 or corner == 3:
        relXPosition = 190 + xposition
    relYPosition = yposition
    if corner == 1 or corner == 2:
        relYPosition = heightTotal - yposition + YPosition
    ObjectSetInteger(0, name, OBJPROP_COLOR, textColor)
    ObjectSetInteger(0, name, OBJPROP_BGCOLOR, backColor)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, relXPosition)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, relYPosition)
    ObjectSetInteger(0, name, OBJPROP_XSIZE, 190)
    ObjectSetInteger(0, name, OBJPROP_YSIZE, 18)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, name, OBJPROP_CORNER, corner)
    ObjectSetString(0, name, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, name, OBJPROP_TEXT, caption)

def setBasicLabel(name, label, xposition, yposition, corner, labelColor, fontSize=10, anchor=ANCHOR_LEFT_UPPER, statusCheck='DailyDataShowBasic', displacement=0):
    relXPosition = xposition
    if corner == 2 or corner == 3:
        relXPosition = 190 + xposition
    relYPosition = yposition + displacement
    if corner == 1 or corner == 2:
        relYPosition = heightTotal - yposition - displacement + YPosition
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(0, name, OBJPROP_COLOR, labelColor)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, relXPosition)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, relYPosition)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, fontSize)
    ObjectSetString(0, name, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, name, OBJPROP_TEXT, label)
    setVisibleState(name, not getState(statusCheck))

def setBasicValue(name, value, xposition, yposition, corner, fontSize=12, statusCheck='DailyDataShowBasic', displacement=0):
    dvalue = StringToDouble(value)
    cvalue = ValuesNeutralColor
    if dvalue > 0:
        cvalue = ValuesPositiveColor
    if dvalue < 0:
        cvalue = ValuesNegativeColor
    if corner == 0 or corner == 1:
        xposition += 190
    if corner == 2 or corner == 3:
        xposition -= 190
    setBasicLabel(name + 'v', value, xposition, yposition, corner, cvalue, fontSize, ANCHOR_RIGHT_UPPER, statusCheck, displacement)

def setSwapLabel(name, label, xposition, yposition, corner, labelColor, fontSize=10):
    heightBasic = (110 if (not getState('DailyDataShowBasic')) else 20)
    setBasicLabel(name, label, xposition, yposition, corner, labelColor, fontSize, ANCHOR_LEFT_UPPER, 'DailyDataShowSwaps', heightBasic)

def setSwapValue(name, value, xposition, yposition, corner, fontSize=12):
    heightBasic = (110 if (not getState('DailyDataShowBasic')) else 20)
    setBasicValue(name, value, xposition, yposition, corner, fontSize, 'DailyDataShowSwaps', heightBasic)

def ShowClock():
    periodMinutes = periodToMinutes(Period())
    shift = periodMinutes * TimerShift * 60
    currentTime = _int(TimeCurrent())
    localTime = _int(TimeLocal())
    barTime = _int(iTime_u())
    diff = _int(MathMax(round((currentTime - localTime) / 3600.0) * 3600, -24 * 3600))
    theColor = Box(0)
    time = getTime(barTime + (periodMinutes * 60) - localTime - diff, theColor)
    time = (time if TerminalInfoInteger(TERMINAL_CONNECTED) else (time + ' x'))
    if ObjectFind(0, 'DailyDataTimer') < 0:
        ObjectCreate(0, 'DailyDataTimer', OBJ_TEXT, 0, barTime + shift, 0)
    ObjectSetString(0, 'DailyDataTimer', OBJPROP_TEXT, time)
    ObjectSetString(0, 'DailyDataTimer', OBJPROP_FONT, 'Arial')
    ObjectSetInteger(0, 'DailyDataTimer', OBJPROP_FONTSIZE, TimeFontSize)
    ObjectSetInteger(0, 'DailyDataTimer', OBJPROP_COLOR, theColor.v)
    if ChartGetInteger(0, CHART_SHIFT, 0) == 0 and shift >= 0:
        ObjectSetInteger(0, 'DailyDataTimer', OBJPROP_TIME, barTime - (shift * 3))
    else:
        ObjectSetInteger(0, 'DailyDataTimer', OBJPROP_TIME, barTime + shift)
    price = Arr(0, 0.0)
    if CopyClose(Symbol(), 0, 0, 1, price) <= 0:
        return
    atr = Arr(0, 0.0)
    if CopyBuffer(atrHandle, 0, 0, 1, atr) <= 0:
        return
    price[0] += (3.0 * atr[0]) / 4.0
    visible = (ChartGetInteger(0, CHART_VISIBLE_BARS, 0) - ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR, 0)) > 0
    if visible and price[0] >= ChartGetDouble(0, CHART_PRICE_MAX, 0):
        ObjectSetDouble(0, 'DailyDataTimer', OBJPROP_PRICE, price[0] - (1.5 * atr[0]))
    else:
        ObjectSetDouble(0, 'DailyDataTimer', OBJPROP_PRICE, price[0])

def getTime(times, theColor):
    stime = ''
    seconds = 0
    minutes = 0
    hours = 0
    if times < 0:
        theColor.v = ValuesNegativeColor
        times = fabs(times)
    else:
        theColor.v = ValuesPositiveColor
    seconds = _imod(times, 60)
    hours = _idiv(times - _imod(times, 3600), 3600)
    minutes = _idiv(times - seconds, 60) - (hours * 60)
    if hours > 0:
        if minutes < 10:
            stime = stime + _str(hours) + ':0'
        else:
            stime = stime + _str(hours) + ':'
    stime = stime + _str(minutes)
    if seconds < 10:
        stime = stime + ':0' + _str(seconds)
    else:
        stime = stime + ':' + _str(seconds)
    return stime

def iTime_u(forPeriod=PERIOD_CURRENT):
    times = Arr(0, 0)
    if CopyTime(Symbol(), forPeriod, 0, 1, times) <= 0:
        return TimeLocal()
    return times[0]

def periodToMinutes(period):
    i = 0
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    for i in range(i, 20):
        if period == _s_periodToMinutes__per[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_periodToMinutes__min[i]

# ---- global variables initialised from expressions
TextColor = _input('TextColor', _uint(White))  # Text color
ButtonColor = _input('ButtonColor', _uint(SteelBlue))  # Background color
SymbolColor = _input('SymbolColor', _uint(PaleVioletRed))  # Symbol color
LabelsColor = _input('LabelsColor', _uint(DarkGray))  # Labels color
ValuesNeutralColor = _input('ValuesNeutralColor', _uint(DimGray))  # Color for unchanged values
ValuesPositiveColor = _input('ValuesPositiveColor', _uint(MediumSeaGreen))  # Color for positive values
ValuesNegativeColor = _input('ValuesNegativeColor', _uint(PaleVioletRed))  # Color for negative values

# ---- static local variables
_s_refreshData_inRefresh = False
_s_refreshData_times = Arr(1, 0, dyn=False)
_s_refreshData_rates = Arr(1, 0, dyn=False, factory=MqlRates)
_s_periodToMinutes__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToMinutes__min = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 360, 480, 720, 1440, 10080, 43200], fill=0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailydata(_MQL5Indicator):
    name = 'dailydata'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XPosition': 10,
        'YPosition': 10,
        'Corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),
        'CandleShift': 5,  # Candle shift
        'TimeFontSize': 10,  # Font size for timer
        'TimerShift': 7,  # Timer shift
    }

