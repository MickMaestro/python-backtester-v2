"""EMA to SMA MACD — converted from MQL5: MQL5 Indicators/EMA to SMA MACD/EMA to SMA MACD.mq5

EMA to SMA MACD
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [11119017], 2: [9662683]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'EMA to SMA MACD', 2: 'Signal'}, 'levels': [], 'description': ['EMA to SMA MACD'], 'name': 'EMA to SMA MACD', 'source': 'MQL5 Indicators/EMA to SMA MACD/EMA to SMA MACD.mq5', 'folder': 'EMA to SMA MACD', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 26, 'label': 'Period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 26)  # Period
inpSignalPeriod = _input('inpSignalPeriod', 5)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
macd = Arr(0, 0.0)
signal = Arr(0, 0.0)
ema = Arr(0, 0.0)
sma = Arr(0, 0.0)
ª_emaHandle = 0
ª_smaHandle = 0
ª_maPeriod = 0

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
        for k in range(0, self.m_arraySize):
            self.m_array[k].summ = 0.0
            self.m_array[k].value = self.m_array[k].summ
    def calculate(self, value, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_array[_indC].value = value
        if i > self.m_period:
            _indP = _imod(i - 1, self.m_arraySize)
            _indB = _imod(i - self.m_period, self.m_arraySize)
            self.m_array[_indC].summ = self.m_array[_indP].summ + value - self.m_array[_indB].value
        else:
            self.m_array[_indC].summ = 0.0
            k = 0
            _indR = _indC
            while k < self.m_period and i >= k:
                if _indR < 0:
                    _indR += self.m_arraySize
                self.m_array[_indC].summ += self.m_array[_indR].value
                k += 1
                _indR -= 1
            return _fdiv(self.m_array[_indC].summ, float(k))
        return _fdiv(self.m_array[_indC].summ, float(self.m_period))

class scSmaArrayStruct(MqlObject):
    _q_fields = ('value', 'summ')
    def __init__(self, *args):
        self.value = 0.0
        self.summ = 0.0

def OnInit():
    global ª_emaHandle, ª_maPeriod, ª_smaHandle
    SetIndexBuffer(0, macd, INDICATOR_DATA)
    SetIndexBuffer(1, signal, INDICATOR_DATA)
    SetIndexBuffer(2, ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, sma, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpPeriod if (inpPeriod > 0) else 1)
    ª_emaHandle = iMA(Symbol(), 0, ª_maPeriod, 0, MODE_EMA, inpPrice)
    if not _checkHandle(ª_emaHandle, 'EMA'):
        return INIT_FAILED
    ª_smaHandle = iMA(Symbol(), 0, ª_maPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_smaHandle, 'SMA'):
        return INIT_FAILED
    iSignal.init(inpSignalPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMA to SMA MACD (' + _str(inpPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_emaHandle, 0, 0, _copyCount, ema) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_smaHandle, 0, 0, _copyCount, sma) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if ema[i] == EMPTY_VALUE:
            ema[i] = 0.0
        if sma[i] == EMPTY_VALUE:
            sma[i] = 0.0
        macd[i] = ema[i] - sma[i]
        signal[i] = iSignal.calculate(macd[i], i)
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
iSignal = _alloc(CSma)
iSignal.__init__()

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAToSMAMACD(_MQL5Indicator):
    name = 'EMA to SMA MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 26,  # Period
        'inpSignalPeriod': 5,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

