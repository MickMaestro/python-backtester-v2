"""KAMA macd — converted from MQL5: MQL5 Indicators/Kaufman AMA MACD/KAMA macd.mq5

KAMA macd
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [14870490, 14278143], 2: [11119017, 3329330, 6333684], 3: [255]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'KAMA macd filling', 2: 'Macd value', 3: 'Macd signal'}, 'levels': [], 'description': ['KAMA macd'], 'name': 'KAMA macd', 'source': 'MQL5 Indicators/Kaufman AMA MACD/KAMA macd.mq5', 'folder': 'Kaufman AMA MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast DEMA period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow DEMA period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpFastEndPeriod', 'py': 'inpFastEndPeriod', 'param': 'inpFastEndPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowEndPeriod', 'py': 'inpSlowEndPeriod', 'param': 'inpSlowEndPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpPower', 'py': 'inpPower', 'param': 'inpPower', 'type': 'double', 'default': 2.0, 'label': 'Smooth power', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast DEMA period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow DEMA period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpFastEndPeriod = _input('inpFastEndPeriod', 2)  # Fast end period
inpSlowEndPeriod = _input('inpSlowEndPeriod', 30)  # Slow end period
inpPower = _input('inpPower', 2.0)  # Smooth power
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
workAma = Arr(0, 0.0, dims=(9,))

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KAMA macd (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iKama(_price, inpFastPeriod, inpFastEndPeriod, inpSlowEndPeriod, inpPower, i, open, close, high, low, rates_total, 0) - iKama(_price, inpSlowPeriod, inpFastEndPeriod, inpSlowEndPeriod, inpPower, i, open, close, high, low, rates_total, 1)
        signal[i] = iKama(val[i], inpSignalPeriod, inpFastEndPeriod, inpSlowEndPeriod, inpPower, i, open, close, high, low, rates_total, 2)
        fillu[i] = val[i]
        filld[i] = signal[i]
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def iKama(price, period, fast, slow, power, i, open, close, high, low, bars, instanceNo=0):
    if ArrayRange(workAma, 0) != bars:
        ArrayResize(workAma, bars)
    r = i
    instanceNo *= 3
    fastend = _fdiv(2.0, fast + 1)
    slowend = _fdiv(2.0, slow + 1)
    efratio = 1.0
    workAma[r][instanceNo + 2] = price
    tsignal = (MathAbs(price - workAma[r - period][instanceNo + 2]) if (r >= period) else 0)
    noise = 0.0
    workAma[r][instanceNo + 0] = (MathAbs(price - workAma[r - 1][instanceNo + 2]) if (r > 0) else 0)
    k = 0
    while k < period and (r - k) >= 0:
        noise += workAma[r - k][instanceNo + 0]
        k += 1
    if noise != 0:
        efratio = _fdiv(tsignal, noise)
    else:
        efratio = 1.0
    smooth = MathPow((efratio * (fastend - slowend)) + slowend, power)
    workAma[r][instanceNo + 1] = ((workAma[r - 1][instanceNo + 1] + (smooth * (price - workAma[r - 1][instanceNo + 1]))) if (r > 0) else price)
    return workAma[r][instanceNo + 1]

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


class KAMAMacd(_MQL5Indicator):
    name = 'KAMA macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 19,  # Fast DEMA period
        'inpSlowPeriod': 39,  # Slow DEMA period
        'inpSignalPeriod': 9,  # Signal period
        'inpFastEndPeriod': 2,  # Fast end period
        'inpSlowEndPeriod': 30,  # Slow end period
        'inpPower': 2.0,  # Smooth power
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

