"""Stochastic of average (on chart) — converted from MQL5: MQL5 Indicators/Stochastic of average (on chart)/Stochastic of average (on chart).mq5

On-chart stochastic of average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 8}, 'colors': {1: [15790335], 2: [15794160], 3: [8421504], 4: [8421504], 5: [8421504], 6: [11119017, 7451452, 17919]}, 'widths': {6: 2}, 'styles': {3: 2, 4: 2, 5: 2}, 'labels': {1: 'Upper filling', 2: 'Lower filling', 3: 'Upper level', 4: 'Middle level', 5: 'Lower level', 6: 'Stochastic'}, 'levels': [], 'description': ['On-chart stochastic of average'], 'name': 'Stochastic of average (on chart)', 'source': 'MQL5 Indicators/Stochastic of average (on chart)/Stochastic of average (on chart).mq5', 'folder': 'Stochastic of average (on chart)', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 14, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpAvgMethod', 'py': 'inpAvgMethod', 'param': 'inpAvgMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpAvgPrice', 'py': 'inpAvgPrice', 'param': 'inpAvgPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpHlPeriod', 'py': 'inpHlPeriod', 'param': 'inpHlPeriod', 'type': 'int', 'default': 25, 'label': 'Highest high/lowest low period', 'sinput': False}, {'mql': 'inpHlLevelUp', 'py': 'inpHlLevelUp', 'param': 'inpHlLevelUp', 'type': 'double', 'default': 70.0, 'label': 'OB level', 'sinput': False}, {'mql': 'inpHlLevelDn', 'py': 'inpHlLevelDn', 'param': 'inpHlLevelDn', 'type': 'double', 'default': 30.0, 'label': 'OS level', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 14)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 3)  # Stochastic slowing
inpAvgPeriod = _input('inpAvgPeriod', 14)  # Average period
inpAvgMethod = _input('inpAvgMethod', MODE_EMA)  # Average method
inpAvgPrice = _input('inpAvgPrice', PRICE_CLOSE)  # Price
inpHlPeriod = _input('inpHlPeriod', 25)  # Highest high/lowest low period
inpHlLevelUp = _input('inpHlLevelUp', 70.0)  # OB level
inpHlLevelDn = _input('inpHlLevelDn', 30.0)  # OS level
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldd = Arr(0, 0.0)
filldu = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
sto = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_maHandle = 0
ª_maPeriod = 0
ª_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")

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
    global ª_maHandle, ª_maPeriod
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, levm, INDICATOR_DATA)
    SetIndexBuffer(5, levu, INDICATOR_DATA)
    SetIndexBuffer(6, levd, INDICATOR_DATA)
    SetIndexBuffer(7, val, INDICATOR_DATA)
    SetIndexBuffer(8, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(9, sto, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, avg, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpAvgMethod, inpAvgPrice)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic of ' + ª_maNames[inpAvgMethod] + ' (' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(ª_maPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if avg[i] == EMPTY_VALUE:
            avg[i] = close[i]
        sto[i] = iStoch.calculate(avg[i], avg[i], avg[i], inpStoPeriod, inpStoSlowing, i)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpHlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = high[ArrayMaximum(high, start, inpHlPeriod - 1)]
            _s_OnCalculate_prev_min = low[ArrayMinimum(low, start, inpHlPeriod - 1)]
        max_ = (high[i] if (high[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (low[i] if (low[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpHlLevelUp * range_)
        levd[i] = min_ + (inpHlLevelDn * range_)
        levm[i] = min_ + (50 * range_)
        filldu[i] = min_ + (sto[i] * range_)
        fillud[i] = filldu[i]
        val[i] = fillud[i]
        filluu[i] = max_
        filldd[i] = min_
        _sw1 = inpColorChange
        if _sw1 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw1 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
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
iStoch = _alloc(cStochastic)
iStoch.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticOfAverageOnChart(_MQL5Indicator):
    name = 'Stochastic of average (on chart)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 14,  # Stochastic period
        'inpStoSlowing': 3,  # Stochastic slowing
        'inpAvgPeriod': 14,  # Average period
        'inpAvgMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpAvgPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpHlPeriod': 25,  # Highest high/lowest low period
        'inpHlLevelUp': 70.0,  # OB level
        'inpHlLevelDn': 30.0,  # OS level
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on OB/OS level', 2: 'Change color on level 50 cross'}, default=1),  # Color changing mode
    }

