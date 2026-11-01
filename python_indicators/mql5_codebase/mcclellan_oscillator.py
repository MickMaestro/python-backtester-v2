"""McClellan Oscillator — converted from MQL5: MQL5 Indicators/McClellan Oscillator - smoother/McClellan Oscillator.mq5

McClellan Oscillator using \\"smoother\\"
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'McClellan Oscillator'}, 'levels': [], 'description': ['McClellan Oscillator using \\"smoother\\"'], 'name': 'McClellan Oscillator', 'source': 'MQL5 Indicators/McClellan Oscillator - smoother/McClellan Oscillator.mq5', 'folder': 'McClellan Oscillator - smoother', 'inputs': [{'mql': 'inpBaseCurrency', 'py': 'inpBaseCurrency', 'param': None, 'type': 'string', 'default': 'USD', 'label': 'Base currency', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast smoother period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow smoother period', 'sinput': False}, {'mql': 'inpPeriodMultiplier', 'py': 'inpPeriodMultiplier', 'param': 'inpPeriodMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Periods multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBaseCurrency = _input('inpBaseCurrency', 'USD')  # Base currency
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast smoother period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow smoother period
inpPeriodMultiplier = _input('inpPeriodMultiplier', 1.0)  # Periods multiplier
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_symbolsSize = 0

class sSymbolInfo(MqlObject):
    _q_fields = ('name', 'bars', 'inverse')
    def __init__(self, *args):
        self.name = ""
        self.bars = 0
        self.inverse = False

class CSmoother(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_beta', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_beta = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=CSmootherStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
        self.m_beta = 1.0
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_beta = _fdiv(0.45 * (self.m_period - 1.0), (0.45 * (self.m_period - 1)) + 2.0)
        self.m_alpha = self.m_beta * self.m_beta * self.m_beta
        return True
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].l0 = ((1.0 - self.m_alpha) * value) + (self.m_alpha * self.m_array[i - 1].l0)
            self.m_array[i].l1 = ((value - self.m_array[i].l0) * (1 - self.m_beta)) + (self.m_beta * self.m_array[i - 1].l1)
            self.m_array[i].l2 = self.m_array[i].l0 + self.m_array[i].l1
            self.m_array[i].l3 = ((self.m_array[i].l2 - self.m_array[i - 1].l4) * (1.0 - self.m_alpha) * (1.0 - self.m_alpha)) + (self.m_alpha * self.m_alpha * self.m_array[i - 1].l3)
            self.m_array[i].l4 = self.m_array[i - 1].l4 + self.m_array[i].l3
        else:
            self.m_array[i].l4 = value
            self.m_array[i].l1 = self.m_array[i].l4
            self.m_array[i].l0 = self.m_array[i].l1
            self.m_array[i].l3 = 0.0
            self.m_array[i].l2 = self.m_array[i].l3
        return self.m_array[i].l4

class CSmootherStruct(MqlObject):
    _q_fields = ('l0', 'l1', 'l2', 'l3', 'l4')
    def __init__(self, *args):
        self.l0 = 0.0
        self.l1 = 0.0
        self.l2 = 0.0
        self.l3 = 0.0
        self.l4 = 0.0

def OnInit():
    global _symbolsSize
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _totalSymbols = SymbolsTotal(True)
    for i in range(0, _totalSymbols):
        _symbol = SymbolName(i, True)
        _foundAt = StringFind(_symbol, inpBaseCurrency)
        if _foundAt != WRONG_VALUE:
            _symbolsSize = ArrayResize(_symbols, _symbolsSize + 1)
            _symbols[_symbolsSize - 1].name = _symbol
            _symbols[_symbolsSize - 1].inverse = _foundAt > 0
            _symbols[_symbolsSize - 1].bars = 0
    iSmootherFast.init(inpFastPeriod * inpPeriodMultiplier)
    iSmootherSlow.init(inpSlowPeriod * inpPeriodMultiplier)
    IndicatorSetString(INDICATOR_SHORTNAME, 'McClellan ' + inpBaseCurrency + ' oscillator (of ' + _str(_symbolsSize) + ' symbols) (' + _str(inpFastPeriod * inpPeriodMultiplier) + ',' + _str(inpSlowPeriod * inpPeriodMultiplier) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(0, _symbolsSize):
        _symbols[i].bars = iBars(_symbols[i].name, 0)
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _up = 0.0
        _dn = 0.0
        _advancesDeclines = 0.0
        for k in range(0, _symbolsSize):
            _shift = iBarShift(_symbols[k].name, 0, time[i])
            if _shift != WRONG_VALUE:
                _close = iClose(_symbols[k].name, 0, _shift)
                _open = iOpen(_symbols[k].name, 0, _shift)
                if _symbols[k].inverse:
                    if _close < _open:
                        _up += 1
                    if _close > _open:
                        _dn += 1
                else:
                    if _close > _open:
                        _up += 1
                    if _close < _open:
                        _dn += 1
            _advancesDeclines = (_fdiv(_up - _dn, _up + _dn) if ((_up + _dn) != 0) else 0)
        val[i] = iSmootherFast.calculate(_advancesDeclines, i, rates_total) - iSmootherSlow.calculate(_advancesDeclines, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
_symbols = Arr(0, 0, factory=sSymbolInfo)
iSmootherFast = _alloc(CSmoother)
iSmootherFast.__init__()
iSmootherSlow = _alloc(CSmoother)
iSmootherSlow.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class McClellanOscillator(_MQL5Indicator):
    name = 'McClellan Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 19,  # Fast smoother period
        'inpSlowPeriod': 39,  # Slow smoother period
        'inpPeriodMultiplier': 1.0,  # Periods multiplier
    }

