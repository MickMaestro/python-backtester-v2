"""2XMA_Ichimoku_Oscillator — converted from MQL5: MQL5 Indicators/2XMA_Ichimoku_Oscillator/2XMA_Ichimoku_Oscillator.mq5

Осциллятор, построенный на разности двух сглаженных, разнопериодных линиях Tenkan-Sen в виде цветной гистограммы
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421376, 14822282, 8421504, 6053069, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: '2Ichimoku XM Oscillator'}, 'levels': [], 'description': ['Осциллятор, построенный на разности двух сглаженных, разнопериодных линиях Tenkan-Sen в виде цветной гистограммы'], 'name': '2XMA_Ichimoku_Oscillator', 'source': 'MQL5 Indicators/2XMA_Ichimoku_Oscillator/2XMA_Ichimoku_Oscillator.mq5', 'folder': '2XMA_Ichimoku_Oscillator', 'inputs': [{'mql': 'Up_period1', 'py': 'Up_period1', 'param': 'Up_period1', 'type': 'uint', 'default': 6, 'label': '1 период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period1', 'py': 'Dn_period1', 'param': 'Dn_period1', 'type': 'uint', 'default': 6, 'label': '1 период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_period2', 'py': 'Up_period2', 'param': 'Up_period2', 'type': 'uint', 'default': 9, 'label': '2 период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period2', 'py': 'Dn_period2', 'param': 'Dn_period2', 'type': 'uint', 'default': 9, 'label': '2 период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_mode1', 'py': 'Up_mode1', 'param': 'Up_mode1', 'type': 'int', 'default': 2, 'label': '1 таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode1', 'py': 'Dn_mode1', 'param': 'Dn_mode1', 'type': 'int', 'default': 1, 'label': '1 таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'Up_mode2', 'py': 'Up_mode2', 'param': 'Up_mode2', 'type': 'int', 'default': 2, 'label': '2 таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode2', 'py': 'Dn_mode2', 'param': 'Dn_mode2', 'type': 'int', 'default': 1, 'label': '2 таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'XMA1_Method', 'py': 'XMA1_Method', 'param': 'XMA1_Method', 'type': 'int', 'default': 0, 'label': '1 метод усреднения', 'sinput': False}, {'mql': 'XMA2_Method', 'py': 'XMA2_Method', 'param': 'XMA2_Method', 'type': 'int', 'default': 0, 'label': '2 метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 25, 'label': '1 глубина сглаживания', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 80, 'label': '2 глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора  по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum MODE_PRICE
OPEN = 0
LOW = 1
HIGH = 2
CLOSE = 3
_enum('MODE_PRICE', {0: 'OPEN', 1: 'LOW', 2: 'HIGH', 3: 'CLOSE'})

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Up_period1 = _input('Up_period1', 6)  # 1 период, используемый для вычисления наивысшего значения цены
Dn_period1 = _input('Dn_period1', 6)  # 1 период, используеммый для вычисления наинизшего значения цены
Up_period2 = _input('Up_period2', 9)  # 2 период, используемый для вычисления наивысшего значения цены
Dn_period2 = _input('Dn_period2', 9)  # 2 период, используеммый для вычисления наинизшего значения цены
Up_mode1 = _input('Up_mode1', HIGH)  # 1 таймсерия для поиска максимумов
Dn_mode1 = _input('Dn_mode1', LOW)  # 1 таймсерия для поиска минимумов
Up_mode2 = _input('Up_mode2', HIGH)  # 2 таймсерия для поиска максимумов
Dn_mode2 = _input('Dn_mode2', LOW)  # 2 таймсерия для поиска минимумов
XMA1_Method = _input('XMA1_Method', MODE_SMA_)  # 1 метод усреднения
XMA2_Method = _input('XMA2_Method', MODE_SMA_)  # 2 метод усреднения
XLength1 = _input('XLength1', 25)  # 1 глубина сглаживания
XLength2 = _input('XLength2', 80)  # 2 глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр усреднения,
Shift = _input('Shift', 0)  # сдвиг индикатора  по горизонтали в барах
ColorBuffer = Arr(0, 0.0)
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
XMA1_Handle = 0
XMA2_Handle = 0

def OnInit():
    global XMA1_Handle, XMA2_Handle, min_rates_total
    XMA = CXMA()
    min_rates_1 = _int(MathMax(Up_period1, Dn_period1))
    min_rates_1 += GetStartBars(XMA1_Method, XLength1, XPhase)
    min_rates_2 = _int(MathMax(Up_period2, Dn_period2))
    min_rates_2 += GetStartBars(XMA2_Method, XLength2, XPhase)
    min_rates_total = MathMax(min_rates_1, min_rates_2)
    XMA1_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XMA_Ichimoku', Up_period1, Dn_period1, Up_mode1, Dn_mode1, XMA1_Method, XLength1, XPhase, 0, 0)
    if XMA1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XMA_Ichimoku 1')
        return INIT_FAILED
    XMA2_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XMA_Ichimoku', Up_period2, Dn_period2, Up_mode2, Dn_mode2, XMA2_Method, XLength2, XPhase, 0, 0)
    if XMA2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XMA_Ichimoku 2')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = '2 Ichimoku XMA Oscillator'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(XMA1_Handle) < rates_total or BarsCalculated(XMA2_Handle) < rates_total) or min_rates_total > rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    XMA1 = Arr(0, 0.0)
    XMA2 = Arr(0, 0.0)
    ArraySetAsSeries(XMA1, True)
    ArraySetAsSeries(XMA2, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
        ColorBuffer[rates_total - 1] = 2.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(XMA1_Handle, 0, 0, to_copy, XMA1) <= 0:
        return 0
    if CopyBuffer(XMA2_Handle, 0, 0, to_copy, XMA2) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer[bar] = _fdiv(XMA1[bar] - XMA2[bar], Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2.0
        bar1 = bar + 1
        if ExtLineBuffer[bar] >= 0:
            if ExtLineBuffer[bar] > ExtLineBuffer[bar1]:
                clr = 0.0
            if ExtLineBuffer[bar] < ExtLineBuffer[bar1]:
                clr = 1.0
            if ExtLineBuffer[bar] == ExtLineBuffer[bar1]:
                clr = ColorBuffer[bar1]
        if ExtLineBuffer[bar] < 0:
            if ExtLineBuffer[bar] < ExtLineBuffer[bar1]:
                clr = 4.0
            if ExtLineBuffer[bar] > ExtLineBuffer[bar1]:
                clr = 3.0
            if ExtLineBuffer[bar] == ExtLineBuffer[bar1]:
                clr = ColorBuffer[bar1]
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2XMAIchimokuOscillator(_MQL5Indicator):
    name = '2XMA_Ichimoku_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Up_period1': 6,  # 1 период, используемый для вычисления наивысшего значения цены
        'Dn_period1': 6,  # 1 период, используеммый для вычисления наинизшего значения цены
        'Up_period2': 9,  # 2 период, используемый для вычисления наивысшего значения цены
        'Dn_period2': 9,  # 2 период, используеммый для вычисления наинизшего значения цены
        'Up_mode1': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # 1 таймсерия для поиска максимумов
        'Dn_mode1': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # 1 таймсерия для поиска минимумов
        'Up_mode2': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # 2 таймсерия для поиска максимумов
        'Dn_mode2': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # 2 таймсерия для поиска минимумов
        'XMA1_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 1 метод усреднения
        'XMA2_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 2 метод усреднения
        'XLength1': 25,  # 1 глубина сглаживания
        'XLength2': 80,  # 2 глубина сглаживания
        'XPhase': 15,  # параметр усреднения,
        'Shift': 0,  # сдвиг индикатора  по горизонтали в барах
    }

