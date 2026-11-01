"""Voltility bands — converted from MQL5: MQL5 Indicators/Volatility bands/Voltility bands.mq5

Volatility bands
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16760576], 2: [12632256], 3: [42495]}, 'widths': {}, 'styles': {2: 2}, 'labels': {}, 'levels': [], 'description': ['Volatility bands'], 'name': 'Voltility bands', 'source': 'MQL5 Indicators/Volatility bands/Voltility bands.mq5', 'folder': 'Volatility bands', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpMidPeriod', 'py': 'inpMidPeriod', 'param': 'inpMidPeriod', 'type': 'int', 'default': 20, 'label': 'Midline period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'CCI price', 'sinput': False}, {'mql': 'inpDeviations', 'py': 'inpDeviations', 'param': 'inpDeviations', 'type': 'double', 'default': 2.4, 'label': 'bands deviation', 'sinput': False}, {'mql': 'inpLowAdjust', 'py': 'inpLowAdjust', 'param': 'inpLowAdjust', 'type': 'double', 'default': 0.9, 'label': 'Low band adjust', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpMidPeriod = _input('inpMidPeriod', 20)  # Midline period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # CCI price
inpDeviations = _input('inpDeviations', 2.4)  # bands deviation
inpLowAdjust = _input('inpLowAdjust', 0.9)  # Low band adjust
mid = Arr(0, 0.0)
bandu = Arr(0, 0.0)
bandd = Arr(0, 0.0)
tr = Arr(0, 0.0)
atr = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_atrPeriod = 0
ª_avgHandle = 0

class CLwma(MqlObject):
    _q_fields = ('m_array', 'm_arraySize', 'm_period', 'm_weight')
    def __init__(self):
        self.m_array = Arr(0, 0, factory=sLwmaArrayStruct)
        self.m_arraySize = 0
        self.m_period = 0
        self.m_weight = 0.0
        self.init(1)
        return
    def _q_dtor(self):
        ArrayFree(self.m_array)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraySize = self.m_period + 32
        self.m_weight = 1.0
        ArrayResize(self.m_array, self.m_arraySize)
        for k in range(0, self.m_arraySize):
            self.m_array[k].vsumm = 0.0
            self.m_array[k].wsumm = self.m_array[k].vsumm
            self.m_array[k].value = self.m_array[k].wsumm
    def calculate(self, value, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_array[_indC].value = value
        if i > self.m_period:
            _indP = _indC - 1
            if _indP < 0:
                _indP += self.m_arraySize
            _indB = _imod(i - self.m_period, self.m_arraySize)
            self.m_array[_indC].wsumm = self.m_array[_indP].wsumm + (value * self.m_period) - self.m_array[_indP].vsumm
            self.m_array[_indC].vsumm = self.m_array[_indP].vsumm + value - self.m_array[_indB].value
        else:
            self.m_weight = 0.0
            self.m_array[_indC].wsumm = 0.0
            self.m_array[_indC].vsumm = 0.0
            k = 0
            w = self.m_period
            _indR = _indC
            while k < self.m_period and i >= k:
                if _indR < 0:
                    _indR += self.m_arraySize
                self.m_weight += w
                self.m_array[_indC].wsumm += self.m_array[_indR].value * float(w)
                self.m_array[_indC].vsumm += self.m_array[_indR].value
                k += 1
                w -= 1
                _indR -= 1
        return _fdiv(self.m_array[_indC].wsumm, self.m_weight)

class sLwmaArrayStruct(MqlObject):
    _q_fields = ('value', 'wsumm', 'vsumm')
    def __init__(self, *args):
        self.value = 0.0
        self.wsumm = 0.0
        self.vsumm = 0.0

def OnInit():
    global ª_atrPeriod, ª_avgHandle
    SetIndexBuffer(0, bandu)
    SetIndexBuffer(1, mid)
    SetIndexBuffer(2, bandd)
    SetIndexBuffer(3, tr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, avg, INDICATOR_CALCULATIONS)
    ª_atrPeriod = (inpPeriod * 2) - 1
    ª_avgHandle = iMA(Symbol(), 0, inpMidPeriod, 0, MODE_LWMA, inpPrice)
    if not _checkHandle(ª_avgHandle, 'Average'):
        return INIT_FAILED
    iLwma.init(inpMidPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility bands (' + _str(inpPeriod) + ',' + _str(inpMidPeriod) + ',' + _str(inpDeviations) + ',' + _str(inpLowAdjust) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_avgHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if i > 0:
            tr[i] = (high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])
            if i > ª_atrPeriod:
                atr[i] = atr[i - 1] + tr[i] - tr[i - ª_atrPeriod]
            else:
                atr[i] = tr[i]
                k = 1
                while k < ª_atrPeriod and i >= k:
                    atr[i] += tr[i - k]
                    k += 1
        else:
            atr[i] = high[i] - low[i]
            tr[i] = atr[i]
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if avg[i] == EMPTY_VALUE:
            mid[i] = _price
        _atr = _fdiv(inpDeviations * atr[i], float(ª_atrPeriod))
        bandu[i] = avg[i] + (avg[i] * _fdiv(_atr, _price))
        bandd[i] = avg[i] - (avg[i] * _fdiv(_atr * inpLowAdjust, _price))
        mid[i] = iLwma.calculate((high[i] + low[i]) / 2.0, i)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- global variables initialised from expressions
iLwma = _alloc(CLwma)
iLwma.__init__()

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VoltilityBands(_MQL5Indicator):
    name = 'Voltility bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpMidPeriod': 20,  # Midline period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # CCI price
        'inpDeviations': 2.4,  # bands deviation
        'inpLowAdjust': 0.9,  # Low band adjust
    }

