"""absolutestrength_v2 — converted from MQL5: MQL5 Indicators/AbsoluteStrength/absolutestrength_v2.mq5

Copyright: Copyright © 2012, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [16760576], 2: [4678655], 3: [16760576], 4: [4678655], 5: [9470064], 6: [9470064]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 2, 6: 2}, 'labels': {1: 'Bulls', 2: 'Bears', 3: 'Signal Bulls', 4: 'Signal Bears', 5: 'Strength Line', 6: 'Weakness Line'}, 'levels': [], 'description': [], 'name': 'absolutestrength_v2', 'source': 'MQL5 Indicators/AbsoluteStrength/absolutestrength_v2.mq5', 'folder': 'AbsoluteStrength', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MathMode', 'py': 'MathMode', 'param': 'MathMode', 'type': 'int', 'default': 0, 'label': 'Math method', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Period of Evaluation', 'sinput': False}, {'mql': 'PreSmooth', 'py': 'PreSmooth', 'param': 'PreSmooth', 'type': 'int', 'default': 1, 'label': 'Period of PreSmoothing', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 1, 'label': 'Period of Smoothing', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 1, 'label': 'Period of Signal Line', 'sinput': False}, {'mql': 'MA_Mode', 'py': 'MA_Mode', 'param': 'MA_Mode', 'type': 'int', 'default': 1, 'label': 'Moving Average Mode', 'sinput': False}, {'mql': 'LevelsMode', 'py': 'LevelsMode', 'param': 'LevelsMode', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StrengthLevel', 'py': 'StrengthLevel', 'param': 'StrengthLevel', 'type': 'double', 'default': 70.0, 'label': 'Strength Level (ex.70)', 'sinput': False}, {'mql': 'WeaknessLevel', 'py': 'WeaknessLevel', 'param': 'WeaknessLevel', 'type': 'double', 'default': 30.0, 'label': 'Weakness Level (ex.30)', 'sinput': False}, {'mql': 'LookBackPeriod', 'py': 'LookBackPeriod', 'param': 'LookBackPeriod', 'type': 'int', 'default': 30, 'label': 'LookBack Period for LevelsMode=2,3', 'sinput': False}, {'mql': 'UpperMultiplier', 'py': 'UpperMultiplier', 'param': 'UpperMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Upper Band Multiplier for LevelsMode=2', 'sinput': False}, {'mql': 'LowerMultiplier', 'py': 'LowerMultiplier', 'param': 'LowerMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Lower Band Multiplier for LevelsMode=2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MATH_MODE
RSI_method = 0
Stochastic_method = 1
DMI_method = 2
_enum('ENUM_MATH_MODE', {0: 'RSI_method', 1: 'Stochastic_method', 2: 'DMI_method'})

# enum ENUM_LEVELS_MODE
Standard = 0
StdDevBands = 1
HighLowChannel = 2
_enum('ENUM_LEVELS_MODE', {0: 'Standard', 1: 'StdDevBands', 2: 'HighLowChannel'})

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
Smooth = _input('Smooth', 1)  # Period of Smoothing
Signal = _input('Signal', 1)  # Period of Signal Line
MA_Mode = _input('MA_Mode', 1)  # Moving Average Mode
LevelsMode = _input('LevelsMode', 0)
StrengthLevel = _input('StrengthLevel', 70.0)  # Strength Level (ex.70)
WeaknessLevel = _input('WeaknessLevel', 30.0)  # Weakness Level (ex.30)
LookBackPeriod = _input('LookBackPeriod', 30)  # LookBack Period for LevelsMode=2,3
UpperMultiplier = _input('UpperMultiplier', 1.0)  # Upper Band Multiplier for LevelsMode=2
LowerMultiplier = _input('LowerMultiplier', 1.0)  # Lower Band Multiplier for LevelsMode=2
Bulls = Arr(0, 0.0)
Bears = Arr(0, 0.0)
signalBulls = Arr(0, 0.0)
signalBears = Arr(0, 0.0)
strength = Arr(0, 0.0)
weakness = Arr(0, 0.0)
price = Arr(0, 0.0)
loprice = Arr(0, 0.0)
bulls = Arr(0, 0.0)
bears = Arr(0, 0.0)
lbulls = Arr(0, 0.0)
lbears = Arr(0, 0.0)
tf = 0
fLength = 0
Price_handle = 0
Lo_handle = 0
mtf_handle = 0
HiArray = Arr(0, 0.0)
LoArray = Arr(0, 0.0)
ema = Arr(6, 0.0, dyn=False, dims=(2,))
_point = 0.0
mtf_bulls = Arr(1, 0.0, dyn=False)
mtf_bears = Arr(1, 0.0, dyn=False)
mtf_sigbulls = Arr(1, 0.0, dyn=False)
mtf_sigbears = Arr(1, 0.0, dyn=False)
mtf_strength = Arr(1, 0.0, dyn=False)
mtf_weakness = Arr(1, 0.0, dyn=False)
prevtime = 0
ptime = Arr(6, 0, dyn=False)
ftime = Arr(6, False, dyn=False)

def OnInit():
    global Lo_handle, Price_handle, _point, fLength, mtf_handle, tf
    if TimeFrame <= Period():
        tf = Period()
    else:
        tf = TimeFrame
    SetIndexBuffer(0, Bulls, INDICATOR_DATA)
    SetIndexBuffer(1, Bears, INDICATOR_DATA)
    SetIndexBuffer(2, signalBulls, INDICATOR_DATA)
    SetIndexBuffer(3, signalBears, INDICATOR_DATA)
    SetIndexBuffer(4, strength, INDICATOR_DATA)
    SetIndexBuffer(5, weakness, INDICATOR_DATA)
    SetIndexBuffer(6, price, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, loprice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, bulls, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, bears, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, lbulls, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, lbears, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
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
    short_name = 'AbsoluteStrength_v2(' + math_name + ',' + priceToString(Price) + ',' + _str(Length) + ',' + _str(PreSmooth) + ',' + _str(Smooth) + ',' + _str(Signal) + ',' + ma_name + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    fLength = LookBackPeriod
    draw_begin = Length + PreSmooth + Smooth + Signal + fLength
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, draw_begin)
    Price_handle = iMA(None, 0, PreSmooth, 0, MA_Mode, Price)
    if MathMode == 2:
        Lo_handle = iMA(None, 0, PreSmooth, 0, MA_Mode, PRICE_LOW)
    ArrayResize(HiArray, LookBackPeriod)
    ArrayResize(LoArray, LookBackPeriod)
    _point = Point() * MathPow(10, _imod(Digits(), 2))
    if TimeFrame > 0:
        mtf_handle = iCustom(Symbol(), TimeFrame, 'AbsoluteStrength_v2', 0, MathMode, Price, Length, PreSmooth, Smooth, Signal, MA_Mode, LevelsMode, StrengthLevel, WeaknessLevel, LookBackPeriod, UpperMultiplier, LowerMultiplier)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    x = 0
    y = 0
    shift = 0
    limit = 0
    mtflimit = 0
    len_ = 0
    copied = 0
    up = 0.0
    lo = 0.0
    upPivot = 0.0
    dnPivot = 0.0
    mtf_time = 0
    if prev_calculated == 0:
        limit = 0
        mtflimit = rates_total - 1
        ArrayInitialize(Bulls, EMPTY_VALUE)
        ArrayInitialize(Bears, EMPTY_VALUE)
        ArrayInitialize(signalBulls, EMPTY_VALUE)
        ArrayInitialize(signalBears, EMPTY_VALUE)
        ArrayInitialize(strength, 0)
        ArrayInitialize(weakness, 0)
    else:
        limit = prev_calculated - 1
        mtflimit = _idiv(PeriodSeconds(tf), PeriodSeconds(Period()))
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
        ArraySetAsSeries(Time, True)
        shift = 0
        y = 0
        while shift < mtflimit:
            if Time[shift] < iTime_u("", TimeFrame, y):
                y += 1
            mtf_time = iTime_u("", TimeFrame, y)
            x = rates_total - shift - 1
            copied = CopyBuffer(mtf_handle, 0, _DT(mtf_time), _DT(mtf_time), mtf_bulls)
            if copied <= 0:
                return 0
            copied = CopyBuffer(mtf_handle, 1, _DT(mtf_time), _DT(mtf_time), mtf_bears)
            if copied <= 0:
                return 0
            Bulls[x] = mtf_bulls[0]
            Bears[x] = mtf_bears[0]
            if Signal > 1:
                copied = CopyBuffer(mtf_handle, 2, _DT(mtf_time), _DT(mtf_time), mtf_sigbulls)
                if copied <= 0:
                    return 0
                copied = CopyBuffer(mtf_handle, 3, _DT(mtf_time), _DT(mtf_time), mtf_sigbears)
                if copied <= 0:
                    return 0
                signalBulls[x] = mtf_sigbulls[0]
                signalBears[x] = mtf_sigbears[0]
            copied = CopyBuffer(mtf_handle, 4, _DT(mtf_time), _DT(mtf_time), mtf_strength)
            if copied <= 0:
                return 0
            copied = CopyBuffer(mtf_handle, 5, _DT(mtf_time), _DT(mtf_time), mtf_weakness)
            if copied <= 0:
                return 0
            strength[x] = mtf_strength[0]
            weakness[x] = mtf_weakness[0]
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
                if LevelsMode == 0:
                    if StrengthLevel > 0:
                        strength[shift] = (StrengthLevel / 100) * (Bulls[shift] + Bears[shift])
                    if WeaknessLevel > 0:
                        weakness[shift] = (WeaknessLevel / 100) * (Bulls[shift] + Bears[shift])
                elif LevelsMode == 1 and shift > (len_ + Smooth + LookBackPeriod):
                    for j in range(0, LookBackPeriod):
                        HiArray[j] = MathMax(Bulls[shift - j], Bears[shift - j])
                        LoArray[j] = MathMin(Bulls[shift - j], Bears[shift - j])
                    if UpperMultiplier > 0:
                        strength[shift] = SMA(HiArray, LookBackPeriod, LookBackPeriod - 1) + (UpperMultiplier * stdDev(HiArray, LookBackPeriod))
                    if LowerMultiplier > 0:
                        weakness[shift] = SMA(LoArray, LookBackPeriod, LookBackPeriod - 1) - (LowerMultiplier * stdDev(LoArray, LookBackPeriod))
                elif LevelsMode == 2 and shift > (len_ + Smooth + LookBackPeriod):
                    for j in range(0, LookBackPeriod):
                        HiArray[j] = MathMax(Bulls[shift - j], Bears[shift - j])
                        LoArray[j] = MathMin(Bulls[shift - j], Bears[shift - j])
                    upPivot = getPivots(0, HiArray, LookBackPeriod)
                    dnPivot = getPivots(1, LoArray, LookBackPeriod)
                    strength[shift] = upPivot - ((upPivot - dnPivot) * (1 - (StrengthLevel / 100)))
                    weakness[shift] = dnPivot + (((upPivot - dnPivot) * WeaknessLevel) / 100)
        else:
            shift = _range_end(shift, rates_total, 1)
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

def stdDev(array, length):
    i = 0
    avg = 0.0
    i = 0
    for i in range(i, length):
        avg += _fdiv(array[i], length)
    else:
        i = _range_end(i, length, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, length):
        sum_ += MathPow(array[i] - avg, 2)
    else:
        i = _range_end(i, length, 1)
    return MathSqrt(_fdiv(sum_, length))

def getPivots(type_, array, len_):
    i = 0
    max_ = 0.0
    min_ = 100000000.0
    i = 0
    for i in range(i, len_):
        if (type_ == 0 and array[i] > max_) and array[i] < 1000000:
            max_ = array[i]
        if type_ == 1 and array[i] < min_:
            min_ = array[i]
    else:
        i = _range_end(i, len_, 1)
    if type_ == 0:
        return max_
    if type_ == 1:
        return min_
    return 0.0

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

def iTime_u(symbol, TF, index):
    if index < 0:
        return -1
    if CopyTime(symbol, TF, index, 1, _s_iTime_timearray) > 0:
        return _s_iTime_timearray[0]
    else:
        return -1

# ---- static local variables
_s_iTime_timearray = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AbsolutestrengthV2(_MQL5Indicator):
    name = 'absolutestrength_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'MathMode': _Choice({0: 'RSI', 1: 'Stochastic', 2: 'DMI'}, default=0),  # Math method
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'Length': 10,  # Period of Evaluation
        'PreSmooth': 1,  # Period of PreSmoothing
        'Smooth': 1,  # Period of Smoothing
        'Signal': 1,  # Period of Signal Line
        'MA_Mode': _Choice({0: 'SMA', 1: 'EMA', 2: 'Wilder', 3: 'LWMA'}, default=1),  # Moving Average Mode
        'LevelsMode': _Choice({0: 'OverBought/OverSold', 1: 'StdDev Bands', 2: 'High/Low Channel'}, default=0),
        'StrengthLevel': 70.0,  # Strength Level (ex.70)
        'WeaknessLevel': 30.0,  # Weakness Level (ex.30)
        'LookBackPeriod': 30,  # LookBack Period for LevelsMode=2,3
        'UpperMultiplier': 1.0,  # Upper Band Multiplier for LevelsMode=2
        'LowerMultiplier': 1.0,  # Lower Band Multiplier for LevelsMode=2
    }

