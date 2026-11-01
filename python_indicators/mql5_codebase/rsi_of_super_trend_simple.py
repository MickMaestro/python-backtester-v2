"""RSI of super trend - simple — converted from MQL5: MQL5 Indicators/RSI of super trend/RSI of super trend - simple.mq5

RSI of Super trend - simple
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'RSI of Super trend'}, 'levels': [], 'description': ['RSI of Super trend - simple'], 'name': 'RSI of super trend - simple', 'source': 'MQL5 Indicators/RSI of super trend/RSI of super trend - simple.mq5', 'folder': 'RSI of super trend', 'inputs': [{'mql': 'inpPeriodRsi', 'py': 'inpPeriodRsi', 'param': 'inpPeriodRsi', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Super trend period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpAtrDevPeriod', 'py': 'inpAtrDevPeriod', 'param': 'inpAtrDevPeriod', 'type': 'int', 'default': 5, 'label': 'Atr / standard deviation period', 'sinput': False}, {'mql': 'inpUseWhat', 'py': 'inpUseWhat', 'param': 'inpUseWhat', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enUseWhat
use_atr = 0
use_dev = 1
_enum('enUseWhat', {0: 'use_atr', 1: 'use_dev'})

# ---- inputs and global variables
inpPeriodRsi = _input('inpPeriodRsi', 14)  # RSI period
inpPeriod = _input('inpPeriod', 14)  # Super trend period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpAtrDevPeriod = _input('inpAtrDevPeriod', 5)  # Atr / standard deviation period
inpUseWhat = _input('inpUseWhat', use_atr)  # Calculation method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
trend = Arr(0, 0.0)
ade = Arr(0, 0.0)
ma = Arr(0, 0.0)
prices = Arr(0, 0.0)
st = Arr(0, 0.0)
ª_adHandle = 0
ª_maHandle = 0
ª_prHandle = 0

class cRsi(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_alpha', 'm_work')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_alpha = 0.0
        self.m_work = Arr(0, 0, factory=sRsiArray)
        self.m_period = 1
        self.m_alpha = 1.0
        self.m_arraySize = 33
        ArrayResize(self.m_work, 33)
        return
    def _q_dtor(self):
        ArrayFree(self.m_work)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraySize = self.m_period + 32
        self.m_alpha = _fdiv(1.0, MathSqrt(self.m_period))
        ArrayResize(self.m_work, self.m_arraySize)
    def calculate(self, price, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_work[_indC].price = price
        if i > self.m_period:
            _indP = _indC - 1
            if _indP < 0:
                _indP += self.m_arraySize
            change = self.m_work[_indC].price - self.m_work[_indP].price
            changa = change
            if change < 0:
                changa = -change
            self.m_work[_indC].change1 = self.m_work[_indP].change1 + (self.m_alpha * (change - self.m_work[_indP].change1))
            self.m_work[_indC].change = self.m_work[_indP].change + (self.m_alpha * (self.m_work[_indC].change1 - self.m_work[_indP].change))
            self.m_work[_indC].changa1 = self.m_work[_indP].changa1 + (self.m_alpha * (changa - self.m_work[_indP].changa1))
            self.m_work[_indC].changa = self.m_work[_indP].changa + (self.m_alpha * (self.m_work[_indC].changa1 - self.m_work[_indP].changa))
        else:
            self.m_work[_indC].changa = 0.0
            k = 0
            while i > k:
                self.m_work[_indC].changa += ((self.m_work[_indC - k].price - self.m_work[_indC - k - 1].price) if (self.m_work[_indC - k].price > self.m_work[_indC - k - 1].price) else (self.m_work[_indC - k - 1].price - self.m_work[_indC - k].price))
                k += 1
            self.m_work[_indC].changa = _fdiv(self.m_work[_indC].changa, i + 1.0)
            self.m_work[_indC].changa1 = self.m_work[_indC].changa
            self.m_work[_indC].change = _fdiv(self.m_work[_indC].price - self.m_work[0].price, i + 1.0)
            self.m_work[_indC].change1 = self.m_work[_indC].change
        if self.m_work[_indC].changa != 0:
            return 50.0 * (_fdiv(self.m_work[_indC].change, self.m_work[_indC].changa) + 1.0)
        else:
            return 0.0

class sRsiArray(MqlObject):
    _q_fields = ('price', 'change1', 'changa1', 'change', 'changa')
    def __init__(self, *args):
        self.price = 0.0
        self.change1 = 0.0
        self.changa1 = 0.0
        self.change = 0.0
        self.changa = 0.0

def OnInit():
    global ª_adHandle, ª_maHandle, ª_prHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ade, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, st, INDICATOR_CALCULATIONS)
    if inpUseWhat == use_atr:
        ª_adHandle = iATR(Symbol(), 0, inpAtrDevPeriod)
        if not _checkHandle(ª_adHandle, 'ATR'):
            return INIT_FAILED
    else:
        ª_adHandle = iStdDev(Symbol(), 0, inpAtrDevPeriod, 0, MODE_SMA, inpPrice)
        if not _checkHandle(ª_adHandle, 'Standard deviation'):
            return INIT_FAILED
    ª_maHandle = iMA(Symbol(), 0, inpPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    ª_prHandle = iMA(Symbol(), 0, 1, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_prHandle, 'Prices'):
        return INIT_FAILED
    iRsi.init(inpPeriodRsi)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI (' + _str(inpPeriodRsi) + ') of super trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_adHandle, 0, 0, _copyCount, ade) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, ma) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_prHandle, 0, 0, _copyCount, prices) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        trend[i] = (1 if (prices[i] > ma[i]) else -1 if (prices[i] < ma[i]) else trend[i - 1] if (i > 0) else 0)
        st[i] = ((MathMax(low[i] - ade[i], st[i - 1]) if (trend[i] == 1) else MathMin(high[i] + ade[i], st[i - 1])) if (i > 0) else close[i])
        val[i] = iRsi.calculate(st[i], i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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
iRsi = _alloc(cRsi)
iRsi.__init__()

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOfSuperTrendSimple(_MQL5Indicator):
    name = 'RSI of super trend - simple'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriodRsi': 14,  # RSI period
        'inpPeriod': 14,  # Super trend period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpAtrDevPeriod': 5,  # Atr / standard deviation period
        'inpUseWhat': _Choice({0: 'Use ATR for calculation', 1: 'Use standard deviation for calculation'}, default=0),  # Calculation method
    }

