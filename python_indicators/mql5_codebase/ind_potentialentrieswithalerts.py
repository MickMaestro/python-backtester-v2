"""IND_PotentialEntriesWithAlerts — converted from MQL5: MQL5 Indicators/Identify potential entries/IND_PotentialEntriesWithAlerts.mq5

Copyright: Copyright 2010, Lizar; Link: Lizar@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.enum import *  # #include Enum.mqh
from backtester.mql5.lib.define import *  # #include Define.mqh
from backtester.mql5.lib.libcisnewbar import *  # #include libcisnewbar.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, Lizar', 'link': 'Lizar@mail.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'IND_PotentialEntriesWithAlerts', 'source': 'MQL5 Indicators/Identify potential entries/IND_PotentialEntriesWithAlerts.mq5', 'folder': 'Identify potential entries', 'inputs': [{'mql': 'PA_TYPE', 'py': 'PA_TYPE', 'param': 'PA_TYPE', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Enum.mqh', 'Define.mqh', 'libcisnewbar.mqh']}

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

# enum iTrend
A1 = 1
A2 = 2
_enum('iTrend', {1: 'A1', 2: 'A2'})

# ---- inputs and global variables
PA_TYPE = _input('PA_TYPE', A1)
sArrowBuy1 = ''
sArrowBuy2 = ''
sArrowSell1 = ''
sArrowSell2 = ''
sTradeIdentification = ''

class cCandlestick(MqlObject):
    _q_fields = ('dOpenPrice', 'dHighPrice', 'dLowPrice', 'dClosePrice', 'dRangeCandle', 'dBodyCandle', 'dUpperWickCandle', 'dLowerWickCandle', 'bBullCandle', 'bBearCandle', 'bDojiCandle')
    def __init__(self, *args):
        self.dOpenPrice = 0.0
        self.dHighPrice = 0.0
        self.dLowPrice = 0.0
        self.dClosePrice = 0.0
        self.dRangeCandle = 0.0
        self.dBodyCandle = 0.0
        self.dUpperWickCandle = 0.0
        self.dLowerWickCandle = 0.0
        self.bBullCandle = False
        self.bBearCandle = False
        self.bDojiCandle = False
    def mvGetCandleStickCharateristics(self, s, i):
        self.dOpenPrice = iOpenMQL4(s, PERIOD_CURRENT, i)
        self.dHighPrice = iHighMQL4(s, PERIOD_CURRENT, i)
        self.dLowPrice = iLowMQL4(s, PERIOD_CURRENT, i)
        self.dClosePrice = iCloseMQL4(s, PERIOD_CURRENT, i)
        self.dRangeCandle = NormalizeDouble(_fdiv(MathAbs(self.dHighPrice - self.dLowPrice), MarketInfoMQL4(s, 11)), Digits())
        self.dBodyCandle = NormalizeDouble(_fdiv(MathAbs(self.dOpenPrice - self.dClosePrice), MarketInfoMQL4(s, 11)), Digits())
        self.dUpperWickCandle = NormalizeDouble(_fdiv(MathAbs(self.dHighPrice - MathMax(self.dClosePrice, self.dOpenPrice)), MarketInfoMQL4(s, 11)), Digits())
        self.dLowerWickCandle = NormalizeDouble(_fdiv(MathAbs(MathMin(self.dClosePrice, self.dOpenPrice) - self.dLowPrice), MarketInfoMQL4(s, 11)), Digits())
        if (self.dBodyCandle <= 1.0 and self.dUpperWickCandle > self.dBodyCandle) and self.dLowerWickCandle > self.dBodyCandle:
            self.bDojiCandle = True
            self.bBullCandle = False
            self.bBearCandle = False
        elif self.dOpenPrice < self.dClosePrice:
            self.bDojiCandle = False
            self.bBullCandle = True
            self.bBearCandle = False
        elif self.dOpenPrice > self.dClosePrice:
            self.bDojiCandle = False
            self.bBullCandle = False
            self.bBearCandle = True

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
    _sw1 = index
    if _sw1 == 0:
        if CopyBuffer(handle, 0, shift, 1, buf) > 0:
            return buf[0]
    elif _sw1 == 1:
        if CopyBuffer(handle, 1, shift, 1, buf) > 0:
            return buf[0]
    elif _sw1 == 2:
        if CopyBuffer(handle, 2, shift, 1, buf) > 0:
            return buf[0]
    elif _sw1 == 3:
        if CopyBuffer(handle, 3, shift, 1, buf) > 0:
            return buf[0]
    elif _sw1 == 4:
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

def SetIndexStyleMQL4(index, type_, style=-1, width=-1, clr=CLR_NONE):
    if width > -1:
        PlotIndexSetInteger(index, PLOT_LINE_WIDTH, width)
    if clr != CLR_NONE:
        PlotIndexSetInteger(index, PLOT_LINE_COLOR, clr)
    _sw2 = type_
    _k3 = 0 if _sw2 == 0 else 1 if _sw2 == 1 else 2 if _sw2 == 2 else 3 if _sw2 == 3 else 4 if _sw2 == 4 else 5 if _sw2 == 12 else 6
    try:
        if _k3 <= 0:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_LINE)
        if _k3 <= 1:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_SECTION)
        if _k3 <= 2:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
        if _k3 <= 3:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_ARROW)
        if _k3 <= 4:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_ZIGZAG)
        if _k3 <= 5:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_NONE)
        if _k3 <= 6:
            PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_LINE)
    except _SwitchBreak:
        pass
    _sw4 = style
    _k5 = 0 if _sw4 == 0 else 1 if _sw4 == 1 else 2 if _sw4 == 2 else 3 if _sw4 == 3 else 4 if _sw4 == 4 else 5
    try:
        if _k5 <= 0:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_SOLID)
        if _k5 <= 1:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASH)
        if _k5 <= 2:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DOT)
        if _k5 <= 3:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASHDOT)
        if _k5 <= 4:
            PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASHDOTDOT)
        if _k5 <= 5:
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
    _sw6 = type_
    if _sw6 == 1:
        return SymbolInfoDouble(symbol, SYMBOL_LASTLOW)
    elif _sw6 == 2:
        return SymbolInfoDouble(symbol, SYMBOL_LASTHIGH)
    elif _sw6 == 5:
        return float(SymbolInfoInteger(symbol, SYMBOL_TIME))
    elif _sw6 == 9:
        return SymbolInfoDouble(symbol, SYMBOL_BID)
    elif _sw6 == 10:
        return SymbolInfoDouble(symbol, SYMBOL_ASK)
    elif _sw6 == 11:
        return SymbolInfoDouble(symbol, SYMBOL_POINT)
    elif _sw6 == 12:
        return float(SymbolInfoInteger(symbol, SYMBOL_DIGITS))
    elif _sw6 == 13:
        return float(SymbolInfoInteger(symbol, SYMBOL_SPREAD))
    elif _sw6 == 14:
        return float(SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL))
    elif _sw6 == 15:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE)
    elif _sw6 == 16:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
    elif _sw6 == 17:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
    elif _sw6 == 18:
        return SymbolInfoDouble(symbol, SYMBOL_SWAP_LONG)
    elif _sw6 == 19:
        return SymbolInfoDouble(symbol, SYMBOL_SWAP_SHORT)
    elif _sw6 == 20:
        return 0.0
    elif _sw6 == 21:
        return 0.0
    elif _sw6 == 22:
        return 0.0
    elif _sw6 == 23:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)
    elif _sw6 == 24:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)
    elif _sw6 == 25:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
    elif _sw6 == 26:
        return float(SymbolInfoInteger(symbol, SYMBOL_SWAP_MODE))
    elif _sw6 == 27:
        return float(SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE))
    elif _sw6 == 28:
        return 0.0
    elif _sw6 == 29:
        return 0.0
    elif _sw6 == 30:
        return 0.0
    elif _sw6 == 31:
        return 0.0
    elif _sw6 == 32:
        return 0.0
    elif _sw6 == 33:
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
    _sw7 = index
    if _sw7 == OBJPROP_COLOR:
        ObjectSetInteger(0, name, OBJPROP_COLOR, _int(value))
        return True
    elif _sw7 == OBJPROP_STYLE:
        ObjectSetInteger(0, name, OBJPROP_STYLE, _int(value))
        return True
    elif _sw7 == OBJPROP_WIDTH:
        ObjectSetInteger(0, name, OBJPROP_WIDTH, _int(value))
        return True
    elif _sw7 == OBJPROP_BACK:
        ObjectSetInteger(0, name, OBJPROP_BACK, _int(value))
        return True
    elif _sw7 == OBJPROP_RAY:
        ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, _int(value))
        return True
    elif _sw7 == OBJPROP_ELLIPSE:
        ObjectSetInteger(0, name, OBJPROP_ELLIPSE, _int(value))
        return True
    elif _sw7 == OBJPROP_SCALE:
        ObjectSetDouble(0, name, OBJPROP_SCALE, value)
        return True
    elif _sw7 == OBJPROP_ANGLE:
        ObjectSetDouble(0, name, OBJPROP_ANGLE, value)
        return True
    elif _sw7 == OBJPROP_ARROWCODE:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, _int(value))
        return True
    elif _sw7 == OBJPROP_TIMEFRAMES:
        ObjectSetInteger(0, name, OBJPROP_TIMEFRAMES, _int(value))
        return True
    elif _sw7 == OBJPROP_DEVIATION:
        ObjectSetDouble(0, name, OBJPROP_DEVIATION, value)
        return True
    elif _sw7 == OBJPROP_FONTSIZE:
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, _int(value))
        return True
    elif _sw7 == OBJPROP_CORNER:
        ObjectSetInteger(0, name, OBJPROP_CORNER, _int(value))
        return True
    elif _sw7 == OBJPROP_XDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_XDISTANCE, _int(value))
        return True
    elif _sw7 == OBJPROP_YDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_YDISTANCE, _int(value))
        return True
    elif _sw7 == OBJPROP_LEVELCOLOR:
        ObjectSetInteger(0, name, OBJPROP_LEVELCOLOR, _int(value))
        return True
    elif _sw7 == OBJPROP_LEVELSTYLE:
        ObjectSetInteger(0, name, OBJPROP_LEVELSTYLE, _int(value))
        return True
    elif _sw7 == OBJPROP_LEVELWIDTH:
        ObjectSetInteger(0, name, OBJPROP_LEVELWIDTH, _int(value))
        return True
    else:
        return False
    return False

def MethodMigrate(method):
    _sw8 = method
    if _sw8 == 0:
        return MODE_SMA
    elif _sw8 == 1:
        return MODE_EMA
    elif _sw8 == 2:
        return MODE_SMMA
    elif _sw8 == 3:
        return MODE_LWMA
    else:
        return MODE_SMA

def PriceMigrate(price):
    _sw9 = price
    if _sw9 == 1:
        return PRICE_CLOSE
    elif _sw9 == 2:
        return PRICE_OPEN
    elif _sw9 == 3:
        return PRICE_HIGH
    elif _sw9 == 4:
        return PRICE_LOW
    elif _sw9 == 5:
        return PRICE_MEDIAN
    elif _sw9 == 6:
        return PRICE_TYPICAL
    elif _sw9 == 7:
        return PRICE_WEIGHTED
    else:
        return PRICE_CLOSE

def StoFieldMigrate(field):
    _sw10 = field
    if _sw10 == 0:
        return STO_LOWHIGH
    elif _sw10 == 1:
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
    _sw11 = ma_method
    if _sw11 == MODE_SMA:
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
    elif _sw11 == MODE_EMA:
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
    elif _sw11 == MODE_SMMA:
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
    elif _sw11 == MODE_LWMA:
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

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    period_seconds = PeriodSeconds(Period())
    new_time = _idiv(TimeCurrent(), period_seconds) * period_seconds
    if current_chart.isNewBar_1(new_time):
        OnNewBarCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread)
    return rates_total

def OnInit():
    return INIT_SUCCEEDED

def OnNewBarCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    cCS1 = cCandlestick()
    cCS2 = cCandlestick()
    cCS1.mvGetCandleStickCharateristics(Symbol(), 1)
    cCS2.mvGetCandleStickCharateristics(Symbol(), 2)
    if PA_TYPE == 1:
        if ((cCS1.bBullCandle and cCS2.bBearCandle) and (2 * cCS1.dBodyCandle) < cCS1.dLowerWickCandle) and cCS1.dLowerWickCandle > (3 * cCS1.dUpperWickCandle):
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dLowPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'HAM', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrGreen)
            Alert('BULLISH HAMMER')
        elif ((cCS1.bBullCandle and cCS2.bBearCandle) and (2 * cCS1.dBodyCandle) < cCS1.dUpperWickCandle) and (3 * cCS1.dLowerWickCandle) < cCS1.dUpperWickCandle:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dLowPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'IVH', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrGreen)
            Alert('BULLISH INVERTED HAMMER')
        elif ((((cCS1.bBullCandle and cCS2.bBearCandle) and cCS1.dRangeCandle > cCS2.dRangeCandle) and cCS1.dBodyCandle > cCS2.dBodyCandle) and cCS1.dHighPrice > cCS2.dHighPrice) and cCS1.dLowPrice < cCS2.dLowPrice:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dLowPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'ENG', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrGreen)
            Alert('BULLISH ENGULFING')
        elif ((((cCS1.bBullCandle and cCS2.bBearCandle) and cCS1.dRangeCandle < cCS2.dRangeCandle) and cCS1.dBodyCandle < cCS2.dBodyCandle) and cCS1.dHighPrice < cCS2.dHighPrice) and cCS1.dLowPrice > cCS2.dLowPrice:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dLowPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'HAR', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrGreen)
            Alert('BULLISH HARAMI')
        elif (((cCS1.bBullCandle and cCS2.bBearCandle) and cCS1.dBodyCandle < cCS1.dLowerWickCandle) and cCS1.dBodyCandle < cCS1.dUpperWickCandle) and cCS1.dLowerWickCandle == cCS1.dUpperWickCandle:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dLowPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'MOS', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrGreen)
            Alert('MORNING STAR')
        if ((cCS1.bBullCandle and cCS2.bBullCandle) and cCS1.dRangeCandle > cCS2.dRangeCandle) and cCS1.dBodyCandle >= (2 * cCS2.dBodyCandle):
            StringConcatenate(_GlobRef(globals(), 'sArrowBuy1'), 'sArrowBuy1', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreate(0, sArrowBuy1, OBJ_ARROW_BUY, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dOpenPrice)
            StringConcatenate(_GlobRef(globals(), 'sArrowBuy2'), 'sArrowBuy2', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 2)))
            ObjectCreate(0, sArrowBuy2, OBJ_ARROW_BUY, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 2), cCS2.dOpenPrice)
            Alert('BUILDING MOMEMTUM')
    if PA_TYPE == 2:
        if ((cCS1.bBearCandle and cCS2.bBullCandle) and (2 * cCS1.dBodyCandle) < cCS1.dUpperWickCandle) and (3 * cCS1.dLowerWickCandle) < cCS1.dUpperWickCandle:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dHighPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'SHS', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrRed)
            Alert('SHOOTING STAR')
        elif ((cCS1.bBearCandle and cCS2.bBullCandle) and (2 * cCS1.dBodyCandle) < cCS1.dLowerWickCandle) and cCS1.dLowerWickCandle > (3 * cCS1.dUpperWickCandle):
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dHighPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'HGM', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrRed)
            Alert('HANGING MAN')
        elif ((((cCS1.bBearCandle and cCS2.bBullCandle) and cCS1.dRangeCandle > cCS2.dRangeCandle) and cCS1.dBodyCandle > cCS2.dBodyCandle) and cCS1.dHighPrice > cCS2.dHighPrice) and cCS1.dLowPrice < cCS2.dLowPrice:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dHighPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'ENG', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrRed)
            Alert('BEARISH ENGULFING')
        elif ((((cCS1.bBearCandle and cCS2.bBullCandle) and cCS1.dRangeCandle < cCS2.dRangeCandle) and cCS1.dBodyCandle < cCS2.dBodyCandle) and cCS1.dHighPrice < cCS2.dHighPrice) and cCS1.dLowPrice > cCS2.dLowPrice:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dHighPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'HAR', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrRed)
            Alert('BEARISH HARAMI')
        elif (((cCS1.bBearCandle and cCS2.bBullCandle) and cCS1.dBodyCandle < cCS1.dLowerWickCandle) and cCS1.dBodyCandle < cCS1.dUpperWickCandle) and cCS1.dLowerWickCandle == cCS1.dUpperWickCandle:
            StringConcatenate(_GlobRef(globals(), 'sTradeIdentification'), 'sTradeIdentification: ', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreateMQL4(sTradeIdentification, OBJ_TEXT, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dHighPrice)
            ObjectSetTextMQL4(sTradeIdentification, 'EVS', 10, '')
            ObjectSetMQL4(sTradeIdentification, OBJPROP_COLOR, clrRed)
            Alert('EVENING STAR')
        elif ((cCS1.bBearCandle and cCS2.bBearCandle) and cCS1.dBodyCandle > cCS2.dBodyCandle) and cCS1.dRangeCandle >= (2 * cCS2.dRangeCandle):
            StringConcatenate(_GlobRef(globals(), 'sArrowSell1'), 'sArrowSell1', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 1)))
            ObjectCreate(0, sArrowSell1, OBJ_ARROW_SELL, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 1), cCS1.dOpenPrice)
            StringConcatenate(_GlobRef(globals(), 'sArrowSell2'), 'sArrowSell2', _str(iTimeMQL4(Symbol(), PERIOD_CURRENT, 2)))
            ObjectCreate(0, sArrowSell2, OBJ_ARROW_SELL, 0, iTimeMQL4(Symbol(), PERIOD_CURRENT, 2), cCS2.dOpenPrice)
            Alert('BUILDING MOMEMTUM')
    return rates_total

# ---- global variables initialised from expressions
current_chart = _alloc(CisNewBar)  # CisNewBar class instance (used for the current chart)
current_chart.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class INDPotentialEntriesWithAlerts(_MQL5Indicator):
    name = 'IND_PotentialEntriesWithAlerts'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PA_TYPE': _Choice({1: 'Bullish Trend', 2: 'Bearish Trend'}, default=1),
    }

