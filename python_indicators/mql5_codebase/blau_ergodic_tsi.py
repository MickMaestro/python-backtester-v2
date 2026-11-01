"""Blau - Ergodic tsi — converted from MQL5: MQL5 Indicators/Blau Ergodic TSI/Blau - Ergodic tsi.mq5

Ergodic True Strength Index (William Blau)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 6333684], 3: [11119017]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'TSI', 2: 'TSI signal line'}, 'levels': [], 'description': ['Ergodic True Strength Index (William Blau)'], 'name': 'Blau - Ergodic tsi', 'source': 'MQL5 Indicators/Blau Ergodic TSI/Blau - Ergodic tsi.mq5', 'folder': 'Blau Ergodic TSI', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 25, 'label': 'TSI smoothing period ("s" period)', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 13, 'label': 'TSI momentum smoothing period  ("r" period)', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 0, 'label': 'Color change type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
col_onSignalCross = 0
col_onZeroCross = 1
col_onSlopeChange = 2
_enum('enColorOn', {0: 'col_onSignalCross', 1: 'col_onZeroCross', 2: 'col_onSlopeChange'})

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 25)  # TSI smoothing period ("s" period)
inpPeriod2 = _input('inpPeriod2', 13)  # TSI momentum smoothing period  ("r" period)
inpSignalPeriod = _input('inpSignalPeriod', 5)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', col_onSignalCross)  # Color change type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
prices = Arr(0, 0.0)
_ub9__signalAlpha = 0.0

def OnInit():
    global _ub9__signalAlpha
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, prices, INDICATOR_CALCULATIONS)
    _ub9__signalAlpha = _fdiv(2.0, 1.0 + (inpSignalPeriod if (inpSignalPeriod > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, ('Ergodic t' if (inpPeriod1 == 5 or inpPeriod2 == 5) else 'T') + 'rue strength index (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
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
        val[i] = 100 * iTsi(((prices[i] - prices[i - 1]) if (i > 0) else 0), inpPeriod2, inpPeriod1, i)
        signal[i] = ((signal[i - 1] + (_ub9__signalAlpha * (val[i] - signal[i - 1]))) if (i > 0) else val[i])
        _sw2 = inpColorOn
        if _sw2 == col_onSignalCross:
            valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw2 == col_onSlopeChange:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def iTsi(value, period1, period2, i, _instance=0):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    valua = (value if (value > 0) else (-value))
    if i > 0 and period1 > 1:
        _s_iTsi__workArray[_indC][_instance] = _s_iTsi__workArray[_indP][_instance] + (_fdiv(2.0, 1.0 + period1) * (value - _s_iTsi__workArray[_indP][_instance]))
        _s_iTsi__workArray[_indC][_instance + 2] = _s_iTsi__workArray[_indP][_instance + 2] + (_fdiv(2.0, 1.0 + period1) * (valua - _s_iTsi__workArray[_indP][_instance + 2]))
    else:
        _s_iTsi__workArray[_indC][_instance + 2] = value
        _s_iTsi__workArray[_indC][_instance] = _s_iTsi__workArray[_indC][_instance + 2]
    if i > 0 and period2 > 1:
        _s_iTsi__workArray[_indC][_instance + 1] = _s_iTsi__workArray[_indP][_instance + 1] + (_fdiv(2.0, 1.0 + period2) * (_s_iTsi__workArray[_indC][_instance] - _s_iTsi__workArray[_indP][_instance + 1]))
        _s_iTsi__workArray[_indC][_instance + 3] = _s_iTsi__workArray[_indP][_instance + 3] + (_fdiv(2.0, 1.0 + period2) * (_s_iTsi__workArray[_indC][_instance + 2] - _s_iTsi__workArray[_indP][_instance + 3]))
    else:
        _s_iTsi__workArray[_indC][_instance + 3] = value
        _s_iTsi__workArray[_indC][_instance + 1] = _s_iTsi__workArray[_indC][_instance + 3]
    return (_fdiv(_s_iTsi__workArray[_indC][_instance + 1], _s_iTsi__workArray[_indC][_instance + 3]) if (_s_iTsi__workArray[_indC][_instance + 3] != 0) else 0)

# ---- static local variables
_s_iTsi__workArray = Arr(6, 0.0, dyn=False, dims=(4,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauErgodicTsi(_MQL5Indicator):
    name = 'Blau - Ergodic tsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 25,  # TSI smoothing period ("s" period)
        'inpPeriod2': 13,  # TSI momentum smoothing period  ("r" period)
        'inpSignalPeriod': 5,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on signal line cross', 1: 'Change color on zero line cross', 2: 'Change color TSI slope change'}, default=0),  # Color change type
    }

