"""Delta_WPR — converted from MQL5: MQL5 Indicators/Delta_WPR/Delta_WPR.mq5

Copyright: Copyright 2016, Tor; Link: http://einvestor.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Tor', 'link': 'http://einvestor.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 8421504, 36095]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Delta_WPR'}, 'levels': [], 'description': [], 'name': 'Delta_WPR', 'source': 'MQL5 Indicators/Delta_WPR/Delta_WPR.mq5', 'folder': 'Delta_WPR', 'inputs': [{'mql': 'TypeGr', 'py': 'TypeGr', 'param': 'TypeGr', 'type': 'int', 'default': 0, 'label': 'Type graph', 'sinput': False}, {'mql': 'WPRPeriod1', 'py': 'WPRPeriod1', 'param': 'WPRPeriod1', 'type': 'uint', 'default': 14, 'label': 'Fast WPR Period', 'sinput': False}, {'mql': 'WPRPeriod2', 'py': 'WPRPeriod2', 'param': 'WPRPeriod2', 'type': 'uint', 'default': 30, 'label': 'Slow WPR Period', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'int', 'default': -50, 'label': 'Signal Level', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum TypeGraph
Histogram = 0
Cute = 1
_enum('TypeGraph', {0: 'Histogram', 1: 'Cute'})

# ---- inputs and global variables
TypeGr = _input('TypeGr', Histogram)  # Type graph
WPRPeriod1 = _input('WPRPeriod1', 14)  # Fast WPR Period
WPRPeriod2 = _input('WPRPeriod2', 30)  # Slow WPR Period
Level = _input('Level', -50)  # Signal Level
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
wpr1 = Arr(0, 0.0)
wpr2 = Arr(0, 0.0)
delta = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Ind1_Handle = 0
Ind2_Handle = 0
min_rates_total = 0
maxLevel = 0
minLevel = 0

def OnInit():
    global Ind1_Handle, Ind2_Handle, maxLevel, minLevel, min_rates_total
    Ind1_Handle = iWPR(Symbol(), PERIOD_CURRENT, WPRPeriod1)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора WPR 1')
        return INIT_FAILED
    Ind2_Handle = iWPR(Symbol(), PERIOD_CURRENT, WPRPeriod2)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора WPR 2')
        return INIT_FAILED
    min_rates_total = _int(MathMax(WPRPeriod1, WPRPeriod2))
    maxLevel = -100 - (-100 - Level)
    minLevel = -100 - Level
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, wpr1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, wpr2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, delta, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    ArraySetAsSeries(wpr1, True)
    ArraySetAsSeries(wpr2, True)
    ArraySetAsSeries(delta, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Delta_WPR(', WPRPeriod1, ',', WPRPeriod2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Ind1_Handle) < rates_total or BarsCalculated(Ind2_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind1_Handle, 0, 0, to_copy, wpr1) <= 0:
        return 0
    if CopyBuffer(Ind2_Handle, 0, 0, to_copy, wpr2) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        delta[bar] = wpr1[bar] - wpr2[bar]
        if TypeGr == Cute:
            IndBuffer[bar] = 1.0
        else:
            IndBuffer[bar] = delta[bar]
        clr = 1
        if wpr2[bar] > maxLevel and wpr1[bar] > wpr2[bar]:
            clr = 0
        if wpr2[bar] < minLevel and wpr1[bar] < wpr2[bar]:
            clr = 2
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeltaWPR(_MQL5Indicator):
    name = 'Delta_WPR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TypeGr': _Choice({0: 'Full Histogram', 1: 'Cute Histogram'}, default=0),  # Type graph
        'WPRPeriod1': 14,  # Fast WPR Period
        'WPRPeriod2': 30,  # Slow WPR Period
        'Level': -50,  # Signal Level
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

