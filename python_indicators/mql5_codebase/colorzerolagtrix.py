"""colorzerolagtrix — converted from MQL5: MQL5 Indicators/ColorZerolagTriX/colorzerolagtrix.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [14822282], 2: [14822282], 3: [16748574, 9639167]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FastTrendLine', 2: 'SlowTrendLine', 3: 'ZerolagTriX'}, 'levels': [], 'description': [], 'name': 'colorzerolagtrix', 'source': 'MQL5 Indicators/ColorZerolagTriX/colorzerolagtrix.mq5', 'folder': 'ColorZerolagTriX', 'inputs': [{'mql': 'smoothing', 'py': 'smoothing', 'param': 'smoothing', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'TriX_period1', 'py': 'TriX_period1', 'param': 'TriX_period1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'TriX_period2', 'py': 'TriX_period2', 'param': 'TriX_period2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'TriX_period3', 'py': 'TriX_period3', 'param': 'TriX_period3', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'TriX_period4', 'py': 'TriX_period4', 'param': 'TriX_period4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'TriX_period5', 'py': 'TriX_period5', 'param': 'TriX_period5', 'type': 'uint', 'default': 89, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
smoothing = _input('smoothing', 15)
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Factor1 = _input('Factor1', 0.05)
TriX_period1 = _input('TriX_period1', 8)
Factor2 = _input('Factor2', 0.1)
TriX_period2 = _input('TriX_period2', 21)
Factor3 = _input('Factor3', 0.16)
TriX_period3 = _input('TriX_period3', 34)
Factor4 = _input('Factor4', 0.26)
TriX_period4 = _input('TriX_period4', 55)
Factor5 = _input('Factor5', 0.43)
TriX_period5 = _input('TriX_period5', 89)
StartBar = 0
smoothConst = 0.0
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
FastBuffer_ = Arr(0, 0.0)
SlowBuffer_ = Arr(0, 0.0)
TriX1_Handle = 0
TriX2_Handle = 0
TriX3_Handle = 0
TriX4_Handle = 0
TriX5_Handle = 0

def OnInit():
    global StartBar, TriX1_Handle, TriX2_Handle, TriX3_Handle, TriX4_Handle, TriX5_Handle, smoothConst
    smoothConst = (smoothing - 1.0) / smoothing
    PeriodBuffer = Arr(5, 0, dyn=False)
    PeriodBuffer[0] = TriX_period1
    PeriodBuffer[1] = TriX_period2
    PeriodBuffer[2] = TriX_period3
    PeriodBuffer[3] = TriX_period4
    PeriodBuffer[4] = TriX_period5
    StartBar = _int(3 * PeriodBuffer[ArrayMaximum(PeriodBuffer, 0, WHOLE_ARRAY)]) + 2
    TriX1_Handle = iTriX(None, 0, TriX_period1, IPC)
    if TriX1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTriX1')
        return INIT_FAILED
    TriX2_Handle = iTriX(None, 0, TriX_period2, IPC)
    if TriX2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTriX2')
        return INIT_FAILED
    TriX3_Handle = iTriX(None, 0, TriX_period3, IPC)
    if TriX3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTriX3')
        return INIT_FAILED
    TriX4_Handle = iTriX(None, 0, TriX_period4, IPC)
    if TriX4_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTriX4')
        return INIT_FAILED
    TriX5_Handle = iTriX(None, 0, TriX_period5, IPC)
    if TriX5_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTriX5')
        return INIT_FAILED
    SetIndexBuffer(0, FastBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(0, PLOT_LABEL, 'FastTrendLine')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(FastBuffer, True)
    SetIndexBuffer(1, SlowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(1, PLOT_LABEL, 'SlowTrendLine')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SlowBuffer, True)
    SetIndexBuffer(2, FastBuffer_, INDICATOR_DATA)
    ArraySetAsSeries(FastBuffer_, True)
    SetIndexBuffer(3, SlowBuffer_, INDICATOR_DATA)
    ArraySetAsSeries(SlowBuffer_, True)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(2, PLOT_LABEL, 'FastTrendLine')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'ZerolagTriX'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(TriX1_Handle) < rates_total or BarsCalculated(TriX2_Handle) < rates_total) or BarsCalculated(TriX3_Handle) < rates_total) or BarsCalculated(TriX4_Handle) < rates_total) or BarsCalculated(TriX5_Handle) < rates_total) or rates_total < StartBar:
        return 0
    Osc1 = 0.0
    Osc2 = 0.0
    Osc3 = 0.0
    Osc4 = 0.0
    Osc5 = 0.0
    FastTrend = 0.0
    SlowTrend = 0.0
    TriX1 = Arr(0, 0.0)
    TriX2 = Arr(0, 0.0)
    TriX3 = Arr(0, 0.0)
    TriX4 = Arr(0, 0.0)
    TriX5 = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBar - 2
        to_copy = limit + 2
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    ArraySetAsSeries(TriX1, True)
    ArraySetAsSeries(TriX2, True)
    ArraySetAsSeries(TriX3, True)
    ArraySetAsSeries(TriX4, True)
    ArraySetAsSeries(TriX5, True)
    if CopyBuffer(TriX1_Handle, 0, 0, to_copy, TriX1) <= 0:
        return 0
    if CopyBuffer(TriX2_Handle, 0, 0, to_copy, TriX2) <= 0:
        return 0
    if CopyBuffer(TriX3_Handle, 0, 0, to_copy, TriX3) <= 0:
        return 0
    if CopyBuffer(TriX4_Handle, 0, 0, to_copy, TriX4) <= 0:
        return 0
    if CopyBuffer(TriX5_Handle, 0, 0, to_copy, TriX5) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        bar = limit + 1
        Osc1 = Factor1 * TriX1[bar]
        Osc2 = Factor2 * TriX2[bar]
        Osc3 = Factor2 * TriX3[bar]
        Osc4 = Factor4 * TriX4[bar]
        Osc5 = Factor5 * TriX5[bar]
        FastTrend = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        FastBuffer_[bar] = FastTrend
        FastBuffer[bar] = FastBuffer_[bar]
        SlowBuffer_[bar] = FastTrend / smoothing
        SlowBuffer[bar] = SlowBuffer_[bar]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Osc1 = Factor1 * TriX1[bar]
        Osc2 = Factor2 * TriX2[bar]
        Osc3 = Factor2 * TriX3[bar]
        Osc4 = Factor4 * TriX4[bar]
        Osc5 = Factor5 * TriX5[bar]
        FastTrend = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        SlowTrend = (FastTrend / smoothing) + (SlowBuffer[bar + 1] * smoothConst)
        SlowBuffer[bar] = SlowTrend
        FastBuffer[bar] = FastTrend
        SlowBuffer_[bar] = SlowTrend
        FastBuffer_[bar] = FastTrend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorzerolagtrix(_MQL5Indicator):
    name = 'colorzerolagtrix'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'smoothing': 15,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Factor1': 0.05,
        'TriX_period1': 8,
        'Factor2': 0.1,
        'TriX_period2': 21,
        'Factor3': 0.16,
        'TriX_period3': 34,
        'Factor4': 0.26,
        'TriX_period4': 55,
        'Factor5': 0.43,
        'TriX_period5': 89,
    }

