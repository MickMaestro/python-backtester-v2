"""TRIX (fast) — converted from MQL5: MQL5 Indicators/TRIX (fast EMA)/TRIX (fast).mq5

Triple Exponential Average using fast ema version
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [6908265, 7451452, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'TRIX'}, 'levels': [], 'description': ['Triple Exponential Average using fast ema version'], 'name': 'TRIX (fast)', 'source': 'MQL5 Indicators/TRIX (fast EMA)/TRIX (fast).mq5', 'folder': 'TRIX (fast EMA)', 'inputs': [{'mql': 'inpPeriodEma', 'py': 'inpPeriodEma', 'param': 'inpPeriodEma', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodEma = _input('inpPeriodEma', 14)  # EMA period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CTrix(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sTrixStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_alpha = _fdiv(2.0, 2.0 + ((self.m_period - 1.0) / 2.0))
        return True
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].ema1 = self.m_array[i - 1].ema1 + (self.m_alpha * (price - self.m_array[i - 1].ema1))
            self.m_array[i].ema2 = self.m_array[i - 1].ema2 + (self.m_alpha * (self.m_array[i].ema1 - self.m_array[i - 1].ema2))
            self.m_array[i].ema3 = self.m_array[i - 1].ema3 + (self.m_alpha * (self.m_array[i].ema2 - self.m_array[i - 1].ema3))
            return _fdiv(self.m_array[i].ema3 - self.m_array[i - 1].ema3, self.m_array[i].ema3)
        else:
            self.m_array[i].ema3 = price
            self.m_array[i].ema2 = self.m_array[i].ema3
            self.m_array[i].ema1 = self.m_array[i].ema2
        return 0.0

class sTrixStruct(MqlObject):
    _q_fields = ('price', 'ema1', 'ema2', 'ema3')
    def __init__(self, *args):
        self.price = 0.0
        self.ema1 = 0.0
        self.ema2 = 0.0
        self.ema3 = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iTrix.init(inpPeriodEma)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRIX (fast EMA)(' + _str(inpPeriodEma) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        val[i] = iTrix.calculate(price[i], i, rates_total)
        valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        i += 1
    return rates_total

# ---- global variables initialised from expressions
iTrix = _alloc(CTrix)
iTrix.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TRIXFast(_MQL5Indicator):
    name = 'TRIX (fast)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriodEma': 14,  # EMA period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

