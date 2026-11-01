"""colorzerolagrvi — converted from MQL5: MQL5 Indicators/ColorZerolagRVI_HTF/colorzerolagrvi.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [14822282], 2: [14822282], 3: [8388352, 255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FastTrendLine', 2: 'SlowTrendLine', 3: 'ZerolagRVI'}, 'levels': [], 'description': [], 'name': 'colorzerolagrvi', 'source': 'MQL5 Indicators/ColorZerolagRVI_HTF/colorzerolagrvi.mq5', 'folder': 'ColorZerolagRVI_HTF', 'inputs': [{'mql': 'smoothing', 'py': 'smoothing', 'param': 'smoothing', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'RVI_period1', 'py': 'RVI_period1', 'param': 'RVI_period1', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'RVI_period2', 'py': 'RVI_period2', 'param': 'RVI_period2', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'RVI_period3', 'py': 'RVI_period3', 'param': 'RVI_period3', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'RVI_period4', 'py': 'RVI_period4', 'param': 'RVI_period4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'RVI_period5', 'py': 'RVI_period5', 'param': 'RVI_period5', 'type': 'int', 'default': 89, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
smoothing = _input('smoothing', 15)
Factor1 = _input('Factor1', 0.05)
RVI_period1 = _input('RVI_period1', 8)
Factor2 = _input('Factor2', 0.1)
RVI_period2 = _input('RVI_period2', 21)
Factor3 = _input('Factor3', 0.16)
RVI_period3 = _input('RVI_period3', 34)
Factor4 = _input('Factor4', 0.26)
RVI_period4 = _input('RVI_period4', 55)
Factor5 = _input('Factor5', 0.43)
RVI_period5 = _input('RVI_period5', 89)
StartBar = 0
smoothConst = 0.0
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
FastBuffer_ = Arr(0, 0.0)
SlowBuffer_ = Arr(0, 0.0)
RVI1_Handle = 0
RVI2_Handle = 0
RVI3_Handle = 0
RVI4_Handle = 0
RVI5_Handle = 0

def OnInit():
    global RVI1_Handle, RVI2_Handle, RVI3_Handle, RVI4_Handle, RVI5_Handle, StartBar, smoothConst
    smoothConst = (smoothing - 1.0) / smoothing
    PeriodBuffer = Arr(5, 0, dyn=False)
    PeriodBuffer[0] = RVI_period1
    PeriodBuffer[1] = RVI_period2
    PeriodBuffer[2] = RVI_period3
    PeriodBuffer[3] = RVI_period4
    PeriodBuffer[4] = RVI_period5
    StartBar = PeriodBuffer[ArrayMaximum(PeriodBuffer, 0, WHOLE_ARRAY)] + 2
    RVI1_Handle = iRVI(None, 0, RVI_period1)
    if RVI1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI1')
    RVI2_Handle = iRVI(None, 0, RVI_period2)
    if RVI2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI2')
    RVI3_Handle = iRVI(None, 0, RVI_period3)
    if RVI3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI3')
    RVI4_Handle = iRVI(None, 0, RVI_period4)
    if RVI4_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI4')
    RVI5_Handle = iRVI(None, 0, RVI_period5)
    if RVI5_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI5')
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
    shortname = 'ZerolagRVI'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(RVI1_Handle) < rates_total or BarsCalculated(RVI2_Handle) < rates_total) or BarsCalculated(RVI3_Handle) < rates_total) or BarsCalculated(RVI4_Handle) < rates_total) or BarsCalculated(RVI5_Handle) < rates_total) or rates_total < StartBar:
        return 0
    Osc1 = 0.0
    Osc2 = 0.0
    Osc3 = 0.0
    Osc4 = 0.0
    Osc5 = 0.0
    FastTrend = 0.0
    SlowTrend = 0.0
    RVI1 = Arr(0, 0.0)
    RVI2 = Arr(0, 0.0)
    RVI3 = Arr(0, 0.0)
    RVI4 = Arr(0, 0.0)
    RVI5 = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBar - 2
        to_copy = limit + 2
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    ArraySetAsSeries(RVI1, True)
    ArraySetAsSeries(RVI2, True)
    ArraySetAsSeries(RVI3, True)
    ArraySetAsSeries(RVI4, True)
    ArraySetAsSeries(RVI5, True)
    if CopyBuffer(RVI1_Handle, 0, 0, to_copy, RVI1) <= 0:
        return 0
    if CopyBuffer(RVI2_Handle, 0, 0, to_copy, RVI2) <= 0:
        return 0
    if CopyBuffer(RVI3_Handle, 0, 0, to_copy, RVI3) <= 0:
        return 0
    if CopyBuffer(RVI4_Handle, 0, 0, to_copy, RVI4) <= 0:
        return 0
    if CopyBuffer(RVI5_Handle, 0, 0, to_copy, RVI5) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        bar = limit + 1
        Osc1 = Factor1 * RVI1[bar]
        Osc2 = Factor2 * RVI2[bar]
        Osc3 = Factor2 * RVI3[bar]
        Osc4 = Factor4 * RVI4[bar]
        Osc5 = Factor5 * RVI5[bar]
        FastTrend = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        FastBuffer_[bar] = FastTrend
        FastBuffer[bar] = FastBuffer_[bar]
        SlowBuffer_[bar] = FastTrend / smoothing
        SlowBuffer[bar] = SlowBuffer_[bar]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Osc1 = Factor1 * RVI1[bar]
        Osc2 = Factor2 * RVI2[bar]
        Osc3 = Factor2 * RVI3[bar]
        Osc4 = Factor4 * RVI4[bar]
        Osc5 = Factor5 * RVI5[bar]
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


class Colorzerolagrvi(_MQL5Indicator):
    name = 'colorzerolagrvi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'smoothing': 15,
        'Factor1': 0.05,
        'RVI_period1': 8,
        'Factor2': 0.1,
        'RVI_period2': 21,
        'Factor3': 0.16,
        'RVI_period3': 34,
        'Factor4': 0.26,
        'RVI_period4': 55,
        'Factor5': 0.43,
        'RVI_period5': 89,
    }

