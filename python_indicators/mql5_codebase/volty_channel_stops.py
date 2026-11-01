"""Volty channel stops — converted from MQL5: MQL5 Indicators/Volty channel stops/Volty channel stops.mq5

Volty channel stops
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 12}, 'colors': {1: [14474460], 2: [14474460], 3: [16748574], 4: [6333684], 5: [12632256, 16748574, 6333684]}, 'widths': {3: 3, 4: 3, 5: 2}, 'styles': {1: 2, 2: 2}, 'labels': {}, 'levels': [], 'description': ['Volty channel stops'], 'name': 'Volty channel stops', 'source': 'MQL5 Indicators/Volty channel stops/Volty channel stops.mq5', 'folder': 'Volty channel stops', 'inputs': [{'mql': 'AtrPeriod', 'py': 'AtrPeriod', 'param': 'AtrPeriod', 'type': 'int', 'default': 10, 'label': 'ATR period', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 4.0, 'label': 'ATR multiplier', 'sinput': False}, {'mql': 'MaPeriod', 'py': 'MaPeriod', 'param': 'MaPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'MaMethod', 'py': 'MaMethod', 'param': 'MaMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 1.0, 'label': 'Money risk', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
AtrPeriod = _input('AtrPeriod', 10)  # ATR period
Kv = _input('Kv', 4.0)  # ATR multiplier
MaPeriod = _input('MaPeriod', 10)  # Smoothing period
MaMethod = _input('MaMethod', ma_sma)  # Smoothing method
Price = _input('Price', PRICE_CLOSE)  # Price
Risk = _input('Risk', 1.0)  # Money risk
bba = Arr(0, 0.0)
bbc = Arr(0, 0.0)
bblu = Arr(0, 0.0)
bbld = Arr(0, 0.0)
amax = Arr(0, 0.0)
amin = Arr(0, 0.0)
bmax = Arr(0, 0.0)
bmin = Arr(0, 0.0)
trend = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, bmax, INDICATOR_DATA)
    SetIndexBuffer(1, bmin, INDICATOR_DATA)
    SetIndexBuffer(2, bblu, INDICATOR_DATA)
    SetIndexBuffer(3, bbld, INDICATOR_DATA)
    SetIndexBuffer(4, bba, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    SetIndexBuffer(5, bbc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, amax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, amin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, trend, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        ma = iCustomMa(MaMethod, price, MaPeriod, i, rates_total, 0)
        atr = 0.0
        k = 0
        while k < AtrPeriod and (i - k - 1) >= 0:
            atr += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        atr = atr / AtrPeriod
        amax[i] = ma + (atr * Kv)
        amin[i] = ma - (atr * Kv)
        bmax[i] = amax[i] + (0.5 * (Risk - 1) * (amax[i] - amin[i]))
        bmin[i] = amin[i] - (0.5 * (Risk - 1) * (amax[i] - amin[i]))
        trend[i] = ((1 if (price > amax[i - 1]) else -1 if (price < amin[i - 1]) else trend[i - 1]) if (i > 0) else 0)
        if i > 0:
            if trend[i] == -1 and amax[i] > amax[i - 1]:
                amax[i] = amax[i - 1]
            if trend[i] == 1 and amin[i] < amin[i - 1]:
                amin[i] = amin[i - 1]
            if trend[i] == -1 and bmax[i] > bmax[i - 1]:
                bmax[i] = bmax[i - 1]
            if trend[i] == 1 and bmin[i] < bmin[i - 1]:
                bmin[i] = bmin[i - 1]
        bblu[i] = EMPTY_VALUE
        bbld[i] = EMPTY_VALUE
        if trend[i] == 1:
            bblu[i] = bmin[i]
            bbc[i] = 1.0
        if trend[i] == -1:
            bbld[i] = bmax[i]
            bbc[i] = 2.0
        bba[i] = (((bblu[i] if (trend[i] == 1) else bbld[i]) if (trend[i] != trend[i - 1]) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        i += 1
    return i

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    k = 1
    workSma[r][instanceNo + 0] = price
    avg = price
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    avg = _fdiv(avg, float(k))
    return avg

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

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


class VoltyChannelStops(_MQL5Indicator):
    name = 'Volty channel stops'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AtrPeriod': 10,  # ATR period
        'Kv': 4.0,  # ATR multiplier
        'MaPeriod': 10,  # Smoothing period
        'MaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'Risk': 1.0,  # Money risk
    }

