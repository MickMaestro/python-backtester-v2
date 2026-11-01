"""Ehlers Fisher transform (original) — converted from MQL5: MQL5 Indicators/Ehlers Fisher transform (original)/Ehlers Fisher transform (original).mq5

Fisher transform
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 7451452, 17919], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Fisher transform', 2: 'Signal'}, 'levels': [], 'description': ['Fisher transform'], 'name': 'Ehlers Fisher transform (original)', 'source': 'MQL5 Indicators/Ehlers Fisher transform (original)/Ehlers Fisher transform (original).mq5', 'folder': 'Ehlers Fisher transform (original)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Period', 'sinput': False}, {'mql': 'inpCalcMode', 'py': 'inpCalcMode', 'param': 'inpCalcMode', 'type': 'int', 'default': 1, 'label': 'Calculation mode', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enCalcMode
calc_hl = 0
calc_no = 1
_enum('enCalcMode', {0: 'calc_hl', 1: 'calc_no'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Period
inpCalcMode = _input('inpCalcMode', calc_no)  # Calculation mode
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
prices = Arr(0, 0.0)
work = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, work, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers Fisher transform (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        _start = i - inpPeriod + 1
        if _start < 0:
            _start = 0
        _hi = (MathMax(high[i], prices[ArrayMaximum(prices, _start, inpPeriod)]) if (inpCalcMode == calc_hl) else prices[ArrayMaximum(prices, _start, inpPeriod)])
        _lo = (MathMin(low[i], prices[ArrayMinimum(prices, _start, inpPeriod)]) if (inpCalcMode == calc_hl) else prices[ArrayMinimum(prices, _start, inpPeriod)])
        _os = ((2.0 * (_fdiv(prices[i] - _lo, _hi - _lo) - 0.5)) if (_hi != _lo) else 0)
        _sm = (((0.5 * _os) + (0.5 * work[i - 1])) if (i > 0) else _os)
        work[i] = MathMax(MathMin(_sm, 0.999), -0.999)
        val[i] = (0.25 * MathLog(_fdiv(1 + work[i], 1 - work[i]))) + ((0.5 * val[i - 1]) if (i > 0) else 0)
        signal[i] = (val[i - 1] if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersFisherTransformOriginal(_MQL5Indicator):
    name = 'Ehlers Fisher transform (original)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Period
        'inpCalcMode': _Choice({0: 'Include current high and low in calculation', 1: "Don't include current high and low in calculation"}, default=1),  # Calculation mode
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

