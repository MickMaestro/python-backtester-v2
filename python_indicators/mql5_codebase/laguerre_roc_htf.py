"""laguerre_roc_htf — converted from MQL5: MQL5 Indicators/Laguerre_ROC_HTF/laguerre_roc_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': -0.1}, 'types': {1: 11}, 'colors': {1: [36095, 2763429, 8421504, 16711680, 16760576]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Laguerre_ROC'}, 'levels': [], 'description': [], 'name': 'laguerre_roc_htf', 'source': 'MQL5 Indicators/Laguerre_ROC_HTF/laguerre_roc_htf.mq5', 'folder': 'Laguerre_ROC_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'vPeriod', 'py': 'vPeriod', 'param': 'vPeriod', 'type': 'uint', 'default': 5, 'label': 'Период', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.5, 'label': 'Коэффициент усреднения', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'double', 'default': 0.75, 'label': 'Уровень перекупленности в %%', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'double', 'default': 0.25, 'label': 'Уровень перепроданности в %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет уровня перекупленности', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет уровня перепроданности', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Толщина уровней', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
vPeriod = _input('vPeriod', 5)  # Период
gamma = _input('gamma', 0.5)  # Коэффициент усреднения
UpLevel = _input('UpLevel', 0.75)  # Уровень перекупленности в %%
DnLevel = _input('DnLevel', 0.25)  # Уровень перепроданности в %%
UpLevelsColor = _input('UpLevelsColor', clrMagenta)  # Цвет уровня перекупленности
DnLevelsColor = _input('DnLevelsColor', clrMagenta)  # Цвет уровня перепроданности
Levelstyle = _input('Levelstyle', DASH_)  # Стиль уровней
LevelsWidth = _input('LevelsWidth', Width_1)  # Толщина уровней
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
min_rates_total = 0
Ind_Handle = 0
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора Laguerre_ROC не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Laguerre_ROC', vPeriod, gamma, UpLevel, DnLevel, CLR_NONE, CLR_NONE, SOLID_, Width_1, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Laguerre_ROC')
        return INIT_FAILED
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Laguerre_ROC HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0.5)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, DASHDOTDOT_)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    UpInd = Arr(2, 0.0, dyn=False)
    DnInd = Arr(2, 0.0, dyn=False)
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
        UpIndBuffer[bar] = EMPTY_VALUE
        DnIndBuffer[bar] = EMPTY_VALUE
        ColorIndBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, UpInd) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, DnInd) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 2, _DT(time[bar]), 1, Col) <= 0:
                return 0
            UpIndBuffer[bar] = UpInd[0]
            DnIndBuffer[bar] = DnInd[0]
            ColorIndBuffer[bar] = Col[0]
        if ReDraw:
            if UpIndBuffer[bar + 1] != EMPTY_VALUE and UpIndBuffer[bar] == EMPTY_VALUE:
                UpIndBuffer[bar] = UpIndBuffer[bar + 1]
                DnIndBuffer[bar] = DnIndBuffer[bar + 1]
                ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreRocHtf(_MQL5Indicator):
    name = 'laguerre_roc_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'vPeriod': 5,  # Период
        'gamma': 0.5,  # Коэффициент усреднения
        'UpLevel': 0.75,  # Уровень перекупленности в %%
        'DnLevel': 0.25,  # Уровень перепроданности в %%
        'Levelstyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # Стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Толщина уровней
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }
    y_range = (-0.1, 1.1)

