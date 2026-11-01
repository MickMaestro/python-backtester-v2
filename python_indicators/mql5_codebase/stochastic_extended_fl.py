"""Stochastic extended (fl) — converted from MQL5: MQL5 Indicators/Stochastic extended - floating levels/Stochastic extended (fl).mq5

Stochastic of choosable price - extended with floating levels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 8, 5: 1}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [12632256, 7451452, 17919], 5: [8421504]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2, 5: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'Stochastic', 5: 'Signal'}, 'levels': [], 'description': ['Stochastic of choosable price - extended with floating levels'], 'name': 'Stochastic extended (fl)', 'source': 'MQL5 Indicators/Stochastic extended - floating levels/Stochastic extended (fl).mq5', 'folder': 'Stochastic extended - floating levels', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpStoSignal', 'py': 'inpStoSignal', 'param': 'inpStoSignal', 'type': 'int', 'default': 5, 'label': 'Stochastic signal period', 'sinput': False}, {'mql': 'inpStoMethod', 'py': 'inpStoMethod', 'param': 'inpStoMethod', 'type': 'int', 'default': 1, 'label': 'Stochastic signal method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum enPrices
pr_close = 1
pr_open = 2
pr_high = 3
pr_low = 4
pr_median = 5
pr_typical = 6
pr_weighted = 7
pr_highlow = -99
_enum('enPrices', {1: 'pr_close', 2: 'pr_open', 3: 'pr_high', 4: 'pr_low', 5: 'pr_median', 6: 'pr_typical', 7: 'pr_weighted', -99: 'pr_highlow'})

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 32)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 5)  # Stochastic slowing
inpStoSignal = _input('inpStoSignal', 5)  # Stochastic signal period
inpStoMethod = _input('inpStoMethod', MODE_EMA)  # Stochastic signal method
inpPrice = _input('inpPrice', pr_close)  # Price
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
sto = Arr(0, 0.0)
stoc = Arr(0, 0.0)
sig = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)

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

class cStochastic(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'slowing', 'slowingSize', 'diffh', 'diffl', 'sumh', 'suml', 'minMax')
    _q_ptrs = ('minMax',)
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.slowing = 0
        self.slowingSize = 0
        self.diffh = Arr(0, 0.0)
        self.diffl = Arr(0, 0.0)
        self.sumh = Arr(0, 0.0)
        self.suml = Arr(0, 0.0)
        self.minMax = None
        self.minMax = cMinMax()
        self.originalPeriod = -1
        return
    def _q_dtor(self):
        if CheckPointer(self.minMax) == POINTER_DYNAMIC:
            _delete(self.minMax)
        ArrayFree(self.diffh)
        ArrayFree(self.diffl)
        ArrayFree(self.sumh)
        ArrayFree(self.suml)
        return
    def calculate(self, price, priceHigh, priceLow, forPeriod, forSlowing, i):
        if self.originalPeriod != forPeriod:
            self.originalPeriod = forPeriod
            self.period = (forPeriod if (forPeriod > 0) else 1)
            self.slowing = (forSlowing if (forSlowing > 0) else 1)
            self.slowingSize = self.slowing + 32
            ArrayResize(self.diffh, self.slowingSize)
            ArrayInitialize(self.diffh, 0)
            ArrayResize(self.diffl, self.slowingSize)
            ArrayInitialize(self.diffl, 0)
            ArrayResize(self.sumh, self.slowingSize)
            ArrayInitialize(self.sumh, 0)
            ArrayResize(self.suml, self.slowingSize)
            ArrayInitialize(self.suml, 0)
        min_ = Box(0.0)
        max_ = Box(0.0)
        self.minMax.calculate(priceLow, priceHigh, self.period, min_, max_, i)
        _pos = _imod(i, self.slowingSize)
        self.diffh[_pos] = max_.v - min_.v
        self.diffl[_pos] = price - min_.v
        if i > self.slowing:
            _posp = _imod(i - 1, self.slowingSize)
            _posf = _imod(i - self.slowing, self.slowingSize)
            self.sumh[_pos] = self.sumh[_posp] + self.diffh[_pos] - self.diffh[_posf]
            self.suml[_pos] = self.suml[_posp] + self.diffl[_pos] - self.diffl[_posf]
        else:
            self.sumh[_pos] = self.diffh[_pos]
            self.suml[_pos] = self.diffl[_pos]
            k = 1
            _posp = _pos - 1
            while k < self.slowing:
                if _posp < 0:
                    _posp += self.slowingSize
                self.sumh[_pos] += self.diffh[_posp]
                self.suml[_pos] += self.diffl[_posp]
                k += 1
                _posp -= 1
        return (_fdiv(100.0 * self.suml[_pos], self.sumh[_pos]) if (self.sumh[_pos] != 0.0) else 0)

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, sto, INDICATOR_DATA)
    SetIndexBuffer(4, stoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, sig, INDICATOR_DATA)
    _priceType = StringSubstr(EnumToString(inpPrice, 'enPrices'), 3)
    _priceType = ((_priceType + '/' + _priceType) if (_priceType != 'highlow') else 'low/high')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic ' + _priceType + ' (' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(inpStoSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = prev_calculated - 1
    if start < 0:
        start = 0
    for i in range(start, rates_total):
        _price = 0.0
        _priceh = 0.0
        _pricel = 0.0
        _sw1 = inpPrice
        if _sw1 == pr_close:
            _pricel = close[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_open:
            _pricel = open[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_high:
            _pricel = high[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_low:
            _pricel = low[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_median:
            _pricel = (high[i] + low[i]) / 2.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_typical:
            _pricel = (high[i] + low[i] + close[i]) / 3.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_weighted:
            _pricel = (high[i] + low[i] + close[i] + close[i]) / 4.0
            _priceh = _pricel
            _price = _priceh
        else:
            _price = close[i]
            _priceh = high[i]
            _pricel = low[i]
        sto[i] = iStoch.calculate(_price, _priceh, _pricel, inpStoPeriod, inpStoSlowing, i)
        _min = Box(0.0)
        _max = Box(0.0)
        _levelsMinMax.calculate(sto[i], sto[i], inpFlPeriod, _min, _max, i)
        range_ = (_max.v - _min.v) / 100.0
        levu[i] = _min.v + (inpFlLevelUp * range_)
        levd[i] = _min.v + (inpFlLevelDn * range_)
        levm[i] = (levu[i] + levd[i]) / 2
    weightsum = Box(0)
    _sw2 = inpStoMethod
    if _sw2 == MODE_SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, inpStoSignal, sto, sig)
    elif _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, inpStoSignal, sto, sig)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, inpStoSignal, sto, sig)
    else:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, inpStoSignal, sto, sig, weightsum)
    for i in range(start, rates_total):
        stoc[i] = (1 if (sto[i] > levu[i]) else 2 if (sto[i] < levd[i]) else 0)
    return rates_total

# ---- global variables initialised from expressions
_levelsMinMax = _alloc(cMinMax)
_levelsMinMax.__init__()
iStoch = _alloc(cStochastic)
iStoch.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticExtendedFl(_MQL5Indicator):
    name = 'Stochastic extended (fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 32,  # Stochastic period
        'inpStoSlowing': 5,  # Stochastic slowing
        'inpStoSignal': 5,  # Stochastic signal period
        'inpStoMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Stochastic signal method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Wighted', -99: 'High/Low'}, default=1),  # Price
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
    }

