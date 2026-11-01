"""vkw_bands_modify — converted from MQL5: MQL5 Indicators/VKW_Bands_Modify_HTF/vkw_bands_modify.mq5

Индикатор показывает, где выставлять отложенные ордера
Когда синяя линия пересекает салатовую или розовую и отходит обратно, тогда следует выставлять отложенный ордер
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [3329330], 3: [9639167]}, 'widths': {1: 2, 2: 3, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'METRO', 2: 'VKW_Bands Upper', 3: 'VKW_Bands Lower'}, 'levels': [60.0, 40.0], 'description': ['Индикатор показывает, где выставлять отложенные ордера', 'Когда синяя линия пересекает салатовую или розовую и отходит обратно, тогда следует выставлять отложенный ордер'], 'name': 'vkw_bands_modify', 'source': 'MQL5 Indicators/VKW_Bands_Modify_HTF/vkw_bands_modify.mq5', 'folder': 'VKW_Bands_Modify_HTF', 'inputs': [{'mql': 'PeriodRSI', 'py': 'PeriodRSI', 'param': 'PeriodRSI', 'type': 'uint', 'default': 7, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Быстрый шаг', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 15, 'label': 'Медленный шаг', 'sinput': False}, {'mql': 'IShift', 'py': 'IShift', 'param': 'IShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены или handle', 'sinput': False}, {'mql': 'RPeriod', 'py': 'RPeriod', 'param': 'RPeriod', 'type': 'uint', 'default': 25, 'label': 'Период поиска для экстремумов', 'sinput': False}, {'mql': 'SmMA_Method', 'py': 'SmMA_Method', 'param': 'SmMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'SLength', 'py': 'SLength', 'param': 'SLength', 'type': 'uint', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'SShift', 'py': 'SShift', 'param': 'SShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
PeriodRSI = _input('PeriodRSI', 7)  # Период индикатора
StepSizeFast = _input('StepSizeFast', 5)  # Быстрый шаг
StepSizeSlow = _input('StepSizeSlow', 15)  # Медленный шаг
IShift = _input('IShift', 0)  # Сдвиг индикатора по горизонтали в барах
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Тип цены или handle
RPeriod = _input('RPeriod', 25)  # Период поиска для экстремумов
SmMA_Method = _input('SmMA_Method', MODE_SMA)  # Метод сглаживания
SLength = _input('SLength', 3)  # Глубина сглаживания
SPhase = _input('SPhase', 100)  # Параметр сглаживания
SShift = _input('SShift', 0)  # Сдвиг индикатора канала по горизонтали в барах
IndBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(PeriodRSI)
    min_rates_1 += _int(RPeriod)
    min_rates_total = min_rates_1 + GetStartBars(SmMA_Method, SLength, SPhase)
    Ind_Handle = iCustom(None, 0, 'METRO', PeriodRSI, StepSizeFast, StepSizeSlow, 0, Applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора METRO')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, IShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(2, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(DnIndBuffer, True)
    shortname = 'VKW_Bands_METRO'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    d_max = 0.0
    d_min = 0.0
    InputInd = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    maxbar = 0
    maxbar = rates_total - 1 - min_rates_1
    ArraySetAsSeries(InputInd, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1 + _int(RPeriod)
    if CopyBuffer(Ind_Handle, 1, 0, to_copy, InputInd) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        d_max = InputInd[ArrayMaximum(InputInd, bar, RPeriod)]
        d_min = InputInd[ArrayMinimum(InputInd, bar, RPeriod)]
        IndBuffer[bar] = InputInd[bar]
        UpIndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, SmMA_Method, SPhase, SLength, d_max, bar, True)
        DnIndBuffer[bar] = XMA2.XMASeries(maxbar, prev_calculated, rates_total, SmMA_Method, SPhase, SLength, d_min, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VkwBandsModify(_MQL5Indicator):
    name = 'vkw_bands_modify'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodRSI': 7,  # Период индикатора
        'StepSizeFast': 5,  # Быстрый шаг
        'StepSizeSlow': 15,  # Медленный шаг
        'IShift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены или handle
        'RPeriod': 25,  # Период поиска для экстремумов
        'SmMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'SLength': 3,  # Глубина сглаживания
        'SPhase': 100,  # Параметр сглаживания
        'SShift': 0,  # Сдвиг индикатора канала по горизонтали в барах
    }

