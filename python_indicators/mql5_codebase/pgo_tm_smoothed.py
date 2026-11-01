"""PGO TM smoothed — converted from MQL5: MQL5 Indicators/PGO TM smoothed/PGO TM smoothed.mq5

Smooth PGO
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Smooth PGO'}, 'levels': [], 'description': ['Smooth PGO'], 'name': 'PGO TM smoothed', 'source': 'MQL5 Indicators/PGO TM smoothed/PGO TM smoothed.mq5', 'folder': 'PGO TM smoothed', 'inputs': [{'mql': 'inpPgoPeriod', 'py': 'inpPgoPeriod', 'param': 'inpPgoPeriod', 'type': 'int', 'default': 89, 'label': 'PGO period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpTmSmoothing', 'py': 'inpTmSmoothing', 'param': 'inpTmSmoothing', 'type': 'double', 'default': 5.0, 'label': 'TM smoothing', 'sinput': False}, {'mql': 'inpTmDamping', 'py': 'inpTmDamping', 'param': 'inpTmDamping', 'type': 'double', 'default': 5.0, 'label': 'TM damping', 'sinput': False}, {'mql': 'inpTmNoise', 'py': 'inpTmNoise', 'param': 'inpTmNoise', 'type': 'double', 'default': 2.0, 'label': 'TM noise', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPgoPeriod = _input('inpPgoPeriod', 89)  # PGO period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpTmSmoothing = _input('inpTmSmoothing', 5.0)  # TM smoothing
inpTmDamping = _input('inpTmDamping', 5.0)  # TM damping
inpTmNoise = _input('inpTmNoise', 2.0)  # TM noise
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
work = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
wrkTm = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TM Smoothed PGO (' + _str(inpPgoPeriod) + ',' + _str(inpTmSmoothing) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArraySize(work) != rates_total:
        ArrayResize(work, rates_total)
    alphaAtr = _fdiv(2.0, 1.0 + inpPgoPeriod)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        work[i] = ((work[i - 1] + (alphaAtr * (MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1]) - work[i - 1]))) if (i > 0) else (high[i] - low[i]))
        val[i] = iTmSmooth(_fdiv(_price - iSma(_price, inpPgoPeriod, i, rates_total), work[i]), inpTmDamping, inpTmNoise, inpTmSmoothing, i, rates_total)
        valc[i] = ((val[i] < val[i - 1]) if (i > 0) else 0)
    return rates_total

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iTmSmooth(price, damping, noise, length, i, bars):
    if ArrayRange(wrkTm, 0) != bars:
        ArrayResize(wrkTm, bars)
    if length <= 1:
        return price
    wrkTm[i][0] = price
    y1 = (wrkTm[i - 1][1] if (i > 0) else 0)
    y2 = (wrkTm[i - 1][2] if (i > 0) else 0)
    err = _fdiv(wrkTm[i][0] - (2.0 * y1) + y2, noise)
    drv = MathMax(MathMin((_fdiv(1.0, length) * err * err) + (_fdiv(1.0, length) * MathAbs(err)), 0.5), 0.0)
    dmp = MathMax(MathMin(_fdiv(_fdiv(1.0, length) * MathAbs(y1 - y2), noise) + (damping / 100.0), 1.0), 0.0)
    tmAvg = y1 + (noise * err * drv) + ((y1 - y2) * (1.0 - dmp))
    wrkTm[i][1] = tmAvg
    wrkTm[i][2] = y1
    return tmAvg

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


class PGOTMSmoothed(_MQL5Indicator):
    name = 'PGO TM smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPgoPeriod': 89,  # PGO period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpTmSmoothing': 5.0,  # TM smoothing
        'inpTmDamping': 5.0,  # TM damping
        'inpTmNoise': 2.0,  # TM noise
    }

