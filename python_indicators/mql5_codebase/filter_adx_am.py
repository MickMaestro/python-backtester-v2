"""FILTER_ADX_AM — converted from MQL5: MQL5 Indicators/FILTER_ADX_AM/FILTER_ADX_AM.mq5

Copyright: Copyright © 2009, Andrey Matvievskiy; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Andrey Matvievskiy', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 3, 2: 3, 3: 3, 4: 3}, 'colors': {1: [65280], 2: [255], 3: [65280], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 3, 4: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Weak Upper Trend', 2: 'Weak Lower Trend', 3: 'Stronge Upper Trend', 4: 'Stronge Lower Trend'}, 'levels': [], 'description': [], 'name': 'FILTER_ADX_AM', 'source': 'MQL5 Indicators/FILTER_ADX_AM/FILTER_ADX_AM.mq5', 'folder': 'FILTER_ADX_AM', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 0.33, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 14)
alpha1 = _input('alpha1', 0.25)
alpha2 = _input('alpha2', 0.33)
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
ADX_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, min_rates_total
    ADX_Handle = iADX(None, 0, period)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ADX')
        return INIT_FAILED
    min_rates_total = period + 2
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtMapBuffer1, True)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtMapBuffer2, True)
    SetIndexBuffer(2, ExtMapBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtMapBuffer3, True)
    SetIndexBuffer(3, ExtMapBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtMapBuffer4, True)
    shortname = Box("")
    StringConcatenate(shortname, 'FILTER_ADX_AM(', period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Adx_prev, _s_OnCalculate_DiMinus_prev, _s_OnCalculate_DiPlus_prev, _s_OnCalculate_xAdx_prev, _s_OnCalculate_xDiMinus_prev, _s_OnCalculate_xDiPlus_prev
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    ADX = Arr(0, 0.0)
    DIP = Arr(0, 0.0)
    DIM = Arr(0, 0.0)
    DiPlus = 0.0
    DiMinus = 0.0
    Adx = 0.0
    xDiPlus = 0.0
    xDiMinus = 0.0
    xAdx = 0.0
    ArraySetAsSeries(ADX, True)
    ArraySetAsSeries(DIP, True)
    ArraySetAsSeries(DIM, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        _s_OnCalculate_xAdx_prev = 0.0
        _s_OnCalculate_xDiMinus_prev = _s_OnCalculate_xAdx_prev
        _s_OnCalculate_xDiPlus_prev = _s_OnCalculate_xDiMinus_prev
        _s_OnCalculate_Adx_prev = _s_OnCalculate_xDiPlus_prev
        _s_OnCalculate_DiMinus_prev = _s_OnCalculate_Adx_prev
        _s_OnCalculate_DiPlus_prev = _s_OnCalculate_DiMinus_prev
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX_Handle, 0, 0, to_copy, ADX) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, DIP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, DIM) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBuffer1[bar] = 0.0
        ExtMapBuffer2[bar] = ExtMapBuffer1[bar]
        ExtMapBuffer3[bar] = ExtMapBuffer2[bar]
        ExtMapBuffer4[bar] = ExtMapBuffer3[bar]
        DiPlus = (2 * DIP[bar]) + ((alpha1 - 2) * DIP[bar + 1]) + ((1 - alpha1) * _s_OnCalculate_DiPlus_prev)
        DiMinus = (2 * DIM[bar]) + ((alpha1 - 2) * DIM[bar + 1]) + ((1 - alpha1) * _s_OnCalculate_DiMinus_prev)
        Adx = (2 * ADX[bar]) + ((alpha1 - 2) * ADX[bar + 1]) + ((1 - alpha1) * _s_OnCalculate_Adx_prev)
        xDiPlus = (alpha2 * DiPlus) + ((1 - alpha2) * _s_OnCalculate_xDiPlus_prev)
        xDiMinus = (alpha2 * DiMinus) + ((1 - alpha2) * _s_OnCalculate_xDiMinus_prev)
        xAdx = (alpha2 * Adx) + ((1 - alpha2) * _s_OnCalculate_xAdx_prev)
        if xDiPlus < xDiMinus:
            if xAdx >= _s_OnCalculate_xAdx_prev:
                ExtMapBuffer4[bar] = 1.0
            else:
                ExtMapBuffer2[bar] = 1.0
        if xDiPlus > xDiMinus:
            if xAdx >= _s_OnCalculate_xAdx_prev:
                ExtMapBuffer3[bar] = 1.0
            else:
                ExtMapBuffer1[bar] = 1.0
        if bar:
            _s_OnCalculate_DiPlus_prev = DiPlus
            _s_OnCalculate_DiMinus_prev = DiMinus
            _s_OnCalculate_Adx_prev = Adx
            _s_OnCalculate_xDiPlus_prev = xDiPlus
            _s_OnCalculate_xDiMinus_prev = xDiMinus
            _s_OnCalculate_xAdx_prev = xAdx
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_DiPlus_prev = 0.0
_s_OnCalculate_DiMinus_prev = 0.0
_s_OnCalculate_Adx_prev = 0.0
_s_OnCalculate_xDiPlus_prev = 0.0
_s_OnCalculate_xDiMinus_prev = 0.0
_s_OnCalculate_xAdx_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FILTERADXAM(_MQL5Indicator):
    name = 'FILTER_ADX_AM'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 14,
        'alpha1': 0.25,
        'alpha2': 0.33,
    }
    y_range = (0.0, 1.0)

