"""Smoother momentum MACD — converted from MQL5: MQL5 Indicators/Smoother momentum MACD/Smoother momentum MACD.mq5

Smoother momentum MACD
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Smoother momentum MACD'}, 'levels': [], 'description': ['Smoother momentum MACD'], 'name': 'Smoother momentum MACD', 'source': 'MQL5 Indicators/Smoother momentum MACD/Smoother momentum MACD.mq5', 'folder': 'Smoother momentum MACD', 'inputs': [{'mql': 'inpMomPeriodFast', 'py': 'inpMomPeriodFast', 'param': 'inpMomPeriodFast', 'type': 'int', 'default': 12, 'label': 'Fast momentum period', 'sinput': False}, {'mql': 'inpMomPeriodSlow', 'py': 'inpMomPeriodSlow', 'param': 'inpMomPeriodSlow', 'type': 'int', 'default': 50, 'label': 'Slow momentum period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMomPeriodFast = _input('inpMomPeriodFast', 12)  # Fast momentum period
inpMomPeriodSlow = _input('inpMomPeriodSlow', 50)  # Slow momentum period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class cSmoothEmaMomentumCoeffs(MqlObject):
    _q_fields = ('period', 'alphaRegular', 'alphaDouble')
    def __init__(self):
        self.period = 0.0
        self.alphaRegular = 0.0
        self.alphaDouble = 0.0
        self.period = DBL_EPSILON
    def _q_dtor(self):
        pass

class sSmoothEmaMomentumArray(MqlObject):
    _q_fields = ('ema', 'ema21', 'ema22')
    def __init__(self, *args):
        self.ema = 0.0
        self.ema21 = 0.0
        self.ema22 = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoother momentum MACD (' + _str(inpMomPeriodFast) + ',' + _str(inpMomPeriodSlow) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

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
        val[i] = iSmoothMomentum(_price, inpMomPeriodSlow, i, 0) - iSmoothMomentum(_price, inpMomPeriodFast, i, 1)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iSmoothMomentum(price, period, i, instance=0):
    if _s_iSmoothMomentum_m_coeffs[instance].period != period:
        _period = (period if (period > 1) else 1)
        _s_iSmoothMomentum_m_coeffs[instance].period = period
        _s_iSmoothMomentum_m_coeffs[instance].alphaRegular = _fdiv(2.0, 1.0 + _period)
        _s_iSmoothMomentum_m_coeffs[instance].alphaDouble = _fdiv(2.0, 1.0 + MathSqrt(_period))
    _indC = _imod(i, 32)
    if i > 0:
        _indP = _indC - 1
        if _indP < 0:
            _indP += 32
        _s_iSmoothMomentum_m_array[_indC][instance].ema = _s_iSmoothMomentum_m_array[_indP][instance].ema + (_s_iSmoothMomentum_m_coeffs[instance].alphaRegular * (price - _s_iSmoothMomentum_m_array[_indP][instance].ema))
        _s_iSmoothMomentum_m_array[_indC][instance].ema21 = _s_iSmoothMomentum_m_array[_indP][instance].ema21 + (_s_iSmoothMomentum_m_coeffs[instance].alphaDouble * (price - _s_iSmoothMomentum_m_array[_indP][instance].ema21))
        _s_iSmoothMomentum_m_array[_indC][instance].ema22 = _s_iSmoothMomentum_m_array[_indP][instance].ema22 + (_s_iSmoothMomentum_m_coeffs[instance].alphaDouble * (_s_iSmoothMomentum_m_array[_indC][instance].ema21 - _s_iSmoothMomentum_m_array[_indP][instance].ema22))
    else:
        _s_iSmoothMomentum_m_array[_indC][instance].ema22 = price
        _s_iSmoothMomentum_m_array[_indC][instance].ema21 = _s_iSmoothMomentum_m_array[_indC][instance].ema22
        _s_iSmoothMomentum_m_array[_indC][instance].ema = _s_iSmoothMomentum_m_array[_indC][instance].ema21
    return _s_iSmoothMomentum_m_array[_indC][instance].ema22 - _s_iSmoothMomentum_m_array[_indC][instance].ema

# ---- static local variables
_s_iSmoothMomentum_m_coeffs = Arr(2, 0, dyn=False, factory=cSmoothEmaMomentumCoeffs)
_s_iSmoothMomentum_m_array = Arr(32, 0, dyn=False, factory=sSmoothEmaMomentumArray, dims=(2,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmootherMomentumMACD(_MQL5Indicator):
    name = 'Smoother momentum MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMomPeriodFast': 12,  # Fast momentum period
        'inpMomPeriodSlow': 50,  # Slow momentum period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

