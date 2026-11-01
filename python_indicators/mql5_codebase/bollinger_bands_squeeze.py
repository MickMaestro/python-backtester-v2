"""Bollinger bands (squeeze) — converted from MQL5: MQL5 Indicators/Bollinger bands - squeeze/Bollinger bands (squeeze).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 8}, 'colors': {1: [13628367], 2: [13492732], 3: [7451452], 4: [6333684], 5: [12632256, 7451452, 6333684]}, 'widths': {5: 2}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Average'}, 'levels': [], 'description': [], 'name': 'Bollinger bands (squeeze)', 'source': 'MQL5 Indicators/Bollinger bands - squeeze/Bollinger bands (squeeze).mq5', 'folder': 'Bollinger bands - squeeze', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDeviations', 'py': 'inpDeviations', 'param': 'inpDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bollinger bands deviations multiplier', 'sinput': False}, {'mql': 'inpAtrMultiplier', 'py': 'inpAtrMultiplier', 'param': 'inpAtrMultiplier', 'type': 'double', 'default': 1.5, 'label': 'ATR multiplier', 'sinput': False}, {'mql': 'inpZonesPercent', 'py': 'inpZonesPercent', 'param': 'inpZonesPercent', 'type': 'double', 'default': 20.0, 'label': 'Zones percent', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Bollinger bands period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDeviations = _input('inpDeviations', 2.0)  # Bollinger bands deviations multiplier
inpAtrMultiplier = _input('inpAtrMultiplier', 1.5)  # ATR multiplier
inpZonesPercent = _input('inpZonesPercent', 20.0)  # Zones percent
bufferUp = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
bufferMec = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
prices = Arr(0, 0.0)
_bandsFillZone = 0.0
_maHandle = 0

class cSqueeze(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_devMultiplier', 'm_atrMultiplier', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_devMultiplier = 0.0
        self.m_atrMultiplier = 0.0
        self.m_array = Arr(0, 0, factory=sSqueezeStruct)
        self.m_period = 1
        self.m_arraySize = -1
        self.m_devMultiplier = 2.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, devMultiplier, atrMultiplier):
        self.m_period = (period if (period > 1) else 1)
        self.m_devMultiplier = devMultiplier
        self.m_atrMultiplier = atrMultiplier
    def calculate(self, price, close, high, low, devs, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].price = price[i]
        self.m_array[i].price2 = price[i] * price[i]
        self.m_array[i].tr = (((high[i] if (close[i - 1] < high[i]) else close[i - 1]) - (low[i] if (close[i - 1] > low[i]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum + self.m_array[i].price - self.m_array[i - self.m_period].price
            self.m_array[i].sum2 = self.m_array[i - 1].sum2 + self.m_array[i].price2 - self.m_array[i - self.m_period].price2
            self.m_array[i].sumtr = self.m_array[i - 1].sumtr + self.m_array[i].tr - self.m_array[i - self.m_period].tr
        else:
            self.m_array[i].sum = self.m_array[i].price
            self.m_array[i].sum2 = self.m_array[i].price2
            self.m_array[i].sumtr = self.m_array[i].tr
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sum += self.m_array[i - k].price
                self.m_array[i].sum2 += self.m_array[i - k].price2
                self.m_array[i].sumtr += self.m_array[i - k].tr
                k += 1
        devs.v = MathSqrt(_fdiv(self.m_array[i].sum2 - _fdiv(self.m_array[i].sum * self.m_array[i].sum, float(self.m_period)), float(self.m_period)))
        _atr = _fdiv(self.m_array[i].sumtr, float(self.m_period))
        _avg = _fdiv(self.m_array[i].sum, float(self.m_period))
        return ((1 if (((high[i] + low[i]) / 2.0) > _avg) else -1) if ((self.m_devMultiplier * devs.v) > (self.m_atrMultiplier * _atr)) else 0)

class sSqueezeStruct(MqlObject):
    _q_fields = ('price', 'price2', 'sum', 'sum2', 'tr', 'sumtr')
    def __init__(self, *args):
        self.price = 0.0
        self.price2 = 0.0
        self.sum = 0.0
        self.sum2 = 0.0
        self.tr = 0.0
        self.sumtr = 0.0

def OnInit():
    global _bandsFillZone, _maHandle
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(6, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(7, bufferMec, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, prices, INDICATOR_CALCULATIONS)
    iBbSqueeze.init(inpPeriod, inpDeviations, inpAtrMultiplier)
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
        prices[i] = getPrice(inpPrice, open, high, low, close, i)
        deviation = Box(0.0)
        state = iBbSqueeze.calculate(prices, close, high, low, deviation, i, rates_total)
        bufferUp[i] = bufferMe[i] + (deviation.v * inpDeviations)
        bufferDn[i] = bufferMe[i] - (deviation.v * inpDeviations)
        fupd[i] = ((bufferMe[i] + (deviation.v * inpDeviations * _bandsFillZone)) if (state != 0) else bufferUp[i])
        fupu[i] = bufferUp[i]
        fdnu[i] = ((bufferMe[i] - (deviation.v * inpDeviations * _bandsFillZone)) if (state != 0) else bufferDn[i])
        fdnd[i] = bufferDn[i]
        bufferMec[i] = (1 if (state == 1) else 2 if (state == -1) else 0)
        i += 1
    return i

def getPrice(tprice, open, high, low, close, i):
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
iBbSqueeze = _alloc(cSqueeze)
iBbSqueeze.__init__()

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerBandsSqueeze(_MQL5Indicator):
    name = 'Bollinger bands (squeeze)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Bollinger bands period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDeviations': 2.0,  # Bollinger bands deviations multiplier
        'inpAtrMultiplier': 1.5,  # ATR multiplier
        'inpZonesPercent': 20.0,  # Zones percent
    }

