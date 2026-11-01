"""Indicator_Arrows — converted from MQL5: MQL5 Indicators/Indicator Arrows II/Indicator_Arrows.mq5

Indicator Arrows by pipPod
Copyright: Copyright 2015, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [3329330], 2: [2237106]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'BuyArrow', 2: 'SellArrow'}, 'levels': [], 'description': ['Indicator Arrows by pipPod'], 'name': 'Indicator_Arrows', 'source': 'MQL5 Indicators/Indicator Arrows II/Indicator_Arrows.mq5', 'folder': 'Indicator Arrows II', 'inputs': [{'mql': 'Indicator1', 'py': 'Indicator1', 'param': 'Indicator1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Indicator2', 'py': 'Indicator2', 'param': 'Indicator2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Range', 'py': 'Range', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'RangePeriod', 'py': 'RangePeriod', 'param': 'RangePeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MovingAverage', 'py': 'MovingAverage', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MACD', 'py': 'MACD', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'FastMACD', 'py': 'FastMACD', 'param': 'FastMACD', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowMACD', 'py': 'SlowMACD', 'param': 'SlowMACD', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalMACD', 'py': 'SignalMACD', 'param': 'SignalMACD', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'MACDPrice', 'py': 'MACDPrice', 'param': 'MACDPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'OsMA', 'py': 'OsMA', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'FastOsMA', 'py': 'FastOsMA', 'param': 'FastOsMA', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowOsMA', 'py': 'SlowOsMA', 'param': 'SlowOsMA', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalOsMA', 'py': 'SignalOsMA', 'param': 'SignalOsMA', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'OsMAPrice', 'py': 'OsMAPrice', 'param': 'OsMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'OsMASignal', 'py': 'OsMASignal', 'param': 'OsMASignal', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'Stochastic', 'py': 'Stochastic', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'StochMAMethod', 'py': 'StochMAMethod', 'param': 'StochMAMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'RSISignal', 'py': 'RSISignal', 'param': 'RSISignal', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'CCI', 'py': 'CCI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RVI', 'py': 'RVI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ADX', 'py': 'ADX', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ADXPrice', 'py': 'ADXPrice', 'param': 'ADXPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'TriX', 'py': 'TriX', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'TriXPeriod', 'py': 'TriXPeriod', 'param': 'TriXPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'TrixSignal', 'py': 'TrixSignal', 'param': 'TrixSignal', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'TriXPrice', 'py': 'TriXPrice', 'param': 'TriXPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Bands', 'py': 'Bands', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 20, 'label': 'Bands Period', 'sinput': False}, {'mql': 'BBDev', 'py': 'BBDev', 'param': 'BBDev', 'type': 'double', 'default': 2.0, 'label': 'Bands Deviation', 'sinput': False}, {'mql': 'BBPrice', 'py': 'BBPrice', 'param': 'BBPrice', 'type': 'int', 'default': 1, 'label': 'Bands Price', 'sinput': False}, {'mql': '_', 'py': '_', 'param': None, 'type': 'string', 'default': '', 'label': '---', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum indicators
INDICATOR_MA = 0
INDICATOR_MACD = 1
INDICATOR_OSMA = 2
INDICATOR_STOCHASTIC = 3
INDICATOR_RSI = 4
INDICATOR_CCI = 5
INDICATOR_RVI = 6
INDICATOR_ADX = 7
INDICATOR_TRIX = 8
INDICATOR_BANDS = 9
INDICATOR_NONE = 10
_enum('indicators', {0: 'INDICATOR_MA', 1: 'INDICATOR_MACD', 2: 'INDICATOR_OSMA', 3: 'INDICATOR_STOCHASTIC', 4: 'INDICATOR_RSI', 5: 'INDICATOR_CCI', 6: 'INDICATOR_RVI', 7: 'INDICATOR_ADX', 8: 'INDICATOR_TRIX', 9: 'INDICATOR_BANDS', 10: 'INDICATOR_NONE'})

# enum ENUM_SIGNAL
SIGNAL_NONE = 0
SIGNAL_BUY = 1
SIGNAL_SELL = 2
_enum('ENUM_SIGNAL', {0: 'SIGNAL_NONE', 1: 'SIGNAL_BUY', 2: 'SIGNAL_SELL'})

# ---- inputs and global variables
Indicator1 = _input('Indicator1', INDICATOR_MACD)
TimeFrame1 = _input('TimeFrame1', 0)
Indicator2 = _input('Indicator2', INDICATOR_MA)
TimeFrame2 = _input('TimeFrame2', 0)
Range = _input('Range', "")
RangePeriod = _input('RangePeriod', 14)
MovingAverage = _input('MovingAverage', "")
MAPeriod = _input('MAPeriod', 5)
MAMethod = _input('MAMethod', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
MACD = _input('MACD', "")
FastMACD = _input('FastMACD', 12)
SlowMACD = _input('SlowMACD', 26)
SignalMACD = _input('SignalMACD', 9)
MACDPrice = _input('MACDPrice', PRICE_CLOSE)
OsMA = _input('OsMA', "")
FastOsMA = _input('FastOsMA', 12)
SlowOsMA = _input('SlowOsMA', 26)
SignalOsMA = _input('SignalOsMA', 9)
OsMAPrice = _input('OsMAPrice', PRICE_CLOSE)
OsMASignal = _input('OsMASignal', 9)
Stochastic = _input('Stochastic', "")
Kperiod = _input('Kperiod', 8)
Dperiod = _input('Dperiod', 3)
Slowing = _input('Slowing', 3)
StochMAMethod = _input('StochMAMethod', MODE_SMA)
PriceField = _input('PriceField', STO_LOWHIGH)
RSI = _input('RSI', "")
RSIPeriod = _input('RSIPeriod', 8)
RSISignal = _input('RSISignal', 5)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
CCI = _input('CCI', "")
CCIPeriod = _input('CCIPeriod', 14)
CCIPrice = _input('CCIPrice', PRICE_CLOSE)
RVI = _input('RVI', "")
RVIPeriod = _input('RVIPeriod', 10)
ADX = _input('ADX', "")
ADXPeriod = _input('ADXPeriod', 14)
ADXPrice = _input('ADXPrice', PRICE_CLOSE)
TriX = _input('TriX', "")
TriXPeriod = _input('TriXPeriod', 14)
TrixSignal = _input('TrixSignal', 9)
TriXPrice = _input('TriXPrice', PRICE_CLOSE)
Bands = _input('Bands', "")
BBPeriod = _input('BBPeriod', 20)  # Bands Period
BBDev = _input('BBDev', 2.0)  # Bands Deviation
BBPrice = _input('BBPrice', PRICE_CLOSE)  # Bands Price
_ = _input('_', "")  # ---
AlertsOn = _input('AlertsOn', True)
AlertsMessage = _input('AlertsMessage', True)
AlertsEmail = _input('AlertsEmail', False)
AlertsSound = _input('AlertsSound', False)
indicator1 = 0
indicator2 = 0
Buy = Arr(0, 0.0)
Sell = Arr(0, 0.0)
label1 = 'Spread '
label2 = 'Range'
doubleToPip = 0
pipToDouble = 0.0
rangeHandle = 0
indHandle1 = 0
indHandle2 = 0

def OnInit():
    global doubleToPip, indHandle1, indHandle2, pipToDouble, rangeHandle
    IndicatorSetString(INDICATOR_SHORTNAME, 'Indicator Arrows')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if Digits() == 2 or Digits() == 3:
        doubleToPip = 100
    else:
        doubleToPip = 10000
    if Digits() == 2 or Digits() == 4:
        pipToDouble = Point()
    else:
        pipToDouble = Point() * 10
    label3 = ""
    label4 = ""
    xStart = 7
    yStart = 80
    yIncrement = 14
    ySize = 40
    ySizeInc = 15
    ObjectCreate(chartID, 'LabelBox', OBJ_RECTANGLE_LABEL, 0, 0, 0)
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_XDISTANCE, 3)
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_YDISTANCE, 75)
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_XSIZE, 135)
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_YSIZE, ySize)
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_BGCOLOR, clrBlack)
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_BORDER_TYPE, BORDER_FLAT)
    ObjectCreate(chartID, 'Label1', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chartID, 'Label1', OBJPROP_XDISTANCE, xStart)
    ObjectSetInteger(chartID, 'Label1', OBJPROP_YDISTANCE, yStart)
    ObjectSetString(chartID, 'Label1', OBJPROP_FONT, 'Arial Bold')
    ObjectSetInteger(chartID, 'Label1', OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(chartID, 'Label1', OBJPROP_COLOR, clrFireBrick)
    ObjectCreate(chartID, 'Label2', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chartID, 'Label2', OBJPROP_XDISTANCE, xStart)
    ObjectSetInteger(chartID, 'Label2', OBJPROP_YDISTANCE, (yStart := yStart + yIncrement))
    ObjectSetString(chartID, 'Label2', OBJPROP_FONT, 'Arial Bold')
    ObjectSetInteger(chartID, 'Label2', OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(chartID, 'Label2', OBJPROP_COLOR, clrYellow)
    timeFrame1 = StringSubstr(EnumToString(TimeFrame1, 'ENUM_TIMEFRAMES'), 7) + ' '
    timeFrame2 = StringSubstr(EnumToString(TimeFrame2, 'ENUM_TIMEFRAMES'), 7) + ' '
    if timeFrame1 == 'CURRENT ':
        timeFrame1 = ''
    if timeFrame2 == 'CURRENT ':
        timeFrame2 = ''
    rangeHandle = iATR(None, 0, RangePeriod)
    if rangeHandle == INVALID_HANDLE:
        return INIT_FAILED
    indHandle1 = INVALID_HANDLE
    indHandle2 = INVALID_HANDLE
    if Indicator1 == INDICATOR_NONE:
        Alert("Indicator1 can't be 'No Indicator'")
    _sw1 = Indicator1
    if _sw1 == INDICATOR_MA:
        label3 = StringFormat('iMA %s %s (%d)', timeFrame1, StringSubstr(EnumToString(MAMethod, 'ENUM_MA_METHOD'), 5), MAPeriod)
        indHandle1 = iMA(Symbol(), TimeFrame1, MAPeriod, 0, MAMethod, MAPrice)
    elif _sw1 == INDICATOR_MACD:
        label3 = StringFormat('iMACD %s (%d,%d,%d)', timeFrame1, FastMACD, SlowMACD, SignalMACD)
        indHandle1 = iMACD(Symbol(), TimeFrame1, FastMACD, SlowMACD, SignalMACD, MACDPrice)
    elif _sw1 == INDICATOR_OSMA:
        label3 = StringFormat('iOsMA %s (%d,%d,%d)', timeFrame1, FastOsMA, SlowOsMA, SignalOsMA)
        indHandle1 = iOsMA(Symbol(), TimeFrame1, FastOsMA, SlowOsMA, SignalOsMA, OsMAPrice)
    elif _sw1 == INDICATOR_STOCHASTIC:
        label3 = StringFormat('iStoch %s (%d,%d,%d) %s', timeFrame1, Kperiod, Dperiod, Slowing, StringSubstr(EnumToString(StochMAMethod, 'ENUM_MA_METHOD'), 5))
        indHandle1 = iStochastic(Symbol(), TimeFrame1, Kperiod, Dperiod, Slowing, StochMAMethod, PriceField)
    elif _sw1 == INDICATOR_RSI:
        label3 = StringFormat('iRSI %s (%d,%d)', timeFrame1, RSIPeriod, RSISignal)
        indHandle1 = iRSI(Symbol(), TimeFrame1, RSIPeriod, RSIPrice)
    elif _sw1 == INDICATOR_CCI:
        label3 = StringFormat('iCCI %s (%d)', timeFrame1, CCIPeriod)
        indHandle1 = iCCI(Symbol(), TimeFrame1, CCIPeriod, CCIPrice)
    elif _sw1 == INDICATOR_RVI:
        label3 = StringFormat('iRVI %s (%d)', timeFrame1, RVIPeriod)
        indHandle1 = iRVI(Symbol(), TimeFrame1, RVIPeriod)
    elif _sw1 == INDICATOR_ADX:
        label3 = StringFormat('iADX %s (%d)', timeFrame1, ADXPeriod)
        indHandle1 = iADX_u(Symbol(), TimeFrame1, ADXPeriod)
    elif _sw1 == INDICATOR_TRIX:
        label3 = StringFormat('iTriX %s (%d)', timeFrame1, TriXPeriod)
        indHandle1 = iTriX(Symbol(), TimeFrame1, TriXPeriod, TriXPrice)
    elif _sw1 == INDICATOR_BANDS:
        label3 = StringFormat('iBands %s (%d,%2.1f)', timeFrame1, BBPeriod, BBDev)
        indHandle1 = iBands_u(Symbol(), TimeFrame1, BBPeriod, 0, BBDev, BBPrice)
    if indHandle1 == INVALID_HANDLE:
        return INIT_FAILED
    ObjectSetInteger(chartID, 'LabelBox', OBJPROP_YSIZE, (ySize := ySize + ySizeInc))
    ObjectCreate(chartID, 'Label3', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chartID, 'Label3', OBJPROP_CORNER, 0)
    ObjectSetInteger(chartID, 'Label3', OBJPROP_XDISTANCE, xStart)
    ObjectSetInteger(chartID, 'Label3', OBJPROP_YDISTANCE, (yStart := yStart + yIncrement))
    ObjectSetString(chartID, 'Label3', OBJPROP_TEXT, label3)
    ObjectSetString(chartID, 'Label3', OBJPROP_FONT, 'Arial Bold')
    ObjectSetInteger(chartID, 'Label3', OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(chartID, 'Label3', OBJPROP_COLOR, clrLimeGreen)
    if Indicator2 != INDICATOR_NONE:
        _sw2 = Indicator2
        if _sw2 == INDICATOR_MA:
            label4 = StringFormat('iMA %s %s (%d)', timeFrame2, StringSubstr(EnumToString(MAMethod, 'ENUM_MA_METHOD'), 5), MAPeriod)
            indHandle2 = iMA(Symbol(), TimeFrame2, MAPeriod, 0, MAMethod, MAPrice)
        elif _sw2 == INDICATOR_MACD:
            label4 = StringFormat('iMACD %s (%d,%d,%d)', timeFrame2, FastMACD, SlowMACD, SignalMACD)
            indHandle2 = iMACD(Symbol(), TimeFrame2, FastMACD, SlowMACD, SignalMACD, MACDPrice)
        elif _sw2 == INDICATOR_OSMA:
            label4 = StringFormat('iOsMA %s (%d,%d,%d)', timeFrame2, FastOsMA, SlowOsMA, SignalOsMA)
            indHandle2 = iOsMA(Symbol(), TimeFrame2, FastOsMA, SlowOsMA, SignalOsMA, OsMAPrice)
        elif _sw2 == INDICATOR_STOCHASTIC:
            label4 = StringFormat('iStoch %s (%d,%d,%d) %s', timeFrame2, Kperiod, Dperiod, Slowing, StringSubstr(EnumToString(StochMAMethod, 'ENUM_MA_METHOD'), 5))
            indHandle2 = iStochastic(Symbol(), TimeFrame2, Kperiod, Dperiod, Slowing, StochMAMethod, PriceField)
        elif _sw2 == INDICATOR_RSI:
            label4 = StringFormat('iRSI %s (%d,%d)', timeFrame2, RSIPeriod, RSISignal)
            indHandle2 = iRSI(Symbol(), TimeFrame2, RSIPeriod, RSIPrice)
        elif _sw2 == INDICATOR_CCI:
            label4 = StringFormat('iCCI %s (%d)', timeFrame2, CCIPeriod)
            indHandle2 = iCCI(Symbol(), TimeFrame2, CCIPeriod, CCIPrice)
        elif _sw2 == INDICATOR_RVI:
            label4 = StringFormat('iRVI %s (%d)', timeFrame2, RVIPeriod)
            indHandle2 = iRVI(Symbol(), TimeFrame2, RVIPeriod)
        elif _sw2 == INDICATOR_ADX:
            label4 = StringFormat('iADX %s (%d)', timeFrame2, ADXPeriod)
            indHandle2 = iADX_u(Symbol(), TimeFrame2, ADXPeriod)
        elif _sw2 == INDICATOR_TRIX:
            label4 = StringFormat('iTriX %s (%d)', timeFrame2, TriXPeriod)
            indHandle2 = iTriX(Symbol(), TimeFrame2, TriXPeriod, TriXPrice)
        elif _sw2 == INDICATOR_BANDS:
            label4 = StringFormat('iBands %s (%d,%2.1f)', timeFrame2, BBPeriod, BBDev)
            indHandle2 = iBands_u(Symbol(), TimeFrame2, BBPeriod, 0, BBDev, BBPrice)
        if indHandle2 == INVALID_HANDLE:
            return INIT_FAILED
        ObjectSetInteger(chartID, 'LabelBox', OBJPROP_YSIZE, (ySize := ySize + ySizeInc))
        ObjectCreate(chartID, 'Label4', OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(chartID, 'Label4', OBJPROP_CORNER, 0)
        ObjectSetInteger(chartID, 'Label4', OBJPROP_XDISTANCE, xStart)
        ObjectSetInteger(chartID, 'Label4', OBJPROP_YDISTANCE, (yStart := yStart + yIncrement))
        ObjectSetString(chartID, 'Label4', OBJPROP_TEXT, label4)
        ObjectSetString(chartID, 'Label4', OBJPROP_FONT, 'Arial Bold')
        ObjectSetInteger(chartID, 'Label4', OBJPROP_FONTSIZE, 10)
        ObjectSetInteger(chartID, 'Label4', OBJPROP_COLOR, clrLimeGreen)
    SetIndexBuffer(0, Buy, INDICATOR_DATA)
    ArraySetAsSeries(Buy, True)
    PlotIndexSetString(0, PLOT_LABEL, 'BuyArrow')
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, Sell, INDICATOR_DATA)
    ArraySetAsSeries(Sell, True)
    PlotIndexSetString(1, PLOT_LABEL, 'SellArrow')
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevTime, indicator1, indicator2
    if rates_total < 100:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if SymbolInfoTick(Symbol(), tick):
        ObjectSetString(chartID, 'Label1', OBJPROP_TEXT, label1 + DoubleToString((tick.ask - tick.bid) * doubleToPip, 1))
    if prev_calculated > 0 and time[0] != _s_OnCalculate_prevTime:
        _s_OnCalculate_prevTime = time[0]
        ObjectSetString(chartID, 'Label2', OBJPROP_TEXT, label2 + StringFormat('(%d) %4.1f', RangePeriod, Range_f(0) * doubleToPip))
    i = 0
    limit = 0
    limit = rates_total - prev_calculated
    if prev_calculated == 0:
        limit = _int(ChartGetInteger(chartID, CHART_VISIBLE_BARS)) + 100
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - limit)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - limit)
    i = limit
    for i in range(i, 0 - 1, -1):
        if CopyTime(Symbol(), TimeFrame1, _DT(time[i]), 1, _s_OnCalculate_Time) != 1:
            return 0
        time1 = _s_OnCalculate_Time[0]
        _sw3 = Indicator1
        if _sw3 == INDICATOR_MA:
            if CopyBuffer(indHandle1, 0, _DT(time1), 1, _s_OnCalculate_MoAv) != 1:
                return 0
            if CopyHigh(Symbol(), TimeFrame1, _DT(time1), 1, _s_OnCalculate_High) != 1:
                return 0
            if CopyLow(Symbol(), TimeFrame1, _DT(time1), 1, _s_OnCalculate_Low) != 1:
                return 0
            if CopyClose(Symbol(), TimeFrame1, _DT(time1), 1, _s_OnCalculate_Close) != 1:
                return 0
            indicator1 = iMA_u(_s_OnCalculate_MoAv, _s_OnCalculate_High, _s_OnCalculate_Low, _s_OnCalculate_Close)
        elif _sw3 == INDICATOR_MACD:
            if CopyBuffer(indHandle1, 0, _DT(time1), 2, _s_OnCalculate_Macd) != 2:
                return 0
            if CopyBuffer(indHandle1, 1, _DT(time1), 2, _s_OnCalculate_Sign) != 2:
                return 0
            indicator1 = iMACD_u(_s_OnCalculate_Macd, _s_OnCalculate_Sign)
        elif _sw3 == INDICATOR_OSMA:
            if ArraySize(_s_OnCalculate_OsMa) != (OsMASignal + 1):
                ArrayResize(_s_OnCalculate_OsMa, OsMASignal + 1)
            if CopyBuffer(indHandle1, 0, _DT(time1), OsMASignal + 1, _s_OnCalculate_OsMa) != (OsMASignal + 1):
                return 0
            indicator1 = iOsMA_u(_s_OnCalculate_OsMa)
        elif _sw3 == INDICATOR_STOCHASTIC:
            if CopyBuffer(indHandle1, 0, _DT(time1), 2, _s_OnCalculate_Stoc) != 2:
                return 0
            if CopyBuffer(indHandle1, 1, _DT(time1), 2, _s_OnCalculate_Sign_) != 2:
                return 0
            indicator1 = iStochastic_u(_s_OnCalculate_Stoc, _s_OnCalculate_Sign_)
        elif _sw3 == INDICATOR_RSI:
            if ArraySize(_s_OnCalculate_Rsi) != (RSISignal + 1):
                ArrayResize(_s_OnCalculate_Rsi, RSISignal + 1)
            if CopyBuffer(indHandle1, 0, _DT(time1), RSISignal + 1, _s_OnCalculate_Rsi) != (RSISignal + 1):
                return 0
            indicator1 = iRSI_u(_s_OnCalculate_Rsi)
        elif _sw3 == INDICATOR_CCI:
            if CopyBuffer(indHandle1, 0, _DT(time1), 2, _s_OnCalculate_Cci) != 2:
                return 0
            indicator1 = iCCI_u(_s_OnCalculate_Cci)
        elif _sw3 == INDICATOR_RVI:
            if CopyBuffer(indHandle1, 0, _DT(time1), 2, _s_OnCalculate_Rvi) != 2:
                return 0
            if CopyBuffer(indHandle1, 1, _DT(time1), 2, _s_OnCalculate_Sig) != 2:
                return 0
            indicator1 = iRVI_u(_s_OnCalculate_Rvi, _s_OnCalculate_Sig)
        elif _sw3 == INDICATOR_ADX:
            if CopyBuffer(indHandle1, 0, _DT(time1), 1, _s_OnCalculate_Adx) != 1:
                return 0
            if CopyBuffer(indHandle1, 1, _DT(time1), 2, _s_OnCalculate_Pdi) != 2:
                return 0
            if CopyBuffer(indHandle1, 2, _DT(time1), 2, _s_OnCalculate_Mdi) != 2:
                return 0
            indicator1 = iADX_u(_s_OnCalculate_Adx, _s_OnCalculate_Pdi, _s_OnCalculate_Mdi)
        elif _sw3 == INDICATOR_TRIX:
            if ArraySize(_s_OnCalculate_Trix) != (TrixSignal + 1):
                ArrayResize(_s_OnCalculate_Trix, TrixSignal + 1)
            if CopyBuffer(indHandle1, 0, _DT(time1), TrixSignal + 1, _s_OnCalculate_Trix) != (TrixSignal + 1):
                return 0
            indicator1 = iTriX_u(_s_OnCalculate_Trix)
        elif _sw3 == INDICATOR_BANDS:
            if CopyBuffer(indHandle1, 0, _DT(time1), 1, _s_OnCalculate_Middle) != 1:
                return 0
            if CopyBuffer(indHandle1, 1, _DT(time1), 1, _s_OnCalculate_Upper) != 1:
                return 0
            if CopyBuffer(indHandle1, 2, _DT(time1), 1, _s_OnCalculate_Lower) != 1:
                return 0
            if CopyHigh(Symbol(), TimeFrame1, _DT(time1), 1, _s_OnCalculate_High_) != 1:
                return 0
            if CopyLow(Symbol(), TimeFrame1, _DT(time1), 1, _s_OnCalculate_Low_) != 1:
                return 0
            if CopyClose(Symbol(), TimeFrame1, _DT(time1), 1, _s_OnCalculate_Close_) != 1:
                return 0
            indicator1 = iBands_u(_s_OnCalculate_Middle, _s_OnCalculate_Upper, _s_OnCalculate_Lower, _s_OnCalculate_High_, _s_OnCalculate_Low_, _s_OnCalculate_Close_)
        if Indicator2 != INDICATOR_NONE:
            if CopyTime(Symbol(), TimeFrame2, _DT(time[i]), 1, _s_OnCalculate_Time) != 1:
                return 0
            time2 = _s_OnCalculate_Time[0]
            _sw4 = Indicator2
            if _sw4 == INDICATOR_MA:
                if CopyBuffer(indHandle2, 0, _DT(time2), 1, _s_OnCalculate_MoAv_) != 1:
                    return 0
                if CopyHigh(Symbol(), TimeFrame2, _DT(time2), 1, _s_OnCalculate_High__) != 1:
                    return 0
                if CopyLow(Symbol(), TimeFrame2, _DT(time2), 1, _s_OnCalculate_Low__) != 1:
                    return 0
                if CopyClose(Symbol(), TimeFrame2, _DT(time2), 1, _s_OnCalculate_Close__) != 1:
                    return 0
                indicator2 = iMA_u(_s_OnCalculate_MoAv_, _s_OnCalculate_High__, _s_OnCalculate_Low__, _s_OnCalculate_Close__)
            elif _sw4 == INDICATOR_MACD:
                if CopyBuffer(indHandle2, 0, _DT(time2), 2, _s_OnCalculate_Macd_) != 2:
                    return 0
                if CopyBuffer(indHandle2, 1, _DT(time2), 2, _s_OnCalculate_Sign__) != 2:
                    return 0
                indicator2 = iMACD_u(_s_OnCalculate_Macd_, _s_OnCalculate_Sign__)
            elif _sw4 == INDICATOR_OSMA:
                if ArraySize(_s_OnCalculate_OsMa_) != (OsMASignal + 1):
                    ArrayResize(_s_OnCalculate_OsMa_, OsMASignal + 1)
                if CopyBuffer(indHandle2, 0, _DT(time2), OsMASignal + 1, _s_OnCalculate_OsMa_) != (OsMASignal + 1):
                    return 0
                indicator2 = iOsMA_u(_s_OnCalculate_OsMa_)
            elif _sw4 == INDICATOR_STOCHASTIC:
                if CopyBuffer(indHandle2, 0, _DT(time2), 2, _s_OnCalculate_Stoc_) != 2:
                    return 0
                if CopyBuffer(indHandle2, 1, _DT(time2), 2, _s_OnCalculate_Sign___) != 2:
                    return 0
                indicator2 = iStochastic_u(_s_OnCalculate_Stoc_, _s_OnCalculate_Sign___)
            elif _sw4 == INDICATOR_RSI:
                if ArraySize(_s_OnCalculate_Rsi_) != (RSISignal + 1):
                    ArrayResize(_s_OnCalculate_Rsi_, RSISignal + 1)
                if CopyBuffer(indHandle2, 0, _DT(time2), RSISignal + 1, _s_OnCalculate_Rsi_) != (RSISignal + 1):
                    return 0
                indicator2 = iRSI_u(_s_OnCalculate_Rsi_)
            elif _sw4 == INDICATOR_CCI:
                if CopyBuffer(indHandle2, 0, _DT(time2), 2, _s_OnCalculate_Cci_) != 2:
                    return 0
                indicator2 = iCCI_u(_s_OnCalculate_Cci_)
            elif _sw4 == INDICATOR_RVI:
                if CopyBuffer(indHandle2, 0, _DT(time2), 2, _s_OnCalculate_Rvi_) != 2:
                    return 0
                if CopyBuffer(indHandle2, 1, _DT(time2), 2, _s_OnCalculate_Sig_) != 2:
                    return 0
                indicator2 = iRVI_u(_s_OnCalculate_Rvi_, _s_OnCalculate_Sig_)
            elif _sw4 == INDICATOR_ADX:
                if CopyBuffer(indHandle2, 0, _DT(time2), 1, _s_OnCalculate_Adx_) != 1:
                    return 0
                if CopyBuffer(indHandle2, 1, _DT(time2), 2, _s_OnCalculate_Pdi_) != 2:
                    return 0
                if CopyBuffer(indHandle2, 2, _DT(time2), 2, _s_OnCalculate_Mdi_) != 2:
                    return 0
                indicator2 = iADX_u(_s_OnCalculate_Adx_, _s_OnCalculate_Pdi_, _s_OnCalculate_Mdi_)
            elif _sw4 == INDICATOR_TRIX:
                if ArraySize(_s_OnCalculate_Trix_) != (TrixSignal + 1):
                    ArrayResize(_s_OnCalculate_Trix_, TrixSignal + 1)
                if CopyBuffer(indHandle2, 0, _DT(time2), TrixSignal + 1, _s_OnCalculate_Trix_) != (TrixSignal + 1):
                    return 0
                indicator2 = iTriX_u(_s_OnCalculate_Trix_)
            elif _sw4 == INDICATOR_BANDS:
                if CopyBuffer(indHandle2, 0, _DT(time2), 1, _s_OnCalculate_Middle_) != 1:
                    return 0
                if CopyBuffer(indHandle2, 1, _DT(time2), 1, _s_OnCalculate_Upper_) != 1:
                    return 0
                if CopyBuffer(indHandle2, 2, _DT(time2), 1, _s_OnCalculate_Lower_) != 1:
                    return 0
                if CopyHigh(Symbol(), TimeFrame2, _DT(time2), 1, _s_OnCalculate_High___) != 1:
                    return 0
                if CopyLow(Symbol(), TimeFrame2, _DT(time2), 1, _s_OnCalculate_Low___) != 1:
                    return 0
                if CopyClose(Symbol(), TimeFrame2, _DT(time2), 1, _s_OnCalculate_Close___) != 1:
                    return 0
                indicator2 = iBands_u(_s_OnCalculate_Middle_, _s_OnCalculate_Upper_, _s_OnCalculate_Lower_, _s_OnCalculate_High___, _s_OnCalculate_Low___, _s_OnCalculate_Close___)
        if Indicator2 == INDICATOR_NONE:
            if indicator1 == SIGNAL_BUY:
                Buy[i] = low[i] - Range_f(i)
                if AlertsOn and prev_calculated > 0:
                    AlertsHandle(time[0], SIGNAL_BUY)
                Sell[i] = 0.0
            elif indicator1 == SIGNAL_SELL:
                Sell[i] = high[i] + Range_f(i)
                if AlertsOn and prev_calculated > 0:
                    AlertsHandle(time[0], SIGNAL_SELL)
                Buy[i] = 0.0
            else:
                Buy[i] = 0.0
                Sell[i] = 0.0
        else:
            if indicator1 == SIGNAL_BUY and indicator2 == SIGNAL_BUY:
                Buy[i] = low[i] - Range_f(i)
                if AlertsOn and prev_calculated > 0:
                    AlertsHandle(time[0], SIGNAL_BUY)
                Sell[i] = 0.0
            elif indicator1 == SIGNAL_SELL and indicator2 == SIGNAL_SELL:
                Sell[i] = high[i] + Range_f(i)
                if AlertsOn and prev_calculated > 0:
                    AlertsHandle(time[0], SIGNAL_SELL)
                Buy[i] = 0.0
            else:
                Buy[i] = 0.0
                Sell[i] = 0.0
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total

def OnDeinit(reason):
    if ObjectFind(0, 'LabelBox') != -1:
        ObjectDelete(0, 'LabelBox')
    if ObjectFind(0, 'Label1') != -1:
        ObjectDelete(0, 'Label1')
    if ObjectFind(0, 'Label2') != -1:
        ObjectDelete(0, 'Label2')
    if ObjectFind(0, 'Label3') != -1:
        ObjectDelete(0, 'Label3')
    if ObjectFind(0, 'Label4') != -1:
        ObjectDelete(0, 'Label4')
    IndicatorRelease(rangeHandle)
    IndicatorRelease(indHandle1)
    IndicatorRelease(indHandle2)
    return

def Range_f(idx):
    if CopyBuffer(rangeHandle, 0, idx + 1, 1, _s_Range_range_) != 1:
        return 0.0
    avgRange = _s_Range_range_[0]
    return avgRange

def iMA_u(moav, high, low, close):
    signal = SIGNAL_NONE
    if close[0] > moav[0] and low[0] < moav[0]:
        signal = SIGNAL_BUY
    if close[0] < moav[0] and high[0] > moav[0]:
        signal = SIGNAL_SELL
    return signal

def iMACD_u(macd, sign):
    currMacd = macd[1]
    prevMacd = macd[0]
    currSign = sign[1]
    prevSign = sign[0]
    signal = SIGNAL_NONE
    if currMacd > currSign and prevMacd < prevSign:
        signal = SIGNAL_BUY
    if currMacd < currSign and prevMacd > prevSign:
        signal = SIGNAL_SELL
    return signal

def iOsMA_u(osma):
    ArraySetAsSeries(osma, True)
    sum1 = 0.0
    sum2 = 0.0
    i = 0
    j = 1
    while i < OsMASignal:
        sum1 += osma[i]
        sum2 += osma[j]
        i += 1
        j += 1
    currOsma = osma[0]
    prevOsma = osma[1]
    currSign = sum1 / OsMASignal
    prevSign = sum2 / OsMASignal
    signal = SIGNAL_NONE
    if currOsma > currSign and prevOsma < prevSign:
        signal = SIGNAL_BUY
    if currOsma < currSign and prevOsma > prevSign:
        signal = SIGNAL_SELL
    return signal

def iStochastic_u(stoc, sign):
    currStoc = stoc[1]
    prevStoc = stoc[0]
    currSign = sign[1]
    prevSign = sign[0]
    signal = SIGNAL_NONE
    if currStoc > currSign and prevStoc < prevSign:
        signal = SIGNAL_BUY
    if currStoc < currSign and prevStoc > prevSign:
        signal = SIGNAL_SELL
    return signal

def iRSI_u(rsi):
    ArraySetAsSeries(rsi, True)
    sum1 = 0.0
    sum2 = 0.0
    i = 0
    j = 1
    while i < RSISignal:
        sum1 += rsi[i]
        sum2 += rsi[j]
        i += 1
        j += 1
    currRsi = rsi[0]
    prevRsi = rsi[1]
    currSig = sum1 / RSISignal
    prevSig = sum2 / RSISignal
    signal = SIGNAL_NONE
    if currRsi > currSig and prevRsi < prevSig:
        signal = SIGNAL_BUY
    if currRsi < currSig and prevRsi > prevSig:
        signal = SIGNAL_SELL
    return signal

def iCCI_u(cci):
    currCci = cci[1]
    prevCci = cci[0]
    level = Arr.of([-100.0, 0.0, 100.0], fill=0.0, dyn=False, size=3)
    signal = SIGNAL_NONE
    for i in range(0, 3):
        if currCci > level[i] and prevCci <= level[i]:
            signal = SIGNAL_BUY
            break
        if currCci < level[i] and prevCci >= level[i]:
            signal = SIGNAL_SELL
            break
    return signal

def iRVI_u(rvi, sig):
    currRvi = rvi[1]
    prevRvi = rvi[0]
    currSig = sig[1]
    prevSig = sig[0]
    signal = SIGNAL_NONE
    if currRvi > currSig and prevRvi < prevSig:
        signal = SIGNAL_BUY
    if currRvi < currSig and prevRvi > prevSig:
        signal = SIGNAL_SELL
    return signal

def iADX_u(Adx, pdi, mdi):
    adx = Adx[0] < 25
    currPdi = pdi[1]
    prevPdi = pdi[0]
    currMdi = mdi[1]
    prevMdi = mdi[0]
    signal = SIGNAL_NONE
    if (adx and currPdi > currMdi) and prevPdi < prevMdi:
        signal = SIGNAL_BUY
    if (adx and currPdi < currMdi) and prevPdi > prevMdi:
        signal = SIGNAL_SELL
    return signal

def iTriX_u(trix):
    ArraySetAsSeries(trix, True)
    sum1 = 0.0
    sum2 = 0.0
    i = 0
    j = 1
    while i < TrixSignal:
        sum1 += trix[i]
        sum2 += trix[j]
        i += 1
        j += 1
    currTrix = trix[0]
    prevTrix = trix[1]
    currSign = sum1 / TrixSignal
    prevSign = sum2 / TrixSignal
    signal = SIGNAL_NONE
    if currTrix > currSign and prevTrix < prevSign:
        signal = SIGNAL_BUY
    if currTrix < currSign and prevTrix > prevSign:
        signal = SIGNAL_SELL
    return signal

def iBands_u(midle, upper, lower, high, low, close):
    signal = SIGNAL_NONE
    if (low[0] < lower[0] and close[0] > lower[0]) or (low[0] < midle[0] and close[0] > midle[0]):
        signal = SIGNAL_BUY
    if (high[0] > upper[0] and close[0] < upper[0]) or (high[0] > midle[0] and close[0] < midle[0]):
        signal = SIGNAL_SELL
    return signal

def AlertsHandle(time, alert_type):
    global _s_AlertsHandle_timePrev, _s_AlertsHandle_typePrev
    alertMessage = ""
    price = 0.0
    if SymbolInfoTick(Symbol(), tick):
        price = tick.bid
    if _s_AlertsHandle_timePrev != time or _s_AlertsHandle_typePrev != alert_type:
        _s_AlertsHandle_timePrev = time
        _s_AlertsHandle_typePrev = alert_type
        alertMessage = StringFormat('%s @ %s %s @ %s', Symbol(), TimeToString(TimeLocal(), TIME_MINUTES), StringSubstr(EnumToString(alert_type, 'ENUM_SIGNAL'), 7), DoubleToString(price, Digits()))
        if AlertsMessage:
            Alert(alertMessage)
        if AlertsEmail:
            SendMail(Symbol() + ' Arrow Alert', alertMessage)
        if AlertsSound:
            PlaySound('alert2.wav')

# ---- global variables initialised from expressions
chartID = ChartID()
tick = MqlTick()

# ---- static local variables
_s_OnCalculate_prevTime = 0
_s_OnCalculate_Time = Arr(1, 0, dyn=False)
_s_OnCalculate_MoAv = Arr(1, 0.0, dyn=False)
_s_OnCalculate_High = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Low = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Close = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Macd = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Sign = Arr(2, 0.0, dyn=False)
_s_OnCalculate_OsMa = Arr(0, 0.0)
_s_OnCalculate_Stoc = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Sign_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Rsi = Arr(0, 0.0)
_s_OnCalculate_Cci = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Rvi = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Sig = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Adx = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Pdi = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Mdi = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Trix = Arr(0, 0.0)
_s_OnCalculate_Middle = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Upper = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Lower = Arr(1, 0.0, dyn=False)
_s_OnCalculate_High_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Low_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Close_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_MoAv_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_High__ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Low__ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Close__ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Macd_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Sign__ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_OsMa_ = Arr(0, 0.0)
_s_OnCalculate_Stoc_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Sign___ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Rsi_ = Arr(0, 0.0)
_s_OnCalculate_Cci_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Rvi_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Sig_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Adx_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Pdi_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Mdi_ = Arr(2, 0.0, dyn=False)
_s_OnCalculate_Trix_ = Arr(0, 0.0)
_s_OnCalculate_Middle_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Upper_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Lower_ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_High___ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Low___ = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Close___ = Arr(1, 0.0, dyn=False)
_s_Range_range_ = Arr(1, 0.0, dyn=False)
_s_AlertsHandle_timePrev = 0
_s_AlertsHandle_typePrev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IndicatorArrows(_MQL5Indicator):
    name = 'Indicator_Arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Indicator1': _Choice({0: 'Moving Average', 1: 'Moving Average Convergence/Divergence', 2: 'Oscillator of Moving Averages', 3: 'Stochastic Oscillator', 4: 'Relative Strength Index', 5: 'Commodity Channel Index', 6: 'Relative Vigor Index', 7: 'Average Directional Movement Index', 8: 'Triple Exponential Average', 9: 'Bollinger Bands', 10: 'No Indicator'}, default=1),
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'Indicator2': _Choice({0: 'Moving Average', 1: 'Moving Average Convergence/Divergence', 2: 'Oscillator of Moving Averages', 3: 'Stochastic Oscillator', 4: 'Relative Strength Index', 5: 'Commodity Channel Index', 6: 'Relative Vigor Index', 7: 'Average Directional Movement Index', 8: 'Triple Exponential Average', 9: 'Bollinger Bands', 10: 'No Indicator'}, default=0),
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'RangePeriod': 14,
        'MAPeriod': 5,
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastMACD': 12,
        'SlowMACD': 26,
        'SignalMACD': 9,
        'MACDPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastOsMA': 12,
        'SlowOsMA': 26,
        'SignalOsMA': 9,
        'OsMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'OsMASignal': 9,
        'Kperiod': 8,
        'Dperiod': 3,
        'Slowing': 3,
        'StochMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'RSIPeriod': 8,
        'RSISignal': 5,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'CCIPeriod': 14,
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RVIPeriod': 10,
        'ADXPeriod': 14,
        'ADXPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'TriXPeriod': 14,
        'TrixSignal': 9,
        'TriXPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'BBPeriod': 20,  # Bands Period
        'BBDev': 2.0,  # Bands Deviation
        'BBPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Bands Price
        'AlertsOn': True,
        'AlertsMessage': True,
        'AlertsEmail': False,
        'AlertsSound': False,
    }

