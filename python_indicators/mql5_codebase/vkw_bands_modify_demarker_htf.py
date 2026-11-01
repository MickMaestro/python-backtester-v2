"""vkw_bands_modify_demarker_htf — converted from MQL5: MQL5 Indicators/VKW_Bands_Modify_DeMarker_HTF/vkw_bands_modify_demarker_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [10061943], 2: [13422920], 3: [255]}, 'widths': {1: 2, 2: 4, 3: 4}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'METRO_DeMarker', 2: 'VKW_Bands Upper', 3: 'VKW_Bands Lower'}, 'levels': [60.0, 40.0], 'description': [], 'name': 'vkw_bands_modify_demarker_htf', 'source': 'MQL5 Indicators/VKW_Bands_Modify_DeMarker_HTF/vkw_bands_modify_demarker_htf.mq5', 'folder': 'VKW_Bands_Modify_DeMarker_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'PeriodDeMarker', 'py': 'PeriodDeMarker', 'param': 'PeriodDeMarker', 'type': 'uint', 'default': 7, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Быстрый шаг', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 15, 'label': 'Медленный шаг', 'sinput': False}, {'mql': 'IShift', 'py': 'IShift', 'param': 'IShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены или handle', 'sinput': False}, {'mql': 'RPeriod', 'py': 'RPeriod', 'param': 'RPeriod', 'type': 'uint', 'default': 25, 'label': 'Период поиска для экстремумов', 'sinput': False}, {'mql': 'SmMA_Method', 'py': 'SmMA_Method', 'param': 'SmMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'SLength', 'py': 'SLength', 'param': 'SLength', 'type': 'uint', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'SShift', 'py': 'SShift', 'param': 'SShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
PeriodDeMarker = _input('PeriodDeMarker', 7)  # Период индикатора
StepSizeFast = _input('StepSizeFast', 5)  # Быстрый шаг
StepSizeSlow = _input('StepSizeSlow', 15)  # Медленный шаг
IShift = _input('IShift', 0)  # Сдвиг индикатора по горизонтали в барах
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Тип цены или handle
RPeriod = _input('RPeriod', 25)  # Период поиска для экстремумов
SmMA_Method = _input('SmMA_Method', MODE_SMA)  # Метод сглаживания
SLength = _input('SLength', 3)  # Глубина сглаживания
SPhase = _input('SPhase', 100)  # Параметр сглаживания
SShift = _input('SShift', 0)  # Сдвиг индикатора канала по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора VKW_Bands_Modify_DeMarker не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'VKW_Bands_Modify_DeMarker' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'VKW_Bands_Modify_DeMarker', PeriodDeMarker, StepSizeFast, StepSizeSlow, 0, Applied_price, RPeriod, SmMA_Method, SLength, SPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора VKW_Bands_Modify_DeMarker')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, IShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, SShift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer2, True)
    SetIndexBuffer(2, IndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, SShift)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer3, True)
    shortname = Box("")
    StringConcatenate(shortname, 'VKW_Bands_Modify_DeMarker(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 1, IndBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 2, IndBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VkwBandsModifyDemarkerHtf(_MQL5Indicator):
    name = 'vkw_bands_modify_demarker_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'PeriodDeMarker': 7,  # Период индикатора
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

