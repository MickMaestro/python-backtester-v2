"""Nonlinear Kalman filter (fl) — converted from MQL5: MQL5 Indicators/Nonlinear Kalman filter - floating levels/Nonlinear Kalman filter (fl).mq5

Nonlinear Kalman filter with floating levels
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'Nonlinear Kalman filter'}, 'levels': [], 'description': ['Nonlinear Kalman filter with floating levels'], 'name': 'Nonlinear Kalman filter (fl)', 'source': 'MQL5 Indicators/Nonlinear Kalman filter - floating levels/Nonlinear Kalman filter (fl).mq5', 'folder': 'Nonlinear Kalman filter - floating levels', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 14, 'label': 'Filter period', 'sinput': False}, {'mql': 'Order', 'py': 'Order', 'param': 'Order', 'type': 'int', 'default': 2, 'label': 'Filter order', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'PreSmooth', 'py': 'PreSmooth', 'param': 'PreSmooth', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'PreSmoothMode', 'py': 'PreSmoothMode', 'param': 'PreSmoothMode', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing MA Mode', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enOrder
ord_1 = 0
ord_2 = 1
ord_3 = 2
_enum('enOrder', {0: 'ord_1', 1: 'ord_2', 2: 'ord_3'})

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
Length = _input('Length', 14)  # Filter period
Order = _input('Order', ord_3)  # Filter order
Price = _input('Price', PRICE_CLOSE)  # Price
PreSmooth = _input('PreSmooth', 3)  # Pre-smoothing period
PreSmoothMode = _input('PreSmoothMode', MODE_LWMA)  # Pre-smoothing MA Mode
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
smoother = Arr(0, 0.0)
ª_maHandle = 0
ª_maPeriod = 0

class CNonLinearKalmanFilter(MqlObject):
    _q_fields = ('m_period', 'm_order', 'm_arraySize', 'm_a', 'm_b', 'm_c', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_order = 0
        self.m_arraySize = 0
        self.m_a = 0.0
        self.m_b = 0.0
        self.m_c = 0.0
        self.m_array = Arr(0, 0, factory=sNonLinearKalmanFilterStruct)
        self.m_period = 1
        self.m_order = 0
        self.m_arraySize = -1
        self.m_a = 0.0
        self.m_b = 0.0
        self.m_c = 0.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, order):
        self.m_period = (period if (period > 0) else 1)
        self.m_order = order
        self.m_arraySize = -1
        _sw1 = self.m_order
        if _sw1 == 0:
            self.m_a = _fdiv(2.0, 1 + self.m_period)
        elif _sw1 == 1:
            self.m_a = MathExp(_fdiv((-MathSqrt(2)) * M_PI, self.m_period))
            self.m_b = 2 * self.m_a * MathCos(_fdiv(MathSqrt(2) * M_PI, self.m_period))
        else:
            self.m_a = MathExp(_fdiv(-M_PI, self.m_period))
            self.m_b = 2 * self.m_a * MathCos(_fdiv(MathSqrt(3) * M_PI, self.m_period))
            self.m_c = MathExp(_fdiv(-2 * M_PI, self.m_period))
        return True
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        detrend = 0.0
        _sw2 = self.m_order
        if _sw2 == 0:
            if i > 0:
                self.m_array[i].lowpass = ((1 - self.m_a) * self.m_array[i - 1].lowpass) + (self.m_a * price)
                detrend = price - self.m_array[i].lowpass
                self.m_array[i].delta = ((1 - self.m_a) * self.m_array[i - 1].delta) + (self.m_a * detrend)
            else:
                self.m_array[i].lowpass = price
                self.m_array[i].delta = 0.0
        elif _sw2 == 1:
            if i > 1:
                self.m_array[i].lowpass = (self.m_b * self.m_array[i - 1].lowpass) - (self.m_a * self.m_a * self.m_array[i - 2].lowpass) + ((1 - self.m_b + (self.m_a * self.m_a)) * price)
                detrend = price - self.m_array[i].lowpass
                self.m_array[i].delta = (self.m_b * self.m_array[i - 1].delta) - (self.m_a * self.m_a * self.m_array[i - 2].delta) + ((1 - self.m_b + (self.m_a * self.m_a)) * detrend)
            else:
                self.m_array[i].lowpass = price
                self.m_array[i].delta = 0.0
        else:
            if i > 2:
                self.m_array[i].lowpass = ((self.m_b + self.m_c) * self.m_array[i - 1].lowpass) - ((self.m_c + (self.m_b * self.m_c)) * self.m_array[i - 2].lowpass) + (self.m_c * self.m_c * self.m_array[i - 3].lowpass) + ((1 - self.m_b + self.m_c) * (1 - self.m_c) * price)
                detrend = price - self.m_array[i].lowpass
                self.m_array[i].delta = ((self.m_b + self.m_c) * self.m_array[i - 1].delta) - ((self.m_c + (self.m_b * self.m_c)) * self.m_array[i - 2].delta) + (self.m_c * self.m_c * self.m_array[i - 3].delta) + ((1 - self.m_b + self.m_c) * (1 - self.m_c) * detrend)
            else:
                self.m_array[i].lowpass = price
                self.m_array[i].delta = 0.0
        return self.m_array[i].lowpass + self.m_array[i].delta

class sNonLinearKalmanFilterStruct(MqlObject):
    _q_fields = ('lowpass', 'delta')
    def __init__(self, *args):
        self.lowpass = 0.0
        self.delta = 0.0

def OnInit():
    global ª_maHandle, ª_maPeriod
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, smoother, INDICATOR_CALCULATIONS)
    ª_maPeriod = (PreSmooth if (PreSmooth > 0) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, PreSmoothMode, Price)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    iKalman.init(Length, Order)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, smoother) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if smoother[i] == EMPTY_VALUE:
            smoother[i] = getPrice(Price, open, close, high, low, i)
        val[i] = iKalman.calculate(smoother[i], i, rates_total)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpFlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
            _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpFlLevelUp * range_)
        levd[i] = min_ + (inpFlLevelDn * range_)
        levm[i] = (levu[i] + levd[i]) / 2
        _sw3 = inpColorChange
        if _sw3 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw3 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw3 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
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

def getPrice(tprice, open, close, high, low, i):
    _sw4 = tprice
    if _sw4 == PRICE_CLOSE:
        return close[i]
    elif _sw4 == PRICE_OPEN:
        return open[i]
    elif _sw4 == PRICE_HIGH:
        return high[i]
    elif _sw4 == PRICE_LOW:
        return low[i]
    elif _sw4 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw4 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw4 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- global variables initialised from expressions
iKalman = _alloc(CNonLinearKalmanFilter)
iKalman.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonlinearKalmanFilterFl(_MQL5Indicator):
    name = 'Nonlinear Kalman filter (fl)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 14,  # Filter period
        'Order': _Choice({0: 'First order (EMA)', 1: 'Second order', 2: 'Third order'}, default=2),  # Filter order
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'PreSmooth': 3,  # Pre-smoothing period
        'PreSmoothMode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Pre-smoothing MA Mode
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color changing mode
    }

