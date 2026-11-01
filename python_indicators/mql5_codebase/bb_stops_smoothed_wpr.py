"""BB stops - smoothed WPR — converted from MQL5: MQL5 Indicators/BB Stops - Smoothed WPR/BB stops - smoothed WPR.mq5

BB stops - WPR
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 12}, 'colors': {1: [12632256], 2: [8421504], 3: [8421504], 4: [16748574], 5: [6333684], 6: [12632256, 16748574, 6333684]}, 'widths': {4: 3, 5: 3, 6: 2}, 'styles': {2: 2, 3: 2}, 'labels': {}, 'levels': [], 'description': ['BB stops - WPR'], 'name': 'BB stops - smoothed WPR', 'source': 'MQL5 Indicators/BB Stops - Smoothed WPR/BB stops - smoothed WPR.mq5', 'folder': 'BB Stops - Smoothed WPR', 'inputs': [{'mql': 'WprPeriod', 'py': 'WprPeriod', 'param': 'WprPeriod', 'type': 'int', 'default': 14, 'label': 'WPR period', 'sinput': False}, {'mql': 'Smoothing', 'py': 'Smoothing', 'param': 'Smoothing', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'SmoothingMethod', 'py': 'SmoothingMethod', 'param': 'SmoothingMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'BbPeriod', 'py': 'BbPeriod', 'param': 'BbPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger stops period', 'sinput': False}, {'mql': 'DeviationPeriod', 'py': 'DeviationPeriod', 'param': 'DeviationPeriod', 'type': 'int', 'default': 20, 'label': 'Deviations period', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 1.0, 'label': 'Risk (%)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
WprPeriod = _input('WprPeriod', 14)  # WPR period
Smoothing = _input('Smoothing', 5)  # Smoothing period
SmoothingMethod = _input('SmoothingMethod', ma_sma)  # Smoothing method
BbPeriod = _input('BbPeriod', 20)  # Bollinger stops period
DeviationPeriod = _input('DeviationPeriod', 20)  # Deviations period
Deviation = _input('Deviation', 1.0)  # Deviation
Risk = _input('Risk', 1.0)  # Risk (%)
wpr = Arr(0, 0.0)
bba = Arr(0, 0.0)
bbc = Arr(0, 0.0)
bblu = Arr(0, 0.0)
bbld = Arr(0, 0.0)
bmax = Arr(0, 0.0)
bmin = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
bbWork = Arr(0, 0.0, dims=(6,))

class _bbReturnStruct(MqlObject):
    _q_fields = ('upValue', 'downValue', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upValue = 0.0
        self.downValue = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    SetIndexBuffer(0, wpr, INDICATOR_DATA)
    SetIndexBuffer(1, bmax, INDICATOR_DATA)
    SetIndexBuffer(2, bmin, INDICATOR_DATA)
    SetIndexBuffer(3, bblu, INDICATOR_DATA)
    SetIndexBuffer(4, bbld, INDICATOR_DATA)
    SetIndexBuffer(5, bba, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    SetIndexBuffer(6, bbc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB stops - WPR (' + _str(WprPeriod) + ',' + _str(Smoothing) + ',' + _str(BbPeriod) + ',' + _str(DeviationPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - WprPeriod + 1, 0)
        _max = high[ArrayMaximum(high, _start, WprPeriod)]
        _min = low[ArrayMinimum(low, _start, WprPeriod)]
        wpr[i] = iCustomMa(SmoothingMethod, (_fdiv((-(_max - close[i])) * 100, _max - _min) if (_max != _min) else 0), Smoothing, i, rates_total)
        _result = iBbStops(wpr[i], BbPeriod, Risk, DeviationPeriod, Deviation, i, rates_total)
        bmax[i] = _result.upValue
        bmin[i] = _result.downValue
        bblu[i] = EMPTY_VALUE
        bbld[i] = EMPTY_VALUE
        if _result.trend == 1:
            bblu[i] = _result.upValue
            bbc[i] = 1.0
        if _result.trend == -1:
            bbld[i] = _result.downValue
            bbc[i] = 2.0
        bba[i] = ((bblu[i] if (_result.trend == 1) else bbld[i]) if _result.trendChange else EMPTY_VALUE)
        i += 1
    return i

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    k = 0
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, k)

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period <= 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iBbStops(price, period, risk, deviationPeriod, deviation, i, bars, instanceNo=0):
    if ArrayRange(bbWork, 0) != bars:
        ArrayResize(bbWork, bars)
    instanceNo *= 6
    bbWork[i][instanceNo + 0] = price
    oldMean = price
    newMean = price
    squares = 0.0
    k = 1
    while k < deviationPeriod and (i - k) >= 0:
        newMean = _fdiv(bbWork[i - k][instanceNo + 0] - oldMean, k + 1) + oldMean
        squares += (bbWork[i - k][instanceNo + 0] - oldMean) * (bbWork[i - k][instanceNo + 0] - newMean)
        oldMean = newMean
        k += 1
    dev = MathSqrt(_fdiv(squares, deviationPeriod))
    ma = price
    k = 1
    while k < period and (i - k) >= 0:
        ma += bbWork[i - k][instanceNo + 0]
        k += 1
    ma = _fdiv(ma, period)
    bbWork[i][instanceNo + 1] = ma + (dev * deviation)
    bbWork[i][instanceNo + 2] = ma - (dev * deviation)
    bbWork[i][instanceNo + 3] = bbWork[i][instanceNo + 1] + (0.5 * (risk - 1) * (bbWork[i][instanceNo + 1] - bbWork[i][instanceNo + 2]))
    bbWork[i][instanceNo + 4] = bbWork[i][instanceNo + 2] - (0.5 * (risk - 1) * (bbWork[i][instanceNo + 1] - bbWork[i][instanceNo + 2]))
    bbWork[i][instanceNo + 5] = ((1 if (price > bbWork[i - 1][instanceNo + 1]) else -1 if (price < bbWork[i - 1][instanceNo + 2]) else bbWork[i - 1][instanceNo + 5]) if (i > 0) else 0)
    if i > 0:
        if bbWork[i][instanceNo + 5] == -1 and bbWork[i][instanceNo + 1] > bbWork[i - 1][instanceNo + 1]:
            bbWork[i][instanceNo + 1] = bbWork[i - 1][instanceNo + 1]
        if bbWork[i][instanceNo + 5] == 1 and bbWork[i][instanceNo + 2] < bbWork[i - 1][instanceNo + 2]:
            bbWork[i][instanceNo + 2] = bbWork[i - 1][instanceNo + 2]
        if bbWork[i][instanceNo + 5] == -1 and bbWork[i][instanceNo + 3] > bbWork[i - 1][instanceNo + 3]:
            bbWork[i][instanceNo + 3] = bbWork[i - 1][instanceNo + 3]
        if bbWork[i][instanceNo + 5] == 1 and bbWork[i][instanceNo + 4] < bbWork[i - 1][instanceNo + 4]:
            bbWork[i][instanceNo + 4] = bbWork[i - 1][instanceNo + 4]
    _result = _bbReturnStruct()
    _result.upValue = bbWork[i][instanceNo + 4]
    _result.downValue = bbWork[i][instanceNo + 3]
    _result.trend = _int(bbWork[i][instanceNo + 5])
    _result.trendChange = ((bbWork[i][instanceNo + 5] != bbWork[i - 1][instanceNo + 5]) if (i > 0) else False)
    return _copy(_result)

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


class BBStopsSmoothedWPR(_MQL5Indicator):
    name = 'BB stops - smoothed WPR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WprPeriod': 14,  # WPR period
        'Smoothing': 5,  # Smoothing period
        'SmoothingMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
        'BbPeriod': 20,  # Bollinger stops period
        'DeviationPeriod': 20,  # Deviations period
        'Deviation': 1.0,  # Deviation
        'Risk': 1.0,  # Risk (%)
    }

