"""Composite index — converted from MQL5: MQL5 Indicators/Composite Index/Composite index.mq5

Composite index
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11119017], 2: [3329330], 3: [17919]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Composite index', 2: 'Composite index 2', 3: 'Composite index 3'}, 'levels': [], 'description': ['Composite index'], 'name': 'Composite index', 'source': 'MQL5 Indicators/Composite Index/Composite index.mq5', 'folder': 'Composite Index', 'inputs': [{'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpRsiSlowPeriod', 'py': 'inpRsiSlowPeriod', 'param': 'inpRsiSlowPeriod', 'type': 'int', 'default': 14, 'label': 'RSI slow period', 'sinput': False}, {'mql': 'inpRsiFastPeriod', 'py': 'inpRsiFastPeriod', 'param': 'inpRsiFastPeriod', 'type': 'int', 'default': 3, 'label': 'RSI fast period', 'sinput': False}, {'mql': 'inpMomentumPeriod', 'py': 'inpMomentumPeriod', 'param': 'inpMomentumPeriod', 'type': 'int', 'default': 9, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpMaPeriod1', 'py': 'inpMaPeriod1', 'param': 'inpMaPeriod1', 'type': 'int', 'default': 3, 'label': 'Average period 1', 'sinput': False}, {'mql': 'inpMaPeriod2', 'py': 'inpMaPeriod2', 'param': 'inpMaPeriod2', 'type': 'int', 'default': 13, 'label': 'Average period 2', 'sinput': False}, {'mql': 'inpMaPeriod3', 'py': 'inpMaPeriod3', 'param': 'inpMaPeriod3', 'type': 'int', 'default': 33, 'label': 'Average period 3', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpRsiSlowPeriod = _input('inpRsiSlowPeriod', 14)  # RSI slow period
inpRsiFastPeriod = _input('inpRsiFastPeriod', 3)  # RSI fast period
inpMomentumPeriod = _input('inpMomentumPeriod', 9)  # Momentum period
inpMaPeriod1 = _input('inpMaPeriod1', 3)  # Average period 1
inpMaPeriod2 = _input('inpMaPeriod2', 13)  # Average period 2
inpMaPeriod3 = _input('inpMaPeriod3', 33)  # Average period 3
val1 = Arr(0, 0.0)
val2 = Arr(0, 0.0)
val3 = Arr(0, 0.0)
rsislow = Arr(0, 0.0)
rsifast = Arr(0, 0.0)
_rsiSlowHandle = 0
_rsiFastHandle = 0
workSma = Arr(0, 0.0, dims=(3,))

def OnInit():
    global _rsiFastHandle, _rsiSlowHandle
    SetIndexBuffer(0, val1, INDICATOR_DATA)
    SetIndexBuffer(1, val2, INDICATOR_DATA)
    SetIndexBuffer(2, val3, INDICATOR_DATA)
    SetIndexBuffer(3, rsislow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, rsifast, INDICATOR_CALCULATIONS)
    _rsiSlowHandle = iRSI(Symbol(), 0, inpRsiSlowPeriod, inpPrice)
    if _rsiSlowHandle == INVALID_HANDLE:
        return INIT_FAILED
    _rsiFastHandle = iRSI(Symbol(), 0, inpRsiFastPeriod, inpPrice)
    if _rsiFastHandle == INVALID_HANDLE:
        IndicatorRelease(_rsiSlowHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Composite index (' + _str(inpRsiSlowPeriod) + ',' + _str(inpRsiFastPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_rsiFastHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_rsiSlowHandle) < rates_total:
        return prev_calculated
    _rsiVal = Arr(1, 0.0, dyn=False)
    _rsiCopied = 0
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _rsiCopied = CopyBuffer(_rsiSlowHandle, 0, _DT(time[i]), 1, _rsiVal)
        rsislow[i] = (_rsiVal[0] if (_rsiCopied == 1) else 0)
        _rsiCopied = CopyBuffer(_rsiFastHandle, 0, _DT(time[i]), 1, _rsiVal)
        RSIDelta = ((rsislow[i] - rsislow[i - inpMomentumPeriod]) if (i >= inpMomentumPeriod) else 0)
        RSIsma = iSma((_rsiVal[0] if (_rsiCopied == 1) else 0), inpMaPeriod1, i, rates_total, 0)
        Composite = RSIDelta + RSIsma
        val1[i] = Composite
        val2[i] = iSma(Composite, inpMaPeriod2, i, rates_total, 1)
        val3[i] = iSma(Composite, inpMaPeriod3, i, rates_total, 1)
        i += 1
    return i

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CompositeIndex(_MQL5Indicator):
    name = 'Composite index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpRsiSlowPeriod': 14,  # RSI slow period
        'inpRsiFastPeriod': 3,  # RSI fast period
        'inpMomentumPeriod': 9,  # Momentum period
        'inpMaPeriod1': 3,  # Average period 1
        'inpMaPeriod2': 13,  # Average period 2
        'inpMaPeriod3': 33,  # Average period 3
    }

