"""LSMA_Angle_HTF — converted from MQL5: MQL5 Indicators/LSMA_Angle_HTF/LSMA_Angle_HTF.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 15631086, 8421504, 16748574, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LSMA_Angle'}, 'levels': [], 'description': [], 'name': 'LSMA_Angle_HTF', 'source': 'MQL5 Indicators/LSMA_Angle_HTF/LSMA_Angle_HTF.mq5', 'folder': 'LSMA_Angle_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'LSMAPeriod', 'py': 'LSMAPeriod', 'param': 'LSMAPeriod', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'AngleTreshold', 'py': 'AngleTreshold', 'param': 'AngleTreshold', 'type': 'int', 'default': 15, 'label': 'Порог срабатывания', 'sinput': False}, {'mql': 'StartLSMAShift', 'py': 'StartLSMAShift', 'param': 'StartLSMAShift', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'EndLSMAShift', 'py': 'EndLSMAShift', 'param': 'EndLSMAShift', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
LSMAPeriod = _input('LSMAPeriod', 25)
AngleTreshold = _input('AngleTreshold', 15)  # Порог срабатывания
StartLSMAShift = _input('StartLSMAShift', 4)
EndLSMAShift = _input('EndLSMAShift', 0)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
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
        Print('Период графика для индикатора LSMA_Angle не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'LSMA_Angle', LSMAPeriod, AngleTreshold, StartLSMAShift, EndLSMAShift)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора LSMA_Angle')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LSMA_Angle HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, AngleTreshold)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -AngleTreshold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
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


class LSMAAngleHTF(_MQL5Indicator):
    name = 'LSMA_Angle_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'LSMAPeriod': 25,
        'AngleTreshold': 15,  # Порог срабатывания
        'StartLSMAShift': 4,
        'EndLSMAShift': 0,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

