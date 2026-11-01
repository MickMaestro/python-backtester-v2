"""wprfast — converted from MQL5: MQL5 Indicators/WPRfast/wprfast.mq5

Copyright: Copyright © 2007, OlegVS; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, OlegVS', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.9, 'indicator_minimum': 0.3}, 'types': {1: 12}, 'colors': {1: [16748574, 16711935]}, 'widths': {1: 4}, 'styles': {}, 'labels': {1: 'WPRfast'}, 'levels': [1.0], 'description': [], 'name': 'wprfast', 'source': 'MQL5 Indicators/WPRfast/wprfast.mq5', 'folder': 'WPRfast', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 9, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Max', 'py': 'Max', 'param': 'Max', 'type': 'uint', 'default': 49, 'label': 'Верхний уровень срабатывания', 'sinput': False}, {'mql': 'Min', 'py': 'Min', 'param': 'Min', 'type': 'uint', 'default': 9, 'label': 'Нижний уровень срабатывания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 9)  # Период индикатора
Max = _input('Max', 49)  # Верхний уровень срабатывания
Min = _input('Min', 9)  # Нижний уровень срабатывания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = _int(iPeriod)
    Ind_Handle = iWPR(Symbol(), PERIOD_CURRENT, iPeriod)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора WPR')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPRfast')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return rates_total
    to_copy = 0
    limit = 0
    bar = 0
    V1 = 0.0
    V2 = 0.0
    WPR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(WPR, True)
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 0.0
        ColorIndBuffer[bar] = 0.0
        V1 = (WPR[bar] * WPR[bar]) / 100
        V2 = MathCeil(V1)
        if V2 < Min:
            IndBuffer[bar] = 1.0
            ColorIndBuffer[bar] = 0.0
        if V2 > Max:
            IndBuffer[bar] = 1.0
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wprfast(_MQL5Indicator):
    name = 'wprfast'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 9,  # Период индикатора
        'Max': 49,  # Верхний уровень срабатывания
        'Min': 9,  # Нижний уровень срабатывания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (0.3, 1.9)

