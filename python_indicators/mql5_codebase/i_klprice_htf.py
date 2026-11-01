"""i-klprice_htf — converted from MQL5: MQL5 Indicators/i-KlPrice_HTF/i-klprice_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 128, 8421504, 16711680, 16760576]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i-KlPrice'}, 'levels': [], 'description': [], 'name': 'i-klprice_htf', 'source': 'MQL5 Indicators/i-KlPrice_HTF/i-klprice_htf.mq5', 'folder': 'i-KlPrice_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения скользящей средней', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 100, 'label': 'Глубина сглаживания скользящей средней', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения скользящей средней', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод усреднения размера свеч', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 20, 'label': 'Глубина усреднения размера свеч', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания размера свеч', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 2.0, 'label': 'Коэффициент расширения канала', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 20, 'label': 'Период сглаживания индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'int', 'default': 50, 'label': 'Верхний уровень', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'int', 'default': -50, 'label': 'Нижний уровень', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 4, 'label': 'Стиль линий уровней', 'sinput': False}, {'mql': 'UpLevelColor', 'py': 'UpLevelColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет верхнего уровня', 'sinput': False}, {'mql': 'DnLevelColor', 'py': 'DnLevelColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет нижнего уровня', 'sinput': False}, {'mql': 'LevelWidth', 'py': 'LevelWidth', 'param': 'LevelWidth', 'type': 'int', 'default': 0, 'label': 'Толщина уровней', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum ENUM_WIDTH
w_1 = 0
w_2 = 1
w_3 = 2
w_4 = 3
w_5 = 4
_enum('ENUM_WIDTH', {0: 'w_1', 1: 'w_2', 2: 'w_3', 3: 'w_4', 4: 'w_5'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Метод усреднения скользящей средней
Length1 = _input('Length1', 100)  # Глубина сглаживания скользящей средней
Phase1 = _input('Phase1', 15)  # Параметр усреднения скользящей средней
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Метод усреднения размера свеч
Length2 = _input('Length2', 20)  # Глубина усреднения размера свеч
Phase2 = _input('Phase2', 100)  # Параметр сглаживания размера свеч
Deviation = _input('Deviation', 2.0)  # Коэффициент расширения канала
Smooth = _input('Smooth', 20)  # Период сглаживания индикатора
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
UpLevel = _input('UpLevel', 50)  # Верхний уровень
DnLevel = _input('DnLevel', -50)  # Нижний уровень
LevelStyle = _input('LevelStyle', STYLE_DASHDOTDOT)  # Стиль линий уровней
UpLevelColor = _input('UpLevelColor', clrBlue)  # Цвет верхнего уровня
DnLevelColor = _input('DnLevelColor', clrMagenta)  # Цвет нижнего уровня
LevelWidth = _input('LevelWidth', w_1)  # Толщина уровней
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
        Print('Период графика для индикатора i-KlPrice не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'i-KlPrice', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, Deviation, Smooth, IPC, UpLevel, DnLevel, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора i-KlPrice')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-KlPrice HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, DnLevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelWidth)
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


class IKlpriceHtf(_MQL5Indicator):
    name = 'i-klprice_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения скользящей средней
        'Length1': 100,  # Глубина сглаживания скользящей средней
        'Phase1': 15,  # Параметр усреднения скользящей средней
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения размера свеч
        'Length2': 20,  # Глубина усреднения размера свеч
        'Phase2': 100,  # Параметр сглаживания размера свеч
        'Deviation': 2.0,  # Коэффициент расширения канала
        'Smooth': 20,  # Период сглаживания индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'UpLevel': 50,  # Верхний уровень
        'DnLevel': -50,  # Нижний уровень
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Стиль линий уровней
        'LevelWidth': _Choice({0: '1', 1: '2', 2: '3', 3: '4', 4: '5'}, default=0),  # Толщина уровней
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

