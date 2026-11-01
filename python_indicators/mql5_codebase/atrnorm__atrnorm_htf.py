"""atrnorm — converted from MQL5: MQL5 Indicators/ATRNorm_HTF/atrnorm.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'ATRNorm', 2: 'LeadATRNorm'}, 'levels': [0.25, 0.5, 0.75], 'description': [], 'name': 'atrnorm', 'source': 'MQL5 Indicators/ATRNorm_HTF/atrnorm.mq5', 'folder': 'ATRNorm_HTF', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 12, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'ma', 'py': 'ma', 'param': 'ma', 'type': 'uint', 'default': 12, 'label': 'Период сглаживания', 'sinput': False}, {'mql': 'ValueType', 'py': 'ValueType', 'param': 'ValueType', 'type': 'int', 'default': 0, 'label': 'Тип нормируемого индикатора', 'sinput': False}, {'mql': 'normLimit', 'py': 'normLimit', 'param': 'normLimit', 'type': 'uint', 'default': 24, 'label': 'Период нормирования', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum IndType
ATR = 0
Volume_ = 1
TrueRange = 2
TrueRangeVolume = 3
Log = 4
stdDev = 5
_enum('IndType', {0: 'ATR', 1: 'Volume_', 2: 'TrueRange', 3: 'TrueRangeVolume', 4: 'Log', 5: 'stdDev'})

# ---- inputs and global variables
period = _input('period', 12)  # Период индикатора
ma = _input('ma', 12)  # Период сглаживания
ValueType = _input('ValueType', ATR)  # Тип нормируемого индикатора
normLimit = _input('normLimit', 24)  # Период нормирования
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
AtrBuffer = Arr(0, 0.0)
FlatBuffer = Arr(0, 0.0)
Handle_v = 0
min_rates_total = 0
Count = Arr(0, 0)
SMABuffer = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global Handle_v, min_rates_total
    min_rates_total = _int(MathMax(period + ma + 1, normLimit))
    if ValueType == ATR:
        Handle_v = iATR(None, 0, _int(period))
        if Handle_v == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора!')
    if ValueType == stdDev:
        Handle_v = iStdDev(None, 0, _int(period), 0, MODE_SMA, PRICE_CLOSE)
        if Handle_v == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора!')
    ArrayResize(Count, normLimit)
    ArrayResize(SMABuffer, normLimit)
    ArrayInitialize(Count, 0.0)
    ArrayInitialize(SMABuffer, 0.0)
    SetIndexBuffer(0, AtrBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, FlatBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'ATRNorm(', period, ',', ma, ',', normLimit, ' ', EnumToString(ValueType, 'IndType'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if ValueType == ATR or ValueType == stdDev:
        if BarsCalculated(Handle_v) < rates_total:
            return 0
    first = 0
    bar = 0
    val = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        val = getValue(ValueType, rates_total - 1, high, low, close, tick_volume, volume, bar)
        if ValueType != ATR or ValueType != stdDev:
            SMABuffer[Count[0]] = XMA1.XMASeries(period + 1, prev_calculated, rates_total, MODE_SMA_, 0, period, val, bar, False)
        else:
            SMABuffer[Count[0]] = val
        AtrBuffer[bar] = normValue(SMABuffer, normLimit, Count[0])
        if AtrBuffer[bar] == EMPTY_VALUE:
            return 0
        FlatBuffer[bar] = XMA2.XMASeries(period + 1 + period + normLimit, prev_calculated, rates_total, MODE_SMA_, 0, ma, AtrBuffer[bar], bar, False)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, normLimit)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def normValue(buffer, count, i):
    max_ = buffer[ArrayMaximum(buffer, 0, WHOLE_ARRAY)]
    min_ = buffer[ArrayMinimum(buffer, 0, WHOLE_ARRAY)]
    value = 0.0
    if (max_ - min_) == 0:
        value = 1.0
    else:
        value = _fdiv(buffer[i] - min_, max_ - min_)
    if value > 1:
        value = 1.0
    elif value < 0:
        value = 0.0
    return value

def getValue(valueType, MaxBar, High, Low, Close, TcVolume, Volume, shift):
    Arr_ = Arr(1, 0.0, dyn=False)
    value = 0.0
    _sw1 = valueType
    if _sw1 == ATR:
        if CopyBuffer(Handle_v, 0, MaxBar - shift, 1, Arr_) <= 0:
            return EMPTY_VALUE
        return Arr_[0]
    elif _sw1 == Volume_:
        vol = 0
        if VolumeType == VOLUME_TICK:
            vol = TcVolume[shift]
        else:
            vol = Volume[shift]
        return float(vol)
    elif _sw1 == TrueRange:
        if shift == 1:
            value = High[shift] - Low[shift]
        else:
            value = MathMax(High[shift], High[shift - 1]) - MathMin(Low[shift], Low[shift - 1])
        return value
    elif _sw1 == TrueRangeVolume:
        if shift == 1:
            value = High[shift] - Low[shift]
        else:
            value = MathMax(High[shift], Close[shift - 1]) - MathMin(Low[shift], Close[shift - 1])
        vol = 0
        if VolumeType == VOLUME_TICK:
            vol = TcVolume[shift]
        else:
            vol = Volume[shift]
        return _fdiv(value, Point()) * vol
    elif _sw1 == Log:
        if Close[shift - 1] == 0:
            value = 0.0
        else:
            value = MathLog(_fdiv(MathMax(Close[shift - 1], Close[shift]), MathMin(Close[shift - 1], Close[shift])))
        return value
    elif _sw1 == stdDev:
        if CopyBuffer(Handle_v, 0, MaxBar - shift, 1, Arr_) <= 0:
            return EMPTY_VALUE
        return Arr_[0]
    else:
        return 0.0
    return 0.0

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atrnorm(_MQL5Indicator):
    name = 'atrnorm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 12,  # Период индикатора
        'ma': 12,  # Период сглаживания
        'ValueType': _Choice({0: 'ATR', 1: 'Volume', 2: 'TrueRange', 3: 'TrueRange Volume', 4: 'Log', 5: 'stdDev'}, default=0),  # Тип нормируемого индикатора
        'normLimit': 24,  # Период нормирования
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

