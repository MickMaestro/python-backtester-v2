"""Volatilty bands percent — converted from MQL5: MQL5 Indicators/Volatility Bands Percent/Volatilty bands percent.mq5

Volatility bands percent
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16760576]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Volatility band percent'}, 'levels': [], 'description': ['Volatility bands percent'], 'name': 'Volatilty bands percent', 'source': 'MQL5 Indicators/Volatility Bands Percent/Volatilty bands percent.mq5', 'folder': 'Volatility Bands Percent', 'inputs': [{'mql': 'inpBandPeriod', 'py': 'inpBandPeriod', 'param': 'inpBandPeriod', 'type': 'int', 'default': 20, 'label': 'Bands period period', 'sinput': False}, {'mql': 'inpBandDeviations', 'py': 'inpBandDeviations', 'param': 'inpBandDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviations', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDeviationsType', 'py': 'inpDeviationsType', 'param': 'inpDeviationsType', 'type': 'int', 'default': 1, 'label': 'Deviations type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDevType
use_classical = 0
use_rooke = 1
_enum('enDevType', {0: 'use_classical', 1: 'use_rooke'})

# ---- inputs and global variables
inpBandPeriod = _input('inpBandPeriod', 20)  # Bands period period
inpBandDeviations = _input('inpBandDeviations', 2.0)  # Bands deviations
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDeviationsType = _input('inpDeviationsType', use_rooke)  # Deviations type
bandm = Arr(0, 0.0)
percent = Arr(0, 0.0)
prices = Arr(0, 0.0)
workTema = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, percent, INDICATOR_DATA)
    SetIndexBuffer(1, bandm, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 100)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility bands percent (' + _str(inpBandPeriod) + ',' + _str(inpBandDeviations) + ')')
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
        width = inpBandDeviations * iDeviationPlus(prices, bandm, inpBandPeriod, i)
        percent[i] = (_fdiv(100.0 * (prices[i] - bandm[i]), width) if (width > 0) else 0)
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


class VolatiltyBandsPercent(_MQL5Indicator):
    name = 'Volatilty bands percent'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBandPeriod': 20,  # Bands period period
        'inpBandDeviations': 2.0,  # Bands deviations
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDeviationsType': _Choice({0: 'Use classical deviations', 1: 'Use David Rooke type of deviations'}, default=1),  # Deviations type
    }

