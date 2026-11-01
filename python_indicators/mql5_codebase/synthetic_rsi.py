"""Synthetic RSI — converted from MQL5: MQL5 Indicators/Synthetic RSI/Synthetic RSI.mq5

Synthetic RSI
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Synthetic RSI', 2: 'Signal'}, 'levels': [80.0, 20.0], 'description': ['Synthetic RSI'], 'name': 'Synthetic RSI', 'source': 'MQL5 Indicators/Synthetic RSI/Synthetic RSI.mq5', 'folder': 'Synthetic RSI', 'inputs': [{'mql': 'inpEmaPeriod1', 'py': 'inpEmaPeriod1', 'param': 'inpEmaPeriod1', 'type': 'int', 'default': 48, 'label': 'Ema 1 period', 'sinput': False}, {'mql': 'inpRsiPeriod1', 'py': 'inpRsiPeriod1', 'param': 'inpRsiPeriod1', 'type': 'int', 'default': 32, 'label': 'Rsi 1 period', 'sinput': False}, {'mql': 'inpEmaPeriod2', 'py': 'inpEmaPeriod2', 'param': 'inpEmaPeriod2', 'type': 'int', 'default': 24, 'label': 'Ema 2 period', 'sinput': False}, {'mql': 'inpRsiPeriod2', 'py': 'inpRsiPeriod2', 'param': 'inpRsiPeriod2', 'type': 'int', 'default': 16, 'label': 'Rsi 2 period', 'sinput': False}, {'mql': 'inpEmaPeriod3', 'py': 'inpEmaPeriod3', 'param': 'inpEmaPeriod3', 'type': 'int', 'default': 12, 'label': 'Ema 3 period', 'sinput': False}, {'mql': 'inpRsiPeriod3', 'py': 'inpRsiPeriod3', 'param': 'inpRsiPeriod3', 'type': 'int', 'default': 8, 'label': 'Rsi 3 period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpEmaPeriod1 = _input('inpEmaPeriod1', 48)  # Ema 1 period
inpRsiPeriod1 = _input('inpRsiPeriod1', 32)  # Rsi 1 period
inpEmaPeriod2 = _input('inpEmaPeriod2', 24)  # Ema 2 period
inpRsiPeriod2 = _input('inpRsiPeriod2', 16)  # Rsi 2 period
inpEmaPeriod3 = _input('inpEmaPeriod3', 12)  # Ema 3 period
inpRsiPeriod3 = _input('inpRsiPeriod3', 8)  # Rsi 3 period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSignalPeriod = _input('inpSignalPeriod', 8)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
signalc = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(9,))
workEma = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, signalc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Synthetic RSI (' + _str(inpRsiPeriod1) + ',' + _str(inpEmaPeriod1) + ',' + _str(inpRsiPeriod2) + ',' + _str(inpEmaPeriod2) + ',' + _str(inpRsiPeriod3) + ',' + _str(inpEmaPeriod3) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        rsi1 = iRsi(iEma(price, inpEmaPeriod1, i, rates_total, 0), inpRsiPeriod1, i, rates_total, 0)
        rsi2 = iRsi(iEma(price, inpEmaPeriod2, i, rates_total, 1), inpRsiPeriod2, i, rates_total, 1)
        rsi3 = iRsi(iEma(price, inpEmaPeriod3, i, rates_total, 2), inpRsiPeriod3, i, rates_total, 2)
        val[i] = (rsi3 + (2.0 * rsi2) + (3.0 * rsi1)) / 6.0
        signal[i] = iEma(val[i], inpSignalPeriod, i, rates_total, 3)
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        signalc[i] = valc[i]
        i += 1
    return i

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

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
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


class SyntheticRSI(_MQL5Indicator):
    name = 'Synthetic RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpEmaPeriod1': 48,  # Ema 1 period
        'inpRsiPeriod1': 32,  # Rsi 1 period
        'inpEmaPeriod2': 24,  # Ema 2 period
        'inpRsiPeriod2': 16,  # Rsi 2 period
        'inpEmaPeriod3': 12,  # Ema 3 period
        'inpRsiPeriod3': 8,  # Rsi 3 period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSignalPeriod': 8,
    }

