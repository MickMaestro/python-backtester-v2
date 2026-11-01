"""XStdDevSpeed — converted from MQL5: MQL5 Indicators/XStdDevSpeed/XStdDevSpeed.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [55295, 8421504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XStdDevSpeed'}, 'levels': [], 'description': [], 'name': 'XStdDevSpeed', 'source': 'MQL5 Indicators/XStdDevSpeed/XStdDevSpeed.mq5', 'folder': 'XStdDevSpeed', 'inputs': [{'mql': 'Std_Method', 'py': 'Std_Method', 'param': 'Std_Method', 'type': 'int', 'default': 0, 'label': 'Тип Std усреднения', 'sinput': False}, {'mql': 'Std_Period', 'py': 'Std_Period', 'param': 'Std_Period', 'type': 'uint', 'default': 20, 'label': 'Период Std', 'sinput': False}, {'mql': 'Std_applied_price', 'py': 'Std_applied_price', 'param': 'Std_applied_price', 'type': 'int', 'default': 1, 'label': 'тип цены', 'sinput': False}, {'mql': 'SpeedBars', 'py': 'SpeedBars', 'param': 'SpeedBars', 'type': 'uint', 'default': 5, 'label': 'Количество баров для определения скорости', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения сглаживания', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Std_Method = _input('Std_Method', MODE_SMA)  # Тип Std усреднения
Std_Period = _input('Std_Period', 20)  # Период Std
Std_applied_price = _input('Std_applied_price', PRICE_CLOSE)  # тип цены
SpeedBars = _input('SpeedBars', 5)  # Количество баров для определения скорости
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод усреднения сглаживания
MA_Length = _input('MA_Length', 5)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = _int(Std_Period)
    min_rates_2 = min_rates_1 + _int(SpeedBars)
    min_rates_total = min_rates_2 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    Ind_Handle = iStdDev(Symbol(), None, Std_Period, 0, Std_Method, Std_applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStdDev')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XStdDevSpeed')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    speed = 0.0
    STD = Arr(0, 0.0)
    limit = 0
    bar = 0
    to_copy = 0
    maxbar1 = 0
    maxbar2 = 0
    maxbar1 = rates_total - min_rates_1
    maxbar2 = rates_total - min_rates_2
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(STD, True)
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, STD) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        speed = Mom.MomentumSeries(maxbar1, prev_calculated, rates_total, SpeedBars, STD[bar], bar, True)
        IndBuffer[bar] = XMA1.XMASeries(maxbar2, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, speed, bar, True)
        if IndBuffer[bar] >= 0:
            ColorIndBuffer[bar] = 0.0
        else:
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
Mom = _alloc(CMomentum)
Mom.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XStdDevSpeed(_MQL5Indicator):
    name = 'XStdDevSpeed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Std_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Тип Std усреднения
        'Std_Period': 20,  # Период Std
        'Std_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # тип цены
        'SpeedBars': 5,  # Количество баров для определения скорости
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения сглаживания
        'MA_Length': 5,  # Глубина сглаживания
        'MA_Phase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

