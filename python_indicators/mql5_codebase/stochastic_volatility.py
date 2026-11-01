"""Stochastic volatility — converted from MQL5: MQL5 Indicators/Stochastic volatility/Stochastic volatility.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 8, 4: 1}, 'colors': {1: [3329330], 2: [42495], 3: [11119017, 3329330], 4: [17919]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2, 4: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'Stochastic volatility', 4: 'Signal'}, 'levels': [], 'description': [], 'name': 'Stochastic volatility', 'source': 'MQL5 Indicators/Stochastic volatility/Stochastic volatility.mq5', 'folder': 'Stochastic volatility', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 30, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'BandsLength', 'py': 'BandsLength', 'param': 'BandsLength', 'type': 'int', 'default': 126, 'label': 'Bands period', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'Bands deviation', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'OriginalStoch', 'py': 'OriginalStoch', 'param': 'OriginalStoch', 'type': 'bool', 'default': True, 'label': 'Calculate using original stochastic', 'sinput': False}, {'mql': 'OriginalVolatility', 'py': 'OriginalVolatility', 'param': 'OriginalVolatility', 'type': 'bool', 'default': True, 'label': 'Calculate using original volatility', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 30)  # Stochastic period
Slowing = _input('Slowing', 5)  # Stochastic slowing
Signal = _input('Signal', 5)  # Signal period
BandsLength = _input('BandsLength', 126)  # Bands period
BandsDeviation = _input('BandsDeviation', 1.0)  # Bands deviation
Price = _input('Price', PRICE_CLOSE)  # Price
OriginalStoch = _input('OriginalStoch', True)  # Calculate using original stochastic
OriginalVolatility = _input('OriginalVolatility', True)  # Calculate using original volatility
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
prices = Arr(0, 0.0)
logBuffer = Arr(0, 0.0)
volBuffer = Arr(0, 0.0)
wrkBuffer = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, logBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, volBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic volatility (' + _str(Length) + ',' + _str(Slowing) + ',' + _str(Signal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(wrkBuffer, 0) != rates_total:
        ArrayResize(wrkBuffer, rates_total)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        vol1 = volatility(prices, logBuffer, 10, i) * 3.0
        vol2 = volatility(prices, logBuffer, 21, i) * 3.0
        vol3 = volatility(prices, logBuffer, 34, i) * 2.0
        vol4 = volatility(prices, logBuffer, 55, i)
        vol5 = volatility(prices, logBuffer, 89, i)
        volBuffer[i] = vol1 + vol2 + vol3 + vol4 + vol5
        hi = volBuffer[i]
        lo = volBuffer[i]
        k = 1
        while k < Length and (i - k) >= 0:
            hi = MathMax(hi, volBuffer[i - k])
            lo = MathMin(lo, volBuffer[i - k])
            k += 1
        wrkBuffer[i][0] = hi
        wrkBuffer[i][1] = lo
        stoc = 0.0
        if OriginalStoch:
            sumRng = 0.0
            sumLow = 0.0
            k = 0
            while k < Slowing and (i - k) >= 0:
                sumRng += wrkBuffer[i - k][0] - wrkBuffer[i - k][1]
                sumLow += volBuffer[i - k] - wrkBuffer[i - k][1]
                k += 1
            if sumRng != 0:
                stoc = _fdiv(100 * sumLow, sumRng)
        else:
            stov = 0.0
            if hi != lo:
                stov = _fdiv(100 * (volBuffer[i] - lo), hi - lo)
            stoc = (MathMax(MathMin(val[i - 1] + (_fdiv(2.0, 1.0 + Slowing) * (stov - val[i - 1])), 100), 0) if (i > 0) else 0)
        val[i] = stoc
        signal[i] = iSma(val, Signal, i)
        average = iSma(val, BandsLength, i)
        deviation = iDeviation(val, BandsLength, average, i)
        levelUp[i] = average + deviation + BandsDeviation
        levelDn[i] = average - deviation + BandsDeviation
        valc[i] = (1 if (val[i] < levelDn[i]) else 0)
        i += 1
    return i

def volatility(array, destArray, length, i):
    destArray[i] = ((MathLog(_fdiv(array[i], array[i - 1])) if (array[i - 1] != 0) else 0) if (i > 0) else 0)
    if i >= length:
        average = destArray[i]
        dSum = 0.0
        k = 0
        while k < length and (i - k) >= 0:
            average += destArray[i - k]
            k += 1
        average = _fdiv(average, float(length))
        k = 0
        while k < length and (i - k) >= 0:
            dSum += (destArray[i - k] - average) * (destArray[i - k] - average)
            k += 1
        deviation = MathSqrt(_fdiv(dSum, length))
        if OriginalVolatility:
            return (average + deviation) * MathSqrt(252)
        else:
            return deviation
    else:
        return 0.0

def iSma(array, period, pos):
    sum_ = array[pos]
    i = 1
    while i < period and (pos - i) >= 0:
        sum_ += array[pos - i]
        i += 1
    return _fdiv(sum_, period)

def iDeviation(array, period, dMA, pos):
    dSum = 0.0
    i = 0
    while i < period and (pos - i) >= 0:
        dSum += (array[pos - i] - dMA) * (array[pos - i] - dMA)
        i += 1
    return MathSqrt(_fdiv(dSum, period))

def getPrice(tprice, open, close, high, low, i, _bars):
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


class StochasticVolatility(_MQL5Indicator):
    name = 'Stochastic volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 30,  # Stochastic period
        'Slowing': 5,  # Stochastic slowing
        'Signal': 5,  # Signal period
        'BandsLength': 126,  # Bands period
        'BandsDeviation': 1.0,  # Bands deviation
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'OriginalStoch': True,  # Calculate using original stochastic
        'OriginalVolatility': True,  # Calculate using original volatility
    }

