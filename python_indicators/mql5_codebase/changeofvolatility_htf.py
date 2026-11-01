"""changeofvolatility_htf — converted from MQL5: MQL5 Indicators/ChangeOfVolatility_HTF/changeofvolatility_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 8388736, 255, 55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ChangeOfVolatility HTF'}, 'levels': [], 'description': [], 'name': 'changeofvolatility_htf', 'source': 'MQL5 Indicators/ChangeOfVolatility_HTF/changeofvolatility_htf.mq5', 'folder': 'ChangeOfVolatility_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'uint', 'default': 1, 'label': 'Период моментума', 'sinput': False}, {'mql': 'Short', 'py': 'Short', 'param': 'Short', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Long', 'py': 'Long', 'param': 'Long', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'MaxTrendLevel', 'py': 'MaxTrendLevel', 'param': 'MaxTrendLevel', 'type': 'uint', 'default': 80, 'label': 'Уровень максимального тренда', 'sinput': False}, {'mql': 'MiddLeTrendLevel', 'py': 'MiddLeTrendLevel', 'param': 'MiddLeTrendLevel', 'type': 'uint', 'default': 50, 'label': 'Уровень умеренного тренда', 'sinput': False}, {'mql': 'FlatLevel', 'py': 'FlatLevel', 'param': 'FlatLevel', 'type': 'uint', 'default': 30, 'label': 'Уровень флета', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
MPeriod = _input('MPeriod', 1)  # Период моментума
Short = _input('Short', 6)
Long = _input('Long', 100)
MaxTrendLevel = _input('MaxTrendLevel', 80)  # Уровень максимального тренда
MiddLeTrendLevel = _input('MiddLeTrendLevel', 50)  # Уровень умеренного тренда
FlatLevel = _input('FlatLevel', 30)  # Уровень флета
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
        Print('Период графика для индикатора ChangeOfVolatility не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ChangeOfVolatility', MPeriod, Short, Long, MaxTrendLevel, MiddLeTrendLevel, FlatLevel)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ChangeOfVolatility')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ChangeOfVolatility HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, MaxTrendLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddLeTrendLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, FlatLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Blue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Gray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Ind = Arr(1, 0.0, dyn=False)
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


class ChangeofvolatilityHtf(_MQL5Indicator):
    name = 'changeofvolatility_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'MPeriod': 1,  # Период моментума
        'Short': 6,
        'Long': 100,
        'MaxTrendLevel': 80,  # Уровень максимального тренда
        'MiddLeTrendLevel': 50,  # Уровень умеренного тренда
        'FlatLevel': 30,  # Уровень флета
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

