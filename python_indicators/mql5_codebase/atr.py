"""ATR — converted from MQL5: MQL5 Indicators/ATR/ATR.mq5

ATR without approximation
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ATR'}, 'levels': [], 'description': ['ATR without approximation'], 'name': 'ATR', 'source': 'MQL5 Indicators/ATR/ATR.mq5', 'folder': 'ATR', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 14)  # ATR period
val = Arr(0, 0.0)

class CAtr(MqlObject):
    _q_fields = ('m_period', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_period = 0
        self.m_array = Arr(0, 0, factory=sAtrStruct)
        self.m_arraySize = 0
        self.m_period = 1
        self.m_arraySize = -1
        return
    def _q_dtor(self):
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
    def calculate(self, high, low, close, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        t_high = ((high[i] if (high[i] > close[i - 1]) else close[i - 1]) if (i > 0) else high[i])
        t_low = ((low[i] if (low[i] < close[i - 1]) else close[i - 1]) if (i > 0) else low[i])
        self.m_array[i].tr = t_high - t_low
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum - self.m_array[i - self.m_period].tr + self.m_array[i].tr
        else:
            self.m_array[i].sum = self.m_array[i].tr
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sum += self.m_array[i - k].tr
                k += 1
        return _fdiv(self.m_array[i].sum, float(self.m_period))

class sAtrStruct(MqlObject):
    _q_fields = ('tr', 'sum')
    def __init__(self, *args):
        self.tr = 0.0
        self.sum = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    iAtr.init(inpAtrPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR (' + _str(inpAtrPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        val[i] = iAtr.calculate(high, low, close, i, rates_total)
        i += 1
    return i

# ---- global variables initialised from expressions
iAtr = _alloc(CAtr)
iAtr.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATR(_MQL5Indicator):
    name = 'ATR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAtrPeriod': 14,  # ATR period
    }

