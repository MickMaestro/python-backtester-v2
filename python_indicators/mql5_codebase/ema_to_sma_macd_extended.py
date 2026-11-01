"""EMA to SMA MACD (extended) — converted from MQL5: MQL5 Indicators/EMA to SMA MACD - extended/EMA to SMA MACD (extended).mq5

EMA to SMA MACD
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 7, 3: 1, 4: 1}, 'colors': {1: [14155735, 15132415], 2: [7451452, 42495], 3: [11119017], 4: [11119017]}, 'widths': {4: 2}, 'styles': {}, 'labels': {1: 'Macd fill area', 2: 'Signal fill area', 3: 'EMA to SMA MACD', 4: 'Signal'}, 'levels': [], 'description': ['EMA to SMA MACD'], 'name': 'EMA to SMA MACD (extended)', 'source': 'MQL5 Indicators/EMA to SMA MACD - extended/EMA to SMA MACD (extended).mq5', 'folder': 'EMA to SMA MACD - extended', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 26, 'label': 'Period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 26)  # Period
inpSignalPeriod = _input('inpSignalPeriod', 5)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
fillmu = Arr(0, 0.0)
fillmd = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
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
    SetIndexBuffer(0, fillmu, INDICATOR_DATA)
    SetIndexBuffer(1, fillmd, INDICATOR_DATA)
    SetIndexBuffer(2, fillu, INDICATOR_DATA)
    SetIndexBuffer(3, filld, INDICATOR_DATA)
    SetIndexBuffer(4, macd, INDICATOR_DATA)
    SetIndexBuffer(5, signal, INDICATOR_DATA)
    SetIndexBuffer(6, ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, sma, INDICATOR_CALCULATIONS)
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
        fillu[i] = ema[i] - sma[i]
        macd[i] = fillu[i]
        filld[i] = iSignal.calculate(macd[i], i)
        signal[i] = filld[i]
        fillmd[i] = 0.0
        fillmu[i] = (MathMax(MathMin(macd[i], signal[i]), 0) if (macd[i] > 0) else MathMin(MathMax(macd[i], signal[i]), 0))
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


class EMAToSMAMACDExtended(_MQL5Indicator):
    name = 'EMA to SMA MACD (extended)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 26,  # Period
        'inpSignalPeriod': 5,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

