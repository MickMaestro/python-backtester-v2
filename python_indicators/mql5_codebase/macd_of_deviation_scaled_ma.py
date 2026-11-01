"""MACD of deviation scaled MA — converted from MQL5: MQL5 Indicators/Deviation scaled MA MACD/MACD of deviation scaled MA.mq5

Deviation scaled macd
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [255]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'MACD', 2: 'MACD signal'}, 'levels': [], 'description': ['Deviation scaled macd'], 'name': 'MACD of deviation scaled MA', 'source': 'MQL5 Indicators/Deviation scaled MA MACD/MACD of deviation scaled MA.mq5', 'folder': 'Deviation scaled MA MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 40, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 100, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'MACD signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 0, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
color_onZero = 0
color_onSlope = 1
color_onSignal = 2
_enum('enColorOn', {0: 'color_onZero', 1: 'color_onSlope', 2: 'color_onSignal'})

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 40)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 100)  # MACD slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # MACD signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', color_onZero)  # Color change on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
workDsma = Arr(0, 0.0, dims=(9,))
workDsmaCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD of deviation scaled MA (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        filter_ = ((close[i] - close[i - 2]) if (i > 1) else 0)
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iDsma(price, filter_, inpFastPeriod, i, rates_total, 0) - iDsma(price, filter_, inpSlowPeriod, i, rates_total, 1)
        filter_ = ((val[i] - val[i - 2]) if (i > 1) else 0)
        signal[i] = iDsma(val[i], filter_, inpSignalPeriod, i, rates_total, 2)
        _sw1 = inpColorOn
        if _sw1 == color_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == color_onSignal:
            valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

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
        _sw2 = tprice
        if _sw2 == PRICE_CLOSE:
            return close[i]
        elif _sw2 == PRICE_OPEN:
            return open[i]
        elif _sw2 == PRICE_HIGH:
            return high[i]
        elif _sw2 == PRICE_LOW:
            return low[i]
        elif _sw2 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDOfDeviationScaledMA(_MQL5Indicator):
    name = 'MACD of deviation scaled MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 40,  # MACD fast period
        'inpSlowPeriod': 100,  # MACD slow period
        'inpSignalPeriod': 9,  # MACD signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on MACD zero line cross', 1: 'Change color on MACD slope change', 2: 'Change color on MACD crossing signal line'}, default=0),  # Color change on :
    }

