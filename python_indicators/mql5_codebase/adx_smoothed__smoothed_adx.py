"""adx_smoothed — converted from MQL5: MQL5 Indicators/Smoothed ADX/adx_smoothed.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Di Plus', 2: 'Di Minus', 3: 'ADX'}, 'levels': [88.0, 50.0, 12.0], 'description': [], 'name': 'adx_smoothed', 'source': 'MQL5 Indicators/Smoothed ADX/adx_smoothed.mq5', 'folder': 'Smoothed ADX', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 0.33, 'label': '', 'sinput': False}, {'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 14)
alpha1 = _input('alpha1', 0.25)
alpha2 = _input('alpha2', 0.33)
PriceType = _input('PriceType', 0)
DiPlusBuffer = Arr(0, 0.0)
DiMinusBuffer = Arr(0, 0.0)
ADXBuffer = Arr(0, 0.0)
ADX_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, min_rates_total
    ADX_Handle = iADX(None, 0, period)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX indicator')
    min_rates_total = period + 1
    SetIndexBuffer(0, DiPlusBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DiPlusBuffer, True)
    SetIndexBuffer(1, DiMinusBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DiMinusBuffer, True)
    SetIndexBuffer(2, ADXBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ADXBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ADX(', period, ')smothed')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Adx_, _s_OnCalculate_DiMinus_, _s_OnCalculate_DiPlus_
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
    ArraySetAsSeries(ADX, True)
    ArraySetAsSeries(DIP, True)
    ArraySetAsSeries(DIM, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        _s_OnCalculate_DiPlus_ = 0.0
        _s_OnCalculate_DiMinus_ = 0.0
        _s_OnCalculate_Adx_ = 0.0
        DiPlusBuffer[rates_total - 1] = 0.0
        DiMinusBuffer[rates_total - 1] = 0.0
        ADXBuffer[rates_total - 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX_Handle, 0, 0, to_copy, ADX) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, DIP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, DIM) <= 0:
        return 0
    DiPlus = _s_OnCalculate_DiPlus_
    DiMinus = _s_OnCalculate_DiMinus_
    Adx = _s_OnCalculate_Adx_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_DiPlus_ = DiPlus
            _s_OnCalculate_DiMinus_ = DiMinus
            _s_OnCalculate_Adx_ = Adx
        DiPlus = (2 * DIP[bar]) + ((alpha1 - 2) * DIP[bar + 1]) + ((1 - alpha1) * DiPlus)
        DiMinus = (2 * DIM[bar]) + ((alpha1 - 2) * DIM[bar + 1]) + ((1 - alpha1) * DiMinus)
        Adx = (2 * ADX[bar]) + ((alpha1 - 2) * ADX[bar + 1]) + ((1 - alpha1) * Adx)
        DiPlusBuffer[bar] = (alpha2 * DiPlus) + ((1 - alpha2) * DiPlusBuffer[bar + 1])
        DiMinusBuffer[bar] = (alpha2 * DiMinus) + ((1 - alpha2) * DiMinusBuffer[bar + 1])
        ADXBuffer[bar] = (alpha2 * Adx) + ((1 - alpha2) * ADXBuffer[bar + 1])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_DiPlus_ = 0.0
_s_OnCalculate_DiMinus_ = 0.0
_s_OnCalculate_Adx_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdxSmoothed(_MQL5Indicator):
    name = 'adx_smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 14,
        'alpha1': 0.25,
        'alpha2': 0.33,
        'PriceType': 0,
    }

