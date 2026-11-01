"""BB stops - MACD — converted from MQL5: MQL5 Indicators/BB Stops - MACD/BB stops - MACD.mq5

BB stops - MACD
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 12}, 'colors': {1: [12632256], 2: [8421504], 3: [8421504], 4: [16748574], 5: [6333684], 6: [12632256, 16748574, 6333684]}, 'widths': {4: 3, 5: 3, 6: 2}, 'styles': {2: 2, 3: 2}, 'labels': {}, 'levels': [], 'description': ['BB stops - MACD'], 'name': 'BB stops - MACD', 'source': 'MQL5 Indicators/BB Stops - MACD/BB stops - MACD.mq5', 'folder': 'BB Stops - MACD', 'inputs': [{'mql': 'MacdFastPeriod', 'py': 'MacdFastPeriod', 'param': 'MacdFastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast MACD period', 'sinput': False}, {'mql': 'MacdSlowPeriod', 'py': 'MacdSlowPeriod', 'param': 'MacdSlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow MACD period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'MACD Price', 'sinput': False}, {'mql': 'BbPeriod', 'py': 'BbPeriod', 'param': 'BbPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger stops period', 'sinput': False}, {'mql': 'DeviationPeriod', 'py': 'DeviationPeriod', 'param': 'DeviationPeriod', 'type': 'int', 'default': 20, 'label': 'Deviations period', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 1.0, 'label': 'Risk (%)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MacdFastPeriod = _input('MacdFastPeriod', 12)  # Fast MACD period
MacdSlowPeriod = _input('MacdSlowPeriod', 26)  # Slow MACD period
Price = _input('Price', PRICE_CLOSE)  # MACD Price
BbPeriod = _input('BbPeriod', 20)  # Bollinger stops period
DeviationPeriod = _input('DeviationPeriod', 20)  # Deviations period
Deviation = _input('Deviation', 1.0)  # Deviation
Risk = _input('Risk', 1.0)  # Risk (%)
macd = Arr(0, 0.0)
bba = Arr(0, 0.0)
bbc = Arr(0, 0.0)
bblu = Arr(0, 0.0)
bbld = Arr(0, 0.0)
bmax = Arr(0, 0.0)
bmin = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(2,))
bbWork = Arr(0, 0.0, dims=(6,))

class _bbReturnStruct(MqlObject):
    _q_fields = ('upValue', 'downValue', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upValue = 0.0
        self.downValue = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    SetIndexBuffer(0, macd, INDICATOR_DATA)
    SetIndexBuffer(1, bmax, INDICATOR_DATA)
    SetIndexBuffer(2, bmin, INDICATOR_DATA)
    SetIndexBuffer(3, bblu, INDICATOR_DATA)
    SetIndexBuffer(4, bbld, INDICATOR_DATA)
    SetIndexBuffer(5, bba, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    SetIndexBuffer(6, bbc, INDICATOR_COLOR_INDEX)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(Price, open, close, high, low, i, rates_total)
        macd[i] = iEma(_price, MacdFastPeriod, i, rates_total, 0) - iEma(_price, MacdSlowPeriod, i, rates_total, 1)
        _result = iBbStops(macd[i], BbPeriod, Risk, DeviationPeriod, Deviation, i, rates_total)
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

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


class BBStopsMACD(_MQL5Indicator):
    name = 'BB stops - MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MacdFastPeriod': 12,  # Fast MACD period
        'MacdSlowPeriod': 26,  # Slow MACD period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD Price
        'BbPeriod': 20,  # Bollinger stops period
        'DeviationPeriod': 20,  # Deviations period
        'Deviation': 1.0,  # Deviation
        'Risk': 1.0,  # Risk (%)
    }

