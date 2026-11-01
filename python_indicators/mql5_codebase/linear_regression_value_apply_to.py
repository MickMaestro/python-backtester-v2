"""Linear regression value (apply to) — converted from MQL5: MQL5 Indicators/Linear Regression Value (apply to)/Linear regression value (apply to).mq5

Copyright: © mladen, 2024; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2024', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 36095]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Linear regression value'}, 'levels': [], 'description': [], 'name': 'Linear regression value (apply to)', 'source': 'MQL5 Indicators/Linear Regression Value (apply to)/Linear regression value (apply to).mq5', 'folder': 'Linear Regression Value (apply to)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # Period
val = Arr(0, 0.0)
valColor = Arr(0, 0.0)

class sWorkStruct(MqlObject):
    _q_fields = ('data', 'dataSize', 'period', 'sumX', 'sumXX', 'divisor')
    def __init__(self):
        self.data = Arr(0, 0, factory=sDataStruct)
        self.dataSize = 0
        self.period = 0
        self.sumX = 0.0
        self.sumXX = 0.0
        self.divisor = 0.0
        self.dataSize = -1
        self.period = -1

class sDataStruct(MqlObject):
    _q_fields = ('value', 'sumY', 'sumXY')
    def __init__(self, *args):
        self.value = 0.0
        self.sumY = 0.0
        self.sumXY = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valColor, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        _slope = Box(0.0)
        _intercept = Box(0.0)
        _price = (price[i] if (price[i] != EMPTY_VALUE) else 0)
        val[i] = iLinearRegression(_price, inpPeriod, _slope, _intercept, i, rates_total)
        valColor[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valColor[i - 1]) if (i > 0) else 0)
    return rates_total

def iLinearRegression(value, period, _slope, _intercept, r, bars):
    if _s_iLinearRegression_m_work.dataSize <= bars:
        _s_iLinearRegression_m_work.dataSize = ArrayResize(_s_iLinearRegression_m_work.data, bars + 500, 2000)
    if period < 1:
        period = 1.0
    if _s_iLinearRegression_m_work.period != _int(period):
        _s_iLinearRegression_m_work.period = _int(period)
        _s_iLinearRegression_m_work.sumX = (_s_iLinearRegression_m_work.period * (_s_iLinearRegression_m_work.period - 1.0)) / 2.0
        _s_iLinearRegression_m_work.sumXX = (_s_iLinearRegression_m_work.period * (_s_iLinearRegression_m_work.period - 1.0) * ((2.0 * _s_iLinearRegression_m_work.period) - 1.0)) / 6.0
        _s_iLinearRegression_m_work.divisor = (_s_iLinearRegression_m_work.sumX * _s_iLinearRegression_m_work.sumX) - (_s_iLinearRegression_m_work.period * _s_iLinearRegression_m_work.sumXX)
        if _s_iLinearRegression_m_work.divisor:
            _s_iLinearRegression_m_work.divisor = _fdiv(1.0, _s_iLinearRegression_m_work.divisor)
    _s_iLinearRegression_m_work.data[r].value = value
    if r >= _s_iLinearRegression_m_work.period:
        _s_iLinearRegression_m_work.data[r].sumY = _s_iLinearRegression_m_work.data[r - 1].sumY + value - _s_iLinearRegression_m_work.data[r - _s_iLinearRegression_m_work.period].value
        _s_iLinearRegression_m_work.data[r].sumXY = _s_iLinearRegression_m_work.data[r - 1].sumXY + _s_iLinearRegression_m_work.data[r].sumY - (_s_iLinearRegression_m_work.data[r - _s_iLinearRegression_m_work.period].value * (_s_iLinearRegression_m_work.period - 1.0)) - value
    else:
        _s_iLinearRegression_m_work.data[r].sumY = value
        _s_iLinearRegression_m_work.data[r].sumXY = 0.0
        k = 1
        while k < _s_iLinearRegression_m_work.period and r >= k:
            _s_iLinearRegression_m_work.data[r].sumY += _s_iLinearRegression_m_work.data[r - k].value
            _s_iLinearRegression_m_work.data[r].sumXY += k * _s_iLinearRegression_m_work.data[r - k].value
            k += 1
    _slope.v = ((_s_iLinearRegression_m_work.period * _s_iLinearRegression_m_work.data[r].sumXY) - (_s_iLinearRegression_m_work.sumX * _s_iLinearRegression_m_work.data[r].sumY)) * _s_iLinearRegression_m_work.divisor
    _intercept.v = _fdiv(_s_iLinearRegression_m_work.data[r].sumY - (_slope.v * _s_iLinearRegression_m_work.sumX), float(_s_iLinearRegression_m_work.period))
    return _intercept.v + (_slope.v * (_s_iLinearRegression_m_work.period - 1.0))

# ---- static local variables
_s_iLinearRegression_m_work = sWorkStruct()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearRegressionValueApplyTo(_MQL5Indicator):
    name = 'Linear regression value (apply to)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

