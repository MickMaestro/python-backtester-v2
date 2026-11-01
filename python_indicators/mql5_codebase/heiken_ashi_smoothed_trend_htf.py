"""Heiken_Ashi_Smoothed_Trend_HTF — converted from MQL5: MQL5 Indicators/Heiken_Ashi_Smoothed_Trend_HTF/Heiken_Ashi_Smoothed_Trend_HTF.mq5

Индикатор Heiken_Ashi_Smoothed_Trend с возможностью изменения таймфрема во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16776960], 2: [9639167]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Heiken_Ashi_Smoothed_Trend Buy', 2: 'Heiken_Ashi_Smoothed_Trend Sell'}, 'levels': [], 'description': ['Индикатор Heiken_Ashi_Smoothed_Trend с возможностью изменения таймфрема во входных параметрах'], 'name': 'Heiken_Ashi_Smoothed_Trend_HTF', 'source': 'MQL5 Indicators/Heiken_Ashi_Smoothed_Trend_HTF/Heiken_Ashi_Smoothed_Trend_HTF.mq5', 'folder': 'Heiken_Ashi_Smoothed_Trend_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 30, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BuySymb', 'py': 'BuySymb', 'param': 'BuySymb', 'type': 'uint', 'default': 171, 'label': 'Символ покупки', 'sinput': False}, {'mql': 'SellSymb', 'py': 'SellSymb', 'param': 'SellSymb', 'type': 'uint', 'default': 171, 'label': 'Символ продажи', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
MA_Method1 = _input('MA_Method1', MODE_JJMA)  # метод усреднения
Length1 = _input('Length1', 30)  # глубина усреднения
Phase1 = _input('Phase1', 15)  # параметр усреднения,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BuySymb = _input('BuySymb', 171)  # Символ покупки
SellSymb = _input('SellSymb', 171)  # Символ продажи
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Heiken_Ashi_Smoothed_Trend', TimeFrame):
        return 0
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Heiken_Ashi_Smoothed_Trend', MA_Method1, Length1, Phase1, Gap, 171, 171)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Heiken_Ashi_Smoothed_Trend')
        return INIT_FAILED
    IndInit(0, DnBuffer, 0.0, min_rates_total, 0, SellSymb)
    IndInit(1, UpBuffer, 0.0, min_rates_total, 0, BuySymb)
    shortname = Box("")
    StringConcatenate(shortname, 'Heiken_Ashi_Smoothed_Trend', '(', GetStringTimeframe(TimeFrame), ', ', Length1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('Heiken_Ashi_Smoothed_Trend', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, DnBuffer, 1, UpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift, Symb):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_ARROW, Symb)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf1[bar] = 0.0
        IndBuf2[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr1 = Arr(1, 0.0, dyn=False)
            Arr2 = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr1) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr2) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr1[0]
            IndBuf2[bar] = Arr2[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiSmoothedTrendHTF(_MQL5Indicator):
    name = 'Heiken_Ashi_Smoothed_Trend_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'Length1': 30,  # глубина усреднения
        'Phase1': 15,  # параметр усреднения,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BuySymb': 171,  # Символ покупки
        'SellSymb': 171,  # Символ продажи
    }

