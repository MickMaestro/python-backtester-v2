"""ChickenKnife — converted from MQL5: MQL5 Indicators/Chicken Knife/ChickenKnife.mq5

Copyright: Marco Marconi; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Marco Marconi', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Main Line'}, 'levels': [], 'description': [], 'name': 'ChickenKnife', 'source': 'MQL5 Indicators/Chicken Knife/ChickenKnife.mq5', 'folder': 'Chicken Knife', 'inputs': [{'mql': 'CKPeriod', 'py': 'CKPeriod', 'param': 'CKPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
CKPeriod = _input('CKPeriod', 14)  # Smoothing Period
Buffer = Arr(0, 0.0)

def OnInit():
    max_period = 0
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    if Digits() == 0:
        IndicatorSetInteger(INDICATOR_DIGITS, 6)
    else:
        IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArrayInitialize(Buffer, 0)
    max_period = CKPeriod
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, max_period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CK(' + IntegerToString(CKPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def inv_logit(x):
    return _fdiv(exp(x), 1 + exp(x))

def OnCalculate(rates_total, prev_calculated, begin, price):
    limit = 0
    limit = rates_total - prev_calculated
    if prev_calculated == 0:
        limit = CKPeriod
    diff = Arr(0, 0.0)
    ArrayResize(diff, rates_total - limit + 1)
    tmp = Arr(0, 0.0)
    ArrayResize(tmp, rates_total)
    ArrayInitialize(tmp, 0)
    for i in range(limit + 1, rates_total):
        diff[i - limit + 1] = (log(price[i]) - log(price[i - 1])) * 100
    err = 0.0
    for i in range(limit + 3, rates_total):
        err = diff[i - limit + 1] - (2 * (inv_logit(tmp[i - 1]) - 0.5) * diff[i - limit])
        tmp[i] = err * diff[i - limit]
    if CKPeriod > 1:
        SimpleMAOnBuffer(rates_total, prev_calculated, begin, CKPeriod, tmp, Buffer)
    else:
        ArrayCopy(Buffer, tmp)
    return rates_total

def SMA(array, length, bar):
    i = 0
    sum_ = 0.0
    i = 0
    for i in range(i, length):
        sum_ += array[bar - i]
    else:
        i = _range_end(i, length, 1)
    return _fdiv(sum_, length)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChickenKnife(_MQL5Indicator):
    name = 'ChickenKnife'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CKPeriod': 14,  # Smoothing Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

