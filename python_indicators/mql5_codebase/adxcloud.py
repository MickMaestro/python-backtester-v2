"""adxcloud — converted from MQL5: MQL5 Indicators/ADXCloud/adxcloud.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65280, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Di Plus;Di Minus'}, 'levels': [], 'description': [], 'name': 'adxcloud', 'source': 'MQL5 Indicators/ADXCloud/adxcloud.mq5', 'folder': 'ADXCloud', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 0.33, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 5)
alpha1 = _input('alpha1', 0.25)
alpha2 = _input('alpha2', 0.33)
DiPlusBuffer = Arr(0, 0.0)
DiMinusBuffer = Arr(0, 0.0)
ADX_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, min_rates_total
    ADX_Handle = iADX(None, 0, period)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX indicator!')
        return INIT_FAILED
    min_rates_total = period + 1
    SetIndexBuffer(0, DiPlusBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DiPlusBuffer, True)
    SetIndexBuffer(1, DiMinusBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DiMinusBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'ADXCloud(', period, ')smothed')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DDiMinus_, _s_OnCalculate_DDiPlus_, _s_OnCalculate_DiMinus_, _s_OnCalculate_DiPlus_
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    DIP = Arr(0, 0.0)
    DIM = Arr(0, 0.0)
    DiPlus = 0.0
    DiMinus = 0.0
    DDiPlus = 0.0
    DDiMinus = 0.0
    ArraySetAsSeries(DIP, True)
    ArraySetAsSeries(DIM, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        _s_OnCalculate_DiPlus_ = 0.0
        _s_OnCalculate_DiMinus_ = 0.0
        _s_OnCalculate_DDiPlus_ = 0.0
        _s_OnCalculate_DDiMinus_ = 0.0
        DiPlusBuffer[rates_total - 1] = 0.0
        DiMinusBuffer[rates_total - 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, DIP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, DIM) <= 0:
        return 0
    DiPlus = _s_OnCalculate_DiPlus_
    DiMinus = _s_OnCalculate_DiMinus_
    DDiPlus = _s_OnCalculate_DDiPlus_
    DDiMinus = _s_OnCalculate_DDiMinus_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DiPlus = (2 * DIP[bar]) + ((alpha1 - 2) * DIP[bar + 1]) + ((1 - alpha1) * DiPlus)
        DiMinus = (2 * DIM[bar]) + ((alpha1 - 2) * DIM[bar + 1]) + ((1 - alpha1) * DiMinus)
        DDiPlus = (alpha2 * DiPlus) + ((1 - alpha2) * _s_OnCalculate_DDiPlus_)
        DDiMinus = (alpha2 * DiMinus) + ((1 - alpha2) * _s_OnCalculate_DDiMinus_)
        DiPlusBuffer[bar] = DDiPlus - DDiMinus
        DiMinusBuffer[bar] = 0.0
        if bar:
            _s_OnCalculate_DiPlus_ = DiPlus
            _s_OnCalculate_DiMinus_ = DiMinus
            _s_OnCalculate_DDiPlus_ = DDiPlus
            _s_OnCalculate_DDiMinus_ = DDiMinus
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_DiPlus_ = 0.0
_s_OnCalculate_DiMinus_ = 0.0
_s_OnCalculate_DDiPlus_ = 0.0
_s_OnCalculate_DDiMinus_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Adxcloud(_MQL5Indicator):
    name = 'adxcloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 5,
        'alpha1': 0.25,
        'alpha2': 0.33,
    }

