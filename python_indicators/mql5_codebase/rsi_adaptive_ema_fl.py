"""RSI adaptive EMA - fl — converted from MQL5: MQL5 Indicators/RSI adaptive EMA - floating levels/RSI adaptive EMA - fl.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [2263842], 2: [11119017], 3: [3937500], 4: [11119017, 3937500, 2263842]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Level up', 2: 'Middle level', 3: 'Level down', 4: 'RSI adaptive EMA'}, 'levels': [], 'description': [], 'name': 'RSI adaptive EMA - fl', 'source': 'MQL5 Indicators/RSI adaptive EMA - floating levels/RSI adaptive EMA - fl.mq5', 'folder': 'RSI adaptive EMA - floating levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 32.0, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 32, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 1, 'label': 'Change color mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
col_onZero = 0
col_onOuter = 1
_enum('enColorMode', {0: 'col_onZero', 1: 'col_onOuter'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32.0)  # RSI period
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
workRsi = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, flup, INDICATOR_DATA)
    SetIndexBuffer(1, flmi, INDICATOR_DATA)
    SetIndexBuffer(2, fldn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI adaptive EMA with floating levels(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _alpha = MathAbs((iRsi(_price, inpPeriod, i, rates_total) / 100.0) - 0.5) * 2.0
        val[i] = ((val[i - 1] + (_alpha * (_price - val[i - 1]))) if (i > 0) else _price)
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

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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


class RSIAdaptiveEMAFl(_MQL5Indicator):
    name = 'RSI adaptive EMA - fl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32.0,  # RSI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 32,  # Floating levels period
        'inpFlLevelUp': 80.0,  # Up level %
        'inpFlLevelDown': 20.0,  # Down level %
        'inpColorMode': _Choice({0: 'Change color on middle line cross', 1: 'Change color on outer levels cross'}, default=1),  # Change color mode
    }

