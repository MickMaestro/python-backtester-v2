"""QQE histo — converted from MQL5: MQL5 Indicators/QQE Histo/QQE histo.mq5

QQE
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 11, 2: 1, 3: 1, 4: 8}, 'colors': {1: [14474460, 16760576, 8036607], 2: [11119017], 3: [11119017], 4: [11119017, 16760576, 8036607]}, 'widths': {1: 2, 4: 2}, 'styles': {2: 2}, 'labels': {1: 'QQE histogram', 2: 'QQE fast', 3: 'QQE slow', 4: 'QQE'}, 'levels': [], 'description': ['QQE'], 'name': 'QQE histo', 'source': 'MQL5 Indicators/QQE Histo/QQE histo.mq5', 'folder': 'QQE Histo', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpRsiSmoothingFactor', 'py': 'inpRsiSmoothingFactor', 'param': 'inpRsiSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'RSI smoothing factor', 'sinput': False}, {'mql': 'inpWPFast', 'py': 'inpWPFast', 'param': 'inpWPFast', 'type': 'double', 'default': 2.618, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpUpBound', 'py': 'inpUpBound', 'param': 'inpUpBound', 'type': 'double', 'default': 60.0, 'label': 'Upper bound', 'sinput': False}, {'mql': 'inpDnBound', 'py': 'inpDnBound', 'param': 'inpDnBound', 'type': 'double', 'default': 40.0, 'label': 'Lower bound', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpRsiSmoothingFactor = _input('inpRsiSmoothingFactor', 5)  # RSI smoothing factor
inpWPFast = _input('inpWPFast', 2.618)  # Fast period
inpWPSlow = _input('inpWPSlow', 4.236)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpUpBound = _input('inpUpBound', 60.0)  # Upper bound
inpDnBound = _input('inpDnBound', 40.0)  # Lower bound
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levs = Arr(0, 0.0)
levf = Arr(0, 0.0)
histoh = Arr(0, 0.0)
histol = Arr(0, 0.0)
histoc = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, histoh, INDICATOR_DATA)
    SetIndexBuffer(1, histol, INDICATOR_DATA)
    SetIndexBuffer(2, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, levf, INDICATOR_DATA)
    SetIndexBuffer(4, levs, INDICATOR_DATA)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpUpBound)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpDnBound)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE histo (' + _str(inpRsiPeriod) + ',' + _str(inpRsiSmoothingFactor) + ')')
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
        _iEmf = _iEmm * inpWPFast
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
        tr = (levf[i - 1] if (i > 0) else 0)
        dv = tr
        if val[i] < tr:
            tr = val[i] + _iEmf
            if (i > 0 and val[i - 1] < dv) and tr > dv:
                tr = dv
        if val[i] > tr:
            tr = val[i] - _iEmf
            if (i > 0 and val[i - 1] > dv) and tr < dv:
                tr = dv
        levf[i] = tr
        histoh[i] = val[i]
        histol[i] = 50.0
        valc[i] = (1 if (val[i] > levf[i] and val[i] > levs[i]) else 2 if (val[i] < levf[i] and val[i] < levs[i]) else valc[i - 1] if (i > 0) else 0)
        histoc[i] = (1 if (val[i] > inpUpBound) else 2 if (val[i] < inpDnBound) else 0)
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        alpha = _fdiv(1.0, MathMax(period, 1))
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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


class QQEHisto(_MQL5Indicator):
    name = 'QQE histo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpRsiSmoothingFactor': 5,  # RSI smoothing factor
        'inpWPFast': 2.618,  # Fast period
        'inpWPSlow': 4.236,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpUpBound': 60.0,  # Upper bound
        'inpDnBound': 40.0,  # Lower bound
    }

