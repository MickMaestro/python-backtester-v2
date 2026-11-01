"""ATR adaptive double smoothed EMA — converted from MQL5: MQL5 Indicators/ATR adaptive double smoothed EMA/ATR adaptive double smoothed EMA.mq5

ATR adaptive double smoothed EMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Double smoothed EMA'}, 'levels': [], 'description': ['ATR adaptive double smoothed EMA'], 'name': 'ATR adaptive double smoothed EMA', 'source': 'MQL5 Indicators/ATR adaptive double smoothed EMA/ATR adaptive double smoothed EMA.mq5', 'folder': 'ATR adaptive double smoothed EMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 25.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25.0)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
work = Arr(0, 0.0)
atr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, work, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, atr, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive double smoothed EMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        atr[i] = 0.0
        k = 0
        while k < inpPeriod and (i - k - 1) >= 0:
            atr[i] += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        atr[i] = atr[i] / inpPeriod
        _start = MathMax(i - _int(inpPeriod) + 1, 0)
        _max = atr[ArrayMaximum(atr, _start, _int(inpPeriod))]
        _min = atr[ArrayMinimum(atr, _start, _int(inpPeriod))]
        _coeff = ((1 - _fdiv(atr[i] - _min, _max - _min)) if (_min != _max) else 0.5)
        _alpha = _fdiv(2.0, 1.0 + MathSqrt(MathMax(1 + ((inpPeriod * (_coeff + 1.0)) / 2.0), 1)))
        work[i] = ((work[i - 1] + (_alpha * (price - work[i - 1]))) if (i > 0) else price)
        val[i] = ((val[i - 1] + (_alpha * (work[i] - val[i - 1]))) if (i > 0) else work[i])
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


class ATRAdaptiveDoubleSmoothedEMA(_MQL5Indicator):
    name = 'ATR adaptive double smoothed EMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

