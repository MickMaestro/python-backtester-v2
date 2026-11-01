"""ADXVMA histogram — converted from MQL5: MQL5 Indicators/ADXVMA Histogram/ADXVMA histogram.mq5

ADXVMA moving average - histogram version
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'ADXVMA'}, 'levels': [], 'description': ['ADXVMA moving average - histogram version'], 'name': 'ADXVMA histogram', 'source': 'MQL5 Indicators/ADXVMA Histogram/ADXVMA histogram.mq5', 'folder': 'ADXVMA Histogram', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
adxvma = Arr(0, 0.0)
adxvmaWork = Arr(0, 0.0, dims=(7,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, adxvma, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADXVMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        adxvma[i] = iAdxvma(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        val[i] = 1.0
        valc[i] = ((2 if (adxvma[i] > adxvma[i - 1]) else 1 if (adxvma[i] < adxvma[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iAdxvma(price, period, r, bars, instanceNo=0):
    if ArrayRange(adxvmaWork, 0) != bars:
        ArrayResize(adxvmaWork, bars)
    instanceNo *= 7
    adxvmaWork[r][instanceNo + 0] = price
    if r < 1:
        adxvmaWork[r][instanceNo + 6] = adxvmaWork[r][instanceNo + 0]
        return adxvmaWork[r][6]
    tpdm = 0.0
    tmdm = 0.0
    diff = adxvmaWork[r][instanceNo + 0] - adxvmaWork[r - 1][instanceNo + 0]
    if diff > 0:
        tpdm = diff
    else:
        tmdm = -diff
    adxvmaWork[r][instanceNo + 1] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 1]) + tpdm, period)
    adxvmaWork[r][instanceNo + 2] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 2]) + tmdm, period)
    trueRange = adxvmaWork[r][instanceNo + 1] + adxvmaWork[r][instanceNo + 2]
    tpdi = 0.0
    tmdi = 0.0
    if trueRange > 0:
        tpdi = _fdiv(adxvmaWork[r][instanceNo + 1], trueRange)
        tmdi = _fdiv(adxvmaWork[r][instanceNo + 2], trueRange)
    adxvmaWork[r][instanceNo + 3] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 3]) + tpdi, period)
    adxvmaWork[r][instanceNo + 4] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 4]) + tmdi, period)
    tout = 0.0
    if (adxvmaWork[r][instanceNo + 3] + adxvmaWork[r][instanceNo + 4]) > 0:
        tout = _fdiv(MathAbs(adxvmaWork[r][instanceNo + 3] - adxvmaWork[r][instanceNo + 4]), adxvmaWork[r][instanceNo + 3] + adxvmaWork[r][instanceNo + 4])
    adxvmaWork[r][instanceNo + 5] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 5]) + tout, period)
    thi = MathMax(adxvmaWork[r][instanceNo + 5], adxvmaWork[r - 1][instanceNo + 5])
    tlo = MathMin(adxvmaWork[r][instanceNo + 5], adxvmaWork[r - 1][instanceNo + 5])
    j = 2
    while j < _int(period) and (r - j) >= 0:
        thi = MathMax(adxvmaWork[r - j][instanceNo + 5], thi)
        tlo = MathMin(adxvmaWork[r - j][instanceNo + 5], tlo)
        j += 1
    vi = 0.0
    if (thi - tlo) > 0:
        vi = _fdiv(adxvmaWork[r][instanceNo + 5] - tlo, thi - tlo)
    adxvmaWork[r][instanceNo + 6] = _fdiv(((period - vi) * adxvmaWork[r - 1][instanceNo + 6]) + (vi * adxvmaWork[r][instanceNo + 0]), period)
    return adxvmaWork[r][instanceNo + 6]

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


class ADXVMAHistogram(_MQL5Indicator):
    name = 'ADXVMA histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }
    y_range = (0.0, 1.0)

