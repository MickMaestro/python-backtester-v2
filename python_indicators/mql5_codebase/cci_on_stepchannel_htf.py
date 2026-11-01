"""cci_on_stepchannel_htf — converted from MQL5: MQL5 Indicators/CCI_On_StepChannel_HTF/cci_on_stepchannel_htf.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [2330219, 16748574, 8421504, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [100.0, 0.0, -100.0], 'description': [], 'name': 'cci_on_stepchannel_htf', 'source': 'MQL5 Indicators/CCI_On_StepChannel_HTF/cci_on_stepchannel_htf.mq5', 'folder': 'CCI_On_StepChannel_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Количество подаваемых алертов', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для сигнала, 0-текущий бар', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'период CCI', 'sinput': False}, {'mql': 'MA_Method0', 'py': 'MA_Method0', 'param': 'MA_Method0', 'type': 'int', 'default': 0, 'label': 'Метод усреднения таймсерий', 'sinput': False}, {'mql': 'Length0', 'py': 'Length0', 'param': 'Length0', 'type': 'int', 'default': 3, 'label': 'Глубина усреднения таймсерий', 'sinput': False}, {'mql': 'Phase0', 'py': 'Phase0', 'param': 'Phase0', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения таймсерий', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 2, 'label': 'Метод усреднения скользящей средней', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 10, 'label': 'Глубина усреднения скользящей средней', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения скользящей средней', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания стандартного отклонения', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 70, 'label': 'Глубина сглаживания стандартного отклонения', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания стандартного отклонения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MA_Method3', 'py': 'MA_Method3', 'param': 'MA_Method3', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания канала', 'sinput': False}, {'mql': 'Length3', 'py': 'Length3', 'param': 'Length3', 'type': 'int', 'default': 3, 'label': 'Глубина сглаживания канала', 'sinput': False}, {'mql': 'Phase3', 'py': 'Phase3', 'param': 'Phase3', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания канала', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 2, 'label': 'Вариант алгоритма', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum MODE
ENAM_SIMPLE = 1
ENAM_HIBRID = 2
_enum('MODE', {1: 'ENAM_SIMPLE', 2: 'ENAM_HIBRID'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
AlertCount = _input('AlertCount', 0)  # Количество подаваемых алертов
SignalBar = _input('SignalBar', 1)  # Номер бара для сигнала, 0-текущий бар
CCIPeriod = _input('CCIPeriod', 14)  # период CCI
MA_Method0 = _input('MA_Method0', MODE_SMA)  # Метод усреднения таймсерий
Length0 = _input('Length0', 3)  # Глубина усреднения таймсерий
Phase0 = _input('Phase0', 15)  # Параметр усреднения таймсерий
MA_Method1 = _input('MA_Method1', MODE_SMMA)  # Метод усреднения скользящей средней
Length1 = _input('Length1', 10)  # Глубина усреднения скользящей средней
Phase1 = _input('Phase1', 15)  # Параметр усреднения скользящей средней
MA_Method2 = _input('MA_Method2', MODE_SMA)  # Метод сглаживания стандартного отклонения
Length2 = _input('Length2', 70)  # Глубина сглаживания стандартного отклонения
Phase2 = _input('Phase2', 100)  # Параметр сглаживания стандартного отклонения
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
MA_Method3 = _input('MA_Method3', MODE_SMA)  # Метод сглаживания канала
Length3 = _input('Length3', 3)  # Глубина сглаживания канала
Phase3 = _input('Phase3', 100)  # Параметр сглаживания канала
BandsDeviation = _input('BandsDeviation', 2.0)  # Девиация
Mode = _input('Mode', ENAM_HIBRID)  # Вариант алгоритма
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора CCI_On_StepChannel не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'CCI_On_StepChannel' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'CCI_On_StepChannel', CCIPeriod, MA_Method0, Length0, Phase0, MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, IPC, MA_Method3, Length3, Phase3, BandsDeviation, Mode, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CCI_On_StepChannel')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'CCI_On_StepChannel', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_DnCount_, _s_OnCalculate_LastCountBar, _s_OnCalculate_UpCount, _s_OnCalculate_UpCount_
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    Ind = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    IndTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer[bar] = Ind[0]
            ColorIndBuffer[bar] = Col[0]
        else:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
        _s_OnCalculate_UpCount_ = 0
        _s_OnCalculate_DnCount_ = 0
    if (_s_OnCalculate_UpCount < AlertCount and ColorIndBuffer[SignalBar + 1] > 2) and ColorIndBuffer[SignalBar] < 2:
        _s_OnCalculate_UpCount += 1
        Alert(Word + ': Сигнал на покупку по ' + Symbol_)
    if (_s_OnCalculate_DnCount < AlertCount and ColorIndBuffer[SignalBar + 1] < 2) and ColorIndBuffer[SignalBar] > 2:
        _s_OnCalculate_DnCount += 1
        Alert(Word + ': Сигнал на продажу по ' + Symbol_)
    return rates_total

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0
_s_OnCalculate_UpCount_ = 0
_s_OnCalculate_DnCount_ = 0
_s_OnCalculate_LastInd = 0.0
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciOnStepchannelHtf(_MQL5Indicator):
    name = 'cci_on_stepchannel_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'AlertCount': 0,  # Количество подаваемых алертов
        'SignalBar': 1,  # Номер бара для сигнала, 0-текущий бар
        'CCIPeriod': 14,  # период CCI
        'MA_Method0': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения таймсерий
        'Length0': 3,  # Глубина усреднения таймсерий
        'Phase0': 15,  # Параметр усреднения таймсерий
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=2),  # Метод усреднения скользящей средней
        'Length1': 10,  # Глубина усреднения скользящей средней
        'Phase1': 15,  # Параметр усреднения скользящей средней
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания стандартного отклонения
        'Length2': 70,  # Глубина сглаживания стандартного отклонения
        'Phase2': 100,  # Параметр сглаживания стандартного отклонения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'MA_Method3': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания канала
        'Length3': 3,  # Глубина сглаживания канала
        'Phase3': 100,  # Параметр сглаживания канала
        'BandsDeviation': 2.0,  # Девиация
        'Mode': _Choice({1: 'Simple Mode', 2: 'hybrid Mode'}, default=2),  # Вариант алгоритма
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

