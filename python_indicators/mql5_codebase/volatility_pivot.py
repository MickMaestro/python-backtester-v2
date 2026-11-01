"""Volatility pivot — converted from MQL5: MQL5 Indicators/Volatility Pivot/Volatility pivot.mq5

Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Volatility pivot'}, 'levels': [], 'description': [], 'name': 'Volatility pivot', 'source': 'MQL5 Indicators/Volatility Pivot/Volatility pivot.mq5', 'folder': 'Volatility Pivot', 'inputs': [{'mql': 'inpAtrRange', 'py': 'inpAtrRange', 'param': 'inpAtrRange', 'type': 'int', 'default': 100, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpAtrFactor', 'py': 'inpAtrFactor', 'param': 'inpAtrFactor', 'type': 'double', 'default': 3.0, 'label': 'ATR factor', 'sinput': False}, {'mql': 'inpMaRange', 'py': 'inpMaRange', 'param': 'inpMaRange', 'type': 'int', 'default': 10, 'label': 'EMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrRange = _input('inpAtrRange', 100)  # ATR period
inpAtrFactor = _input('inpAtrFactor', 3.0)  # ATR factor
inpMaRange = _input('inpMaRange', 10)  # EMA period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
atr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, atr, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _alpha = _fdiv(2.0, inpMaRange + 1.0)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _atr = 0.0
        k = 0
        while k < inpAtrRange and (i - k - 1) >= 0:
            _atr += ((MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])) if (i > 0) else (high[i - k] - low[i - k]))
            k += 1
        _atr = _atr / inpAtrRange
        atr[i] = ((atr[i - 1] + (_alpha * (_atr - atr[i - 1]))) if (i > 0) else _atr)
        val[i] = close[i]
        _deltaStop = atr[i] * inpAtrFactor
        while i > 0 and True:
            if close[i] == val[i - 1]:
                val[i] = val[i - 1]
                break
            if close[i - 1] < val[i - 1] and close[i] < val[i - 1]:
                val[i] = MathMin(val[i - 1], close[i] + _deltaStop)
                break
            if close[i - 1] > val[i - 1] and close[i] > val[i - 1]:
                val[i] = MathMax(val[i - 1], close[i] - _deltaStop)
                break
            if close[i] > val[i - 1]:
                val[i] = close[i] - _deltaStop
            else:
                val[i] = close[i] + _deltaStop
            break
        valc[i] = (1 if (close[i] > val[i]) else 2 if (close[i] < val[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityPivot(_MQL5Indicator):
    name = 'Volatility pivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpAtrRange': 100,  # ATR period
        'inpAtrFactor': 3.0,  # ATR factor
        'inpMaRange': 10,  # EMA period
    }

