"""SpearmanRankCorrelation_3HTF — converted from MQL5: MQL5 Indicators/SpearmanRankCorrelation_3HTF/SpearmanRankCorrelation_3HTF.mq5

Три осциллятора SpearmanRankCorrelation с разных таймфреймов с одинаковыми параметрами на одном графике.
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.70

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.70', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3, 'indicator_minimum': -1.0, 'indicator_maximum': 1.0}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [13850042], 3: [255]}, 'widths': {1: 2, 2: 3, 3: 5}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME+"1"', 2: 'INDICATOR_NAME+"2"', 3: 'INDICATOR_NAME+"3"'}, 'levels': [], 'description': ['Три осциллятора SpearmanRankCorrelation с разных таймфреймов с одинаковыми параметрами на одном графике.'], 'name': 'SpearmanRankCorrelation_3HTF', 'source': 'MQL5 Indicators/SpearmanRankCorrelation_3HTF/SpearmanRankCorrelation_3HTF.mq5', 'folder': 'SpearmanRankCorrelation_3HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 30, 'label': 'Период графика индикатора 1 (младший таймфрейм)', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Период графика индикатора 2 (средний таймфрейм)', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора 3 (старший таймфрейм)', 'sinput': False}, {'mql': 'rangeN', 'py': 'rangeN', 'param': 'rangeN', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CalculatedBars', 'py': 'CalculatedBars', 'param': 'CalculatedBars', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Maxrange', 'py': 'Maxrange', 'param': 'Maxrange', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'direction', 'py': 'direction', 'param': 'direction', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_M30)  # Период графика индикатора 1 (младший таймфрейм)
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Период графика индикатора 2 (средний таймфрейм)
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # Период графика индикатора 3 (старший таймфрейм)
rangeN = _input('rangeN', 14)
CalculatedBars = _input('CalculatedBars', 0)
Maxrange = _input('Maxrange', 30)
direction = _input('direction', True)
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

def OnInit():
    global Ind1_Handle, Ind2_Handle, Ind3_Handle, min_rates_total
    min_rates_total = 2
    Ind1_Handle = iCustom(Symbol(), TimeFrame1, 'SpearmanRankCorrelation', rangeN, CalculatedBars, Maxrange, direction)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SpearmanRankCorrelation 1')
        return INIT_FAILED
    Ind2_Handle = iCustom(Symbol(), TimeFrame2, 'SpearmanRankCorrelation', rangeN, CalculatedBars, Maxrange, direction)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SpearmanRankCorrelation 2')
        return INIT_FAILED
    Ind3_Handle = iCustom(Symbol(), TimeFrame3, 'SpearmanRankCorrelation', rangeN, CalculatedBars, Maxrange, direction)
    if Ind3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SpearmanRankCorrelation 3')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, EMPTY_VALUE, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'SpearmanRankCorrelation', '(', GetStringTimeframe(TimeFrame1), ' ,', GetStringTimeframe(TimeFrame2), ' ,', GetStringTimeframe(TimeFrame3), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -0.5)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('SpearmanRankCorrelation', TimeFrame1, TimeFrame2, TimeFrame3):
        return 0
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
    if not CountIndicator(0, "", TimeFrame2, Ind2_Handle, 0, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame3, Ind3_Handle, 0, Ind3Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Draw_Begin)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Buffer, True)

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

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
        Print('Период графика 1 для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    if TFrame2 <= TFrame1:
        Print('Период графика 2 для индикатора ' + IndName + ' должен быть больше периода графика 1! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    if TFrame3 <= TFrame2:
        Print('Период графика 3 для индикатора ' + IndName + ' должен быть больше периода графика 2! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpearmanRankCorrelation3HTF(_MQL5Indicator):
    name = 'SpearmanRankCorrelation_3HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Период графика индикатора 1 (младший таймфрейм)
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика индикатора 2 (средний таймфрейм)
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора 3 (старший таймфрейм)
        'rangeN': 14,
        'CalculatedBars': 0,
        'Maxrange': 30,
        'direction': True,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (-1.0, 1.0)

