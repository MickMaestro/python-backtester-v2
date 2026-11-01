"""Rsx QQE - new zl — converted from MQL5: MQL5 Indicators/RSX QQE New/Rsx QQE - new zl.mq5

Rsx QQE new
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'QQE'}, 'levels': [], 'description': ['Rsx QQE new'], 'name': 'Rsx QQE - new zl', 'source': 'MQL5 Indicators/RSX QQE New/Rsx QQE - new zl.mq5', 'folder': 'RSX QQE New', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSX period', 'sinput': False}, {'mql': 'inpRsiSmoothingFactor', 'py': 'inpRsiSmoothingFactor', 'param': 'inpRsiSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'RSX smoothing factor', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'QQE quantifier', 'sinput': False}, {'mql': 'inpUpBound', 'py': 'inpUpBound', 'param': 'inpUpBound', 'type': 'double', 'default': 10.0, 'label': 'Upper bound', 'sinput': False}, {'mql': 'inpDnBound', 'py': 'inpDnBound', 'param': 'inpDnBound', 'type': 'double', 'default': -10.0, 'label': 'Lower bound', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSX period
inpRsiSmoothingFactor = _input('inpRsiSmoothingFactor', 5)  # RSX smoothing factor
inpWPSlow = _input('inpWPSlow', 4.236)  # QQE quantifier
inpUpBound = _input('inpUpBound', 10.0)  # Upper bound
inpDnBound = _input('inpDnBound', -10.0)  # Lower bound
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
vald = Arr(0, 0.0)
valc = Arr(0, 0.0)
levs = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(13,))
workEma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, vald, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, levs, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpUpBound)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpDnBound)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsx QQE new (' + _str(inpRsiPeriod) + ',' + _str(inpRsiSmoothingFactor) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iEma(iRsi(getPrice(inpPrice, open, close, high, low, i, rates_total), inpRsiPeriod, i, rates_total), inpRsiSmoothingFactor, i, rates_total, 0)
        _iEma = iEma((MathAbs(val[i - 1] - val[i]) if (i > 0) else 0), inpRsiPeriod, i, rates_total, 1)
        _iEmm = iEma(_iEma, inpRsiPeriod, i, rates_total, 2)
        _iEms = _iEmm * inpWPSlow
        tr = (levs[i - 1] if (i > 0) else 0)
        dv = tr
        if val[i] < tr:
            tr = val[i] + _iEms
            if (i > 0 and val[i - 1] < dv) and tr > dv:
                tr = dv
        if val[i] > tr:
            tr = val[i] - _iEms
            if (i > 0 and val[i - 1] > dv) and tr < dv:
                tr = dv
        levs[i] = tr
        vald[i] = val[i] - 50
        valc[i] = (1 if (vald[i] > inpUpBound) else 2 if (vald[i] < inpDnBound) else 0)
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 13
    workRsi[r][z + 0] = price
    Kg = _fdiv(3.0, 2.0 + period)
    Hg = 1.0 - Kg
    if r < period:
        for k in range(1, 13):
            workRsi[r][k + z] = 0.0
        return 50.0
    mom = workRsi[r][0 + z] - workRsi[r - 1][0 + z]
    moa = MathAbs(mom)
    for k in range(0, 3):
        kk = k * 2
        workRsi[r][z + kk + 1] = (Kg * mom) + (Hg * workRsi[r - 1][z + kk + 1])
        workRsi[r][z + kk + 2] = (Kg * workRsi[r][z + kk + 1]) + (Hg * workRsi[r - 1][z + kk + 2])
        mom = (1.5 * workRsi[r][z + kk + 1]) - (0.5 * workRsi[r][z + kk + 2])
        workRsi[r][z + kk + 7] = (Kg * moa) + (Hg * workRsi[r - 1][z + kk + 7])
        workRsi[r][z + kk + 8] = (Kg * workRsi[r][z + kk + 7]) + (Hg * workRsi[r - 1][z + kk + 8])
        moa = (1.5 * workRsi[r][z + kk + 7]) - (0.5 * workRsi[r][z + kk + 8])
    return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)

def iEma(price, period, r, bars, instanceNo=0):
    if ArrayRange(workEma, 0) != bars:
        ArrayResize(workEma, bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


class RsxQQENewZl(_MQL5Indicator):
    name = 'Rsx QQE - new zl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSX period
        'inpRsiSmoothingFactor': 5,  # RSX smoothing factor
        'inpWPSlow': 4.236,  # QQE quantifier
        'inpUpBound': 10.0,  # Upper bound
        'inpDnBound': -10.0,  # Lower bound
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

