"""PdfMA awesome oscillator — converted from MQL5: MQL5 Indicators/PdfMA awesome oscillator/PdfMA awesome oscillator.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 7451452, 42495, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'PdfMA awesome oscillator'}, 'levels': [], 'description': [], 'name': 'PdfMA awesome oscillator', 'source': 'MQL5 Indicators/PdfMA awesome oscillator/PdfMA awesome oscillator.mq5', 'folder': 'PdfMA awesome oscillator', 'inputs': [{'mql': 'inpVariance', 'py': 'inpVariance', 'param': 'inpVariance', 'type': 'double', 'default': 2.0, 'label': 'Variance', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVariance = _input('inpVariance', 2.0)  # Variance
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class cPdfMa(MqlObject):
    _q_fields = ('m_period', 'm_arraysize', 'm_work', 'm_coeffs', 'm_coeffw')
    def __init__(self):
        self.m_period = 0
        self.m_arraysize = 0
        self.m_work = Arr(0, 0.0)
        self.m_coeffs = Arr(0, 0.0)
        self.m_coeffw = 0.0
        self.init_3(1, 1.0, 0.0)
    def _q_dtor(self):
        pass
    def init_2(self, period, variance):
        self.init_3(period, variance, 0.0)
    def init_3(self, period, variance, mean):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraysize = self.m_period + 32
        self.m_coeffw = 0.0
        ArrayResize(self.m_work, self.m_arraysize)
        ArrayInitialize(self.m_work, 0)
        ArrayResize(self.m_coeffs, self.m_period)
        if variance < 0.01:
            variance = 0.01
        if mean < -1:
            mean = -1.0
        if mean > 1:
            mean = 1.0
        if self.m_period > 1:
            step = _fdiv(3.5, self.m_period - 1)
            for i in range(0, self.m_period):
                self.m_coeffs[i] = _fdiv(1.0, MathSqrt(2 * M_PI * variance * variance)) * MathExp(_fdiv(-(((i * step) - (mean * 3.5)) * ((i * step) - (mean * 3.5))), 2 * variance * variance))
                self.m_coeffw += self.m_coeffs[i]
        else:
            self.m_coeffw = 1.0
            self.m_coeffs[0] = self.m_coeffw
    def calculate(self, price, i):
        _indC = _imod(i, self.m_arraysize)
        self.m_work[_indC] = price
        _avg = 0.0
        k = 0
        while k < self.m_period:
            if _indC < 0:
                _indC += self.m_arraysize
            _avg += self.m_work[_indC] * self.m_coeffs[k]
            k += 1
            _indC -= 1
        return _fdiv(_avg, self.m_coeffw)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iPdfMaFast.init_2(5, inpVariance)
    iPdfMaSlow.init_2(34, inpVariance)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PdfMA AO (' + _str(inpVariance) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = (high[i] + low[i]) / 2.0
        val[i] = iPdfMaFast.calculate(_price, i) - iPdfMaSlow.calculate(_price, i)
        valc[i] = (((0 if (val[i] > val[i - 1]) else 1) if (val[i] > 0) else 2 if (val[i] < val[i - 1]) else 3) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iPdfMaFast = _alloc(cPdfMa)
iPdfMaFast.__init__()
iPdfMaSlow = _alloc(cPdfMa)
iPdfMaSlow.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PdfMAAwesomeOscillator(_MQL5Indicator):
    name = 'PdfMA awesome oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVariance': 2.0,  # Variance
    }

