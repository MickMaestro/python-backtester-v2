"""Macd FRAMA — converted from MQL5: MQL5 Indicators/Fractal Adaptive MACD/Macd FRAMA.mq5

Macd FRAMA
Copyright: © mladen, 2018; Link: https://www.mql5.com/en/users/mladen/publications; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'https://www.mql5.com/en/users/mladen/publications', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [14870490, 14278143], 2: [11119017, 16748574, 3937500], 3: [255]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'Macd frama filling', 2: 'Macd frama value', 3: 'Macd signal'}, 'levels': [], 'description': ['Macd FRAMA'], 'name': 'Macd FRAMA', 'source': 'MQL5 Indicators/Fractal Adaptive MACD/Macd FRAMA.mq5', 'folder': 'Fractal Adaptive MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast FRAMA period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow FRAMA period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 25, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 25, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast FRAMA period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow FRAMA period
inpSignalPeriod = _input('inpSignalPeriod', 25)  # Signal period
inpSmoothPeriod = _input('inpSmoothPeriod', 25)  # Smoothing period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
workSsm = Arr(0, 0.0, dims=(4,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))
workFrama = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Macd FRAMA (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iSsm(iFrama(_price, inpFastPeriod, i, rates_total, 0), inpSmoothPeriod, i, rates_total, 0) - iSsm(iFrama(_price, inpSlowPeriod, i, rates_total, 1), inpSmoothPeriod, i, rates_total, 1)
        signal[i] = iFrama(val[i], inpSignalPeriod, i, rates_total, 2)
        fillu[i] = val[i]
        filld[i] = signal[i]
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

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

def iFrama(price, fperiod, r, bars, instanceNo=0):
    if ArrayRange(workFrama, 0) != bars:
        ArrayResize(workFrama, bars)
    instanceNo *= 2
    workFrama[r][instanceNo + 0] = price
    if r < 1 or fperiod <= 1:
        workFrama[r][instanceNo + 1] = price
    else:
        halfPeriod = MathMax(_idiv(fperiod, 2), 1)
        k = 0
        hh = workFrama[r][instanceNo + 0]
        ll = workFrama[r][instanceNo + 0]
        k = 1
        while k < fperiod and (r - k) >= 0:
            hh = MathMax(workFrama[r - k][instanceNo + 0], hh)
            ll = MathMin(workFrama[r - k][instanceNo + 0], ll)
            k += 1
        n3 = _fdiv(hh - ll, float(fperiod))
        ll = workFrama[r][instanceNo + 0]
        hh = ll
        k = 1
        while k < halfPeriod and (r - k) >= 0:
            hh = MathMax(workFrama[r - k][instanceNo + 0], hh)
            ll = MathMin(workFrama[r - k][instanceNo + 0], ll)
            k += 1
        n1 = _fdiv(hh - ll, float(halfPeriod))
        ll = workFrama[MathMax(r - halfPeriod, 0)][instanceNo + 0]
        hh = ll
        k = halfPeriod + 1
        while k < fperiod and (r - k) >= 0:
            hh = MathMax(workFrama[r - k][instanceNo + 0], hh)
            ll = MathMin(workFrama[r - k][instanceNo + 0], ll)
            k += 1
        n2 = _fdiv(hh - ll, float(halfPeriod))
        dimen = 0.0
        if (n1 + n2) > 0 and n3 > 0:
            dimen = _fdiv(MathLog(n1 + n2) - MathLog(n3), MathLog(2.0))
        alpha = MathMin(MathMax(MathExp(-4.6 * (dimen - 1.0)), 0.001), 1.0)
        workFrama[r][instanceNo + 1] = (alpha * price) + ((1 - alpha) * workFrama[r - 1][instanceNo + 1])
    return workFrama[r][instanceNo + 1]

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


class MacdFRAMA(_MQL5Indicator):
    name = 'Macd FRAMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 19,  # Fast FRAMA period
        'inpSlowPeriod': 39,  # Slow FRAMA period
        'inpSignalPeriod': 25,  # Signal period
        'inpSmoothPeriod': 25,  # Smoothing period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

