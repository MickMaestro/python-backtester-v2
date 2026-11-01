"""trvi — converted from MQL5: MQL5 Indicators/Color RMACD/trvi.mq5

True RVI
Copyright: Copyright © 2010, VladMsk, contact@mqlsoft.com; Link: http://www.becemal.ru/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, VladMsk, contact@mqlsoft.com', 'link': 'http://www.becemal.ru/', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [9639167], 2: [16748574]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TRVI', 2: 'Signal'}, 'levels': [], 'description': ['True RVI'], 'name': 'trvi', 'source': 'MQL5 Indicators/Color RMACD/trvi.mq5', 'folder': 'Color RMACD', 'inputs': [{'mql': 'TRVIPeriod', 'py': 'TRVIPeriod', 'param': 'TRVIPeriod', 'type': 'uint', 'default': 10, 'label': 'TRVI period', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TRVIPeriod = _input('TRVIPeriod', 10)  # TRVI period
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
TRVIBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
min_rates_total = 0

def CountVal(B, A, V, tV, Type, ii):
    if VolumeType == VOLUME_TICK:
        return (tV[ii] * (A[ii] - B[ii])) + (8 * tV[ii - 1] * (A[ii - 1] - B[ii - 1])) + (8 * tV[ii - 2] * (A[ii - 2] - B[ii - 2])) + (tV[ii - 3] * (A[ii - 3] - B[ii - 3]))
    else:
        return (V[ii] * (A[ii] - B[ii])) + (8 * V[ii - 1] * (A[ii - 1] - B[ii - 1])) + (8 * V[ii - 2] * (A[ii - 2] - B[ii - 2])) + (V[ii - 3] * (A[ii - 3] - B[ii - 3]))

def OnInit():
    global min_rates_total
    min_rates_total = _int(TRVIPeriod + 8)
    SetIndexBuffer(0, TRVIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'TRVI(', TRVIPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Norm = 0
    rrr = 0
    kkk = 0
    dNum = 0.0
    dDeNum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = _int(TRVIPeriod + 4)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dNum = 0.0
        dDeNum = 0.0
        kkk = 0
        for kkk in range(kkk, _int(TRVIPeriod)):
            rrr = bar - kkk
            Norm = _int(TRVIPeriod) - kkk + 1
            dNum += Norm * CountVal(open, close, volume, tick_volume, VolumeType, rrr)
            dDeNum += Norm * CountVal(low, high, volume, tick_volume, VolumeType, rrr)
        else:
            kkk = _range_end(kkk, _int(TRVIPeriod), 1)
        if dDeNum != 0.0:
            TRVIBuffer[bar] = _fdiv(dNum, dDeNum)
        else:
            TRVIBuffer[bar] = dNum
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 4
    bar = first
    for bar in range(bar, rates_total):
        SignalBuffer[bar] = ((4 * TRVIBuffer[bar]) + (3 * TRVIBuffer[bar - 1]) + (2 * TRVIBuffer[bar - 2]) + TRVIBuffer[bar - 3]) / 10
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trvi(_MQL5Indicator):
    name = 'trvi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TRVIPeriod': 10,  # TRVI period
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

