"""Skyscraper_Fix_HTF — converted from MQL5: MQL5 Indicators/Skyscraper_Fix_HTF/Skyscraper_Fix_HTF.mq5

Skyscraper_Fix с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.70

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.70', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 12}, 'colors': {1: [3329330], 2: [9639167], 3: [3329330], 4: [9639167], 5: [8421376, 2237106]}, 'widths': {1: 2, 2: 2, 3: 5, 4: 5, 5: 1}, 'styles': {}, 'labels': {1: 'Lower Skyscraper_Fix', 2: 'Upper Skyscraper_Fix', 3: 'Skyscraper_Fix Buy', 4: 'Skyscraper_Fix Sell', 5: 'Skyscraper Middle'}, 'levels': [], 'description': ['Skyscraper_Fix с возможностью изменения таймфрейма во входных параметрах'], 'name': 'Skyscraper_Fix_HTF', 'source': 'MQL5 Indicators/Skyscraper_Fix_HTF/Skyscraper_Fix_HTF.mq5', 'folder': 'Skyscraper_Fix_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Период ATR', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 0.9, 'label': 'Фактор чувствительности индикатора', 'sinput': False}, {'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'double', 'default': 0.0, 'label': 'Приближение средней линии к линиям экстремумов', 'sinput': False}, {'mql': 'HighLow', 'py': 'HighLow', 'param': 'HighLow', 'type': 'int', 'default': 0, 'label': 'Расчёт индикатора по High/Low или Close', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Method
MODE_HighLow = 0
MODE_Close = 1
_enum('Method', {0: 'MODE_HighLow', 1: 'MODE_Close'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Length = _input('Length', 10)  # Период ATR
Kv = _input('Kv', 0.9)  # Фактор чувствительности индикатора
Percentage = _input('Percentage', 0.0)  # Приближение средней линии к линиям экстремумов
HighLow = _input('HighLow', MODE_HighLow)  # Расчёт индикатора по High/Low или Close
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer5 = Arr(0, 0.0)
IndBuffer6 = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Skyscraper_Fix', Length, Kv, Percentage, HighLow)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Skyscraper_Fix')
        return INIT_FAILED
    IndInit(0, IndBuffer1, INDICATOR_DATA)
    IndInit(1, IndBuffer2, INDICATOR_DATA)
    IndInit(2, IndBuffer3, INDICATOR_DATA)
    IndInit(3, IndBuffer4, INDICATOR_DATA)
    IndInit(4, IndBuffer5, INDICATOR_DATA)
    IndInit(5, IndBuffer6, INDICATOR_COLOR_INDEX)
    PlotInit(0, 0.0, 0, Shift)
    PlotInit(1, 0.0, 0, Shift)
    PlotInit(2, 0.0, 0, Shift)
    PlotInit(3, 0.0, 0, Shift)
    PlotInit(4, 0.0, 0, Shift)
    PlotIndexSetInteger(2, PLOT_ARROW, 172)
    PlotIndexSetInteger(3, PLOT_ARROW, 172)
    PlotIndexSetInteger(4, PLOT_ARROW, 172)
    shortname = Box("")
    StringConcatenate(shortname, 'Skyscraper_Fix', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('Skyscraper_Fix', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, 1, IndBuffer2, 2, IndBuffer3, 3, IndBuffer4, 4, IndBuffer5, 5, IndBuffer6, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, BuffNumb4, IndBuf4, BuffNumb5, IndBuf5, BuffNumb6, IndBuf6, nTime, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(nTime[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        IndBuf1[bar] = 0.0
        IndBuf5[bar] = IndBuf1[bar]
        IndBuf4[bar] = IndBuf5[bar]
        IndBuf3[bar] = IndBuf4[bar]
        IndBuf2[bar] = IndBuf3[bar]
        IndBuf1[bar] = IndBuf2[bar]
        if nTime[bar] >= IndTime[0] and nTime[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr1 = Arr(1, 0.0, dyn=False)
            Arr2 = Arr(1, 0.0, dyn=False)
            Arr3 = Arr(1, 0.0, dyn=False)
            Arr4 = Arr(1, 0.0, dyn=False)
            Arr5 = Arr(1, 0.0, dyn=False)
            Arr6 = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(nTime[bar]), 1, Arr1) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb2, _DT(nTime[bar]), 1, Arr2) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb3, _DT(nTime[bar]), 1, Arr3) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb4, _DT(nTime[bar]), 1, Arr4) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb5, _DT(nTime[bar]), 1, Arr5) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb6, _DT(nTime[bar]), 1, Arr6) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr1[0]
            IndBuf2[bar] = Arr2[0]
            IndBuf3[bar] = Arr3[0]
            IndBuf4[bar] = Arr4[0]
            IndBuf5[bar] = Arr5[0]
            IndBuf6[bar] = Arr6[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
            IndBuf4[bar] = IndBuf4[bar + 1]
            IndBuf5[bar] = IndBuf5[bar + 1]
            IndBuf6[bar] = IndBuf6[bar + 1]
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


class SkyscraperFixHTF(_MQL5Indicator):
    name = 'Skyscraper_Fix_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Length': 10,  # Период ATR
        'Kv': 0.9,  # Фактор чувствительности индикатора
        'Percentage': 0.0,  # Приближение средней линии к линиям экстремумов
        'HighLow': _Choice({0: 'High/Low', 1: 'Close'}, default=0),  # Расчёт индикатора по High/Low или Close
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

