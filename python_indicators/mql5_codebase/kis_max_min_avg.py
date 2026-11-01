"""KiS_max_min_Avg — converted from MQL5: MQL5 Indicators/KiS_max_min_Avg/KiS_max_min_Avg.mq5

Copyright: Copyright © 2009, KCBT; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, KCBT', 'link': '', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 8, 5: 1}, 'colors': {1: [13688896], 2: [14053594], 3: [32768], 4: [16711680, 255], 5: [16711935]}, 'widths': {3: 1, 4: 3, 5: 1}, 'styles': {3: 0, 4: 0, 5: 0}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud', 3: 'Upper PC Channel', 4: 'Middle PC Channel', 5: 'Lower PC Channel'}, 'levels': [], 'description': [], 'name': 'KiS_max_min_Avg', 'source': 'MQL5 Indicators/KiS_max_min_Avg/KiS_max_min_Avg.mq5', 'folder': 'KiS_max_min_Avg', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
ColorMiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
UpBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, UpBuffer2, INDICATOR_DATA)
    SetIndexBuffer(1, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, DnBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(6, ColorMiddleBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'KiS_max_min_Avg'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global _s_OnCalculate_BarCount_prev, _s_OnCalculate_Color_prev, _s_OnCalculate_CurDay_prev, _s_OnCalculate_DayMax_prev, _s_OnCalculate_DayMin_prev, _s_OnCalculate_lastbar
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    CurDay = 0
    Color = 0
    BarCount = 0
    DayMax = 0.0
    DayMin = 0.0
    DayOpen = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_BarCount_prev = 0
        _s_OnCalculate_DayMax_prev = 0.0
        _s_OnCalculate_DayMin_prev = 999999999.0
        Color = 0
        _s_OnCalculate_Color_prev = 0
        _s_OnCalculate_CurDay_prev = 0
        CurDay = 0
    else:
        first = prev_calculated - 1
    DayMin = _s_OnCalculate_DayMin_prev
    DayMax = _s_OnCalculate_DayMax_prev
    BarCount = _s_OnCalculate_BarCount_prev
    CurDay = _s_OnCalculate_CurDay_prev
    Color = _s_OnCalculate_Color_prev
    bar = first
    for bar in range(bar, rates_total):
        str_ = MqlDateTime()
        TimeToStruct(Time[bar], str_)
        if CurDay != str_.day:
            for iii in range(BarCount, 0 - 1, -1):
                barx = bar - iii
                UpperBuffer[barx] = _s_OnCalculate_DayMax_prev
                UpBuffer2[barx] = UpperBuffer[barx]
                MiddleBuffer[barx] = (_s_OnCalculate_DayMax_prev + _s_OnCalculate_DayMin_prev) / 2
                DnBuffer1[barx] = MiddleBuffer[barx]
                UpBuffer1[barx] = DnBuffer1[barx]
                LowerBuffer[barx] = _s_OnCalculate_DayMin_prev
                DnBuffer2[barx] = LowerBuffer[barx]
                if iii == BarCount:
                    if MiddleBuffer[barx - 1] < MiddleBuffer[barx]:
                        Color = 0
                    elif MiddleBuffer[barx - 1] > MiddleBuffer[barx]:
                        Color = 1
                ColorMiddleBuffer[barx] = Color
                _s_OnCalculate_lastbar = bar
            CurDay = str_.day
            BarCount = 0
            DayMax = 0.0
            DayMin = 999999999.0
            DayOpen = Open[bar]
        else:
            barx = bar - 1
            UpperBuffer[bar] = UpBuffer2[barx]
            UpBuffer2[bar] = UpperBuffer[bar]
            MiddleBuffer[bar] = UpBuffer1[barx]
            DnBuffer1[bar] = MiddleBuffer[bar]
            UpBuffer1[bar] = DnBuffer1[bar]
            LowerBuffer[bar] = DnBuffer2[barx]
            DnBuffer2[bar] = LowerBuffer[bar]
            ColorMiddleBuffer[bar] = ColorMiddleBuffer[barx]
        if DayMax < High[bar]:
            DayMax = High[bar]
        if DayMin > Low[bar]:
            DayMin = Low[bar]
        BarCount += 1
        BarCount = MathMin(rates_total - 1, BarCount)
        if bar < (rates_total - 1):
            _s_OnCalculate_BarCount_prev = BarCount
            _s_OnCalculate_DayMax_prev = DayMax
            _s_OnCalculate_DayMin_prev = DayMin
            _s_OnCalculate_Color_prev = Color
            _s_OnCalculate_CurDay_prev = CurDay
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = rates_total - BarCount - 1
    for bar in range(bar, rates_total):
        UpperBuffer[bar] = DayMax
        UpBuffer2[bar] = UpperBuffer[bar]
        MiddleBuffer[bar] = (DayMax + DayMin) / 2
        DnBuffer1[bar] = MiddleBuffer[bar]
        UpBuffer1[bar] = DnBuffer1[bar]
        LowerBuffer[bar] = DayMin
        DnBuffer2[bar] = LowerBuffer[bar]
        if bar == (rates_total - BarCount - 1):
            if MiddleBuffer[bar - 1] < MiddleBuffer[bar]:
                Color = 0
            elif MiddleBuffer[bar - 1] > MiddleBuffer[bar]:
                Color = 1
        else:
            Color = _int(ColorMiddleBuffer[bar - 1])
        ColorMiddleBuffer[bar] = Color
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_BarCount_prev = 0
_s_OnCalculate_Color_prev = 0
_s_OnCalculate_CurDay_prev = 0
_s_OnCalculate_lastbar = 0
_s_OnCalculate_DayMax_prev = 0.0
_s_OnCalculate_DayMin_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KiSMaxMinAvg(_MQL5Indicator):
    name = 'KiS_max_min_Avg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

