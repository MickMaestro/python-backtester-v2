"""ColorJFatl_x2_cloud_HTF — converted from MQL5: MQL5 Indicators/ColorJFatl_x2_cloud_HTF/ColorJFatl_x2_cloud_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.62

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.62', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10025880, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'ColorJFatl_x2_cloud_HTF', 'source': 'MQL5 Indicators/ColorJFatl_x2_cloud_HTF/ColorJFatl_x2_cloud_HTF.mq5', 'folder': 'ColorJFatl_x2_cloud_HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16385, 'label': 'Период графика 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16388, 'label': 'Период графика 2', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'Phase', 'py': 'Phase', 'param': 'Phase', 'type': 'int', 'default': -100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_H1)  # Период графика 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H4)  # Период графика 2
Length = _input('Length', 5)  # глубина сглаживания
Phase = _input('Phase', -100)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle1 = 0
Ind_Handle2 = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle1, Ind_Handle2, min_rates_total
    if TimeFrame1 < Period() and TimeFrame1 != PERIOD_CURRENT:
        Print('Период графика 1 для индикатора ColorJFatl не может быть меньше периода текущего графика')
        return INIT_FAILED
    if TimeFrame2 < Period() and TimeFrame2 != PERIOD_CURRENT:
        Print('Период графика 2 для индикатора ColorJFatl не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle1 = iCustom(Symbol(), TimeFrame1, 'ColorJFatl', Length, Phase, IPC, 0, PriceShift)
    if Ind_Handle1 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorJFatl 1')
        return INIT_FAILED
    Ind_Handle2 = iCustom(Symbol(), TimeFrame2, 'ColorJFatl', Length, Phase, IPC, 0, PriceShift)
    if Ind_Handle2 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorJFatl 2')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorJFatl_x2_cloud', '(', GetStringTimeframe(TimeFrame1) + ',' + GetStringTimeframe(TimeFrame2), ' ,', Length, ' ,', Phase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar1, _s_OnCalculate_LastCountBar2
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle1) < Bars(Symbol(), TimeFrame1) or BarsCalculated(Ind_Handle2) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    JFatl = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    limit1 = 0
    limit2 = 0
    bar = 0
    JFatlTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit1 = rates_total - min_rates_total - 1
        limit2 = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar1 = rates_total
        _s_OnCalculate_LastCountBar2 = rates_total
    else:
        limit1 = _int(_s_OnCalculate_LastCountBar1) + rates_total - prev_calculated
        limit2 = _int(_s_OnCalculate_LastCountBar2) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit1
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame1, _DT(time[bar]), 1, JFatlTime) <= 0:
            return 0
        if time[bar] >= JFatlTime[0] and time[bar + 1] < JFatlTime[0]:
            _s_OnCalculate_LastCountBar1 = bar
            if CopyBuffer(Ind_Handle1, 0, _DT(time[bar]), 1, JFatl) <= 0:
                return 0
            UpBuffer[bar] = JFatl[0]
        else:
            UpBuffer[bar] = UpBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit2
    for bar in range(bar, 0 - 1, -1):
        DnBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame2, _DT(time[bar]), 1, JFatlTime) <= 0:
            return 0
        if time[bar] >= JFatlTime[0] and time[bar + 1] < JFatlTime[0]:
            _s_OnCalculate_LastCountBar2 = bar
            if CopyBuffer(Ind_Handle2, 0, _DT(time[bar]), 1, JFatl) <= 0:
                return 0
            DnBuffer[bar] = JFatl[0]
        else:
            DnBuffer[bar] = DnBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastJFatl = 0.0
_s_OnCalculate_LastCountBar1 = 0
_s_OnCalculate_LastCountBar2 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorJFatlX2CloudHTF(_MQL5Indicator):
    name = 'ColorJFatl_x2_cloud_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика 2
        'Length': 5,  # глубина сглаживания
        'Phase': -100,  # параметр сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

