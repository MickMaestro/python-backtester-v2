"""Volatilty bands — converted from MQL5: MQL5 Indicators/Volatilty Bands/Volatilty bands.mq5

Volatility bands
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [11119017], 3: [17919]}, 'widths': {}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Volatility band up', 2: 'Volatility band middle', 3: 'Volatility band down'}, 'levels': [], 'description': ['Volatility bands'], 'name': 'Volatilty bands', 'source': 'MQL5 Indicators/Volatilty Bands/Volatilty bands.mq5', 'folder': 'Volatilty Bands', 'inputs': [{'mql': 'inpBandPeriod', 'py': 'inpBandPeriod', 'param': 'inpBandPeriod', 'type': 'int', 'default': 20, 'label': 'Bands period period', 'sinput': False}, {'mql': 'inpBandDeviations', 'py': 'inpBandDeviations', 'param': 'inpBandDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviations', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDeviationsType', 'py': 'inpDeviationsType', 'param': 'inpDeviationsType', 'type': 'int', 'default': 1, 'label': 'Deviations type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDevType
use_classical = 0
use_rooke = 1
_enum('enDevType', {0: 'use_classical', 1: 'use_rooke'})

# ---- inputs and global variables
inpBandPeriod = _input('inpBandPeriod', 20)  # Bands period period
inpBandDeviations = _input('inpBandDeviations', 2.0)  # Bands deviations
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDeviationsType = _input('inpDeviationsType', use_rooke)  # Deviations type
bandu = Arr(0, 0.0)
bandm = Arr(0, 0.0)
bandd = Arr(0, 0.0)
prices = Arr(0, 0.0)
workTema = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, bandu, INDICATOR_DATA)
    SetIndexBuffer(1, bandm, INDICATOR_DATA)
    SetIndexBuffer(2, bandd, INDICATOR_DATA)
    SetIndexBuffer(3, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility bands (' + _str(inpBandPeriod) + ',' + _str(inpBandDeviations) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, close, open, high, low, i, rates_total)
        tema1 = iTema(prices[i], inpBandPeriod, i, rates_total, 0)
        tema2 = iTema(tema1, inpBandPeriod, i, rates_total, 1)
        bandm[i] = (2.0 * tema1) - tema2
        deviation = iDeviationPlus(prices, bandm, inpBandPeriod, i)
        bandu[i] = bandm[i] + (deviation * inpBandDeviations)
        bandd[i] = bandm[i] - (deviation * inpBandDeviations)
        i += 1
    return i

def iTema(price, period, r, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workTema, 0) != bars:
        ArrayResize(workTema, bars)
    instanceNo *= 3
    workTema[r][0 + instanceNo] = price
    workTema[r][1 + instanceNo] = price
    workTema[r][2 + instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workTema[r][0 + instanceNo] = workTema[r - 1][0 + instanceNo] + (alpha * (price - workTema[r - 1][0 + instanceNo]))
        workTema[r][1 + instanceNo] = workTema[r - 1][1 + instanceNo] + (alpha * (workTema[r][0 + instanceNo] - workTema[r - 1][1 + instanceNo]))
        workTema[r][2 + instanceNo] = workTema[r - 1][2 + instanceNo] + (alpha * (workTema[r][1 + instanceNo] - workTema[r - 1][2 + instanceNo]))
    return workTema[r][2 + instanceNo] + (3.0 * (workTema[r][0 + instanceNo] - workTema[r][1 + instanceNo]))

def iDeviationPlus(values, ma, period, i):
    sum_ = 0.0
    if inpDeviationsType == use_classical:
        k = 0
        while k < period and (i - k) >= 0:
            sum_ += (values[i - k] - ma[i]) * (values[i - k] - ma[i])
            k += 1
    else:
        k = 0
        while k < period and (i - k) >= 0:
            sum_ += (values[i - k] - ma[i - k]) * (values[i - k] - ma[i - k])
            k += 1
    return MathSqrt(_fdiv(sum_, period))

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


class VolatiltyBands(_MQL5Indicator):
    name = 'Volatilty bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBandPeriod': 20,  # Bands period period
        'inpBandDeviations': 2.0,  # Bands deviations
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDeviationsType': _Choice({0: 'Use classical deviations', 1: 'Use David Rooke type of deviations'}, default=1),  # Deviations type
    }

