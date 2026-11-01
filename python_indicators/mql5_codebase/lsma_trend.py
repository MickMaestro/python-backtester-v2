"""LSMA trend — converted from MQL5: MQL5 Indicators/LSMA Trend/LSMA trend.mq5

LSMA trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LSMA trend'}, 'levels': [], 'description': ['LSMA trend'], 'name': 'LSMA trend', 'source': 'MQL5 Indicators/LSMA Trend/LSMA trend.mq5', 'folder': 'LSMA Trend', 'inputs': [{'mql': 'inpLsmaPeriod', 'py': 'inpLsmaPeriod', 'param': 'inpLsmaPeriod', 'type': 'int', 'default': 35, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpAcceleration', 'py': 'inpAcceleration', 'param': 'inpAcceleration', 'type': 'double', 'default': 1.05, 'label': 'Acceleration factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLsmaPeriod = _input('inpLsmaPeriod', 35)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpAcceleration = _input('inpAcceleration', 1.05)  # Acceleration factor
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lsma = Arr(0, 0.0)
trend = Arr(0, 0.0)
step = Arr(0, 0.0)
workLinr = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, lsma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, step, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LSMA trend (' + _str(inpLsmaPeriod) + ',' + _str(inpAcceleration) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        lsma[i] = iLinr(getPrice(inpPrice, open, close, high, low, i, rates_total), inpLsmaPeriod, i, rates_total)
        trend[i] = ((1 if (lsma[i] > lsma[i - 1]) else -1 if (lsma[i] < lsma[i - 1]) else trend[i - 1]) if (i > 0) else 0)
        step[i] = ((0.01 if (trend[i] != trend[i - 1]) else (step[i - 1] * inpAcceleration)) if (i > 0) else 0.01)
        val[i] = ((val[i - 1] + (trend[i] * step[i])) if (i > 0) else 0)
        valc[i] = (1 if (trend[i] == 1) else 2 if (trend[i] == -1) else 0)
        i += 1
    return i

def iLinr(price, period, r, bars, instanceNo=0):
    if ArrayRange(workLinr, 0) != bars:
        ArrayResize(workLinr, bars)
    period = MathMax(period, 1)
    workLinr[r][instanceNo] = price
    if r < period:
        return price
    lwmw = period
    lwma = lwmw * price
    sma = price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        lwmw += weight
        lwma += weight * workLinr[r - k][instanceNo]
        sma += workLinr[r - k][instanceNo]
        k += 1
    return _fdiv(3.0 * lwma, lwmw) - _fdiv(2.0 * sma, period)

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


class LSMATrend(_MQL5Indicator):
    name = 'LSMA trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpLsmaPeriod': 35,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpAcceleration': 1.05,  # Acceleration factor
    }

