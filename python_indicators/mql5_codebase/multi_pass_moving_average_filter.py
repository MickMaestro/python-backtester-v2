"""Multi pass moving average filter — converted from MQL5: MQL5 Indicators/Multi pass average filter/Multi pass moving average filter.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [8421504], 2: [11119017, 3329330, 36095]}, 'widths': {1: 6, 2: 2}, 'styles': {}, 'labels': {1: 'Multi pass moving average filter', 2: 'Multi pass moving average filter'}, 'levels': [], 'description': [], 'name': 'Multi pass moving average filter', 'source': 'MQL5 Indicators/Multi pass average filter/Multi pass moving average filter.mq5', 'folder': 'Multi pass average filter', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 10, 'label': 'MP average period', 'sinput': False}, {'mql': 'inpFilterPass', 'py': 'inpFilterPass', 'param': 'inpFilterPass', 'type': 'int', 'default': 1, 'label': 'Filter pass', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 10)  # MP average period
inpFilterPass = _input('inpFilterPass', 1)  # Filter pass
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
_pass = 0
_filter = Arr(0, 0.0, dims=(6,))

def OnInit():
    global _pass
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    _pass = MathMax(MathMin(inpFilterPass, 5), 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Multi pass moving average filter (' + _str(inpPeriod) + ',' + _str(_pass) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iMpFilter(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, _pass, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        vals[i] = val[i]
        i += 1
    return i

def iMpFilter(price, period, passes, i, bars, instance=0):
    if ArrayRange(_filter, 0) != bars:
        ArrayResize(_filter, bars)
    ma = 0.0
    for p in range(0, passes):
        if p == 0:
            _filter[i][0] = price
        if i >= period:
            ma = _filter[i - 1][p + 1] + _fdiv(_filter[i][p] - _filter[i - period][p], float(period))
        else:
            ma = _filter[i][p]
            k = 1
            while k < period and (i - k) >= 0:
                ma += _filter[i - k][p]
                k += 1
            ma = _fdiv(ma, float(k))
        _filter[i][p + 1] = ma
    return ma

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


class MultiPassMovingAverageFilter(_MQL5Indicator):
    name = 'Multi pass moving average filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 10,  # MP average period
        'inpFilterPass': 1,  # Filter pass
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

