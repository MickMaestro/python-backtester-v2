"""AMA (ds) — converted from MQL5: MQL5 Indicators/Adaptive moving average - double smoothed/AMA (ds).mq5

AMA - double smoothed
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'AMA'}, 'levels': [], 'description': ['AMA - double smoothed'], 'name': 'AMA (ds)', 'source': 'MQL5 Indicators/Adaptive moving average - double smoothed/AMA (ds).mq5', 'folder': 'Adaptive moving average - double smoothed', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFastPeriod = _input('inpFastPeriod', 2)  # Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # Slow end period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valw = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
_minMaxPeriod = 0
_fastEnd = 0.0
_slowEnd = 0.0

def OnInit():
    global _fastEnd, _minMaxPeriod, _slowEnd
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valw, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, prices, INDICATOR_CALCULATIONS)
    _minMaxPeriod = ((inpPeriod - 1) if (inpPeriod > 1) else 1)
    _fastEnd = _fdiv(2.0, MathMin(inpFastPeriod, inpPeriod) + 1.0)
    _slowEnd = _fdiv(2.0, MathMax(inpSlowPeriod, inpPeriod) + 1.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, high, low, close, i)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = prices[ArrayMaximum(prices, start, _minMaxPeriod)]
            _s_OnCalculate_prev_min = prices[ArrayMinimum(prices, start, _minMaxPeriod)]
        max_ = (prices[i] if (prices[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (prices[i] if (prices[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        if i > 0:
            mltp = (_fdiv(prices[i] - min_ - (max_ - prices[i]), max_ - min_) if (max_ != min_) else 1)
            if mltp < 0:
                mltp *= -1
            ssc = (mltp * (_fastEnd - _slowEnd)) + _slowEnd
            valw[i] = valw[i - 1] + (ssc * (prices[i] - valw[i - 1]))
            val[i] = val[i - 1] + (ssc * (valw[i] - val[i - 1]))
            valc[i] = (1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1])
        else:
            val[i] = prices[i]
            valw[i] = val[i]
            valc[i] = 0.0
        i += 1
    return i

def getPrice(tprice, open, high, low, close, i):
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

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMADs(_MQL5Indicator):
    name = 'AMA (ds)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFastPeriod': 2,  # Fast end period
        'inpSlowPeriod': 30,  # Slow end period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

