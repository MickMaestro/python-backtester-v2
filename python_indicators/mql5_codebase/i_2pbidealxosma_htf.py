"""2pbidealxosma_htf — converted from MQL5: MQL5 Indicators/2pbIdealXOSMA_HTF/2pbidealxosma_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 2330219, 16748574, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: '2pbIdealXOSMA HTF'}, 'levels': [], 'description': [], 'name': '2pbidealxosma_htf', 'source': 'MQL5 Indicators/2pbIdealXOSMA_HTF/2pbidealxosma_htf.mq5', 'folder': '2pbIdealXOSMA_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'uint', 'default': 10, 'label': 'Грубое усреднение', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'uint', 'default': 10, 'label': 'Уточняющее усреднение', 'sinput': False}, {'mql': 'PeriodX1', 'py': 'PeriodX1', 'param': 'PeriodX1', 'type': 'uint', 'default': 10, 'label': 'Первое грубое усреднение', 'sinput': False}, {'mql': 'PeriodX2', 'py': 'PeriodX2', 'param': 'PeriodX2', 'type': 'uint', 'default': 10, 'label': 'Первое уточняющее усреднение', 'sinput': False}, {'mql': 'PeriodY1', 'py': 'PeriodY1', 'param': 'PeriodY1', 'type': 'uint', 'default': 10, 'label': 'Второе грубое усреднение', 'sinput': False}, {'mql': 'PeriodY2', 'py': 'PeriodY2', 'param': 'PeriodY2', 'type': 'uint', 'default': 10, 'label': 'Второе уточняющее усреднение', 'sinput': False}, {'mql': 'PeriodZ1', 'py': 'PeriodZ1', 'param': 'PeriodZ1', 'type': 'uint', 'default': 10, 'label': 'Третье грубое усреднение', 'sinput': False}, {'mql': 'PeriodZ2', 'py': 'PeriodZ2', 'param': 'PeriodZ2', 'type': 'uint', 'default': 10, 'label': 'Третье уточняющее усреднение', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'Smooth_XMA', 'py': 'Smooth_XMA', 'param': 'Smooth_XMA', 'type': 'uint', 'default': 9, 'label': 'Период сглаживания', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Period1 = _input('Period1', 10)  # Грубое усреднение
Period2 = _input('Period2', 10)  # Уточняющее усреднение
PeriodX1 = _input('PeriodX1', 10)  # Первое грубое усреднение
PeriodX2 = _input('PeriodX2', 10)  # Первое уточняющее усреднение
PeriodY1 = _input('PeriodY1', 10)  # Второе грубое усреднение
PeriodY2 = _input('PeriodY2', 10)  # Второе уточняющее усреднение
PeriodZ1 = _input('PeriodZ1', 10)  # Третье грубое усреднение
PeriodZ2 = _input('PeriodZ2', 10)  # Третье уточняющее усреднение
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Метод сглаживания
Smooth_XMA = _input('Smooth_XMA', 9)  # Период сглаживания
Smooth_Phase = _input('Smooth_Phase', 100)  # Параметр усреднения
ReDraw = _input('ReDraw', True)  # повтор отображения инфомации на пустых барах
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
        Print('Период графика для индикатора 2pbIdealXOSMA не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, '2pbIdealXOSMA', Period1, Period2, PeriodX1, PeriodX2, PeriodY1, PeriodY2, PeriodZ1, PeriodZ2, SmoothMethod, Smooth_Phase)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора 2pbIdealXOSMA')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, '2pbIdealXOSMA HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
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
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 2, Ind) <= 0:
                return 0
            IndBuffer[bar] = Ind[1]
            if IndBuffer[bar] > 0:
                if Ind[1] > Ind[0]:
                    ColorIndBuffer[bar] = 1.0
                if Ind[1] < Ind[0]:
                    ColorIndBuffer[bar] = 2.0
            if IndBuffer[bar] < 0:
                if Ind[1] < Ind[0]:
                    ColorIndBuffer[bar] = 3.0
                if Ind[1] > Ind[0]:
                    ColorIndBuffer[bar] = 4.0
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


class Ind2pbidealxosmaHtf(_MQL5Indicator):
    name = '2pbidealxosma_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Period1': 10,  # Грубое усреднение
        'Period2': 10,  # Уточняющее усреднение
        'PeriodX1': 10,  # Первое грубое усреднение
        'PeriodX2': 10,  # Первое уточняющее усреднение
        'PeriodY1': 10,  # Второе грубое усреднение
        'PeriodY2': 10,  # Второе уточняющее усреднение
        'PeriodZ1': 10,  # Третье грубое усреднение
        'PeriodZ2': 10,  # Третье уточняющее усреднение
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'Smooth_XMA': 9,  # Период сглаживания
        'Smooth_Phase': 100,  # Параметр усреднения
        'ReDraw': True,  # повтор отображения инфомации на пустых барах
    }

