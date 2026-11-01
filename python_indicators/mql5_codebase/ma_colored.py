"""ma_colored — converted from MQL5: MQL5 Indicators/Classic Moving Averages with colors/ma_colored.mq5

Classic Moving Averages with colors
Copyright: Copyright © 2020, mplavonil; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2020, mplavonil', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Classic Moving Averages with colors'], 'name': 'ma_colored', 'source': 'MQL5 Indicators/Classic Moving Averages with colors/ma_colored.mq5', 'folder': 'Classic Moving Averages with colors', 'inputs': [{'mql': 'MaPeriod', 'py': 'MaPeriod', 'param': 'MaPeriod', 'type': 'int', 'default': 9, 'label': 'Period', 'sinput': False}, {'mql': 'MaMethod', 'py': 'MaMethod', 'param': 'MaMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMATypes
_sma = 0
_ema = 1
_smma = 2
_lwma = 3
_enum('enMATypes', {0: '_sma', 1: '_ema', 2: '_smma', 3: '_lwma'})

# ---- inputs and global variables
MaPeriod = _input('MaPeriod', 9)  # Period
MaMethod = _input('MaMethod', _sma)  # Method
Price = _input('Price', PRICE_CLOSE)  # Price
MaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
maArray = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, shortName(MaMethod))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total, 0)
        MaBuffer[i] = iCustomMa(MaMethod, price, MaPeriod, rates_total, i)
        if i > 0:
            ColorBuffer[i] = ColorBuffer[i - 1]
            if MaBuffer[i] > MaBuffer[i - 1]:
                ColorBuffer[i] = 0.0
            if MaBuffer[i] < MaBuffer[i - 1]:
                ColorBuffer[i] = 1.0
        else:
            ColorBuffer[i] = 0.0
        i += 1
    return rates_total

def shortName(mode):
    _sw1 = mode
    if _sw1 == _sma:
        return 'Simple MA (' + _str(MaPeriod) + ')'
    elif _sw1 == _ema:
        return 'Exponential MA (' + _str(MaPeriod) + ')'
    elif _sw1 == _smma:
        return 'Smoothed MA (' + _str(MaPeriod) + ')'
    elif _sw1 == _lwma:
        return 'Linear weighted  MA (' + _str(MaPeriod) + ')'
    else:
        return 'Moving Average (' + _str(MaPeriod) + ')'

def iCustomMa(mode, price, period, bars, r):
    _sw2 = mode
    if _sw2 == _sma:
        return iSMA(price, period, bars, r)
    elif _sw2 == _ema:
        return iEMA(price, period, bars, r)
    elif _sw2 == _smma:
        return iSMMA(price, period, bars, r)
    elif _sw2 == _lwma:
        return iLWMA(price, period, bars, r)
    else:
        return price

def iSMA(price, period, bars, r):
    if ArraySize(maArray) != bars:
        ArrayResize(maArray, bars)
    maArray[r] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += maArray[r - k]
        k += 1
    return _fdiv(avg, float(k))

def iEMA(price, period, bars, r):
    if ArraySize(maArray) != bars:
        ArrayResize(maArray, bars)
    maArray[r] = price
    if r > 0 and period > 1:
        maArray[r] = maArray[r - 1] + (_fdiv(2.0, 1.0 + period) * (price - maArray[r - 1]))
    return maArray[r]

def iSMMA(price, period, bars, r):
    if ArraySize(maArray) != bars:
        ArrayResize(maArray, bars)
    maArray[r] = price
    if r > 1 and period > 1:
        maArray[r] = maArray[r - 1] + _fdiv(price - maArray[r - 1], period)
    return maArray[r]

def iLWMA(price, period, bars, r):
    if ArraySize(maArray) != bars:
        ArrayResize(maArray, bars)
    maArray[r] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * maArray[r - k]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    _sw3 = tprice
    if _sw3 == PRICE_CLOSE:
        return close[i]
    elif _sw3 == PRICE_OPEN:
        return open[i]
    elif _sw3 == PRICE_HIGH:
        return high[i]
    elif _sw3 == PRICE_LOW:
        return low[i]
    elif _sw3 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaColored(_MQL5Indicator):
    name = 'ma_colored'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaPeriod': 9,  # Period
        'MaMethod': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear weighted'}, default=0),  # Method
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

