"""Corrected RSI — converted from MQL5: MQL5 Indicators/Corrected RSI/Corrected RSI.mq5

Corrected RSI
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017, 16760576, 8036607]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'RSI', 2: 'Corrected RSI'}, 'levels': [], 'description': ['Corrected RSI'], 'name': 'Corrected RSI', 'source': 'MQL5 Indicators/Corrected RSI/Corrected RSI.mq5', 'folder': 'Corrected RSI', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
rsi = Arr(0, 0.0)
rsic = Arr(0, 0.0)
workCorrMa = Arr(0, 0.0, dims=(3,))
workRsi = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, rsi, INDICATOR_DATA)
    SetIndexBuffer(1, rsic, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Corrected RSI (' + _str(inpRsiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _rsiVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        rsi[i] = iRsi(getPrice(inpPrice, open, close, high, low, i, rates_total), inpRsiPeriod, i, rates_total)
        val[i] = iCorrMa(rsi[i], rsi[i], inpRsiPeriod, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        rsic[i] = valc[i]
        i += 1
    return i

def iCorrMa(_avg, price, period, i, _bars, instanceNo=0):
    if ArrayRange(workCorrMa, 0) != _bars:
        ArrayResize(workCorrMa, _bars)
    instanceNo *= 3
    workCorrMa[i][0] = price
    workCorrMa[i][1] = _avg
    oldMean = price
    newMean = price
    squares = 0.0
    k = 1
    while k < period and (i - k) >= 0:
        newMean = _fdiv(workCorrMa[i - k][0] - oldMean, k + 1) + oldMean
        squares += (workCorrMa[i - k][0] - oldMean) * (workCorrMa[i - k][0] - newMean)
        oldMean = newMean
        k += 1
    _deviation = MathSqrt(_fdiv(squares, k))
    v1 = MathPow(_deviation, 2)
    v2 = (MathPow(workCorrMa[i - 1][2] - workCorrMa[i][1], 2) if (i > 0) else 0)
    c = (0 if (v2 < v1 or v2 == 0) else (1 - _fdiv(v1, v2)))
    workCorrMa[i][2] = ((workCorrMa[i - 1][2] + (c * (workCorrMa[i][1] - workCorrMa[i - 1][2]))) if (i > 0) else workCorrMa[i][1])
    return workCorrMa[i][2]

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
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
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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


class CorrectedRSI(_MQL5Indicator):
    name = 'Corrected RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

