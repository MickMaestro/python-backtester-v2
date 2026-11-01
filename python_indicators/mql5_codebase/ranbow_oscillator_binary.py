"""Ranbow oscillator - binary — converted from MQL5: MQL5 Indicators/Rainbow Oscillator - Binary/Ranbow oscillator - binary.mq5

Rainbow oscillator binary
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 6333684, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rainbow oscillator'}, 'levels': [], 'description': ['Rainbow oscillator binary'], 'name': 'Ranbow oscillator - binary', 'source': 'MQL5 Indicators/Rainbow Oscillator - Binary/Ranbow oscillator - binary.mq5', 'folder': 'Rainbow Oscillator - Binary', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'inpRwmaDepth', 'py': 'inpRwmaDepth', 'param': 'inpRwmaDepth', 'type': 'int', 'default': 10, 'label': 'RWMA depth (maximal 50)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 5)  # Period
inpRwmaDepth = _input('inpRwmaDepth', 10)  # RWMA depth (maximal 50)
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
pBuffer = Arr(0, 0.0, dims=(50,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rainbow oscillator binary (' + _str(inpPeriod) + ',' + _str(inpRwmaDepth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(pBuffer, 0) != rates_total:
        ArrayResize(pBuffer, rates_total)
    _weight = (inpPeriod + 1) * inpPeriod * 0.5
    _depth = MathMax(MathMin(inpRwmaDepth, 50), 1)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        minp = price
        maxp = price
        sum_ = 0.0
        k = 0
        j = 0
        while k < _depth:
            pBuffer[i][k] = price
            if i > inpPeriod:
                j = 0
                price = 0.0
                while j < inpPeriod:
                    price += (inpPeriod - j) * pBuffer[i - j][k]
                    j += 1
                price = _fdiv(price, _weight)
            sum_ += price
            minp = (MathMin(minp, pBuffer[i - k][0]) if (i >= k) else 0)
            maxp = (MathMax(maxp, pBuffer[i - k][0]) if (i >= k) else 0)
            k += 1
        rma = _fdiv(sum_, _depth)
        rangep = maxp - minp
        if rangep != 0:
            _osc = _fdiv(100 * (pBuffer[i][0] - rma), rangep)
            val[i] = (1 if (_osc > 0) else 0)
            valc[i] = (2 if (val[i] > 0) else 1 if (val[i] == 0) else 0)
    return rates_total

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RanbowOscillatorBinary(_MQL5Indicator):
    name = 'Ranbow oscillator - binary'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 5,  # Period
        'inpRwmaDepth': 10,  # RWMA depth (maximal 50)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

