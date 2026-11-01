"""absolutestrengthmarket_v1 — converted from MQL5: MQL5 Indicators/AbsoluteStrengthMarket/absolutestrengthmarket_v1.mq5

Copyright: Copyright © 2013, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'window': 'separate', 'indicator_buffers': 16, 'indicator_plots': 6, 'indicator_maximum': 2.0, 'indicator_minimum': 0.0}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [16760576], 2: [255], 3: [16436871], 4: [8036607], 5: [55295], 6: [8421504]}, 'widths': {1: 4, 2: 4, 3: 2, 4: 2, 5: 2, 6: 0}, 'styles': {}, 'labels': {1: 'Bull Market', 2: 'Bear Market', 3: 'Correction ', 4: 'Bear Market Rally', 5: 'Choppy Market', 6: 'Sideways Market'}, 'levels': [], 'description': [], 'name': 'absolutestrengthmarket_v1', 'source': 'MQL5 Indicators/AbsoluteStrengthMarket/absolutestrengthmarket_v1.mq5', 'folder': 'AbsoluteStrengthMarket', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MathMode', 'py': 'MathMode', 'param': 'MathMode', 'type': 'int', 'default': 0, 'label': 'Math method', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Period of Evaluation', 'sinput': False}, {'mql': 'PreSmooth', 'py': 'PreSmooth', 'param': 'PreSmooth', 'type': 'int', 'default': 1, 'label': 'Period of PreSmoothing', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 5, 'label': 'Period of Smoothing', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 5, 'label': 'Period of Signal Line', 'sinput': False}, {'mql': 'MA_Mode', 'py': 'MA_Mode', 'param': 'MA_Mode', 'type': 'int', 'default': 3, 'label': 'Moving Average Mode', 'sinput': False}, {'mql': 'IndicatorValue', 'py': 'IndicatorValue', 'param': 'IndicatorValue', 'type': 'double', 'default': 1.0, 'label': 'Indicator Value (ex.1.0)', 'sinput': False}, {'mql': 'ArrowCode', 'py': 'ArrowCode', 'param': 'ArrowCode', 'type': 'int', 'default': 167, 'label': 'Arrow Code in Wingdings', 'sinput': False}, {'mql': 'AlertMode', 'py': 'AlertMode', 'param': 'AlertMode', 'type': 'int', 'default': 0, 'label': 'Alert Mode: 0-off,1-on', 'sinput': False}, {'mql': 'ShowName', 'py': 'ShowName', 'param': 'ShowName', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'ShowTimeFrame', 'py': 'ShowTimeFrame', 'param': 'ShowTimeFrame', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UniqueName', 'py': 'UniqueName', 'param': None, 'type': 'string', 'default': 'Market', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Black = 0x000000  # MQL4 colour name

# enum ENUM_MATH_MODE
RSI_method = 0
Stochastic_method = 1
DMI_method = 2
_enum('ENUM_MATH_MODE', {0: 'RSI_method', 1: 'Stochastic_method', 2: 'DMI_method'})

# enum ENUM_SMOOTH_MODE
sma = 0
ema = 1
wilder = 2
lwma = 3
_enum('ENUM_SMOOTH_MODE', {0: 'sma', 1: 'ema', 2: 'wilder', 3: 'lwma'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', 0)
MathMode = _input('MathMode', 0)  # Math method
Price = _input('Price', PRICE_CLOSE)  # Apply to
Length = _input('Length', 10)  # Period of Evaluation
PreSmooth = _input('PreSmooth', 1)  # Period of PreSmoothing
Smooth = _input('Smooth', 5)  # Period of Smoothing
Signal = _input('Signal', 5)  # Period of Signal Line
MA_Mode = _input('MA_Mode', 3)  # Moving Average Mode
IndicatorValue = _input('IndicatorValue', 1.0)  # Indicator Value (ex.1.0)
ArrowCode = _input('ArrowCode', 167)  # Arrow Code in Wingdings
AlertMode = _input('AlertMode', 0)  # Alert Mode: 0-off,1-on
ShowName = _input('ShowName', True)
ShowTimeFrame = _input('ShowTimeFrame', True)
FontName = _input('FontName', 'Arial')
FontSize = _input('FontSize', 8)
UniqueName = _input('UniqueName', 'Market')
BullMarket = Arr(0, 0.0)
BearMarket = Arr(0, 0.0)
Correction = Arr(0, 0.0)
BearRally = Arr(0, 0.0)
Choppy = Arr(0, 0.0)
Sideways = Arr(0, 0.0)
Bulls = Arr(0, 0.0)
Bears = Arr(0, 0.0)
signalBulls = Arr(0, 0.0)
signalBears = Arr(0, 0.0)
price = Arr(0, 0.0)
loprice = Arr(0, 0.0)
bulls = Arr(0, 0.0)
bears = Arr(0, 0.0)
lbulls = Arr(0, 0.0)
lbears = Arr(0, 0.0)
tf = 0
Price_handle = 0
Lo_handle = 0
mtf_handle = 0
ema = Arr(6, 0.0, dyn=False, dims=(2,))
_point = 0.0
mtf_bullmarket = Arr(1, 0.0, dyn=False)
mtf_bearmarket = Arr(1, 0.0, dyn=False)
mtf_correction = Arr(1, 0.0, dyn=False)
mtf_bearrally = Arr(1, 0.0, dyn=False)
mtf_choppy = Arr(1, 0.0, dyn=False)
mtf_sideways = Arr(1, 0.0, dyn=False)
prevAlertTime = 0
ptime = Arr(6, 0, dyn=False)
ftime = Arr(6, False, dyn=False)
short_name = ""

def OnInit():
    global Lo_handle, Price_handle, _point, mtf_handle, short_name, tf
    if TimeFrame <= Period():
        tf = Period()
    else:
        tf = TimeFrame
    SetIndexBuffer(0, BullMarket, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, ArrowCode)
    SetIndexBuffer(1, BearMarket, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, ArrowCode)
    SetIndexBuffer(2, Correction, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, ArrowCode)
    SetIndexBuffer(3, BearRally, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, ArrowCode)
    SetIndexBuffer(4, Choppy, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, ArrowCode)
    SetIndexBuffer(5, Sideways, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_ARROW, ArrowCode)
    SetIndexBuffer(6, Bulls, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, Bears, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, signalBulls, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, signalBears, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, price, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, loprice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, bulls, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, bears, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, lbulls, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, lbears, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    math_name = ""
    ma_name = ""
    _sw1 = MathMode
    if _sw1 == 0:
        math_name = 'RSI'
    elif _sw1 == 1:
        math_name = 'Stoch'
    elif _sw1 == 2:
        math_name = 'DMI'
    _sw2 = MA_Mode
    if _sw2 == 0:
        ma_name = 'SMA'
    elif _sw2 == 1:
        ma_name = 'EMA'
    elif _sw2 == 2:
        ma_name = 'Wilder'
    elif _sw2 == 3:
        ma_name = 'LWMA'
    if ShowName:
        short_name = 'AbsoluteStrengthMarket_v1[' + timeframeToString(tf) + '](' + math_name + ',' + priceToString(Price) + ',' + _str(Length) + ',' + _str(PreSmooth) + ',' + _str(Smooth) + ',' + _str(Signal) + ',' + ma_name + ')'
    else:
        short_name = ' '
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    draw_begin = Length + PreSmooth + Smooth + Signal
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, draw_begin)
    Price_handle = iMA(None, 0, PreSmooth, 0, MA_Mode, Price)
    if MathMode == 2:
        Lo_handle = iMA(None, 0, PreSmooth, 0, MA_Mode, PRICE_LOW)
    _point = Point() * MathPow(10, _imod(Digits(), 2))
    if TimeFrame > 0:
        mtf_handle = iCustom(Symbol(), TimeFrame, 'AbsoluteStrengthMarket_v1', 0, MathMode, Price, Length, PreSmooth, Smooth, Signal, MA_Mode, IndicatorValue, ArrowCode, AlertMode)

def OnDeinit(reason):
    deleteObj(UniqueName + timeframeToString(tf))
    Comment('')
    return

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global prevAlertTime
    i = 0
    x = 0
    y = 0
    shift = 0
    limit = 0
    mtflimit = 0
    len_ = 0
    copied = 0
    window = 0
    up = 0.0
    lo = 0.0
    mtf_time = 0
    message = ""
    if prev_calculated == 0:
        limit = 0
        mtflimit = rates_total - 1
        ArrayInitialize(BullMarket, EMPTY_VALUE)
        ArrayInitialize(BearMarket, EMPTY_VALUE)
        ArrayInitialize(Correction, EMPTY_VALUE)
        ArrayInitialize(BearRally, EMPTY_VALUE)
        ArrayInitialize(Choppy, EMPTY_VALUE)
        ArrayInitialize(Sideways, EMPTY_VALUE)
    else:
        limit = prev_calculated - 1
        mtflimit = _idiv(PeriodSeconds(tf), PeriodSeconds(Period()))
    window = ChartWindowFind()
    ArraySetAsSeries(Time, True)
    copied = CopyBuffer(Price_handle, 0, 0, rates_total - 1, price)
    if copied < 0:
        Print('not all prices copied. Will try on next tick Error =', GetLastError(), ', copied =', copied)
        return 0
    if MathMode == 2:
        copied = CopyBuffer(Lo_handle, 0, 0, rates_total - 1, loprice)
        if copied < 0:
            Print('not all prices copied. Will try on next tick Error =', GetLastError(), ', copied =', copied)
            return 0
    if tf > Period():
        shift = 0
        y = 0
        while shift < mtflimit:
            if Time[shift] < iTime_u("", TimeFrame, y):
                y += 1
            mtf_time = iTime_u("", TimeFrame, y)
            x = rates_total - shift - 1
            copied = CopyBuffer(mtf_handle, 0, _DT(mtf_time), _DT(mtf_time), mtf_bullmarket)
            if copied <= 0:
                return 0
            BullMarket[x] = mtf_bullmarket[0]
            copied = CopyBuffer(mtf_handle, 1, _DT(mtf_time), _DT(mtf_time), mtf_bearmarket)
            if copied <= 0:
                return 0
            BearMarket[x] = mtf_bearmarket[0]
            copied = CopyBuffer(mtf_handle, 2, _DT(mtf_time), _DT(mtf_time), mtf_correction)
            if copied <= 0:
                return 0
            Correction[x] = mtf_correction[0]
            copied = CopyBuffer(mtf_handle, 3, _DT(mtf_time), _DT(mtf_time), mtf_bearrally)
            if copied <= 0:
                return 0
            BearRally[x] = mtf_bearrally[0]
            copied = CopyBuffer(mtf_handle, 4, _DT(mtf_time), _DT(mtf_time), mtf_choppy)
            if copied <= 0:
                return 0
            Choppy[x] = mtf_choppy[0]
            copied = CopyBuffer(mtf_handle, 5, _DT(mtf_time), _DT(mtf_time), mtf_sideways)
            if copied <= 0:
                return 0
            Sideways[x] = mtf_sideways[0]
            shift += 1
    else:
        shift = limit
        for shift in range(shift, rates_total):
            if shift > Length:
                _sw3 = MathMode
                if _sw3 == 0:
                    bulls[shift] = _fdiv(0.5 * (MathAbs(price[shift] - price[shift - 1]) + (price[shift] - price[shift - 1])), _point)
                    bears[shift] = _fdiv(0.5 * (MathAbs(price[shift] - price[shift - 1]) - (price[shift] - price[shift - 1])), _point)
                elif _sw3 == 1:
                    up = 0.0
                    lo = 10000000000.0
                    i = 0
                    for i in range(i, Length):
                        up = MathMax(up, High[shift - i])
                        lo = MathMin(lo, Low[shift - i])
                    else:
                        i = _range_end(i, Length, 1)
                    bulls[shift] = _fdiv(price[shift] - lo, _point)
                    bears[shift] = _fdiv(up - price[shift], _point)
                elif _sw3 == 2:
                    bulls[shift] = _fdiv(MathMax(0, 0.5 * (MathAbs(price[shift] - price[shift - 1]) + (price[shift] - price[shift - 1]))), _point)
                    bears[shift] = _fdiv(MathMax(0, 0.5 * (MathAbs(loprice[shift - 1] - loprice[shift]) + (loprice[shift - 1] - loprice[shift]))), _point)
                    if bulls[shift] > bears[shift]:
                        bears[shift] = 0.0
                    elif bulls[shift] < bears[shift]:
                        bulls[shift] = 0.0
                    elif bulls[shift] == bears[shift]:
                        bulls[shift] = 0.0
                        bears[shift] = 0.0
                if MathMode == 1:
                    len_ = 1
                else:
                    len_ = Length
                if shift < len_:
                    continue
                lbulls[shift] = mAverage(0, MA_Mode, bulls, len_, Time[shift], shift)
                lbears[shift] = mAverage(1, MA_Mode, bears, len_, Time[shift], shift)
                if shift < (len_ + Smooth):
                    continue
                Bulls[shift] = mAverage(2, MA_Mode, lbulls, Smooth, Time[shift], shift)
                Bears[shift] = mAverage(3, MA_Mode, lbears, Smooth, Time[shift], shift)
                if shift < (len_ + Smooth + Signal):
                    continue
                if Signal > 1:
                    signalBulls[shift] = mAverage(4, MA_Mode, Bulls, Signal, Time[shift], shift)
                    signalBears[shift] = mAverage(5, MA_Mode, Bears, Signal, Time[shift], shift)
                else:
                    signalBulls[shift] = Bulls[shift - 1]
                    signalBears[shift] = Bears[shift - 1]
                BullMarket[shift] = EMPTY_VALUE
                BearMarket[shift] = EMPTY_VALUE
                Correction[shift] = EMPTY_VALUE
                BearRally[shift] = EMPTY_VALUE
                Choppy[shift] = EMPTY_VALUE
                Sideways[shift] = EMPTY_VALUE
                if (Bulls[shift] > signalBulls[shift] and Bulls[shift] > Bears[shift]) and (Bears[shift] <= signalBears[shift] or Bears[shift] == 0):
                    BullMarket[shift] = IndicatorValue
                elif (Bears[shift] > signalBears[shift] and Bears[shift] > Bulls[shift]) and (Bulls[shift] <= signalBulls[shift] or Bulls[shift] == 0):
                    BearMarket[shift] = IndicatorValue
                elif (Bulls[shift] < signalBulls[shift] and Bulls[shift] > Bears[shift]) and Bears[shift] >= signalBears[shift]:
                    Correction[shift] = IndicatorValue
                elif (Bears[shift] < signalBears[shift] and Bears[shift] > Bulls[shift]) and Bulls[shift] >= signalBulls[shift]:
                    BearRally[shift] = IndicatorValue
                elif Bears[shift] > signalBears[shift] and Bulls[shift] > signalBulls[shift]:
                    Choppy[shift] = IndicatorValue
                elif (Bears[shift] < signalBears[shift] or Bears[shift] == 0) and (Bulls[shift] < signalBulls[shift] or Bulls[shift] == 0):
                    Sideways[shift] = IndicatorValue
                message = ' ' + Symbol() + ' ' + timeframeToString(tf) + ' '
                if shift == (rates_total - 1) and AlertMode > 0:
                    if ((BullMarket[shift - 1] > 0 and BullMarket[shift - 1] != EMPTY_VALUE) and BullMarket[shift - 2] == EMPTY_VALUE) and Time[0] != prevAlertTime:
                        Alert(message + 'Bull Market Begins!')
                        prevAlertTime = Time[0]
                    if ((BearMarket[shift - 1] > 0 and BearMarket[shift - 1] != EMPTY_VALUE) and BearMarket[shift - 2] == EMPTY_VALUE) and Time[0] != prevAlertTime:
                        Alert(message + 'Bear Market Begins!')
                        prevAlertTime = Time[0]
                    if ((Correction[shift - 1] > 0 and Correction[shift - 1] != EMPTY_VALUE) and Correction[shift - 2] == EMPTY_VALUE) and Time[0] != prevAlertTime:
                        Alert(message + 'Correction Begins!')
                        prevAlertTime = Time[0]
                    if ((BearRally[shift - 1] > 0 and BearRally[shift - 1] != EMPTY_VALUE) and BearRally[shift - 2] == EMPTY_VALUE) and Time[0] != prevAlertTime:
                        Alert(message + 'BearRally  Begins!')
                        prevAlertTime = Time[0]
                    if ((Choppy[shift - 1] > 0 and Choppy[shift - 1] != EMPTY_VALUE) and Choppy[shift - 2] == EMPTY_VALUE) and Time[0] != prevAlertTime:
                        Alert(message + 'Choppy Market Begins!')
                        prevAlertTime = Time[0]
                    if ((Sideways[shift - 1] > 0 and Sideways[shift - 1] != EMPTY_VALUE) and Sideways[shift - 2] == EMPTY_VALUE) and Time[0] != prevAlertTime:
                        Alert(message + 'Sideways Market Begins!')
                        prevAlertTime = Time[0]
        else:
            shift = _range_end(shift, rates_total, 1)
    if ShowTimeFrame:
        timedelta = (Time[0] - Time[1]) * 4
        name = UniqueName + timeframeToString(tf) + ' text '
        ObjectDelete(0, name)
        ObjectCreate(0, name, OBJ_TEXT, window, Time[0] + timedelta, IndicatorValue + 0.1)
        ObjectSetString(0, name, OBJPROP_TEXT, timeframeToString(tf))
        ObjectSetString(0, name, OBJPROP_FONT, FontName)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
        ObjectSetInteger(0, name, OBJPROP_COLOR, TextColor)
    return rates_total

def mAverage(index, mode, array, length, time, bar):
    ma = 0.0
    _sw4 = mode
    if _sw4 == 1:
        ma = EMA(index, array[bar], length, time, bar)
    elif _sw4 == 2:
        ma = EMA(index, array[bar], (2 * length) - 1, time, bar)
    elif _sw4 == 3:
        ma = LWMA(array, length, bar)
    elif _sw4 == 0:
        ma = SMA(array, length, bar)
    return ma

def SMA(array, length, bar):
    i = 0
    sum_ = 0.0
    i = 0
    for i in range(i, length):
        sum_ += array[bar - i]
    else:
        i = _range_end(i, length, 1)
    return _fdiv(sum_, length)

def EMA(index, _price, length, time, bar):
    if ptime[index] < time:
        ema[index][1] = ema[index][0]
        ptime[index] = time
    if ftime[index]:
        ema[index][0] = _price
        ftime[index] = False
    else:
        ema[index][0] = ema[index][1] + (_fdiv(2.0, 1 + length) * (_price - ema[index][1]))
    return ema[index][0]

def LWMA(array, length, bar):
    lwma_ = 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, length):
        weight += length - i
        sum_ += array[bar - i] * (length - i)
    if weight > 0:
        lwma_ = _fdiv(sum_, weight)
    else:
        lwma_ = 0.0
    return lwma_

def priceToString(app_price):
    _sw5 = app_price
    if _sw5 == PRICE_CLOSE:
        return 'Close'
    elif _sw5 == PRICE_HIGH:
        return 'High'
    elif _sw5 == PRICE_LOW:
        return 'Low'
    elif _sw5 == PRICE_MEDIAN:
        return 'Median'
    elif _sw5 == PRICE_OPEN:
        return 'Open'
    elif _sw5 == PRICE_TYPICAL:
        return 'Typical'
    elif _sw5 == PRICE_WEIGHTED:
        return 'Weighted'
    else:
        return ''

def timeframeToString(TF):
    _sw6 = TF
    if _sw6 == PERIOD_CURRENT:
        return 'Current'
    elif _sw6 == PERIOD_M1:
        return 'M1'
    elif _sw6 == PERIOD_M2:
        return 'M2'
    elif _sw6 == PERIOD_M3:
        return 'M3'
    elif _sw6 == PERIOD_M4:
        return 'M4'
    elif _sw6 == PERIOD_M5:
        return 'M5'
    elif _sw6 == PERIOD_M6:
        return 'M6'
    elif _sw6 == PERIOD_M10:
        return 'M10'
    elif _sw6 == PERIOD_M12:
        return 'M12'
    elif _sw6 == PERIOD_M15:
        return 'M15'
    elif _sw6 == PERIOD_M20:
        return 'M20'
    elif _sw6 == PERIOD_M30:
        return 'M30'
    elif _sw6 == PERIOD_H1:
        return 'H1'
    elif _sw6 == PERIOD_H2:
        return 'H2'
    elif _sw6 == PERIOD_H3:
        return 'H3'
    elif _sw6 == PERIOD_H4:
        return 'H4'
    elif _sw6 == PERIOD_H6:
        return 'H6'
    elif _sw6 == PERIOD_H8:
        return 'H8'
    elif _sw6 == PERIOD_H12:
        return 'H12'
    elif _sw6 == PERIOD_D1:
        return 'D1'
    elif _sw6 == PERIOD_W1:
        return 'W1'
    elif _sw6 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'

def iTime_u(symbol, TF, index):
    if index < 0:
        return -1
    if CopyTime(symbol, TF, index, 1, _s_iTime_timearray) > 0:
        return _s_iTime_timearray[0]
    else:
        return -1

def deleteObj(prefix):
    name = ''
    total = ObjectsTotal(0) - 1
    for i in range(total, 0 - 1, -1):
        name = ObjectName(0, i)
        if StringFind(name, prefix) >= 0:
            ObjectDelete(0, name)

# ---- global variables initialised from expressions
TextColor = _input('TextColor', _uint(Black))

# ---- static local variables
_s_iTime_timearray = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AbsolutestrengthmarketV1(_MQL5Indicator):
    name = 'absolutestrengthmarket_v1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'MathMode': _Choice({0: 'RSI', 1: 'Stochastic', 2: 'DMI'}, default=0),  # Math method
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'Length': 10,  # Period of Evaluation
        'PreSmooth': 1,  # Period of PreSmoothing
        'Smooth': 5,  # Period of Smoothing
        'Signal': 5,  # Period of Signal Line
        'MA_Mode': _Choice({0: 'SMA', 1: 'EMA', 2: 'Wilder', 3: 'LWMA'}, default=3),  # Moving Average Mode
        'IndicatorValue': 1.0,  # Indicator Value (ex.1.0)
        'ArrowCode': 167,  # Arrow Code in Wingdings
        'AlertMode': 0,  # Alert Mode: 0-off,1-on
        'ShowName': True,
        'ShowTimeFrame': True,
        'FontSize': 8,
    }
    y_range = (0.0, 2.0)

