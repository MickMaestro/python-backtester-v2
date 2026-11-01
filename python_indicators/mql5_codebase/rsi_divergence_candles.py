"""Rsi divergence candles — converted from MQL5: MQL5 Indicators/RSI divergence candles/Rsi divergence candles.mq5

Rsi divergence candles
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 7451452, 17919]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RSI'}, 'levels': [], 'description': ['Rsi divergence candles'], 'name': 'Rsi divergence candles', 'source': 'MQL5 Indicators/RSI divergence candles/Rsi divergence candles.mq5', 'folder': 'RSI divergence candles', 'inputs': [{'mql': 'inpFastRsiPeriod', 'py': 'inpFastRsiPeriod', 'param': 'inpFastRsiPeriod', 'type': 'int', 'default': 8, 'label': 'Fast RSI period', 'sinput': False}, {'mql': 'inpSlowRsiPeriod', 'py': 'inpSlowRsiPeriod', 'param': 'inpSlowRsiPeriod', 'type': 'int', 'default': 55, 'label': 'Slow RSI period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastRsiPeriod = _input('inpFastRsiPeriod', 8)  # Fast RSI period
inpSlowRsiPeriod = _input('inpSlowRsiPeriod', 55)  # Slow RSI period
inpSmoothPeriod = _input('inpSmoothPeriod', 10)  # Smoothing period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
rsio = Arr(0, 0.0)
rsih = Arr(0, 0.0)
rsil = Arr(0, 0.0)
rsic = Arr(0, 0.0)
rsicl = Arr(0, 0.0)
rsif = Arr(0, 0.0)
rsis = Arr(0, 0.0)
ª_workRsi = Arr(4, 0.0, dyn=False)
ª_rsfHandle = 0
ª_rssHandle = 0

class CSma(MqlObject):
    _q_fields = ('m_array', 'm_arraySize', 'm_period')
    def __init__(self):
        self.m_array = Arr(0, 0, factory=scSmaArrayStruct)
        self.m_arraySize = 0
        self.m_period = 0
        self.init(1)
        return
    def _q_dtor(self):
        ArrayFree(self.m_array)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraySize = self.m_period + 32
        ArrayResize(self.m_array, self.m_arraySize)
        k = 0
        while k < self.m_arraySize:
            self.m_array[k].init()
            k += 1
    def calculate(self, value, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_array[_indC].value = value
        if i > self.m_period:
            _indP = _imod(i - 1, self.m_arraySize)
            _indF = _imod(i - self.m_period, self.m_arraySize)
            self.m_array[_indC].sum = self.m_array[_indP].sum + value - self.m_array[_indF].value
        else:
            self.m_array[_indC].sum = 0.0
            k = 0
            _indR = _indC
            while k < self.m_period and i >= k:
                if _indR < 0:
                    _indR += self.m_arraySize
                self.m_array[_indC].sum += self.m_array[_indR].value
                k += 1
                _indR -= 1
            return _fdiv(self.m_array[_indC].sum, float(k))
        return _fdiv(self.m_array[_indC].sum, float(self.m_period))

class scSmaArrayStruct(MqlObject):
    _q_fields = ('value', 'sum')
    def __init__(self, *args):
        self.value = 0.0
        self.sum = 0.0
    def init(self):
        self.sum = 0.0
        self.value = self.sum

def OnInit():
    global ª_rsfHandle, ª_rssHandle
    SetIndexBuffer(0, rsio, INDICATOR_DATA)
    SetIndexBuffer(1, rsih, INDICATOR_DATA)
    SetIndexBuffer(2, rsil, INDICATOR_DATA)
    SetIndexBuffer(3, rsic, INDICATOR_DATA)
    SetIndexBuffer(4, rsicl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, rsif, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, rsis, INDICATOR_CALCULATIONS)
    ª_rsfHandle = iRSI(Symbol(), 0, inpFastRsiPeriod, inpPrice)
    if not _checkHandle(ª_rsfHandle, 'Fast RSI'):
        return INIT_FAILED
    ª_rssHandle = iRSI(Symbol(), 0, inpSlowRsiPeriod, inpPrice)
    if not _checkHandle(ª_rssHandle, 'Slow RSI'):
        return INIT_FAILED
    iSma[0].init(inpSmoothPeriod)
    iSma[1].init(inpSmoothPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi divergence candles (' + _str(inpFastRsiPeriod) + ',' + _str(inpSlowRsiPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_rsfHandle, 0, 0, _copyCount, rsif) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_rssHandle, 0, 0, _copyCount, rsis) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if rsif[i] == EMPTY_VALUE:
            rsif[i] = 0.0
        if rsis[i] == EMPTY_VALUE:
            rsis[i] = 0.0
        rsio[i] = iSma[0].calculate(rsis[i], i)
        rsih[i] = (rsif[i] if (rsif[i] > rsis[i]) else rsis[i])
        rsil[i] = (rsif[i] if (rsif[i] < rsis[i]) else rsis[i])
        rsic[i] = iSma[1].calculate(rsif[i], i)
        rsicl[i] = (1 if (rsic[i] > rsio[i]) else 2 if (rsic[i] < rsio[i]) else 0)
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
iSma = Arr(2, 0, dyn=False, factory=CSma)

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiDivergenceCandles(_MQL5Indicator):
    name = 'Rsi divergence candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastRsiPeriod': 8,  # Fast RSI period
        'inpSlowRsiPeriod': 55,  # Slow RSI period
        'inpSmoothPeriod': 10,  # Smoothing period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

