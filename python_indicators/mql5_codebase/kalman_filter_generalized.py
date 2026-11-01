"""Kalman filter (generalized) — converted from MQL5: MQL5 Indicators/Kalman filter - generalized version/Kalman filter (generalized).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Kalman filter'}, 'levels': [], 'description': [], 'name': 'Kalman filter (generalized)', 'source': 'MQL5 Indicators/Kalman filter - generalized version/Kalman filter (generalized).mq5', 'folder': 'Kalman filter - generalized version', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 1.0, 'label': 'Period/smoothing ratio', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 1.0)  # Period/smoothing ratio
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CKalmanFilter(MqlObject):
    _q_fields = ('m_period', 'm_coeff', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_period = 0.0
        self.m_coeff = 0.0
        self.m_array = Arr(0, 0, factory=sKalmanFilter)
        self.m_arraySize = 0
        self.m_arraySize = -1
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_coeff = (period if (period > 0) else 1.0) / 100.0
        self.m_period = MathSqrt(self.m_coeff)
    def calculate(self, value, velocity, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
        if i > 0:
            _distance = value - self.m_array[i - 1].filter
            _error = self.m_array[i - 1].filter + (_distance * self.m_period)
            self.m_array[i].velocity = self.m_array[i - 1].velocity + (_distance * self.m_coeff)
            self.m_array[i].filter = _error + self.m_array[i].velocity
        else:
            self.m_array[i].filter = value
            self.m_array[i].velocity = 0.0
        velocity.v = self.m_array[i].velocity
        return self.m_array[i].filter

class sKalmanFilter(MqlObject):
    _q_fields = ('filter', 'velocity')
    def __init__(self, *args):
        self.filter = 0.0
        self.velocity = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iKalmanFilter.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kalman filter (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _velocity = Box(0.0)
        val[i] = iKalmanFilter.calculate((0 if (price[i] == EMPTY_VALUE) else price[i]), _velocity, i, rates_total)
        valc[i] = (1 if (_velocity.v > 0) else 2 if (_velocity.v < 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iKalmanFilter = _alloc(CKalmanFilter)
iKalmanFilter.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KalmanFilterGeneralized(_MQL5Indicator):
    name = 'Kalman filter (generalized)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 1.0,  # Period/smoothing ratio
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

