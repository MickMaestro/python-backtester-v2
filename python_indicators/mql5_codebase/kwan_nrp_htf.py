"""KWAN_NRP_HTF — converted from MQL5: MQL5 Indicators/KWAN_NRP_HTF/KWAN_NRP_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [7451452, 8421504, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'KWAN_NRP_HTF', 'source': 'MQL5 Indicators/KWAN_NRP_HTF/KWAN_NRP_HTF.mq5', 'folder': 'KWAN_NRP_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'количество подаваемых алертов', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'номер бара для сигнала, 0-текущий бар', 'sinput': False}, {'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'uint', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'uint', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'тип сглаживания', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'способ расчета стохастика', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора RSI', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена RSI', 'sinput': False}, {'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'uint', 'default': 14, 'label': 'Период индикатора Momentum', 'sinput': False}, {'mql': 'MomentumPrice', 'py': 'MomentumPrice', 'param': 'MomentumPrice', 'type': 'int', 'default': 1, 'label': 'Цена индикатора Momentum', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AlertCount = _input('AlertCount', 0)  # количество подаваемых алертов
SignalBar = _input('SignalBar', 1)  # номер бара для сигнала, 0-текущий бар
InpKPeriod = _input('InpKPeriod', 5)  # K period
InpDPeriod = _input('InpDPeriod', 3)  # D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
ma_method = _input('ma_method', MODE_SMA)  # тип сглаживания
price_field = _input('price_field', STO_LOWHIGH)  # способ расчета стохастика
RSIPeriod = _input('RSIPeriod', 14)  # период индикатора RSI
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена RSI
MomentumPeriod = _input('MomentumPeriod', 14)  # Период индикатора Momentum
MomentumPrice = _input('MomentumPrice', PRICE_CLOSE)  # Цена индикатора Momentum
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 3)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора KWAN_NRP не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'KWAN_NRP' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'KWAN_NRP', InpKPeriod, InpDPeriod, InpSlowing, ma_method, price_field, RSIPeriod, RSIPrice, MomentumPeriod, MomentumPrice, XMA_Method, XLength, XPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора KWAN_NRP')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KWAN_NRP')
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
    if (_s_OnCalculate_UpCount < AlertCount and ColorIndBuffer[SignalBar + 1] == 1) and ColorIndBuffer[SignalBar] == 0:
        _s_OnCalculate_UpCount += 1
        Alert(Word + ': Сигнал на покупку по ' + Symbol_)
    if (_s_OnCalculate_DnCount < AlertCount and ColorIndBuffer[SignalBar + 1] == 0) and ColorIndBuffer[SignalBar] == 1:
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


class KWANNRPHTF(_MQL5Indicator):
    name = 'KWAN_NRP_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'AlertCount': 0,  # количество подаваемых алертов
        'SignalBar': 1,  # номер бара для сигнала, 0-текущий бар
        'InpKPeriod': 5,  # K period
        'InpDPeriod': 3,  # D period
        'InpSlowing': 3,  # Slowing
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # тип сглаживания
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # способ расчета стохастика
        'RSIPeriod': 14,  # период индикатора RSI
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена RSI
        'MomentumPeriod': 14,  # Период индикатора Momentum
        'MomentumPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена индикатора Momentum
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 3,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

