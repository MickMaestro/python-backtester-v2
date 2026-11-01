"""ATR adaptive EMA — converted from MQL5: MQL5 Indicators/ATR adaptive EMA/ATR adaptive EMA.mq5

ATR adaptive EMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'EMA'}, 'levels': [], 'description': ['ATR adaptive EMA'], 'name': 'ATR adaptive EMA', 'source': 'MQL5 Indicators/ATR adaptive EMA/ATR adaptive EMA.mq5', 'folder': 'ATR adaptive EMA', 'inputs': [{'mql': 'inpEmaPeriod', 'py': 'inpEmaPeriod', 'param': 'inpEmaPeriod', 'type': 'int', 'default': 25, 'label': 'EMA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpEmaPeriod = _input('inpEmaPeriod', 25)  # EMA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
atr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, atr, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive EMA (' + _str(inpEmaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        atr[i] = 0.0
        k = 0
        while k < inpEmaPeriod and (i - k - 1) >= 0:
            atr[i] += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        atr[i] = atr[i] / inpEmaPeriod
        _start = MathMax(i - inpEmaPeriod + 1, 0)
        _max = atr[ArrayMaximum(atr, _start, inpEmaPeriod)]
        _min = atr[ArrayMinimum(atr, _start, inpEmaPeriod)]
        _coeff = ((1 - _fdiv(atr[i] - _min, _max - _min)) if (_min != _max) else 0.5)
        _alpha = _fdiv(2.0, 1 + ((inpEmaPeriod * (_coeff + 1.0)) / 2.0))
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = ((val[i - 1] + (_alpha * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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


class ATRAdaptiveEMA(_MQL5Indicator):
    name = 'ATR adaptive EMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpEmaPeriod': 25,  # EMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

