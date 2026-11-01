"""Deviation scaled MA — converted from MQL5: MQL5 Indicators/Deviation scaled MA/Deviation scaled MA.mq5

Deviation scaled MA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'DSMA'}, 'levels': [], 'description': ['Deviation scaled MA'], 'name': 'Deviation scaled MA', 'source': 'MQL5 Indicators/Deviation scaled MA/Deviation scaled MA.mq5', 'folder': 'Deviation scaled MA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'MA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # MA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
flt = Arr(0, 0.0)
workSsm = Arr(0, 0.0, dims=(2,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, flt, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Deviation scaled MA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        flt[i] = (iSsm(close[i] - close[i - 2], inpPeriod, i, rates_total) if (i > 1) else 0)
        rms = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            rms += flt[i - k] * flt[i - k]
            k += 1
        rms = MathSqrt(rms / inpPeriod)
        _scaledFilt = (_fdiv(flt[i], rms) if (rms != 0) else 1)
        _alpha = (MathAbs(_scaledFilt) * 5) / inpPeriod
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = ((val[i - 1] + (_alpha * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iSsm(price, period, i, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSsm, 0) != bars:
        ArrayResize(workSsm, bars)
    if ArrayRange(workSsmCoeffs, 0) < (instanceNo + 1):
        ArrayResize(workSsmCoeffs, instanceNo + 1)
    if workSsmCoeffs[instanceNo][0] != period:
        workSsmCoeffs[instanceNo][0] = period
        a1 = MathExp(_fdiv(-1.414 * M_PI, period))
        b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, period))
        workSsmCoeffs[instanceNo][2] = b1
        workSsmCoeffs[instanceNo][3] = (-a1) * a1
        workSsmCoeffs[instanceNo][1] = 1.0 - workSsmCoeffs[instanceNo][2] - workSsmCoeffs[instanceNo][3]
    s = instanceNo * 2
    workSsm[i][s + 1] = price
    workSsm[i][s + 0] = price
    if i > 1:
        workSsm[i][s + 1] = ((workSsmCoeffs[instanceNo][1] * (workSsm[i][s + 0] + workSsm[i - 1][s + 0])) / 2.0) + (workSsmCoeffs[instanceNo][2] * workSsm[i - 1][s + 1]) + (workSsmCoeffs[instanceNo][3] * workSsm[i - 2][s + 1])
    return workSsm[i][s + 1]

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


class DeviationScaledMA(_MQL5Indicator):
    name = 'Deviation scaled MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # MA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

