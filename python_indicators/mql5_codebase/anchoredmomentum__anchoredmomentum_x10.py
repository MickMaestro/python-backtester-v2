"""AnchoredMomentum — converted from MQL5: MQL5 Indicators/AnchoredMomentum_x10/AnchoredMomentum.mq5

Copyright: Copyright © 2010, Umnyashkin Victor; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Umnyashkin Victor', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 5, 3: 5, 4: 5}, 'colors': {1: [8421504], 2: [8388352], 3: [9639167], 4: [8421504]}, 'widths': {1: 1, 2: 3, 3: 3, 4: 3}, 'styles': {1: 0}, 'labels': {1: 'Momentum', 2: 'Up_Signal', 3: 'Dn_Signal', 4: 'No_Signal'}, 'levels': [], 'description': [], 'name': 'AnchoredMomentum', 'source': 'MQL5 Indicators/AnchoredMomentum_x10/AnchoredMomentum.mq5', 'folder': 'AnchoredMomentum_x10', 'inputs': [{'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 8, 'label': 'период SMA', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'uint', 'default': 6, 'label': 'период EMA', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа, по которой производится расчёт индикатора', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'double', 'default': 0.025, 'label': 'верхний пробойный уровень', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'double', 'default': -0.025, 'label': 'нижний пробойный уровень', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MomPeriod = _input('MomPeriod', 8)  # период SMA
SmoothPeriod = _input('SmoothPeriod', 6)  # период EMA
IPC = _input('IPC', PRICE_CLOSE)  # ценовая константа, по которой производится расчёт индикатора
UpLevel = _input('UpLevel', 0.025)  # верхний пробойный уровень
DnLevel = _input('DnLevel', -0.025)  # нижний пробойный уровень
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
MomBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
FlBuffer = Arr(0, 0.0)
SMA_Handle = 0
EMA_Handle = 0
min_rates_total = 0

def OnInit():
    global EMA_Handle, SMA_Handle, min_rates_total
    SMA_Handle = iMA(None, 0, MomPeriod, 0, MODE_SMA, IPC)
    if SMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SMA')
    EMA_Handle = iMA(None, 0, MomPeriod, 0, MODE_EMA, IPC)
    if EMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора EMA')
    min_rates_total = _int(MomPeriod)
    SetIndexBuffer(0, MomBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MomBuffer, True)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(2, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(3, FlBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(3, PLOT_LABEL, 'No Signal')
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(FlBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Momentum(', MomPeriod, ', ', SmoothPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(SMA_Handle) < rates_total or BarsCalculated(EMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    res = 0.0
    Momentum = 0.0
    SMA = Arr(0, 0.0)
    EMA = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(SMA_Handle, 0, 0, to_copy, SMA) <= 0:
        return 0
    if CopyBuffer(EMA_Handle, 0, 0, to_copy, EMA) <= 0:
        return 0
    ArraySetAsSeries(SMA, True)
    ArraySetAsSeries(EMA, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = SMA[bar]
        if res:
            Momentum = 100 * (_fdiv(EMA[bar], SMA[bar]) - 1)
        else:
            Momentum = EMPTY_VALUE
        MomBuffer[bar] = Momentum
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        FlBuffer[bar] = EMPTY_VALUE
        if Momentum == EMPTY_VALUE:
            continue
        if Momentum > UpLevel:
            UpBuffer[bar] = Momentum
        elif Momentum < DnLevel:
            DnBuffer[bar] = Momentum
        else:
            FlBuffer[bar] = Momentum
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AnchoredMomentum(_MQL5Indicator):
    name = 'AnchoredMomentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MomPeriod': 8,  # период SMA
        'SmoothPeriod': 6,  # период EMA
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # ценовая константа, по которой производится расчёт индикатора
        'UpLevel': 0.025,  # верхний пробойный уровень
        'DnLevel': -0.025,  # нижний пробойный уровень
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

