"""Ravi — converted from MQL5: MQL5 Indicators/Range Action Verification Index - extended/Ravi.mq5

Range Action Verification Index
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [2263842], 2: [11119017], 3: [3937500], 4: [11119017, 3937500, 2263842]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Level up', 2: 'Middle level', 3: 'Level down', 4: 'Range Action Verification Index'}, 'levels': [], 'description': ['Range Action Verification Index'], 'name': 'Ravi', 'source': 'MQL5 Indicators/Range Action Verification Index - extended/Ravi.mq5', 'folder': 'Range Action Verification Index - extended', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 7, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 65, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 32, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 1, 'label': 'Change color mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
col_onZero = 0
col_onOuter = 1
_enum('enColorMode', {0: 'col_onZero', 1: 'col_onOuter'})

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 7)  # Fast period
inpSlowPeriod = _input('inpSlowPeriod', 65)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpFlPeriod = _input('inpFlPeriod', 32)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 80.0)  # Up level %
inpFlLevelDown = _input('inpFlLevelDown', 20.0)  # Down level %
inpColorMode = _input('inpColorMode', col_onOuter)  # Change color mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
flup = Arr(0, 0.0)
flmi = Arr(0, 0.0)
fldn = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, flup, INDICATOR_DATA)
    SetIndexBuffer(1, flmi, INDICATOR_DATA)
    SetIndexBuffer(2, fldn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range action verification index (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _maFast = iSma(_price, inpFastPeriod, i, rates_total, 0)
        _maSlow = iSma(_price, inpSlowPeriod, i, rates_total, 1)
        val[i] = (_fdiv(100.0 * (_maFast - _maSlow), _maSlow) if (_maSlow != 0) else 0)
        _start = MathMax(i - inpFlPeriod + 1, 0)
        min_ = val[ArrayMinimum(val, _start, inpFlPeriod)]
        max_ = val[ArrayMaximum(val, _start, inpFlPeriod)]
        range_ = max_ - min_
        flup[i] = min_ + ((inpFlLevelUp * range_) / 100.0)
        fldn[i] = min_ + ((inpFlLevelDown * range_) / 100.0)
        flmi[i] = min_ + ((50 * range_) / 100.0)
        _sw1 = inpColorMode
        if _sw1 == col_onOuter:
            valc[i] = (2 if (val[i] > flup[i]) else 1 if (val[i] < fldn[i]) else 0)
        elif _sw1 == col_onZero:
            valc[i] = (2 if (val[i] > flmi[i]) else 1 if (val[i] < flmi[i]) else valc[i - 1] if (i > 0) else 0)
    return rates_total

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

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw2 = tprice
        if _sw2 == PRICE_CLOSE:
            return close[i]
        elif _sw2 == PRICE_OPEN:
            return open[i]
        elif _sw2 == PRICE_HIGH:
            return high[i]
        elif _sw2 == PRICE_LOW:
            return low[i]
        elif _sw2 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ravi(_MQL5Indicator):
    name = 'Ravi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpFastPeriod': 7,  # Fast period
        'inpSlowPeriod': 65,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 32,  # Floating levels period
        'inpFlLevelUp': 80.0,  # Up level %
        'inpFlLevelDown': 20.0,  # Down level %
        'inpColorMode': _Choice({0: 'Change color on middle line cross', 1: 'Change color on outer levels cross'}, default=1),  # Change color mode
    }

