"""vkw_bands_modify_candle — converted from MQL5: MQL5 Indicators/VKW_Bands_Modify_Candle/vkw_bands_modify_candle.mq5

Индикатор показывает, где выставлять отложенные ордера
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 17, 2: 1, 3: 1}, 'colors': {1: [255, 8421504, 16711680], 2: [3329330], 3: [16711935]}, 'widths': {2: 1, 3: 1}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'Open;High;Low;Close', 2: 'VKW_Bands Upper', 3: 'VKW_Bands Lower'}, 'levels': [60.0, 40.0], 'description': ['Индикатор показывает, где выставлять отложенные ордера'], 'name': 'vkw_bands_modify_candle', 'source': 'MQL5 Indicators/VKW_Bands_Modify_Candle/vkw_bands_modify_candle.mq5', 'folder': 'VKW_Bands_Modify_Candle', 'inputs': [{'mql': 'PeriodRSI', 'py': 'PeriodRSI', 'param': 'PeriodRSI', 'type': 'uint', 'default': 7, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Быстрый шаг', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 15, 'label': 'Медленный шаг', 'sinput': False}, {'mql': 'IShift', 'py': 'IShift', 'param': 'IShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'RPeriod', 'py': 'RPeriod', 'param': 'RPeriod', 'type': 'uint', 'default': 25, 'label': 'Период поиска для экстремумов', 'sinput': False}, {'mql': 'SmMA_Method', 'py': 'SmMA_Method', 'param': 'SmMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'SLength', 'py': 'SLength', 'param': 'SLength', 'type': 'uint', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'SShift', 'py': 'SShift', 'param': 'SShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
PeriodRSI = _input('PeriodRSI', 7)  # Период индикатора
StepSizeFast = _input('StepSizeFast', 5)  # Быстрый шаг
StepSizeSlow = _input('StepSizeSlow', 15)  # Медленный шаг
IShift = _input('IShift', 0)  # Сдвиг индикатора по горизонтали в барах
RPeriod = _input('RPeriod', 25)  # Период поиска для экстремумов
SmMA_Method = _input('SmMA_Method', MODE_SMA)  # Метод сглаживания
SLength = _input('SLength', 3)  # Глубина сглаживания
SPhase = _input('SPhase', 100)  # Параметр сглаживания
SShift = _input('SShift', 0)  # Сдвиг индикатора канала по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
Ind_Handle = Arr(4, 0, dyn=False)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(PeriodRSI)
    min_rates_1 += _int(RPeriod)
    min_rates_total = min_rates_1 + GetStartBars(SmMA_Method, SLength, SPhase)
    Ind_Handle[0] = iCustom(None, 0, 'METRO', PeriodRSI, StepSizeFast, StepSizeSlow, 0, PRICE_OPEN)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора METRO[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'METRO', PeriodRSI, StepSizeFast, StepSizeSlow, 0, PRICE_HIGH)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора METRO[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'METRO', PeriodRSI, StepSizeFast, StepSizeSlow, 0, PRICE_LOW)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора METRO[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'METRO', PeriodRSI, StepSizeFast, StepSizeSlow, 0, PRICE_CLOSE)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора METRO[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, IShift)
    SetIndexBuffer(5, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(6, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(DnIndBuffer, True)
    shortname = 'VKW_Bands_METRO_Candle'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    d_max = 0.0
    d_min = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    maxbar = 0
    maxbar = rates_total - 1 - min_rates_1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1 + _int(RPeriod)
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        d_max = ExtHighBuffer[ArrayMaximum(ExtHighBuffer, bar, RPeriod)]
        d_min = ExtLowBuffer[ArrayMinimum(ExtLowBuffer, bar, RPeriod)]
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


class VkwBandsModifyCandle(_MQL5Indicator):
    name = 'vkw_bands_modify_candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodRSI': 7,  # Период индикатора
        'StepSizeFast': 5,  # Быстрый шаг
        'StepSizeSlow': 15,  # Медленный шаг
        'IShift': 0,  # Сдвиг индикатора по горизонтали в барах
        'RPeriod': 25,  # Период поиска для экстремумов
        'SmMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'SLength': 3,  # Глубина сглаживания
        'SPhase': 100,  # Параметр сглаживания
        'SShift': 0,  # Сдвиг индикатора канала по горизонтали в барах
    }

