"""Coppock — converted from MQL5: MQL5 Indicators/Coppock MT5 indicator/Coppock.mq5

Classical Coppock indicator. Should be applied on monthly timeframe.
Periods shouldn't be changed. Change timeframe and parameters for
experimental Coppock usage. Works only with Weighted MA.
Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.0', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [255]}, 'widths': {}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Classical Coppock indicator. Should be applied on monthly timeframe.', "Periods shouldn't be changed. Change timeframe and parameters for", 'experimental Coppock usage. Works only with Weighted MA.'], 'name': 'Coppock', 'source': 'MQL5 Indicators/Coppock MT5 indicator/Coppock.mq5', 'folder': 'Coppock MT5 indicator', 'inputs': [{'mql': 'ROC1Period', 'py': 'ROC1Period', 'param': 'ROC1Period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ROC2Period', 'py': 'ROC2Period', 'param': 'ROC2Period', 'type': 'int', 'default': 11, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ROC1Period = _input('ROC1Period', 14)
ROC2Period = _input('ROC2Period', 11)
MAPeriod = _input('MAPeriod', 10)
Coppock = Arr(0, 0.0)
ROCSum = Arr(0, 0.0)
DrawBegin = 0
FirstTime = True

def OnInit():
    global DrawBegin
    DrawBegin = MathMax(ROC1Period, ROC2Period) + MAPeriod
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DrawBegin)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, Coppock, INDICATOR_DATA)
    SetIndexBuffer(1, ROCSum, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Coppock, True)
    ArraySetAsSeries(ROCSum, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Coppock(' + _str(ROC1Period) + ', ' + _str(ROC2Period) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Coppock')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, Close, tick_volume, volume, spread):
    ArraySetAsSeries(Close, True)
    limit = 0
    i = 0
    counted_bars = prev_calculated
    if counted_bars < 0:
        return -1
    if counted_bars > 0:
        counted_bars -= 1
    limit = rates_total - counted_bars
    if (limit - rates_total) < DrawBegin:
        limit = rates_total - DrawBegin
    i = 0
    for i in range(i, limit):
        ROCSum[i] = _fdiv(Close[i] - Close[i + ROC1Period], Close[i + ROC1Period]) + _fdiv(Close[i] - Close[i + ROC2Period], Close[i + ROC2Period])
    else:
        i = _range_end(i, limit, 1)
    CalculateLWMA(0, MAPeriod, ROCSum, limit)
    return rates_total

def CalculateLWMA(begin, period, price, big_limit):
    global FirstTime, _s_CalculateLWMA_weightsum
    i = 0
    limit = 0
    sum_ = 0.0
    limit = period + begin
    if FirstTime:
        _s_CalculateLWMA_weightsum = 0
        i = begin
        for i in range(i, limit):
            Coppock[i] = 0.0
        else:
            i = _range_end(i, limit, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            k = limit - i
            _s_CalculateLWMA_weightsum += k
            firstValue += k * price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = _fdiv(firstValue, float(_s_CalculateLWMA_weightsum))
        Coppock[limit] = firstValue
        FirstTime = False
    i = begin
    for i in range(i, big_limit):
        sum_ = 0.0
        for j in range(0, period):
            sum_ += (period - j) * price[i + j]
        Coppock[i] = _fdiv(sum_, _s_CalculateLWMA_weightsum)
    else:
        i = _range_end(i, big_limit, 1)

# ---- static local variables
_s_CalculateLWMA_weightsum = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CoppockIndicator(_MQL5Indicator):
    name = 'Coppock'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ROC1Period': 14,
        'ROC2Period': 11,
        'MAPeriod': 10,
    }

