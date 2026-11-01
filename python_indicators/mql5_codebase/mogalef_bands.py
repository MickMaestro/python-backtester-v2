"""Mogalef bands — converted from MQL5: MQL5 Indicators/Mogalef bands/Mogalef bands.mq5

Mogalef bands
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [2263842], 2: [11119017], 3: [3937500]}, 'widths': {}, 'styles': {2: 2}, 'labels': {1: 'Level up', 2: 'Middle level', 3: 'Level down'}, 'levels': [], 'description': ['Mogalef bands'], 'name': 'Mogalef bands', 'source': 'MQL5 Indicators/Mogalef bands/Mogalef bands.mq5', 'folder': 'Mogalef bands', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 3, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDeviationsPeriod', 'py': 'inpDeviationsPeriod', 'param': 'inpDeviationsPeriod', 'type': 'int', 'default': 7, 'label': 'Deviations period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 3)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDeviationsPeriod = _input('inpDeviationsPeriod', 7)  # Deviations period
levup = Arr(0, 0.0)
levmi = Arr(0, 0.0)
levdn = Arr(0, 0.0)
workDev = Arr(0, 0.0, dims=(1,))
workLinr = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levmi, INDICATOR_DATA)
    SetIndexBuffer(2, levdn, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mogalef bands (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        linreg = iLinr(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        deviation = iDeviation(linreg, inpDeviationsPeriod, i, rates_total)
        if i == 0:
            levup[i] = linreg
            levdn[i] = linreg
            levmi[i] = linreg
            continue
        levup[i] = levup[i - 1]
        levdn[i] = levdn[i - 1]
        levmi[i] = levmi[i - 1]
        if linreg > levup[i - 1] or linreg < levdn[i - 1]:
            levup[i] = linreg + (2.0 * deviation)
            levdn[i] = linreg - (2.0 * deviation)
            levmi[i] = linreg
    return rates_total

def iDeviation(value, length, i, bars, instanceNo=0, isSample=False):
    if ArrayRange(workDev, 0) != bars:
        ArrayResize(workDev, bars)
    workDev[i][instanceNo] = value
    if i < length:
        return 0.0
    sumx = 0.0
    sumxx = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        pass
        sumx += workDev[i - k][instanceNo]
        sumxx += workDev[i - k][instanceNo] * workDev[i - k][instanceNo]
        k += 1
    return MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, float(length)), MathMax(length - isSample, 1)))

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
    return _fdiv(3.0 * lwma, lwmw) - _fdiv(2.0 * sma, float(period))

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


class MogalefBands(_MQL5Indicator):
    name = 'Mogalef bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 3,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDeviationsPeriod': 7,  # Deviations period
    }

