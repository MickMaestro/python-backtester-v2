"""cmx_htf — converted from MQL5: MQL5 Indicators/CMx_HTF/cmx_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 8721863, 8421504, 16711680, 16748574]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'CMx HTF'}, 'levels': [], 'description': [], 'name': 'cmx_htf', 'source': 'MQL5 Indicators/CMx_HTF/cmx_htf.mq5', 'folder': 'CMx_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'F', 'py': 'F', 'param': 'F', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.682, 'label': '', 'sinput': False}, {'mql': 'L_adx', 'py': 'L_adx', 'param': 'L_adx', 'type': 'double', 'default': 18.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 423.6, 'label': 'Уровень 1', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 261.8, 'label': 'Уровень 2', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 161.8, 'label': 'Уровень 3', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 61.8, 'label': 'Уровень 4', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.0, 'label': 'Уровень 5', 'sinput': False}, {'mql': 'Level6', 'py': 'Level6', 'param': 'Level6', 'type': 'double', 'default': -61.8, 'label': 'Уровень 6', 'sinput': False}, {'mql': 'Level7', 'py': 'Level7', 'param': 'Level7', 'type': 'double', 'default': -161.8, 'label': 'Уровень 7', 'sinput': False}, {'mql': 'Level8', 'py': 'Level8', 'param': 'Level8', 'type': 'double', 'default': -261.8, 'label': 'Уровень 8', 'sinput': False}, {'mql': 'Level9', 'py': 'Level9', 'param': 'Level9', 'type': 'double', 'default': -423.6, 'label': 'Уровень 9', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
F = _input('F', 12)
k = _input('k', 1.682)
L_adx = _input('L_adx', 18.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Level1 = _input('Level1', 423.6)  # Уровень 1
Level2 = _input('Level2', 261.8)  # Уровень 2
Level3 = _input('Level3', 161.8)  # Уровень 3
Level4 = _input('Level4', 61.8)  # Уровень 4
Level5 = _input('Level5', 0.0)  # Уровень 5
Level6 = _input('Level6', -61.8)  # Уровень 6
Level7 = _input('Level7', -161.8)  # Уровень 7
Level8 = _input('Level8', -261.8)  # Уровень 8
Level9 = _input('Level9', -423.6)  # Уровень 9
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
        Print('Период графика для индикатора CMx не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'CMx', F, k, L_adx, 0, Level1, Level2, Level3, Level4, Level5, Level6, Level7, Level8, Level9)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CMx')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'CMx HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 9)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Level2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, Level3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, Level4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, Level5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, Level6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, Level7)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 7, Level8)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 8, Level9)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 5, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 6, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 7, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 8, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 5, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 6, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 7, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 8, STYLE_DASHDOTDOT)
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
        ColorIndBuffer[bar] = 2.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 2, Ind) <= 0:
                return 0
            IndBuffer[bar] = Ind[1]
            clr = 2
            if IndBuffer[bar] > 0:
                if Ind[1] > Ind[0]:
                    clr = 4
                if Ind[1] < Ind[0]:
                    clr = 3
            if IndBuffer[bar] < 0:
                if Ind[1] < Ind[0]:
                    clr = 0
                if Ind[1] > Ind[0]:
                    clr = 1
            ColorIndBuffer[bar] = clr
        if (ReDraw and IndBuffer[bar + 1] != EMPTY_VALUE) and IndBuffer[bar] == EMPTY_VALUE:
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


class CmxHtf(_MQL5Indicator):
    name = 'cmx_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'F': 12,
        'k': 1.682,
        'L_adx': 18.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Level1': 423.6,  # Уровень 1
        'Level2': 261.8,  # Уровень 2
        'Level3': 161.8,  # Уровень 3
        'Level4': 61.8,  # Уровень 4
        'Level5': 0.0,  # Уровень 5
        'Level6': -61.8,  # Уровень 6
        'Level7': -161.8,  # Уровень 7
        'Level8': -261.8,  # Уровень 8
        'Level9': -423.6,  # Уровень 9
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

