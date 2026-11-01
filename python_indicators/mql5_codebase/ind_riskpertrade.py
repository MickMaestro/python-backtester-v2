"""IND_RiskPerTrade — converted from MQL5: MQL5 Indicators/IND - RiskPerTrade - MT5/IND_RiskPerTrade.mq5

Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com
 
RISK DISCLAIMER : Investing involves risks. Any decision to invest in either real estate or stock markets is a personal decision that should be made after thorough research, including an assessment of your personal risk tolerance and your personal financial condition and goals. Results are based on market conditions and on each personal and the action they take and the time and effort they put in
Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com
 
RISK DISCLAIMER : Investing involves risks. Any decision to invest in either real estate or stock markets is a personal decision that should be made after thorough research, including an assessment of your personal risk tolerance and your personal financial condition and goals. Results are based on market conditions and on each personal and the action they take and the time and effort they put in
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.fxweirdos_createobjects import *  # #include createObjects.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com', ' ', 'RISK DISCLAIMER : Investing involves risks. Any decision to invest in either real estate or stock markets is a personal decision that should be made after thorough research, including an assessment of your personal risk tolerance and your personal financial condition and goals. Results are based on market conditions and on each personal and the action they take and the time and effort they put in', 'Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com', ' ', 'RISK DISCLAIMER : Investing involves risks. Any decision to invest in either real estate or stock markets is a personal decision that should be made after thorough research, including an assessment of your personal risk tolerance and your personal financial condition and goals. Results are based on market conditions and on each personal and the action they take and the time and effort they put in'], 'name': 'IND_RiskPerTrade', 'source': 'MQL5 Indicators/IND - RiskPerTrade - MT5/IND_RiskPerTrade.mq5', 'folder': 'IND - RiskPerTrade - MT5', 'inputs': [{'mql': 'cRPTFontClr', 'py': 'cRPTFontClr', 'param': None, 'type': 'color', 'default': 2402047, 'label': 'Font color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['createObjects.mqh']}

SYMBOL_SWAP_MODE = 0  # MQL5 constant unknown to the converter

# enum ALLIGATOR_MODE
MODE_GATORJAW = 1
MODE_GATORTEETH = 2
MODE_GATORLIPS = 3
_enum('ALLIGATOR_MODE', {1: 'MODE_GATORJAW', 2: 'MODE_GATORTEETH', 3: 'MODE_GATORLIPS'})

# enum ADX_MODE
MODE_MAIN = 0
MODE_PLUSDI = 1
MODE_MINUSDI = 2
_enum('ADX_MODE', {0: 'MODE_MAIN', 1: 'MODE_PLUSDI', 2: 'MODE_MINUSDI'})

# enum UP_LOW_MODE
MODE_BASE = 0
MODE_UPPER = 1
MODE_LOWER = 2
_enum('UP_LOW_MODE', {0: 'MODE_BASE', 1: 'MODE_UPPER', 2: 'MODE_LOWER'})

# enum ICHIMOKU_MODE
MODE_TENKANSEN = 1
MODE_KIJUNSEN = 2
MODE_SENKOUSPANA = 3
MODE_SENKOUSPANB = 4
MODE_CHINKOUSPAN = 5
_enum('ICHIMOKU_MODE', {1: 'MODE_TENKANSEN', 2: 'MODE_KIJUNSEN', 3: 'MODE_SENKOUSPANA', 4: 'MODE_SENKOUSPANB', 5: 'MODE_CHINKOUSPAN'})

# ---- inputs and global variables
cRPTFontClr = _input('cRPTFontClr', 0x24A6FF)  # Font color
dRPTAmtRisking = 0.0  # Used to calculate the overall risk
dRPTAmtRewarding = 0.0  # Used to calculate the overall target
kRPT = 0  # Used to loop all open orders to get the overall risk
sRPTObjectName = ""  # To name all objects

def TFMigrate(tf):
    _sw1 = tf
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    elif _sw1 == 2:
        return PERIOD_M2
    elif _sw1 == 3:
        return PERIOD_M3
    elif _sw1 == 4:
        return PERIOD_M4
    elif _sw1 == 6:
        return PERIOD_M6
    elif _sw1 == 10:
        return PERIOD_M10
    elif _sw1 == 12:
        return PERIOD_M12
    elif _sw1 == 16385:
        return PERIOD_H1
    elif _sw1 == 16386:
        return PERIOD_H2
    elif _sw1 == 16387:
        return PERIOD_H3
    elif _sw1 == 16388:
        return PERIOD_H4
    elif _sw1 == 16390:
        return PERIOD_H6
    elif _sw1 == 16392:
        return PERIOD_H8
    elif _sw1 == 16396:
        return PERIOD_H12
    elif _sw1 == 16408:
        return PERIOD_D1
    elif _sw1 == 32769:
        return PERIOD_W1
    elif _sw1 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

def iLowMQL4(symbol, tf, index):
    if index < 0:
        return -1.0
    Arr_ = Arr(0, 0.0)
    timeframe = TFMigrate(tf)
    if CopyLow(symbol, timeframe, index, 1, Arr_) > 0:
        return Arr_[0]
    else:
        return -1.0

def iHighMQL4(symbol, tf, index):
    if index < 0:
        return -1.0
    Arr_ = Arr(0, 0.0)
    timeframe = TFMigrate(tf)
    if CopyHigh(symbol, timeframe, index, 1, Arr_) > 0:
        return Arr_[0]
    else:
        return -1.0

def iHighestMQL4(symbol, tf, type_, count=WHOLE_ARRAY, start=0):
    if start < 0:
        return -1
    timeframe = TFMigrate(tf)
    if count <= 0:
        count = Bars(symbol, timeframe)
    if type_ <= 0:
        Open = Arr(0, 0.0)
        ArraySetAsSeries(Open, True)
        CopyOpen(symbol, timeframe, start, count, Open)
        return ArrayMaximum(Open, 0, count) + start
    if type_ == 1:
        Low = Arr(0, 0.0)
        ArraySetAsSeries(Low, True)
        CopyLow(symbol, timeframe, start, count, Low)
        return ArrayMaximum(Low, 0, count) + start
    if type_ == 2:
        High = Arr(0, 0.0)
        ArraySetAsSeries(High, True)
        CopyHigh(symbol, timeframe, start, count, High)
        return ArrayMaximum(High, 0, count) + start
    if type_ == 3:
        Close = Arr(0, 0.0)
        ArraySetAsSeries(Close, True)
        CopyClose(symbol, timeframe, start, count, Close)
        return ArrayMaximum(Close, 0, count) + start
    if type_ == 4:
        Volume = Arr(0, 0)
        ArraySetAsSeries(Volume, True)
        CopyTickVolume(symbol, timeframe, start, count, Volume)
        return ArrayMaximum(Volume, 0, count) + start
    if type_ >= 5:
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(symbol, timeframe, start, count, Time)
        return ArrayMaximum(Time, 0, count) + start
    return 0

def iLowestMQL4(symbol, tf, type_, count=WHOLE_ARRAY, start=0):
    if start < 0:
        return -1
    timeframe = TFMigrate(tf)
    if count <= 0:
        count = Bars(symbol, timeframe)
    if type_ <= 0:
        Open = Arr(0, 0.0)
        ArraySetAsSeries(Open, True)
        CopyOpen(symbol, timeframe, start, count, Open)
        return ArrayMinimum(Open, 0, count) + start
    if type_ == 1:
        Low = Arr(0, 0.0)
        ArraySetAsSeries(Low, True)
        CopyLow(symbol, timeframe, start, count, Low)
        return ArrayMinimum(Low, 0, count) + start
    if type_ == 2:
        High = Arr(0, 0.0)
        ArraySetAsSeries(High, True)
        CopyHigh(symbol, timeframe, start, count, High)
        return ArrayMinimum(High, 0, count) + start
    if type_ == 3:
        Close = Arr(0, 0.0)
        ArraySetAsSeries(Close, True)
        CopyClose(symbol, timeframe, start, count, Close)
        return ArrayMinimum(Close, 0, count) + start
    if type_ == 4:
        Volume = Arr(0, 0)
        ArraySetAsSeries(Volume, True)
        CopyTickVolume(symbol, timeframe, start, count, Volume)
        return ArrayMinimum(Volume, 0, count) + start
    if type_ >= 5:
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(symbol, timeframe, start, count, Time)
        return ArrayMinimum(Time, 0, count) + start
    return 0

def ObjectsDeleteAllMQL4(window=-1, type_=-1):
    return ObjectsDeleteAll(0, window, type_)

def CopyBufferMQL4(handle, index, shift):
    buf = Arr(0, 0.0)
    _sw2 = index
    if _sw2 == 0:
        if CopyBuffer(handle, 0, shift, 1, buf) > 0:
            return buf[0]
    elif _sw2 == 1:
        if CopyBuffer(handle, 1, shift, 1, buf) > 0:
            return buf[0]
    elif _sw2 == 2:
        if CopyBuffer(handle, 2, shift, 1, buf) > 0:
            return buf[0]
    elif _sw2 == 3:
        if CopyBuffer(handle, 3, shift, 1, buf) > 0:
            return buf[0]
    elif _sw2 == 4:
        if CopyBuffer(handle, 4, shift, 1, buf) > 0:
            return buf[0]
    else:
        pass
    return EMPTY_VALUE

def iATRMQL4(symbol, tf, period, shift):
    timeframe = TFMigrate(tf)
    handle = iATR(symbol, timeframe, period)
    if handle < 0:
        Print('The iATR object is not created: Error', GetLastError())
        return -1.0
    else:
        return CopyBufferMQL4(handle, 0, shift)

def iTimeMQL4(symbol, tf, index):
    if index < 0:
        return -1
    timeframe = TFMigrate(tf)
    Arr_ = Arr(0, 0)
    if CopyTime(symbol, timeframe, index, 1, Arr_) > 0:
        return Arr_[0]
    else:
        return -1

def HourMQL4():
    tm = MqlDateTime()
    TimeCurrent(tm)
    return tm.hour

def TimeHourMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.hour

def TimeMinuteMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.min

def TimeSecondsMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.sec

def DayOfWeekMQL4():
    tm = MqlDateTime()
    TimeCurrent(tm)
    return tm.day_of_week

def TimeDayOfYearMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_year

def SetIndexStyleMQL4(index, type_, style=-1, width=-1, clr=CLR_NONE):
    if width > -1:
        PlotIndexSetInteger(index, PLOT_LINE_WIDTH, width)
    if clr != CLR_NONE:
        PlotIndexSetInteger(index, PLOT_LINE_COLOR, clr)
    _sw3 = type_
    _k4 = 0 if _sw3 == 0 else 1 if _sw3 == 1 else 2 if _sw3 == 2 else 3 if _sw3 == 3 else 4 if _sw3 == 4 else 5 if _sw3 == 12 else 6
    try:
        if _k4 <= 0:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_LINE)
        if _k4 <= 1:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_SECTION)
        if _k4 <= 2:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
        if _k4 <= 3:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_ARROW)
        if _k4 <= 4:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_ZIGZAG)
        if _k4 <= 5:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_NONE)
        if _k4 <= 6:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_LINE)
    except _SwitchBreak:
        pass
    _sw5 = style
    _k6 = 0 if _sw5 == 0 else 1 if _sw5 == 1 else 2 if _sw5 == 2 else 3 if _sw5 == 3 else 4 if _sw5 == 4 else 5
    try:
        if _k6 <= 0:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_SOLID)
        if _k6 <= 1:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASH)
        if _k6 <= 2:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DOT)
        if _k6 <= 3:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASHDOT)
        if _k6 <= 4:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASHDOTDOT)
        if _k6 <= 5:
            return
    except _SwitchBreak:
        pass

def ObjectFindMQL4(name):
    return ObjectFind(0, name)

def ObjectsTotalMQL4(type_=-1, window=-1):
    return ObjectsTotal(0, window, type_)

def ObjectNameMQL4(index):
    return ObjectName(0, index)

def ObjectDeleteMQL4(name):
    return ObjectDelete(0, name)

def TimeDayOfWeekMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

def TimeDayMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day

def MonthMQL4():
    tm = MqlDateTime()
    TimeCurrent(tm)
    return tm.mon

def MarketInfoMQL4(symbol, type_):
    _sw7 = type_
    if _sw7 == 1:
        return SymbolInfoDouble(symbol, SYMBOL_LASTLOW)
    elif _sw7 == 2:
        return SymbolInfoDouble(symbol, SYMBOL_LASTHIGH)
    elif _sw7 == 5:
        return float(SymbolInfoInteger(symbol, SYMBOL_TIME))
    elif _sw7 == 9:
        return SymbolInfoDouble(symbol, SYMBOL_BID)
    elif _sw7 == 10:
        return SymbolInfoDouble(symbol, SYMBOL_ASK)
    elif _sw7 == 11:
        return SymbolInfoDouble(symbol, SYMBOL_POINT)
    elif _sw7 == 12:
        return float(SymbolInfoInteger(symbol, SYMBOL_DIGITS))
    elif _sw7 == 13:
        return float(SymbolInfoInteger(symbol, SYMBOL_SPREAD))
    elif _sw7 == 14:
        return float(SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL))
    elif _sw7 == 15:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE)
    elif _sw7 == 16:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
    elif _sw7 == 17:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
    elif _sw7 == 18:
        return SymbolInfoDouble(symbol, SYMBOL_SWAP_LONG)
    elif _sw7 == 19:
        return SymbolInfoDouble(symbol, SYMBOL_SWAP_SHORT)
    elif _sw7 == 20:
        return 0.0
    elif _sw7 == 21:
        return 0.0
    elif _sw7 == 22:
        return 0.0
    elif _sw7 == 23:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)
    elif _sw7 == 24:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)
    elif _sw7 == 25:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
    elif _sw7 == 26:
        return float(SymbolInfoInteger(symbol, SYMBOL_SWAP_MODE))
    elif _sw7 == 27:
        return float(SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE))
    elif _sw7 == 28:
        return 0.0
    elif _sw7 == 29:
        return 0.0
    elif _sw7 == 30:
        return 0.0
    elif _sw7 == 31:
        return 0.0
    elif _sw7 == 32:
        return 0.0
    elif _sw7 == 33:
        return float(SymbolInfoInteger(symbol, SYMBOL_TRADE_FREEZE_LEVEL))
    else:
        return 0.0
    return 0.0

def iCloseMQL4(symbol, tf, index):
    if index < 0:
        return -1.0
    Arr_ = Arr(0, 0.0)
    timeframe = TFMigrate(tf)
    if CopyClose(symbol, timeframe, index, 1, Arr_) > 0:
        return Arr_[0]
    else:
        return -1.0

def iOpenMQL4(symbol, tf, index):
    if index < 0:
        return -1.0
    Arr_ = Arr(0, 0.0)
    timeframe = TFMigrate(tf)
    if CopyOpen(symbol, timeframe, index, 1, Arr_) > 0:
        return Arr_[0]
    else:
        return -1.0

def ObjectCreateMQL4(name, type_, window, time1, price1, time2=0, price2=0.0, time3=0, price3=0.0):
    return ObjectCreate(0, name, type_, window, time1, price1, time2, price2, time3, price3)

def ObjectSetTextMQL4(name, text, font_size, font='', text_color=CLR_NONE):
    tmpObjType = _int(ObjectGetInteger(0, name, OBJPROP_TYPE))
    if tmpObjType != OBJ_LABEL and tmpObjType != OBJ_TEXT:
        return False
    if StringLen(text) > 0 and font_size > 0:
        if ObjectSetString(0, name, OBJPROP_TEXT, text) == True and ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size) == True:
            if StringLen(font) > 0 and ObjectSetString(0, name, OBJPROP_FONT, font) == False:
                return False
            if text_color >= 1 and ObjectSetInteger(0, name, OBJPROP_COLOR, text_color) == False:
                return False
            return True
        return False
    return False

def ObjectSetMQL4(name, index, value):
    _sw8 = index
    if _sw8 == OBJPROP_COLOR:
        ObjectSetInteger(0, name, OBJPROP_COLOR, _int(value))
        return True
    elif _sw8 == OBJPROP_STYLE:
        ObjectSetInteger(0, name, OBJPROP_STYLE, _int(value))
        return True
    elif _sw8 == OBJPROP_WIDTH:
        ObjectSetInteger(0, name, OBJPROP_WIDTH, _int(value))
        return True
    elif _sw8 == OBJPROP_BACK:
        ObjectSetInteger(0, name, OBJPROP_BACK, _int(value))
        return True
    elif _sw8 == OBJPROP_RAY:
        ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, _int(value))
        return True
    elif _sw8 == OBJPROP_ELLIPSE:
        ObjectSetInteger(0, name, OBJPROP_ELLIPSE, _int(value))
        return True
    elif _sw8 == OBJPROP_SCALE:
        ObjectSetDouble(0, name, OBJPROP_SCALE, value)
        return True
    elif _sw8 == OBJPROP_ANGLE:
        ObjectSetDouble(0, name, OBJPROP_ANGLE, value)
        return True
    elif _sw8 == OBJPROP_ARROWCODE:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, _int(value))
        return True
    elif _sw8 == OBJPROP_TIMEFRAMES:
        ObjectSetInteger(0, name, OBJPROP_TIMEFRAMES, _int(value))
        return True
    elif _sw8 == OBJPROP_DEVIATION:
        ObjectSetDouble(0, name, OBJPROP_DEVIATION, value)
        return True
    elif _sw8 == OBJPROP_FONTSIZE:
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, _int(value))
        return True
    elif _sw8 == OBJPROP_CORNER:
        ObjectSetInteger(0, name, OBJPROP_CORNER, _int(value))
        return True
    elif _sw8 == OBJPROP_XDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_XDISTANCE, _int(value))
        return True
    elif _sw8 == OBJPROP_YDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_YDISTANCE, _int(value))
        return True
    elif _sw8 == OBJPROP_LEVELCOLOR:
        ObjectSetInteger(0, name, OBJPROP_LEVELCOLOR, _int(value))
        return True
    elif _sw8 == OBJPROP_LEVELSTYLE:
        ObjectSetInteger(0, name, OBJPROP_LEVELSTYLE, _int(value))
        return True
    elif _sw8 == OBJPROP_LEVELWIDTH:
        ObjectSetInteger(0, name, OBJPROP_LEVELWIDTH, _int(value))
        return True
    else:
        return False
    return False

def MethodMigrate(method):
    _sw9 = method
    if _sw9 == 0:
        return MODE_SMA
    elif _sw9 == 1:
        return MODE_EMA
    elif _sw9 == 2:
        return MODE_SMMA
    elif _sw9 == 3:
        return MODE_LWMA
    else:
        return MODE_SMA

def PriceMigrate(price):
    _sw10 = price
    if _sw10 == 1:
        return PRICE_CLOSE
    elif _sw10 == 2:
        return PRICE_OPEN
    elif _sw10 == 3:
        return PRICE_HIGH
    elif _sw10 == 4:
        return PRICE_LOW
    elif _sw10 == 5:
        return PRICE_MEDIAN
    elif _sw10 == 6:
        return PRICE_TYPICAL
    elif _sw10 == 7:
        return PRICE_WEIGHTED
    else:
        return PRICE_CLOSE

def StoFieldMigrate(field):
    _sw11 = field
    if _sw11 == 0:
        return STO_LOWHIGH
    elif _sw11 == 1:
        return STO_CLOSECLOSE
    else:
        return STO_LOWHIGH

def iMAMQL4(symbol, tf, period, ma_shift, method, price, shift):
    timeframe = TFMigrate(tf)
    ma_method = MethodMigrate(method)
    applied_price = PriceMigrate(price)
    handle = iMA(symbol, timeframe, period, ma_shift, ma_method, applied_price)
    if handle < 0:
        Print('The iMA object is not created: Error', GetLastError())
        return -1.0
    else:
        return CopyBufferMQL4(handle, 0, shift)

def iMAOnArrayMQL4(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    _sw12 = ma_method
    if _sw12 == MODE_SMA:
        total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        pos = total - 1
        i = 1
        while i < period:
            sum_ += arr[pos]
            i += 1
            pos -= 1
        while pos >= 0:
            sum_ += arr[pos]
            buf[pos] = _fdiv(sum_, period)
            sum_ -= arr[pos + period - 1]
            pos -= 1
        return buf[0]
    elif _sw12 == MODE_EMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2):
                buf[pos + 1] = array[pos + 1]
            buf[pos] = (array[pos] * pr) + (buf[pos + 1] * (1 - pr))
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw12 == MODE_SMMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        k = 0
        pos = 0
        pos = total - period
        while pos >= 0:
            if pos == (total - period):
                i = 0
                k = pos
                while i < period:
                    sum_ += array[k]
                    buf[k] = 0.0
                    i += 1
                    k += 1
            else:
                sum_ = (buf[pos + 1] * (period - 1)) + array[pos]
            buf[pos] = _fdiv(sum_, period)
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw12 == MODE_LWMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        lsum = 0.0
        price = 0.0
        i = 0
        weight = 0
        pos = total - 1
        i = 1
        while i <= period:
            price = array[pos]
            sum_ += price * i
            lsum += price
            weight += i
            i += 1
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            buf[pos] = _fdiv(sum_, weight)
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            sum_ = sum_ - lsum + (price * period)
            lsum -= array[i]
            lsum += price
        return buf[shift + ma_shift]
    else:
        return 0.0
    return 0.0

def iBarsMQL4(symbol, tf):
    timeframe = TFMigrate(tf)
    return Bars(symbol, timeframe)

def dpipPos(sSymbol):
    dpipPosition = 0.0
    if MarketInfoMQL4(sSymbol, 27) == 0:
        if (MarketInfoMQL4(sSymbol, 12) == 1 or MarketInfoMQL4(sSymbol, 12) == 3) or MarketInfoMQL4(sSymbol, 12) == 5:
            dpipPosition = MarketInfoMQL4(sSymbol, 11) * 10
        else:
            dpipPosition = MarketInfoMQL4(sSymbol, 11)
    else:
        dpipPosition = 1.0
    return dpipPosition

def dNbPips(sSymbol, dPrice1, dPrice2):
    dpipPosition = dpipPos(sSymbol)
    return NormalizeDouble(MathAbs(_fdiv(dPrice1 - dPrice2, dpipPosition)), 5)

def dValuePips(sSymbol, dPrice1, dPrice2, dVolume):
    dpipPosition = dpipPos(sSymbol)
    dNumberPips = dNbPips(sSymbol, dPrice1, dPrice2)
    dPipValue = _fdiv(MarketInfoMQL4(sSymbol, 16) * dpipPosition, MarketInfoMQL4(sSymbol, 17))
    return NormalizeDouble(dNumberPips * dPipValue * dVolume, 2)

def dPriceSL(sSymbol, dPrice, iTradeType, dnbPips):
    dpipPosition = dpipPos(sSymbol)
    iType = 1
    if (iTradeType == 0 or iTradeType == 2) or iTradeType == 4:
        iType = -1
    elif (iTradeType == 1 or iTradeType == 3) or iTradeType == 5:
        iType = 1
    return NormalizeDouble(dPrice + (iType * dnbPips * dpipPosition), 5)

def dPriceTP(sSymbol, dPrice, iTradeType, dnbPips):
    dpipPosition = dpipPos(sSymbol)
    iType = 1
    if (iTradeType == 0 or iTradeType == 2) or iTradeType == 4:
        iType = 1
    elif (iTradeType == 1 or iTradeType == 3) or iTradeType == 5:
        iType = -1
    return NormalizeDouble(dPrice + (iType * dnbPips * dpipPosition), 5)

def dPercentSL(sSymbol, dPrice, iTradeType, dVol, dPercent):
    dpipPosition = dpipPos(sSymbol)
    dPipValue = _fdiv(MarketInfoMQL4(sSymbol, 16) * dpipPosition, MarketInfoMQL4(sSymbol, 17))
    dAmtPerPercentRisk = (AccountInfoDouble(ACCOUNT_BALANCE) * dPercent) / 100
    ndNbPips = _fdiv(dAmtPerPercentRisk, dPipValue * dVol)
    if (iTradeType == 0 or iTradeType == 2) or iTradeType == 4:
        return dPrice - (ndNbPips * dpipPosition)
    elif (iTradeType == 1 or iTradeType == 3) or iTradeType == 5:
        return dPrice + (ndNbPips * dpipPosition)
    return False

def dPercentTP(sSymbol, dPrice, iTradeType, dVol, dPercent):
    dpipPosition = dpipPos(sSymbol)
    dPipValue = _fdiv(MarketInfoMQL4(sSymbol, 16) * dpipPosition, MarketInfoMQL4(sSymbol, 17))
    dAmtPerPercentRisk = (AccountInfoDouble(ACCOUNT_BALANCE) * dPercent) / 100
    ndNbPips = _fdiv(dAmtPerPercentRisk, dPipValue * dVol)
    if (iTradeType == 0 or iTradeType == 2) or iTradeType == 4:
        return dPrice + (ndNbPips * dpipPosition)
    elif (iTradeType == 1 or iTradeType == 3) or iTradeType == 5:
        return dPrice - (ndNbPips * dpipPosition)
    return False

def dPercentVol(sSymbol, dPrice, dPriceSL_, dPercent):
    dpipPosition = dpipPos(sSymbol)
    dNumberPips = dNbPips(sSymbol, dPrice, dPriceSL_)
    dPipValue = _fdiv(MarketInfoMQL4(sSymbol, 16) * dpipPosition, MarketInfoMQL4(sSymbol, 17))
    dAmtPerPercentRisk = (AccountInfoDouble(ACCOUNT_BALANCE) * dPercent) / 100
    return _fdiv(dAmtPerPercentRisk, dNumberPips * dPipValue)

def OnInit():
    ChartSetInteger(0, CHART_SHOW_ONE_CLICK, False)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global dRPTAmtRewarding, dRPTAmtRisking, kRPT, sRPTObjectName
    ObjectsDeleteAll(0)
    dRPTAmtRisking = 0.0
    dRPTAmtRewarding = 0.0
    sRPTObjectName = ''
    kRPT = 0
    while kRPT < PositionsTotal():
        if PositionSelectByTicket(PositionGetTicket(kRPT)):
            if PositionGetInteger(POSITION_TYPE) == 0 or PositionGetInteger(POSITION_TYPE) == 1:
                if PositionGetString(POSITION_SYMBOL) == Symbol():
                    if PositionGetDouble(POSITION_SL) != 0:
                        sRPTObjectName = ''
                        StringConcatenate(_GlobRef(globals(), 'sRPTObjectName'), PositionGetTicket(kRPT), PositionGetDouble(POSITION_SL))
                        vSetText(0, sRPTObjectName, 0, TimeCurrent(), PositionGetDouble(POSITION_SL), 8, cRPTFontClr, 'SL: ' + DoubleToString(_fdiv(dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_SL), PositionGetDouble(POSITION_VOLUME)), AccountInfoDouble(ACCOUNT_BALANCE)) * 100, 2) + '% = ' + DoubleToString(dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_SL), PositionGetDouble(POSITION_VOLUME)), 2) + ' ' + AccountInfoString(ACCOUNT_CURRENCY))
                    if PositionGetDouble(POSITION_TP) != 0:
                        sRPTObjectName = ''
                        StringConcatenate(_GlobRef(globals(), 'sRPTObjectName'), PositionGetTicket(kRPT), PositionGetDouble(POSITION_TP))
                        vSetText(0, sRPTObjectName, 0, TimeCurrent(), PositionGetDouble(POSITION_TP), 8, cRPTFontClr, 'TP: ' + DoubleToString(_fdiv(dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_TP), PositionGetDouble(POSITION_VOLUME)), AccountInfoDouble(ACCOUNT_BALANCE)) * 100, 2) + '% = ' + DoubleToString(dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_TP), PositionGetDouble(POSITION_VOLUME)), 2) + ' ' + AccountInfoString(ACCOUNT_CURRENCY))
                    if PositionGetDouble(POSITION_SL) != 0:
                        dRPTAmtRisking = dRPTAmtRisking + dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_SL), PositionGetDouble(POSITION_VOLUME))
                    if PositionGetDouble(POSITION_TP) != 0:
                        dRPTAmtRewarding = dRPTAmtRewarding + dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_TP), PositionGetDouble(POSITION_VOLUME))
        kRPT += 1
    ChartSetInteger(0, CHART_SHOW_ONE_CLICK, False)
    vSetLabel(0, 'RPTBalance', 0, 25, 20, 8, cRPTFontClr, 'Balance: ' + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + ' ' + AccountInfoString(ACCOUNT_CURRENCY))
    vSetLabel(0, 'RPTAllSymbolPercentRisked', 0, 45, 20, 8, cRPTFontClr, 'All ' + Symbol() + "'s % Risked : " + DoubleToString(_fdiv(dRPTAmtRisking, AccountInfoDouble(ACCOUNT_BALANCE)) * 100, 2) + '%')
    vSetLabel(0, 'RPTAllSymbolPercentTarget', 0, 65, 20, 8, cRPTFontClr, 'All ' + Symbol() + "'s % Target : " + DoubleToString(_fdiv(dRPTAmtRewarding, AccountInfoDouble(ACCOUNT_BALANCE)) * 100, 2) + '%')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class INDRiskPerTrade(_MQL5Indicator):
    name = 'IND_RiskPerTrade'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

