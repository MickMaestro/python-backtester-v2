"""CCI (double smoothed Wilders EMA)(zl) — converted from MQL5: MQL5 Indicators/Smoothed CCI/CCI (double smoothed Wilders EMA)(zl).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: "CCI of ds Wilder's EMA"}, 'levels': [], 'description': [], 'name': 'CCI (double smoothed Wilders EMA)(zl)', 'source': 'MQL5 Indicators/Smoothed CCI/CCI (double smoothed Wilders EMA)(zl).mq5', 'folder': 'Smoothed CCI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpEmaPeriod', 'py': 'inpEmaPeriod', 'param': 'inpEmaPeriod', 'type': 'int', 'default': 14, 'label': "Wilder's EMA period", 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # CCI period
inpEmaPeriod = _input('inpEmaPeriod', 14)  # Wilder's EMA period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ema1 = Arr(0, 0.0)
ema2 = Arr(0, 0.0)
_alpha = 0.0

class CCci(MqlObject):
    _q_fields = ('m_array', 'm_period', 'm_arraySize')
    def __init__(self):
        self.m_array = Arr(0, 0, factory=sCciWork)
        self.m_period = 0
        self.m_arraySize = 0
        self.m_period = 1
        self.m_arraySize = -1
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 0) else 1)
        return
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].value = value
        self.m_array[i].value2 = value * value
        if i > self.m_period:
            self.m_array[i].summ = self.m_array[i - 1].summ + self.m_array[i].value - self.m_array[i - self.m_period].value
            self.m_array[i].summ2 = self.m_array[i - 1].summ2 + self.m_array[i].value2 - self.m_array[i - self.m_period].value2
        else:
            self.m_array[i].summ = self.m_array[i].value
            self.m_array[i].summ2 = self.m_array[i].value2
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].summ += self.m_array[i - k].value
                self.m_array[i].summ2 += self.m_array[i - k].value2
                k += 1
        _avg = _fdiv(self.m_array[i].summ, float(self.m_period))
        _dev = MathSqrt(_fdiv(self.m_array[i].summ2 - (self.m_array[i].summ * _avg), float(self.m_period)))
        return (_fdiv(value - _avg, 0.015 * _dev) if (_dev != 0) else 0)

class sCciWork(MqlObject):
    _q_fields = ('value', 'value2', 'summ', 'summ2')
    def __init__(self, *args):
        self.value = 0.0
        self.value2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ema1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ema2, INDICATOR_CALCULATIONS)
    _workCci.init(inpPeriod)
    _alpha = _fdiv(1.0, MathSqrt((inpEmaPeriod if (inpEmaPeriod > 1) else 1)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI std based (' + _str(inpPeriod) + ")(ds Wilder's EMA " + _str(inpEmaPeriod) + ' smoothed)')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if i > 0:
            ema1[i] = ema1[i - 1] + (_alpha * (_price - ema1[i - 1]))
            ema2[i] = ema2[i - 1] + (_alpha * (ema1[i] - ema2[i - 1]))
        else:
            ema2[i] = _price
            ema1[i] = ema2[i]
        val[i] = _workCci.calculate(ema2[i], i, rates_total)
        valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return rates_total

# ---- global variables initialised from expressions
_workCci = _alloc(CCci)
_workCci.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIDoubleSmoothedWildersEMAZl(_MQL5Indicator):
    name = 'CCI (double smoothed Wilders EMA)(zl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # CCI period
        'inpEmaPeriod': 14,  # Wilder's EMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
    }

