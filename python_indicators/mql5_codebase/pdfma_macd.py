"""PdfMA MACD — converted from MQL5: MQL5 Indicators/PdfMA MACD/PdfMA MACD.mq5

Probability Density Funcion based MA MACD
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [11119017], 2: [9662683]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': ['Probability Density Funcion based MA MACD'], 'name': 'PdfMA MACD', 'source': 'MQL5 Indicators/PdfMA MACD/PdfMA MACD.mq5', 'folder': 'PdfMA MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpVariance', 'py': 'inpVariance', 'param': 'inpVariance', 'type': 'double', 'default': 1.0, 'label': 'Variance', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # Fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # Slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpVariance = _input('inpVariance', 1.0)  # Variance
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
macd = Arr(0, 0.0)
signal = Arr(0, 0.0)

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
    SetIndexBuffer(0, macd, INDICATOR_DATA)
    SetIndexBuffer(1, signal, INDICATOR_DATA)
    iPdfMaFast.init_2(inpFastPeriod, inpVariance)
    iPdfMaSlow.init_2(inpSlowPeriod, inpVariance)
    iPdfMaSignal.init_2(inpSignalPeriod, inpVariance)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Pdf MA MACD (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')(' + _str(inpVariance) + ')')
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
        macd[i] = iPdfMaFast.calculate(_price, i) - iPdfMaSlow.calculate(_price, i)
        signal[i] = iPdfMaSignal.calculate(macd[i], i)
        i += 1
    return i

# ---- global variables initialised from expressions
iPdfMaFast = _alloc(cPdfMa)
iPdfMaFast.__init__()
iPdfMaSlow = _alloc(cPdfMa)
iPdfMaSlow.__init__()
iPdfMaSignal = _alloc(cPdfMa)
iPdfMaSignal.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PdfMAMACD(_MQL5Indicator):
    name = 'PdfMA MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # Fast period
        'inpSlowPeriod': 26,  # Slow period
        'inpSignalPeriod': 9,  # Signal period
        'inpVariance': 1.0,  # Variance
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

