"""Volatility adjusted WPR — converted from MQL5: MQL5 Indicators/Volatility adjusted WPR/Volatility adjusted WPR.mq5

WPR
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 10, 2: 10, 3: 8}, 'colors': {1: [11119017, 16760576, 5275647], 2: [11119017, 16760576, 5275647], 3: [11119017, 16748574, 6053069]}, 'widths': {1: 2, 2: 0, 3: 2}, 'styles': {}, 'labels': {1: 'Wpr trending', 2: 'Wpr reverting', 3: 'Wpr'}, 'levels': [30.0, -30.0], 'description': ['WPR'], 'name': 'Volatility adjusted WPR', 'source': 'MQL5 Indicators/Volatility adjusted WPR/Volatility adjusted WPR.mq5', 'folder': 'Volatility adjusted WPR', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'WPR period', 'sinput': False}, {'mql': 'inpVolPeriod', 'py': 'inpVolPeriod', 'param': 'inpVolPeriod', 'type': 'int', 'default': 0, 'label': 'Volatilty period (<=0 for same as WPR period)', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 8.0, 'label': 'Smoothing/slowing period (<= 1 for no smoothing)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # WPR period
inpVolPeriod = _input('inpVolPeriod', 0)  # Volatilty period (<=0 for same as WPR period)
inpSmooth = _input('inpSmooth', 8.0)  # Smoothing/slowing period (<= 1 for no smoothing)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valw = Arr(0, 0.0)
valht = Arr(0, 0.0)
valhtc = Arr(0, 0.0)
valhr = Arr(0, 0.0)
valhrc = Arr(0, 0.0)
ª_alpha = 0.0
ª_volPeriod = 0
_volArray = Arr(0, 0.0, dims=(4,))

def OnInit():
    global ª_alpha, ª_volPeriod
    SetIndexBuffer(0, valht, INDICATOR_DATA)
    SetIndexBuffer(1, valhtc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valhr, INDICATOR_DATA)
    SetIndexBuffer(3, valhrc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, valw, INDICATOR_CALCULATIONS)
    ª_volPeriod = (inpVolPeriod if (inpVolPeriod > 1) else inpPeriod)
    ª_alpha = _fdiv(2.0, 1.0 + MathSqrt((inpSmooth if (inpSmooth > 1) else 1)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility adjusted WPR (' + _str(inpPeriod) + ',' + _str(ª_volPeriod) + ',' + _str((inpSmooth if (inpSmooth > 1) else 1)) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        _wprPeriod = _int(_fdiv(inpPeriod, iVolatility(_price, ª_volPeriod, i, rates_total)))
        _start = ((i - _wprPeriod + 1) if (i > _wprPeriod) else 0)
        _min = low[ArrayMinimum(low, _start, _wprPeriod)]
        _max = high[ArrayMaximum(high, _start, _wprPeriod)]
        _wpr = ((50 - _fdiv(100 * (_max - close[i]), _max - _min)) if (_max != _min) else 0)
        valw[i] = ((valw[i - 1] + (ª_alpha * (_wpr - valw[i - 1]))) if (i > 0) else 0)
        val[i] = ((val[i - 1] + (ª_alpha * (valw[i] - val[i - 1]))) if (i > 0) else 0)
        slope = (((1 if (val[i] > val[i - 1]) else 0) if (val[i] > 0) else 1 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
        valht[i] = (val[i] if (slope == 1) else EMPTY_VALUE)
        valhr[i] = (val[i] if (slope == 0) else EMPTY_VALUE)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        valhtc[i] = (1 if (val[i] > 0) else 2)
        valhrc[i] = (1 if (val[i] > 0) else 2)
        i += 1
    return i

def iVolatility(price, period, i, _bars, instance=0):
    global _s_iVolatility__arrayError, _s_iVolatility__arrayResizedTo
    if _s_iVolatility__arrayResizedTo < _bars:
        _res = _bars + 500
        _res -= ArrayResize(_volArray, _res)
        if _res:
            _s_iVolatility__arrayError = True
        else:
            _s_iVolatility__arrayResizedTo = _bars + 500
    if _s_iVolatility__arrayError:
        return 1.0
    _volArray[i][instance] = price
    diff = ((_volArray[i][instance] - _volArray[i - 1][instance]) if (i > 0) else 0)
    _volArray[i][instance + 1] = (diff if (diff > 0) else (-diff))
    if i <= period:
        _volArray[i][instance + 2] = _volArray[i][instance + 1]
        k = 1
        while k < period and i >= k:
            _volArray[i][instance + 2] += _volArray[i - k][instance + 1]
            k += 1
        _volArray[i][instance + 3] = _volArray[i][instance + 2]
        k = 1
        while k < period and i >= k:
            _volArray[i][instance + 3] += _volArray[i - k][instance + 2]
            k += 1
    else:
        _volArray[i][instance + 2] = _volArray[i - 1][instance + 2] - _volArray[i - period][instance + 1] + _volArray[i][instance + 1]
        _volArray[i][instance + 3] = _volArray[i - 1][instance + 3] - _volArray[i - period][instance + 2] + _volArray[i][instance + 2]
    return (_fdiv(float(period) * _volArray[i][instance + 2], _volArray[i][instance + 3]) if (_volArray[i][instance + 3] != 0 and _volArray[i][instance + 2] != 0) else 1)

# ---- static local variables
_s_iVolatility__arrayError = False
_s_iVolatility__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityAdjustedWPR(_MQL5Indicator):
    name = 'Volatility adjusted WPR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # WPR period
        'inpVolPeriod': 0,  # Volatilty period (<=0 for same as WPR period)
        'inpSmooth': 8.0,  # Smoothing/slowing period (<= 1 for no smoothing)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

