"""Parabolic SAR (oma) — converted from MQL5: MQL5 Indicators/Parabolic SAR of average/Parabolic SAR (oma).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [9662683, 3329330]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Parabolic SAR (oma)', 'source': 'MQL5 Indicators/Parabolic SAR of average/Parabolic SAR (oma).mq5', 'folder': 'Parabolic SAR of average', 'inputs': [{'mql': 'inpSARStep', 'py': 'inpSARStep', 'param': 'inpSARStep', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'inpSARMaximum', 'py': 'inpSARMaximum', 'param': 'inpSARMaximum', 'type': 'double', 'default': 0.2, 'label': 'SAR maximum', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpMahPrice', 'py': 'inpMahPrice', 'param': 'inpMahPrice', 'type': 'int', 'default': 3, 'label': 'Price for high', 'sinput': False}, {'mql': 'inpMalPrice', 'py': 'inpMalPrice', 'param': 'inpMalPrice', 'type': 'int', 'default': 4, 'label': 'Price for low', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSARStep = _input('inpSARStep', 0.02)  # SAR step
inpSARMaximum = _input('inpSARMaximum', 0.2)  # SAR maximum
inpMaPeriod = _input('inpMaPeriod', 14)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpMahPrice = _input('inpMahPrice', PRICE_HIGH)  # Price for high
inpMalPrice = _input('inpMalPrice', PRICE_LOW)  # Price for low
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avgh = Arr(0, 0.0)
avgl = Arr(0, 0.0)
_mahHandle = 0
_malHandle = 0
sarOpen = 0.0
sarPosition = 0.0
sarChange = 0.0

class CParabolic(MqlObject):
    _q_fields = ('m_step', 'm_maximum', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_step = 0.0
        self.m_maximum = 0.0
        self.m_array = Arr(0, 0, factory=sParabolicStruct)
        self.m_arraySize = 0
        self.m_step = 0.02
        self.m_maximum = 0.2
        self.m_arraySize = -1
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, step, maximum):
        self.m_step = step
        self.m_maximum = maximum
        return True
    def calculate(self, high, low, pOpen, pPosition, pChange, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if high < low:
            temp = high
            high = low
            low = temp
        pClose = high
        pChange.v = 0.0
        self.m_array[i].ohigh = high
        self.m_array[i].olow = low
        if i < 1:
            self.m_array[i].high = high
            self.m_array[i].low = low
            self.m_array[i].open = high
            self.m_array[i].position = -1.0
            return EMPTY_VALUE
        self.m_array[i].open = self.m_array[i - 1].open
        self.m_array[i].af = self.m_array[i - 1].af
        self.m_array[i].position = self.m_array[i - 1].position
        self.m_array[i].high = MathMax(self.m_array[i - 1].high, high)
        self.m_array[i].low = MathMin(self.m_array[i - 1].low, low)
        if self.m_array[i].position == 1:
            if low <= self.m_array[i].open:
                self.m_array[i].position = -1.0
                pChange.v = -1.0
                pClose = self.m_array[i].high
                self.m_array[i].high = high
                self.m_array[i].low = low
                self.m_array[i].af = self.m_step
                self.m_array[i].open = pClose + (self.m_array[i].af * (self.m_array[i].low - pClose))
                if self.m_array[i].open < self.m_array[i].ohigh:
                    self.m_array[i].open = self.m_array[i].ohigh
                if self.m_array[i].open < self.m_array[i - 1].ohigh:
                    self.m_array[i].open = self.m_array[i - 1].ohigh
            else:
                pClose = self.m_array[i].open
                if self.m_array[i].high > self.m_array[i - 1].high and self.m_array[i].af < self.m_maximum:
                    self.m_array[i].af = MathMin(self.m_array[i].af + self.m_step, self.m_maximum)
                self.m_array[i].open = pClose + (self.m_array[i].af * (self.m_array[i].high - pClose))
                if self.m_array[i].open > self.m_array[i].olow:
                    self.m_array[i].open = self.m_array[i].olow
                if self.m_array[i].open > self.m_array[i - 1].olow:
                    self.m_array[i].open = self.m_array[i - 1].olow
        elif high >= self.m_array[i].open:
            self.m_array[i].position = 1.0
            pChange.v = 1.0
            pClose = self.m_array[i].low
            self.m_array[i].low = low
            self.m_array[i].high = high
            self.m_array[i].af = self.m_step
            self.m_array[i].open = pClose + (self.m_array[i].af * (self.m_array[i].high - pClose))
            if self.m_array[i].open > self.m_array[i].olow:
                self.m_array[i].open = self.m_array[i].olow
            if self.m_array[i].open > self.m_array[i - 1].olow:
                self.m_array[i].open = self.m_array[i - 1].olow
        else:
            pClose = self.m_array[i].open
            if self.m_array[i].low < self.m_array[i - 1].low and self.m_array[i].af < self.m_maximum:
                self.m_array[i].af = MathMin(self.m_array[i].af + self.m_step, self.m_maximum)
            self.m_array[i].open = pClose + (self.m_array[i].af * (self.m_array[i].low - pClose))
            if self.m_array[i].open < self.m_array[i].ohigh:
                self.m_array[i].open = self.m_array[i].ohigh
            if self.m_array[i].open < self.m_array[i - 1].ohigh:
                self.m_array[i].open = self.m_array[i - 1].ohigh
        pOpen.v = self.m_array[i].open
        pPosition.v = self.m_array[i].position
        return pClose

class sParabolicStruct(MqlObject):
    _q_fields = ('open', 'high', 'low', 'ohigh', 'olow', 'position', 'af')
    def __init__(self, *args):
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.ohigh = 0.0
        self.olow = 0.0
        self.position = 0.0
        self.af = 0.0

def OnInit():
    global _mahHandle, _malHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, avgh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, avgl, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    _mahHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpMahPrice)
    if not _checkHandle(_mahHandle, 'average of high'):
        return INIT_FAILED
    _malHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpMalPrice)
    if not _checkHandle(_malHandle, 'average of low'):
        return INIT_FAILED
    iParabolic.init(inpSARStep, inpSARMaximum)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_mahHandle, 0, 0, _copyCount, avgh) != _copyCount:
        return prev_calculated
    if CopyBuffer(_malHandle, 0, 0, _copyCount, avgl) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        val[i] = iParabolic.calculate(avgh[i], avgl[i], _GlobRef(globals(), 'sarOpen'), _GlobRef(globals(), 'sarPosition'), _GlobRef(globals(), 'sarChange'), i, rates_total)
        valc[i] = (1 if (sarPosition == 1) else 0)
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
iParabolic = _alloc(CParabolic)
iParabolic.__init__()

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ParabolicSAROma(_MQL5Indicator):
    name = 'Parabolic SAR (oma)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSARStep': 0.02,  # SAR step
        'inpSARMaximum': 0.2,  # SAR maximum
        'inpMaPeriod': 14,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpMahPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=3),  # Price for high
        'inpMalPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=4),  # Price for low
    }

