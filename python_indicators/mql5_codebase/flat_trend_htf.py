"""flat-trend_htf — converted from MQL5: MQL5 Indicators/Flat-Trend_HTF/flat-trend_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 14822282, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Flat-Trend'}, 'levels': [], 'description': [], 'name': 'flat-trend_htf', 'source': 'MQL5 Indicators/Flat-Trend_HTF/flat-trend_htf.mq5', 'folder': 'Flat-Trend_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'StDevPeriod', 'py': 'StDevPeriod', 'param': 'StDevPeriod', 'type': 'uint', 'default': 20, 'label': 'Период StDev', 'sinput': False}, {'mql': 'StDev_Method', 'py': 'StDev_Method', 'param': 'StDev_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения StDev', 'sinput': False}, {'mql': 'StDevLength', 'py': 'StDevLength', 'param': 'StDevLength', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания StDev', 'sinput': False}, {'mql': 'StDevPhase', 'py': 'StDevPhase', 'param': 'StDevPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания StDev', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 20, 'label': 'Период StDev', 'sinput': False}, {'mql': 'ATR_Method', 'py': 'ATR_Method', 'param': 'ATR_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения ATR', 'sinput': False}, {'mql': 'ATRLength', 'py': 'ATRLength', 'param': 'ATRLength', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания ATR', 'sinput': False}, {'mql': 'ATRPhase', 'py': 'ATRPhase', 'param': 'ATRPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания ATR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
StDevPeriod = _input('StDevPeriod', 20)  # Период StDev
StDev_Method = _input('StDev_Method', MODE_LWMA)  # Метод усреднения StDev
StDevLength = _input('StDevLength', 5)  # Глубина сглаживания StDev
StDevPhase = _input('StDevPhase', 15)  # Параметр сглаживания StDev
ATRPeriod = _input('ATRPeriod', 20)  # Период StDev
ATR_Method = _input('ATR_Method', MODE_LWMA)  # Метод усреднения ATR
ATRLength = _input('ATRLength', 5)  # Глубина сглаживания ATR
ATRPhase = _input('ATRPhase', 15)  # Параметр сглаживания ATR
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
min_rates_total = 0
Ind_Handle = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора Flat-Trend не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Flat-Trend', StDevPeriod, StDev_Method, StDevLength, StDevPhase, ATRPeriod, ATR_Method, ATRLength, ATRPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Flat-Trend')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Flat-Trend HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Ind = Arr(2, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
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
        ColorIndBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer[bar] = Ind[0]
            ColorIndBuffer[bar] = Col[0]
        if ReDraw:
            if IndBuffer[bar + 1] != EMPTY_VALUE and IndBuffer[bar] == EMPTY_VALUE:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FlatTrendHtf(_MQL5Indicator):
    name = 'flat-trend_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'StDevPeriod': 20,  # Период StDev
        'StDev_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения StDev
        'StDevLength': 5,  # Глубина сглаживания StDev
        'StDevPhase': 15,  # Параметр сглаживания StDev
        'ATRPeriod': 20,  # Период StDev
        'ATR_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения ATR
        'ATRLength': 5,  # Глубина сглаживания ATR
        'ATRPhase': 15,  # Параметр сглаживания ATR
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

