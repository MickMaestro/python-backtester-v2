"""dots_htf — converted from MQL5: MQL5 Indicators/Dots_HTF/dots_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711680, 255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Dots'}, 'levels': [], 'description': [], 'name': 'dots_htf', 'source': 'MQL5 Indicators/Dots_HTF/dots_htf.mq5', 'folder': 'Dots_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Количество подаваемых алертов', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для сигнала, 0-текущий бар', 'sinput': False}, {'mql': 'Repeat', 'py': 'Repeat', 'param': 'Repeat', 'type': 'bool', 'default': True, 'label': 'Повтор значений на следующих барах', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 0, 'label': 'Параметр, позволяющий фильтровать всплески цен без добавления задержек в отображение', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
AlertCount = _input('AlertCount', 0)  # Количество подаваемых алертов
SignalBar = _input('SignalBar', 1)  # Номер бара для сигнала, 0-текущий бар
Repeat = _input('Repeat', True)  # Повтор значений на следующих барах
Length = _input('Length', 10)  # Глубина сглаживания
Filter = _input('Filter', 0)  # Параметр, позволяющий фильтровать всплески цен без добавления задержек в отображение
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Dots_Handle = 0

def OnInit():
    global Dots_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора Dots не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'Dots' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Dots_Handle = iCustom(Symbol_, TimeFrame, 'Dots', Length, Filter, IPC, PriceShift, 0)
    if Dots_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Dots')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dots')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_DnCount_, _s_OnCalculate_LastCountBar, _s_OnCalculate_UpCount, _s_OnCalculate_UpCount_
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Dots_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    Dots = Arr(1, 0.0, dyn=False)
    CLR = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    DotsTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 0.0
        ColorIndBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, DotsTime) <= 0:
            return 0
        if time[bar] >= DotsTime[0] and time[bar + 1] < DotsTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Dots_Handle, 0, _DT(time[bar]), 1, Dots) <= 0:
                return 0
            if CopyBuffer(Dots_Handle, 1, _DT(time[bar]), 1, CLR) <= 0:
                return 0
            IndBuffer[bar] = Dots[0]
            ColorIndBuffer[bar] = CLR[0]
        elif Repeat:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
        _s_OnCalculate_UpCount_ = 0
        _s_OnCalculate_DnCount_ = 0
    if _s_OnCalculate_UpCount < AlertCount and ColorIndBuffer[SignalBar] == 2:
        _s_OnCalculate_UpCount += 1
        Alert(Word + ': Сигнал на покупку по ' + Symbol_)
    if _s_OnCalculate_DnCount < AlertCount and ColorIndBuffer[SignalBar] == 1:
        _s_OnCalculate_DnCount += 1
        Alert(Word + ': Сигнал на продажу по ' + Symbol_)
    return rates_total

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0
_s_OnCalculate_UpCount_ = 0
_s_OnCalculate_DnCount_ = 0
_s_OnCalculate_LastDots = 0.0
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DotsHtf(_MQL5Indicator):
    name = 'dots_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'AlertCount': 0,  # Количество подаваемых алертов
        'SignalBar': 1,  # Номер бара для сигнала, 0-текущий бар
        'Repeat': True,  # Повтор значений на следующих барах
        'Length': 10,  # Глубина сглаживания
        'Filter': 0,  # Параметр, позволяющий фильтровать всплески цен без добавления задержек в отображение
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

