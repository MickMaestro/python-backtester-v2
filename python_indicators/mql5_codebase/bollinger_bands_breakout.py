"""Bollinger bands breakout — converted from MQL5: MQL5 Indicators/Bollinger bands breakout/Bollinger bands breakout.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 5, 7: 5}, 'colors': {1: [13628367], 2: [13492732], 3: [7451452], 4: [6333684], 5: [11119017], 6: [32768], 7: [36095]}, 'widths': {}, 'styles': {5: 2}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Average', 6: 'Break up', 7: 'Break down'}, 'levels': [], 'description': [], 'name': 'Bollinger bands breakout', 'source': 'MQL5 Indicators/Bollinger bands breakout/Bollinger bands breakout.mq5', 'folder': 'Bollinger bands breakout', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDeviations', 'py': 'inpDeviations', 'param': 'inpDeviations', 'type': 'double', 'default': 2.5, 'label': 'Bollinger bands deviations', 'sinput': False}, {'mql': 'inpZonesPercent', 'py': 'inpZonesPercent', 'param': 'inpZonesPercent', 'type': 'double', 'default': 20.0, 'label': 'Zones percent', 'sinput': False}, {'mql': 'inpDevType', 'py': 'inpDevType', 'param': 'inpDevType', 'type': 'int', 'default': 1, 'label': 'Standard deviations type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDevType
dev_sample = 0
dev_regular = 1
_enum('enDevType', {0: 'dev_sample', 1: 'dev_regular'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Bollinger bands period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDeviations = _input('inpDeviations', 2.5)  # Bollinger bands deviations
inpZonesPercent = _input('inpZonesPercent', 20.0)  # Zones percent
inpDevType = _input('inpDevType', dev_regular)  # Standard deviations type
bufferUp = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
breakup = Arr(0, 0.0)
breakdn = Arr(0, 0.0)
_bandsFillZone = 0.0
_maHandle = 0

class cStdDeviation(MqlObject):
    _q_fields = ('m_period', 'm_periodDiv', 'm_arraySize', 'm_isSample', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_periodDiv = 0.0
        self.m_arraySize = 0
        self.m_isSample = False
        self.m_array = Arr(0, 0, factory=sStdStruct)
        self.m_arraySize = -1
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, isSample):
        self.m_period = (period if (period > 1) else 1)
        self.m_isSample = isSample
        self.m_periodDiv = MathMax(self.m_period - self.m_isSample, 1)
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].price = price
        self.m_array[i].price2 = price * price
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum + self.m_array[i].price - self.m_array[i - self.m_period].price
            self.m_array[i].sum2 = self.m_array[i - 1].sum2 + self.m_array[i].price2 - self.m_array[i - self.m_period].price2
        else:
            self.m_array[i].sum = self.m_array[i].price
            self.m_array[i].sum2 = self.m_array[i].price2
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sum += self.m_array[i - k].price
                self.m_array[i].sum2 += self.m_array[i - k].price2
                k += 1
        return MathSqrt(_fdiv(self.m_array[i].sum2 - _fdiv(self.m_array[i].sum * self.m_array[i].sum, float(self.m_period)), self.m_periodDiv))

class sStdStruct(MqlObject):
    _q_fields = ('price', 'price2', 'sum', 'sum2')
    def __init__(self, *args):
        self.price = 0.0
        self.price2 = 0.0
        self.sum = 0.0
        self.sum2 = 0.0

def OnInit():
    global _bandsFillZone, _maHandle
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(6, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(7, breakup, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_ARROW, 217)
    PlotIndexSetInteger(5, PLOT_ARROW_SHIFT, -10)
    SetIndexBuffer(8, breakdn, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_ARROW, 218)
    PlotIndexSetInteger(6, PLOT_ARROW_SHIFT, 10)
    iStdDeviation.init(inpPeriod, inpDevType == dev_sample)
    _bandsFillZone = ((1.0 - (inpZonesPercent / 100.0)) if (inpZonesPercent < 100 and inpZonesPercent > 0) else 0)
    _maHandle = iMA(Symbol(), Period(), inpPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(_maHandle, 'Average'):
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_maHandle, 0, 0, _copyCount, bufferMe) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            price = close[i]
        elif _sw1 == PRICE_OPEN:
            price = open[i]
        elif _sw1 == PRICE_HIGH:
            price = high[i]
        elif _sw1 == PRICE_LOW:
            price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            price = 0.0
        deviation = iStdDeviation.calculate(price, i, rates_total)
        bufferUp[i] = bufferMe[i] + (deviation * inpDeviations)
        bufferDn[i] = bufferMe[i] - (deviation * inpDeviations)
        fupd[i] = bufferMe[i] + (deviation * inpDeviations * _bandsFillZone)
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i] - (deviation * inpDeviations * _bandsFillZone)
        fdnd[i] = bufferDn[i]
        breakup[i] = (high[i] if (close[i] > bufferUp[i]) else EMPTY_VALUE)
        breakdn[i] = (low[i] if (close[i] < bufferDn[i]) else EMPTY_VALUE)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- global variables initialised from expressions
iStdDeviation = _alloc(cStdDeviation)
iStdDeviation.__init__()

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerBandsBreakout(_MQL5Indicator):
    name = 'Bollinger bands breakout'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Bollinger bands period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDeviations': 2.5,  # Bollinger bands deviations
        'inpZonesPercent': 20.0,  # Zones percent
        'inpDevType': _Choice({0: 'Standard deviation of a sample', 1: 'Standard deviation'}, default=1),  # Standard deviations type
    }

