"""Inverse Fisher RVI — converted from MQL5: MQL5 Indicators/Inverse Fisher RVI/Inverse Fisher RVI.mq5

Inverse Fisher RVI
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Inverse Fisher', 2: 'Signal'}, 'levels': [], 'description': ['Inverse Fisher RVI'], 'name': 'Inverse Fisher RVI', 'source': 'MQL5 Indicators/Inverse Fisher RVI/Inverse Fisher RVI.mq5', 'folder': 'Inverse Fisher RVI', 'inputs': [{'mql': 'inpRviPeriod', 'py': 'inpRviPeriod', 'param': 'inpRviPeriod', 'type': 'int', 'default': 10, 'label': 'RVI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRviPeriod = _input('inpRviPeriod', 10)  # RVI period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
rvi = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, rvi, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Inverse Fisher RVI (' + _str(inpRviPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        num = 0.0
        denom = 0.0
        k = 0
        while k < inpRviPeriod and (i - k - 3) >= 0:
            num += close[i - k] - open[i - k] + (2 * (close[i - k - 1] - open[i - k - 1])) + (2 * (close[i - k - 2] - open[i - k - 2])) + close[i - k - 3] - open[i - k - 3]
            denom += high[i - k] - low[i - k] + (2 * (high[i - k - 1] - low[i - k - 1])) + (2 * (high[i - k - 2] - low[i - k - 2])) + high[i - k - 3] - low[i - k - 3]
            k += 1
        rvi[i] = (_fdiv(num, denom) if (denom != 0.0) else 0)
        _start = MathMax(i - inpRviPeriod + 1, 0)
        _lo = rvi[ArrayMinimum(rvi, _start, inpRviPeriod)]
        _hi = rvi[ArrayMaximum(rvi, _start, inpRviPeriod)]
        stoRvi = (MathMax(MathMin(2.0 * (_fdiv(rvi[i] - _lo, _hi - _lo) - 0.5), 0.99999), -0.99999) if (_hi != _lo) else 0)
        val[i] = _fdiv(MathExp(2 * stoRvi) - 1, MathExp(2 * stoRvi) + 1)
        signal[i] = (val[i - 1] if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InverseFisherRVI(_MQL5Indicator):
    name = 'Inverse Fisher RVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRviPeriod': 10,  # RVI period
    }

