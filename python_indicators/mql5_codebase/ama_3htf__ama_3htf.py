"""ama_3htf_ — converted from MQL5: MQL5 Indicators/AMA_3HTF/ama_3htf_.mq5

Три мувинга AMA с разных таймфреймов с одинаковыми параметрами на одном графике.
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [13850042], 3: [9639167]}, 'widths': {1: 2, 2: 3, 3: 5}, 'styles': {}, 'labels': {1: 'AMA 1', 2: 'AMA 2', 3: 'AMA 3'}, 'levels': [], 'description': ['Три мувинга AMA с разных таймфреймов с одинаковыми параметрами на одном графике.'], 'name': 'ama_3htf_', 'source': 'MQL5 Indicators/AMA_3HTF/ama_3htf_.mq5', 'folder': 'AMA_3HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 30, 'label': 'Период графика индикатора 1 (младший таймфрейм)', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Период графика индикатора 2 (средний таймфрейм)', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора 3 (старший таймфрейм)', 'sinput': False}, {'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'int', 'default': 9, 'label': 'Период AMA', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'int', 'default': 2, 'label': 'Период быстрой скользящей', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'int', 'default': 30, 'label': 'Период медленной скользящей', 'sinput': False}, {'mql': 'AMAPrice', 'py': 'AMAPrice', 'param': 'AMAPrice', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_M30)  # Период графика индикатора 1 (младший таймфрейм)
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Период графика индикатора 2 (средний таймфрейм)
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # Период графика индикатора 3 (старший таймфрейм)
ama_period = _input('ama_period', 9)  # Период AMA
fast_ma_period = _input('fast_ma_period', 2)  # Период быстрой скользящей
slow_ma_period = _input('slow_ma_period', 30)  # Период медленной скользящей
AMAPrice = _input('AMAPrice', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind1_Handle = 0
Ind2_Handle = 0
Ind3_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def GetStringPrice(price):
    return StringSubstr(EnumToString(price, 'ENUM_APPLIED_PRICE'), 6, -1)

def OnInit():
    global Ind1_Handle, Ind2_Handle, Ind3_Handle, min_rates_total
    if not TimeFramesCheck('AMA', TimeFrame1, TimeFrame2, TimeFrame3):
        return INIT_FAILED
    min_rates_total = 2
    Ind1_Handle = iAMA(Symbol(), TimeFrame1, ama_period, fast_ma_period, slow_ma_period, 0, AMAPrice)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AMA 1')
        return INIT_FAILED
    Ind2_Handle = iAMA(Symbol(), TimeFrame2, ama_period, fast_ma_period, slow_ma_period, 0, AMAPrice)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AMA 2')
        return INIT_FAILED
    Ind3_Handle = iAMA(Symbol(), TimeFrame3, ama_period, fast_ma_period, slow_ma_period, 0, AMAPrice)
    if Ind3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AMA 3')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, 0.0, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, 0.0, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'AMA', '(', GetStringTimeframe(TimeFrame1), ' ,', GetStringTimeframe(TimeFrame2), ' ,', GetStringTimeframe(TimeFrame3), ' ,', ama_period, ' ,', fast_ma_period, ' ,', slow_ma_period, ' ,', GetStringPrice(AMAPrice), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind1_Handle) < Bars(Symbol(), TimeFrame1):
        return prev_calculated
    if BarsCalculated(Ind2_Handle) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    if BarsCalculated(Ind3_Handle) < Bars(Symbol(), TimeFrame3):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame1, Ind1_Handle, 0, Ind1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame2, Ind2_Handle, 0, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame3, Ind3_Handle, 0, Ind3Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Draw_Begin)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

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
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
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

def TimeFramesCheck(IndName, TFrame1, TFrame2, TFrame3):
    if TFrame1 < Period() and TFrame1 != PERIOD_CURRENT:
        Print('Период графика 1 для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    if TFrame2 <= TFrame1:
        Print('Период графика 2 для индикатора ' + IndName + ' должен быть больше периода графика 1!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    if TFrame3 <= TFrame2:
        Print('Период графика 3 для индикатора ' + IndName + ' должен быть больше периода графика 2!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ama3htf(_MQL5Indicator):
    name = 'ama_3htf_'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Период графика индикатора 1 (младший таймфрейм)
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика индикатора 2 (средний таймфрейм)
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора 3 (старший таймфрейм)
        'ama_period': 9,  # Период AMA
        'fast_ma_period': 2,  # Период быстрой скользящей
        'slow_ma_period': 30,  # Период медленной скользящей
        'AMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

