"""colorzerolagjjrsx — converted from MQL5: MQL5 Indicators/ColorZerolagJJRSX_HTF/colorzerolagjjrsx.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [14822282], 2: [14822282], 3: [13749760, 9639167]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FastTrendLine', 2: 'SlowTrendLine', 3: 'ZerolagJJRSX'}, 'levels': [0.5, -0.5, 0.0], 'description': [], 'name': 'colorzerolagjjrsx', 'source': 'MQL5 Indicators/ColorZerolagJJRSX_HTF/colorzerolagjjrsx.mq5', 'folder': 'ColorZerolagJJRSX_HTF', 'inputs': [{'mql': 'smoothing', 'py': 'smoothing', 'param': 'smoothing', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 8, 'label': 'Глубина JJMA усреднения', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'Параметр JJMA усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'JJRSX_period1', 'py': 'JJRSX_period1', 'param': 'JJRSX_period1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'JJRSX_period2', 'py': 'JJRSX_period2', 'param': 'JJRSX_period2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'JJRSX_period3', 'py': 'JJRSX_period3', 'param': 'JJRSX_period3', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'JJRSX_period4', 'py': 'JJRSX_period4', 'param': 'JJRSX_period4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'JJRSX_period5', 'py': 'JJRSX_period5', 'param': 'JJRSX_period5', 'type': 'uint', 'default': 89, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
smoothing = _input('smoothing', 15)
Smooth = _input('Smooth', 8)  # Глубина JJMA усреднения
JPhase = _input('JPhase', 100)  # Параметр JJMA усреднения
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Factor1 = _input('Factor1', 0.05)
JJRSX_period1 = _input('JJRSX_period1', 8)
Factor2 = _input('Factor2', 0.1)
JJRSX_period2 = _input('JJRSX_period2', 21)
Factor3 = _input('Factor3', 0.16)
JJRSX_period3 = _input('JJRSX_period3', 34)
Factor4 = _input('Factor4', 0.26)
JJRSX_period4 = _input('JJRSX_period4', 55)
Factor5 = _input('Factor5', 0.43)
JJRSX_period5 = _input('JJRSX_period5', 89)
StartBar = 0
smoothConst = 0.0
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
FastBuffer_ = Arr(0, 0.0)
SlowBuffer_ = Arr(0, 0.0)
JJRSX1_Handle = 0
JJRSX2_Handle = 0
JJRSX3_Handle = 0
JJRSX4_Handle = 0
JJRSX5_Handle = 0

def OnInit():
    global JJRSX1_Handle, JJRSX2_Handle, JJRSX3_Handle, JJRSX4_Handle, JJRSX5_Handle, StartBar, smoothConst
    smoothConst = (smoothing - 1.0) / smoothing
    StartBar = (3 * 32) + 2
    JJRSX1_Handle = iCustom(None, 0, 'JJRSX', JJRSX_period1, Smooth, JPhase, IPC, 0)
    if JJRSX1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJJRSX1')
        return INIT_FAILED
    JJRSX2_Handle = iCustom(None, 0, 'JJRSX', JJRSX_period2, Smooth, JPhase, IPC, 0)
    if JJRSX2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJJRSX2')
        return INIT_FAILED
    JJRSX3_Handle = iCustom(None, 0, 'JJRSX', JJRSX_period3, Smooth, JPhase, IPC, 0)
    if JJRSX3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJJRSX3')
        return INIT_FAILED
    JJRSX4_Handle = iCustom(None, 0, 'JJRSX', JJRSX_period4, Smooth, JPhase, IPC, 0)
    if JJRSX4_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJJRSX4')
        return INIT_FAILED
    JJRSX5_Handle = iCustom(None, 0, 'JJRSX', JJRSX_period5, Smooth, JPhase, IPC, 0)
    if JJRSX5_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJJRSX5')
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
    shortname = 'ZerolagJJRSX'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(JJRSX1_Handle) < rates_total or BarsCalculated(JJRSX2_Handle) < rates_total) or BarsCalculated(JJRSX3_Handle) < rates_total) or BarsCalculated(JJRSX4_Handle) < rates_total) or BarsCalculated(JJRSX5_Handle) < rates_total) or rates_total < StartBar:
        return 0
    Osc1 = 0.0
    Osc2 = 0.0
    Osc3 = 0.0
    Osc4 = 0.0
    Osc5 = 0.0
    FastTrend = 0.0
    SlowTrend = 0.0
    JJRSX1 = Arr(0, 0.0)
    JJRSX2 = Arr(0, 0.0)
    JJRSX3 = Arr(0, 0.0)
    JJRSX4 = Arr(0, 0.0)
    JJRSX5 = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBar - 2
        to_copy = limit + 2
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    ArraySetAsSeries(JJRSX1, True)
    ArraySetAsSeries(JJRSX2, True)
    ArraySetAsSeries(JJRSX3, True)
    ArraySetAsSeries(JJRSX4, True)
    ArraySetAsSeries(JJRSX5, True)
    if CopyBuffer(JJRSX1_Handle, 0, 0, to_copy, JJRSX1) <= 0:
        return 0
    if CopyBuffer(JJRSX2_Handle, 0, 0, to_copy, JJRSX2) <= 0:
        return 0
    if CopyBuffer(JJRSX3_Handle, 0, 0, to_copy, JJRSX3) <= 0:
        return 0
    if CopyBuffer(JJRSX4_Handle, 0, 0, to_copy, JJRSX4) <= 0:
        return 0
    if CopyBuffer(JJRSX5_Handle, 0, 0, to_copy, JJRSX5) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        bar = limit + 1
        Osc1 = Factor1 * JJRSX1[bar]
        Osc2 = Factor2 * JJRSX2[bar]
        Osc3 = Factor2 * JJRSX3[bar]
        Osc4 = Factor4 * JJRSX4[bar]
        Osc5 = Factor5 * JJRSX5[bar]
        FastTrend = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        FastBuffer_[bar] = FastTrend
        FastBuffer[bar] = FastBuffer_[bar]
        SlowBuffer_[bar] = FastTrend / smoothing
        SlowBuffer[bar] = SlowBuffer_[bar]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Osc1 = Factor1 * JJRSX1[bar]
        Osc2 = Factor2 * JJRSX2[bar]
        Osc3 = Factor2 * JJRSX3[bar]
        Osc4 = Factor4 * JJRSX4[bar]
        Osc5 = Factor5 * JJRSX5[bar]
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


class Colorzerolagjjrsx(_MQL5Indicator):
    name = 'colorzerolagjjrsx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'smoothing': 15,
        'Smooth': 8,  # Глубина JJMA усреднения
        'JPhase': 100,  # Параметр JJMA усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Factor1': 0.05,
        'JJRSX_period1': 8,
        'Factor2': 0.1,
        'JJRSX_period2': 21,
        'Factor3': 0.16,
        'JJRSX_period3': 34,
        'Factor4': 0.26,
        'JJRSX_period4': 55,
        'Factor5': 0.43,
        'JJRSX_period5': 89,
    }

