"""Deviation scaled MA crosses — converted from MQL5: MQL5 Indicators/Deviation scaled MA crosses/Deviation scaled MA crosses.mq5

Deviation scaled ma crosses
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'DSMA fast', 2: 'DSMA slow'}, 'levels': [], 'description': ['Deviation scaled ma crosses'], 'name': 'Deviation scaled MA crosses', 'source': 'MQL5 Indicators/Deviation scaled MA crosses/Deviation scaled MA crosses.mq5', 'folder': 'Deviation scaled MA crosses', 'inputs': [{'mql': 'inpPeriodFast', 'py': 'inpPeriodFast', 'param': 'inpPeriodFast', 'type': 'double', 'default': 40.0, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpPeriodSlow', 'py': 'inpPeriodSlow', 'param': 'inpPeriodSlow', 'type': 'double', 'default': 100.0, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodFast = _input('inpPeriodFast', 40.0)  # Fast period
inpPeriodSlow = _input('inpPeriodSlow', 100.0)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
valsc = Arr(0, 0.0)
workDsma = Arr(0, 0.0, dims=(6,))
workDsmaCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vals, INDICATOR_DATA)
    SetIndexBuffer(3, valsc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Deviation scaled MA crosses (' + _str(inpPeriodFast) + ',' + _str(inpPeriodSlow) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        filter_ = ((close[i] - close[i - 2]) if (i > 1) else 0)
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iDsma(price, filter_, inpPeriodFast, i, rates_total, 0)
        vals[i] = iDsma(price, filter_, inpPeriodSlow, i, rates_total, 1)
        valc[i] = (2 if (val[i] > vals[i]) else 1 if (val[i] < vals[i]) else valc[i - 1] if (i > 0) else 0)
        valsc[i] = valc[i]
    return rates_total

def iDsma(price, filter_, period, i, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workDsma, 0) != bars:
        ArrayResize(workDsma, bars)
    if ArrayRange(workDsmaCoeffs, 0) < (instanceNo + 1):
        ArrayResize(workDsmaCoeffs, instanceNo + 1)
    if workDsmaCoeffs[instanceNo][0] != period:
        workDsmaCoeffs[instanceNo][0] = period
        a1 = MathExp(_fdiv(-1.414 * M_PI, period))
        b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, period))
        workDsmaCoeffs[instanceNo][2] = b1
        workDsmaCoeffs[instanceNo][3] = (-a1) * a1
        workDsmaCoeffs[instanceNo][1] = 1.0 - workDsmaCoeffs[instanceNo][2] - workDsmaCoeffs[instanceNo][3]
    s = instanceNo * 3
    workDsma[i][s + 2] = filter_
    workDsma[i][s + 0] = filter_
    if i > 1:
        workDsma[i][s + 2] = ((workDsmaCoeffs[instanceNo][1] * (workDsma[i][s + 0] + workDsma[i - 1][s + 0])) / 2.0) + (workDsmaCoeffs[instanceNo][2] * workDsma[i - 1][s + 2]) + (workDsmaCoeffs[instanceNo][3] * workDsma[i - 2][s + 2])
    rms = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        rms += workDsma[i - k][s + 2] * workDsma[i - k][s + 2]
        k += 1
    rms = MathSqrt(_fdiv(rms, period))
    _scaledFilt = (_fdiv(workDsma[i][s + 2], rms) if (rms != 0) else 1)
    _alpha = _fdiv(MathAbs(_scaledFilt) * 5, period)
    workDsma[i][s + 1] = ((workDsma[i - 1][s + 1] + (_alpha * (price - workDsma[i - 1][s + 1]))) if (i > 0) else price)
    return workDsma[i][s + 1]

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


class DeviationScaledMACrosses(_MQL5Indicator):
    name = 'Deviation scaled MA crosses'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriodFast': 40.0,  # Fast period
        'inpPeriodSlow': 100.0,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

