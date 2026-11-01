"""TRIX (ds Wilder ema) — converted from MQL5: MQL5 Indicators/TRIX (using double smoothed Wilder's EMA)/TRIX (ds Wilder ema).mq5

Triple Exponential Average using double smoothed Wilder's EMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [6908265, 7451452, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'TRIX'}, 'levels': [], 'description': ["Triple Exponential Average using double smoothed Wilder's EMA"], 'name': 'TRIX (ds Wilder ema)', 'source': "MQL5 Indicators/TRIX (using double smoothed Wilder's EMA)/TRIX (ds Wilder ema).mq5", 'folder': "TRIX (using double smoothed Wilder's EMA)", 'inputs': [{'mql': 'inpPeriodEma', 'py': 'inpPeriodEma', 'param': 'inpPeriodEma', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodEma = _input('inpPeriodEma', 14)  # EMA period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CTrixDsWilders(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sTrixDsWildersStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_alpha = _fdiv(2.0, 1.0 + MathSqrt(self.m_period))
        return True
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].ema10 = self.m_array[i - 1].ema10 + (self.m_alpha * (price - self.m_array[i - 1].ema10))
            self.m_array[i].ema11 = self.m_array[i - 1].ema11 + (self.m_alpha * (self.m_array[i].ema10 - self.m_array[i - 1].ema11))
            self.m_array[i].ema20 = self.m_array[i - 1].ema20 + (self.m_alpha * (self.m_array[i].ema11 - self.m_array[i - 1].ema20))
            self.m_array[i].ema21 = self.m_array[i - 1].ema21 + (self.m_alpha * (self.m_array[i].ema20 - self.m_array[i - 1].ema21))
            self.m_array[i].ema30 = self.m_array[i - 1].ema30 + (self.m_alpha * (self.m_array[i].ema21 - self.m_array[i - 1].ema30))
            self.m_array[i].ema31 = self.m_array[i - 1].ema31 + (self.m_alpha * (self.m_array[i].ema30 - self.m_array[i - 1].ema31))
            return _fdiv(self.m_array[i].ema31 - self.m_array[i - 1].ema31, self.m_array[i].ema31)
        else:
            self.m_array[i].ema31 = price
            self.m_array[i].ema30 = self.m_array[i].ema31
            self.m_array[i].ema21 = self.m_array[i].ema30
            self.m_array[i].ema20 = self.m_array[i].ema21
            self.m_array[i].ema11 = self.m_array[i].ema20
            self.m_array[i].ema10 = self.m_array[i].ema11
        return 0.0

class sTrixDsWildersStruct(MqlObject):
    _q_fields = ('price', 'ema10', 'ema11', 'ema20', 'ema21', 'ema30', 'ema31')
    def __init__(self, *args):
        self.price = 0.0
        self.ema10 = 0.0
        self.ema11 = 0.0
        self.ema20 = 0.0
        self.ema21 = 0.0
        self.ema30 = 0.0
        self.ema31 = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iTrix.init(inpPeriodEma)
    IndicatorSetString(INDICATOR_SHORTNAME, "TRIX (ds Wilder's EMA)(" + _str(inpPeriodEma) + ')')

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
iTrix = _alloc(CTrixDsWilders)
iTrix.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TRIXDsWilderEma(_MQL5Indicator):
    name = 'TRIX (ds Wilder ema)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriodEma': 14,  # EMA period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

