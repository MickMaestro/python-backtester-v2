"""Highest high - lowest low SR — converted from MQL5: MQL5 Indicators/Highest high & lowest low support resistance/Highest high - lowest low SR.mq5

Highest high / lowest low SR
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 8, 6: 8}, 'colors': {1: [15466475, 15461375], 2: [16777195, 15132415], 3: [4294967295, 8421504], 4: [4294967295, 8421504], 5: [4294967295, 8421504], 6: [4294967295, 8421504]}, 'widths': {}, 'styles': {3: 2, 4: 2, 5: 2, 6: 2}, 'labels': {1: 'fill 1', 2: 'fill 2', 3: 'hh1', 4: 'll1', 5: 'hh2', 6: 'll2'}, 'levels': [], 'description': ['Highest high / lowest low SR'], 'name': 'Highest high - lowest low SR', 'source': 'MQL5 Indicators/Highest high & lowest low support resistance/Highest high - lowest low SR.mq5', 'folder': 'Highest high & lowest low support resistance', 'inputs': [{'mql': 'inpFastHlPeriod', 'py': 'inpFastHlPeriod', 'param': 'inpFastHlPeriod', 'type': 'int', 'default': 8, 'label': 'Fast highest high/lowest low period', 'sinput': False}, {'mql': 'inpSlowHlPeriod', 'py': 'inpSlowHlPeriod', 'param': 'inpSlowHlPeriod', 'type': 'int', 'default': 21, 'label': 'Slow highest high/lowest low period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastHlPeriod = _input('inpFastHlPeriod', 8)  # Fast highest high/lowest low period
inpSlowHlPeriod = _input('inpSlowHlPeriod', 21)  # Slow highest high/lowest low period
hh1 = Arr(0, 0.0)
hh1c = Arr(0, 0.0)
hh2 = Arr(0, 0.0)
hh2c = Arr(0, 0.0)
ll1 = Arr(0, 0.0)
ll1c = Arr(0, 0.0)
ll2 = Arr(0, 0.0)
ll2c = Arr(0, 0.0)
fh1 = Arr(0, 0.0)
fh2 = Arr(0, 0.0)
fl1 = Arr(0, 0.0)
fl2 = Arr(0, 0.0)
trend = Arr(0, 0.0)
ª_rsfHandle = 0
ª_rssHandle = 0

class cMinMax(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'prevbar', 'currmin', 'currmax', 'prevmax', 'prevmin', 'minArray', 'maxArray')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.prevbar = 0
        self.currmin = 0.0
        self.currmax = 0.0
        self.prevmax = 0.0
        self.prevmin = 0.0
        self.minArray = Arr(0, 0.0)
        self.maxArray = Arr(0, 0.0)
        self.prevbar = INT_MIN
        self.originalPeriod = self.prevbar
        return
    def _q_dtor(self):
        ArrayFree(self.minArray)
        ArrayFree(self.maxArray)
        return
    def calculate(self, valueMin, valueMax, forPeriod, min_, max_, i):
        if self.prevbar != i:
            self.prevbar = i
            if self.originalPeriod != forPeriod:
                self.originalPeriod = forPeriod
                self.period = (forPeriod if (forPeriod > 0) else 1)
                self.prevmin = valueMin
                self.prevmax = valueMax
                self.currmin = valueMin
                self.currmax = valueMax
                ArrayResize(self.minArray, self.period - 1)
                ArrayInitialize(self.minArray, valueMin)
                ArrayResize(self.maxArray, self.period - 1)
                ArrayInitialize(self.maxArray, valueMax)
            if self.period > 1:
                _pos = _imod(i, self.period - 1)
                self.minArray[_pos] = self.currmin
                self.maxArray[_pos] = self.currmax
                self.prevmin = self.minArray[ArrayMinimum(self.minArray)]
                self.prevmax = self.maxArray[ArrayMaximum(self.maxArray)]
            else:
                self.prevmin = valueMin
                self.prevmax = valueMax
        self.currmin = valueMin
        self.currmax = valueMax
        max_.v = (self.prevmax if (self.prevmax > valueMax) else valueMax)
        min_.v = (self.prevmin if (self.prevmin < valueMin) else valueMin)
        return

def OnInit():
    SetIndexBuffer(0, fh1, INDICATOR_DATA)
    SetIndexBuffer(1, fl1, INDICATOR_DATA)
    SetIndexBuffer(2, fh2, INDICATOR_DATA)
    SetIndexBuffer(3, fl2, INDICATOR_DATA)
    SetIndexBuffer(4, hh1, INDICATOR_DATA)
    SetIndexBuffer(5, hh1c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, ll1, INDICATOR_DATA)
    SetIndexBuffer(7, ll1c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, hh2, INDICATOR_DATA)
    SetIndexBuffer(9, hh2c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, ll2, INDICATOR_DATA)
    SetIndexBuffer(11, ll2c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(12, trend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Highest high / lowest low SR (' + _str(inpFastHlPeriod) + ',' + _str(inpSlowHlPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        iMinMaxFast.calculate(low[i], high[i], inpFastHlPeriod, _ElemRef(ll2, i), _ElemRef(hh2, i), i)
        fh2[i] = hh2[i]
        fl2[i] = ll2[i]
        iMinMaxSlow.calculate(low[i], high[i], inpSlowHlPeriod, _ElemRef(ll1, i), _ElemRef(hh1, i), i)
        if i > 0:
            trend[i] = (1 if (hh1[i] > hh1[i - 1] or ll1[i] > ll1[i - 1]) else -1 if (hh1[i] < hh1[i - 1] or ll1[i] < ll1[i - 1]) else trend[i - 1])
            fh1[i] = (hh1[i] if (trend[i] == 1) else ll1[i])
            fl1[i] = (ll1[i] if (trend[i] == 1) else hh1[i])
            hh1c[i] = (1 if (hh1[i] == hh1[i - 1]) else 0)
            hh2c[i] = (1 if (hh2[i] == hh2[i - 1]) else 0)
            ll1c[i] = (1 if (ll1[i] == ll1[i - 1]) else 0)
            ll2c[i] = (1 if (ll2[i] == ll2[i - 1]) else 0)
        else:
            fh1[i] = hh1[i]
            fl1[i] = ll1[i]
            trend[i] = 0.0
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
iMinMaxFast = _alloc(cMinMax)
iMinMaxFast.__init__()
iMinMaxSlow = _alloc(cMinMax)
iMinMaxSlow.__init__()

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HighestHighLowestLowSR(_MQL5Indicator):
    name = 'Highest high - lowest low SR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastHlPeriod': 8,  # Fast highest high/lowest low period
        'inpSlowHlPeriod': 21,  # Slow highest high/lowest low period
    }

