"""UltraAbsolutelyNoLagLwma_HTF — converted from MQL5: MQL5 Indicators/UltraAbsolutelyNoLagLwma_HTF/UltraAbsolutelyNoLagLwma_HTF.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 11}, 'colors': {1: [8421504, 16711935, 11823615, 255, 2763429, 3329330, 8421376, 65280, 10025880]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'UltraAbsolutelyNoLagLwma HTF'}, 'levels': [], 'description': [], 'name': 'UltraAbsolutelyNoLagLwma_HTF', 'source': 'MQL5 Indicators/UltraAbsolutelyNoLagLwma_HTF/UltraAbsolutelyNoLagLwma_HTF.mq5', 'folder': 'UltraAbsolutelyNoLagLwma_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'FLength', 'py': 'FLength', 'param': 'FLength', 'type': 'uint', 'default': 7, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'Стартовый период усреднения', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'Шаг изменения периода', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'Количество изменений периода', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности в %%', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности в %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет уровня перекупленности', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет уровня перепроданности', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Толщина уровней', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
FLength = _input('FLength', 7)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
W_Method = _input('W_Method', MODE_JJMA)  # Метод усреднения
StartLength = _input('StartLength', 3)  # Стартовый период усреднения
WPhase = _input('WPhase', 100)  # Параметр усреднения
Step = _input('Step', 5)  # Шаг изменения периода
StepsTotal = _input('StepsTotal', 10)  # Количество изменений периода
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Метод сглаживания
SmoothLength = _input('SmoothLength', 3)  # Глубина сглаживания
SmoothPhase = _input('SmoothPhase', 100)  # Параметр сглаживания
UpLevel = _input('UpLevel', 80)  # Уровень перекупленности в %%
DnLevel = _input('DnLevel', 20)  # Уровень перепроданности в %%
UpLevelsColor = _input('UpLevelsColor', clrBlue)  # Цвет уровня перекупленности
DnLevelsColor = _input('DnLevelsColor', clrBlue)  # Цвет уровня перепроданности
Levelstyle = _input('Levelstyle', DASH_)  # Стиль уровней
LevelsWidth = _input('LevelsWidth', Width_1)  # Толщина уровней
ReDraw = _input('ReDraw', True)  # повтор отображения инфомации на пустых барах
period = Arr(0, 0)
min_rates_total = 0
Ind_Handle = 0
dUpLevel = 0.0
dDnLevel = 0.0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, dDnLevel, dUpLevel, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора UltraAbsolutelyNoLagLwma не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'UltraAbsolutelyNoLagLwma', FLength, IPC, W_Method, StartLength, WPhase, Step, StepsTotal, SmoothMethod, SmoothLength, SmoothPhase, UpLevel, DnLevel, clrNONE, clrNONE, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора UltraAbsolutelyNoLagLwma')
        return INIT_FAILED
    dUpLevel = (StepsTotal * UpLevel) / 100.0
    dDnLevel = (StepsTotal * DnLevel) / 100.0
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'UltraAbsolutelyNoLagLwma HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, dUpLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, dDnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    UpValue = Arr(1, 0.0, dyn=False)
    DnValue = Arr(1, 0.0, dyn=False)
    clrValue = Arr(1, 0.0, dyn=False)
    UltraAbsolutelyNoLagLwmaTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        ColorBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, UltraAbsolutelyNoLagLwmaTime) <= 0:
            return 0
        if time[bar] >= UltraAbsolutelyNoLagLwmaTime[0] and time[bar + 1] < UltraAbsolutelyNoLagLwmaTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, DnValue) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, UpValue) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 2, _DT(time[bar]), 1, clrValue) <= 0:
                return 0
            UpBuffer[bar] = UpValue[0]
            DnBuffer[bar] = DnValue[0]
            ColorBuffer[bar] = clrValue[0]
        if ReDraw:
            if UpBuffer[bar + 1] != EMPTY_VALUE and UpBuffer[bar] == EMPTY_VALUE:
                ColorBuffer[bar] = ColorBuffer[bar + 1]
                UpBuffer[bar] = UpBuffer[bar + 1]
                DnBuffer[bar] = DnBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraAbsolutelyNoLagLwmaHTF(_MQL5Indicator):
    name = 'UltraAbsolutelyNoLagLwma_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'FLength': 7,  # глубина сглаживания
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'StartLength': 3,  # Стартовый период усреднения
        'WPhase': 100,  # Параметр усреднения
        'Step': 5,  # Шаг изменения периода
        'StepsTotal': 10,  # Количество изменений периода
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'SmoothLength': 3,  # Глубина сглаживания
        'SmoothPhase': 100,  # Параметр сглаживания
        'UpLevel': 80,  # Уровень перекупленности в %%
        'DnLevel': 20,  # Уровень перепроданности в %%
        'Levelstyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # Стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Толщина уровней
        'ReDraw': True,  # повтор отображения инфомации на пустых барах
    }

