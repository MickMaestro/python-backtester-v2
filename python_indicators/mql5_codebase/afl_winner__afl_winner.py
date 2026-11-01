"""afl_winner — converted from MQL5: MQL5 Indicators/AFL_Winner/afl_winner.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_maximum': 60.0, 'indicator_minimum': -60.0}, 'types': {1: 11}, 'colors': {1: [16711935, 14822282]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AFL_Winner'}, 'levels': [50.0, 0.0, -50.0], 'description': [], 'name': 'afl_winner', 'source': 'MQL5 Indicators/AFL_Winner/afl_winner.mq5', 'folder': 'AFL_Winner', 'inputs': [{'mql': 'iAverage', 'py': 'iAverage', 'param': 'iAverage', 'type': 'uint', 'default': 5, 'label': 'Период для обработки входных данных', 'sinput': False}, {'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'iMA_Method', 'py': 'iMA_Method', 'param': 'iMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'iLength', 'py': 'iLength', 'param': 'iLength', 'type': 'uint', 'default': 5, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'iPhase', 'py': 'iPhase', 'param': 'iPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 7, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объем', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
iAverage = _input('iAverage', 5)  # Период для обработки входных данных
iPeriod = _input('iPeriod', 10)  # Период поиска экстремумов
iMA_Method = _input('iMA_Method', MODE_SMA)  # Метод усреднения первого сглаживания
iLength = _input('iLength', 5)  # Глубина  сглаживания
iPhase = _input('iPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_WEIGHTED)  # Ценовая константа
VolumeType = _input('VolumeType', VOLUME_TICK)  # объем
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Count1 = Arr(0, 0)
Count2 = Arr(0, 0)
Value = Arr(0, 0.0)
Price = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0

def Recount_ArrayZeroPos1(CoArr, Size):
    global _s_Recount_ArrayZeroPos1_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos1_count -= 1
    if _s_Recount_ArrayZeroPos1_count < 0:
        _s_Recount_ArrayZeroPos1_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos1_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Recount_ArrayZeroPos2(CoArr, Size):
    global _s_Recount_ArrayZeroPos2_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos2_count -= 1
    if _s_Recount_ArrayZeroPos2_count < 0:
        _s_Recount_ArrayZeroPos2_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos2_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = _int(iAverage)
    min_rates_2 = min_rates_1 + _int(iPeriod)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(iMA_Method, iLength, iPhase)
    min_rates_total = min_rates_3 + XMA1.GetStartBars(iMA_Method, iLength, iPhase)
    XMA1.XMALengthCheck('Length', iLength)
    XMA1.XMAPhaseCheck('Phase', iPhase, iMA_Method)
    ArrayResize(Count1, iPeriod)
    ArrayResize(Value, iPeriod)
    ArrayResize(Count2, iAverage)
    ArrayResize(Price, iAverage)
    ArrayInitialize(Count1, 0)
    ArrayInitialize(Value, 0.0)
    ArrayInitialize(Count2, 0)
    ArrayInitialize(Price, 0.0)
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'AFL_Winner'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    rsv = 0.0
    scost5 = 0.0
    max_ = 0.0
    min_ = 0.0
    x1xma = 0.0
    x2xma = 0.0
    first = 0
    bar = 0
    svolume5 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Price[Count2[0]] = PriceSeries(IPC, bar, open, low, high, close)
        if bar < (min_rates_1 - 1):
            if bar < (rates_total - 1):
                Recount_ArrayZeroPos2(Count2, iAverage)
            continue
        scost5 = 0.0
        svolume5 = 0
        for kkk in range(0, _int(iAverage)):
            res = 0
            if VolumeType == VOLUME_TICK:
                res = tick_volume[bar - kkk]
            else:
                res = volume[bar - kkk]
            scost5 += res * Price[Count2[kkk]]
            svolume5 += res
        svolume5 = MathMax(svolume5, 1)
        Value[Count1[0]] = _fdiv(scost5, svolume5)
        if bar < (min_rates_2 - 1):
            if bar < (rates_total - 1):
                Recount_ArrayZeroPos1(Count1, iPeriod)
                Recount_ArrayZeroPos2(Count2, iAverage)
            continue
        max_ = Value[ArrayMaximum(Value, 0, iPeriod)]
        min_ = Value[ArrayMinimum(Value, 0, iPeriod)]
        rsv = (_fdiv(Value[Count1[0]] - min_, MathMax(max_ - min_, Point())) * 100) - 50
        x1xma = XMA1.XMASeries(min_rates_2, prev_calculated, rates_total, iMA_Method, iPhase, iLength, rsv, bar, False)
        x2xma = XMA2.XMASeries(min_rates_3, prev_calculated, rates_total, iMA_Method, iPhase, iLength, x1xma, bar, False)
        if x1xma > x2xma:
            UpIndBuffer[bar] = x1xma
            DnIndBuffer[bar] = x2xma
            ColorIndBuffer[bar] = 1.0
        else:
            UpIndBuffer[bar] = x2xma
            DnIndBuffer[bar] = x1xma
            ColorIndBuffer[bar] = 0.0
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos1(Count1, iPeriod)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos2(Count2, iAverage)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos1_count = 1
_s_Recount_ArrayZeroPos2_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AflWinner(_MQL5Indicator):
    name = 'afl_winner'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iAverage': 5,  # Период для обработки входных данных
        'iPeriod': 10,  # Период поиска экстремумов
        'iMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения первого сглаживания
        'iLength': 5,  # Глубина  сглаживания
        'iPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # Ценовая константа
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объем
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (-60.0, 60.0)

