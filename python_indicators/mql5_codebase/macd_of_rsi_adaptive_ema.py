"""MACD of RSI adaptive EMA — converted from MQL5: MQL5 Indicators/MACD of RSI adaptive EMA/MACD of RSI adaptive EMA.mq5

MACD of RSI adaptive EMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [255]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'MACD', 2: 'MACD signal line'}, 'levels': [], 'description': ['MACD of RSI adaptive EMA'], 'name': 'MACD of RSI adaptive EMA', 'source': 'MQL5 Indicators/MACD of RSI adaptive EMA/MACD of RSI adaptive EMA.mq5', 'folder': 'MACD of RSI adaptive EMA', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'MACD signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
color_onSlope = 0
color_onZero = 1
color_onSignal = 2
_enum('enColorOn', {0: 'color_onSlope', 1: 'color_onZero', 2: 'color_onSignal'})

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # MACD signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', color_onZero)  # Color change on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
emaf = Arr(0, 0.0)
emas = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, emaf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, emas, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD of RSI adaptive EMA (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _alphaSignal = _fdiv(2.0, 1.0 + inpSignalPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _alphaf = MathAbs((iRsi(_price, inpFastPeriod, i, rates_total, 0) / 100.0) - 0.5) * 2.0
        _alphas = MathAbs((iRsi(_price, inpSlowPeriod, i, rates_total, 1) / 100.0) - 0.5) * 2.0
        emaf[i] = ((emaf[i - 1] + (_alphaf * (_price - emaf[i - 1]))) if (i > 0) else _price)
        emas[i] = ((emas[i - 1] + (_alphas * (_price - emas[i - 1]))) if (i > 0) else _price)
        val[i] = emaf[i] - emas[i]
        signal[i] = ((signal[i - 1] + (_alphaSignal * (val[i] - signal[i - 1]))) if (i > 0) else val[i])
        _sw1 = inpColorOn
        if _sw1 == color_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == color_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else valc[i - 1] if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
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


class MACDOfRSIAdaptiveEMA(_MQL5Indicator):
    name = 'MACD of RSI adaptive EMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpSignalPeriod': 9,  # MACD signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on MACD slope change', 1: 'Change color on MACD crossing zero line', 2: 'Change color on MACD crossing signal line'}, default=1),  # Color change on :
    }

