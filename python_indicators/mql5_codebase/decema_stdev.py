"""decema_stdev — converted from MQL5: MQL5 Indicators/DecEMA_StDev/decema_stdev.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 8, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [11823615, 8421504, 15570276], 2: [16711935], 3: [8388352], 4: [16711935], 5: [8388352]}, 'widths': {1: 3, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0}, 'labels': {1: 'DecEMA', 2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': [], 'name': 'decema_stdev', 'source': 'MQL5 Indicators/DecEMA_StDev/decema_stdev.mq5', 'folder': 'DecEMA_StDev', 'inputs': [{'mql': 'EMA_Period', 'py': 'EMA_Period', 'param': 'EMA_Period', 'type': 'uint', 'default': 3, 'label': 'Период EMA', 'sinput': False}, {'mql': 'ELength', 'py': 'ELength', 'param': 'ELength', 'type': 'int', 'default': 15, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг Фатла по вертикали в пунктах', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'Коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'Коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
EMA_Period = _input('EMA_Period', 3)  # Период EMA
ELength = _input('ELength', 15)  # Глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
PriceShift = _input('PriceShift', 0)  # Сдвиг Фатла по вертикали в пунктах
dK1 = _input('dK1', 1.5)  # Коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # Коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
min_rates_total = 0
alfa = 0.0
dPriceShift = 0.0
dDecEMA = Arr(0, 0.0)

def OnInit():
    global alfa, dPriceShift, min_rates_total
    min_rates_total = 2 + _int(std_period)
    alfa = _fdiv(2.0, 1.0 + ELength)
    dPriceShift = Point() * PriceShift
    ArrayResize(dDecEMA, std_period)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DecEMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BearsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BullsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, BearsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, BullsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'DecEMA(', EMA_Period, ',', ELength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_sdEMA1, _s_OnCalculate_sdEMA10, _s_OnCalculate_sdEMA2, _s_OnCalculate_sdEMA3, _s_OnCalculate_sdEMA4, _s_OnCalculate_sdEMA5, _s_OnCalculate_sdEMA6, _s_OnCalculate_sdEMA7, _s_OnCalculate_sdEMA8, _s_OnCalculate_sdEMA9
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    maxbar = 0
    price = 0.0
    EMA0 = 0.0
    EMA1 = 0.0
    EMA2 = 0.0
    EMA3 = 0.0
    EMA4 = 0.0
    EMA5 = 0.0
    EMA6 = 0.0
    EMA7 = 0.0
    EMA8 = 0.0
    EMA9 = 0.0
    EMA10 = 0.0
    decema = 0.0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS1 = 0.0
    BULLS1 = 0.0
    BEARS2 = 0.0
    BULLS2 = 0.0
    Filter1 = 0.0
    Filter2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_sdEMA1 = PriceSeries(IPC, first - 1, open, low, high, close)
        _s_OnCalculate_sdEMA2 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA3 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA4 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA5 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA6 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA7 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA8 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA9 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA10 = _s_OnCalculate_sdEMA1
    else:
        first = prev_calculated - 1
    EMA1 = _s_OnCalculate_sdEMA1
    EMA2 = _s_OnCalculate_sdEMA2
    EMA3 = _s_OnCalculate_sdEMA3
    EMA4 = _s_OnCalculate_sdEMA4
    EMA5 = _s_OnCalculate_sdEMA5
    EMA6 = _s_OnCalculate_sdEMA6
    EMA7 = _s_OnCalculate_sdEMA7
    EMA8 = _s_OnCalculate_sdEMA8
    EMA9 = _s_OnCalculate_sdEMA9
    EMA10 = _s_OnCalculate_sdEMA10
    maxbar = rates_total - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        EMA0 = XMA1.XMASeries(1, prev_calculated, rates_total, 1, 0, EMA_Period, price, bar, False)
        EMA1 = (alfa * EMA0) + ((1 - alfa) * EMA1)
        EMA2 = (alfa * EMA1) + ((1 - alfa) * EMA2)
        EMA3 = (alfa * EMA2) + ((1 - alfa) * EMA3)
        EMA4 = (alfa * EMA3) + ((1 - alfa) * EMA4)
        EMA5 = (alfa * EMA4) + ((1 - alfa) * EMA5)
        EMA6 = (alfa * EMA5) + ((1 - alfa) * EMA6)
        EMA7 = (alfa * EMA6) + ((1 - alfa) * EMA7)
        EMA8 = (alfa * EMA7) + ((1 - alfa) * EMA8)
        EMA9 = (alfa * EMA8) + ((1 - alfa) * EMA9)
        EMA10 = (alfa * EMA9) + ((1 - alfa) * EMA10)
        ExtLineBuffer[bar] = (10 * EMA1) - (45 * EMA2) + (120 * EMA3) - (210 * EMA4) + (252 * EMA5) - (210 * EMA6) + (120 * EMA7) - (45 * EMA8) + (10 * EMA9) - EMA10
        ExtLineBuffer[bar] += dPriceShift
        if bar < maxbar:
            _s_OnCalculate_sdEMA1 = EMA1
            _s_OnCalculate_sdEMA2 = EMA2
            _s_OnCalculate_sdEMA3 = EMA3
            _s_OnCalculate_sdEMA4 = EMA4
            _s_OnCalculate_sdEMA5 = EMA5
            _s_OnCalculate_sdEMA6 = EMA6
            _s_OnCalculate_sdEMA7 = EMA7
            _s_OnCalculate_sdEMA8 = EMA8
            _s_OnCalculate_sdEMA9 = EMA9
            _s_OnCalculate_sdEMA10 = EMA10
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        if ExtLineBuffer[bar - 1] < ExtLineBuffer[bar]:
            clr = 2
        if ExtLineBuffer[bar - 1] > ExtLineBuffer[bar]:
            clr = 0
        ColorExtLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dDecEMA[iii] = ExtLineBuffer[bar - iii] - ExtLineBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dDecEMA[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dDecEMA[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dDecEMA[0], Digits() + 2)
        Filter1 = NormalizeDouble(dK1 * StDev, Digits() + 2)
        Filter2 = NormalizeDouble(dK2 * StDev, Digits() + 2)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        decema = ExtLineBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = decema
        if dstd < (-Filter2):
            BEARS2 = decema
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = decema
        if dstd > Filter2:
            BULLS2 = decema
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_sdEMA1 = 0.0
_s_OnCalculate_sdEMA2 = 0.0
_s_OnCalculate_sdEMA3 = 0.0
_s_OnCalculate_sdEMA4 = 0.0
_s_OnCalculate_sdEMA5 = 0.0
_s_OnCalculate_sdEMA6 = 0.0
_s_OnCalculate_sdEMA7 = 0.0
_s_OnCalculate_sdEMA8 = 0.0
_s_OnCalculate_sdEMA9 = 0.0
_s_OnCalculate_sdEMA10 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DecemaStdev(_MQL5Indicator):
    name = 'decema_stdev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EMA_Period': 3,  # Период EMA
        'ELength': 15,  # Глубина сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'PriceShift': 0,  # Сдвиг Фатла по вертикали в пунктах
        'dK1': 1.5,  # Коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # Коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

