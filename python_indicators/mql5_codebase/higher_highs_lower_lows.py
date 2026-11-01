"""Higher Highs & Lower Lows — converted from MQL5: MQL5 Indicators/Higher Highs & Lower Lows Stochastic/Higher Highs & Lower Lows.mq5

Higher Highs & Lower Lows
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [15466475, 15461375], 2: [7451452], 3: [17919]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Fill zone', 2: 'HH value', 3: 'LL value'}, 'levels': [], 'description': ['Higher Highs & Lower Lows'], 'name': 'Higher Highs & Lower Lows', 'source': 'MQL5 Indicators/Higher Highs & Lower Lows Stochastic/Higher Highs & Lower Lows.mq5', 'folder': 'Higher Highs & Lower Lows Stochastic', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
valhh = Arr(0, 0.0)
valll = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
ª_alpha = 0.0

class cMinMax(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'prevbar', 'currmin', 'currmax', 'prevmax', 'prevmin', 'minArray', 'maxArray')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.prevbar = 0
        self.currmin = 0.0
        self.currmax = 0.0
        self.prevmax = 0.0
        self.prevmin = 0.0
        self.minArray = Arr(0, 0.0)
        self.maxArray = Arr(0, 0.0)
        self.prevbar = INT_MIN
        self.originalPeriod = self.prevbar
        return
    def _q_dtor(self):
        ArrayFree(self.minArray)
        ArrayFree(self.maxArray)
        return
    def calculate(self, valueMin, valueMax, forPeriod, min_, max_, i):
        if self.prevbar != i:
            self.prevbar = i
            if self.originalPeriod != forPeriod:
                self.originalPeriod = forPeriod
                self.period = (forPeriod if (forPeriod > 0) else 1)
                self.prevmin = valueMin
                self.prevmax = valueMax
                self.currmin = valueMin
                self.currmax = valueMax
                ArrayResize(self.minArray, self.period - 1)
                ArrayInitialize(self.minArray, valueMin)
                ArrayResize(self.maxArray, self.period - 1)
                ArrayInitialize(self.maxArray, valueMax)
            if self.period > 1:
                _pos = _imod(i, self.period - 1)
                self.minArray[_pos] = self.currmin
                self.maxArray[_pos] = self.currmax
                self.prevmin = self.minArray[ArrayMinimum(self.minArray)]
                self.prevmax = self.maxArray[ArrayMaximum(self.maxArray)]
            else:
                self.prevmin = valueMin
                self.prevmax = valueMax
        self.currmin = valueMin
        self.currmax = valueMax
        max_.v = (self.prevmax if (self.prevmax > valueMax) else valueMax)
        min_.v = (self.prevmin if (self.prevmin < valueMin) else valueMin)
        return

def OnInit():
    global ª_alpha
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valhh, INDICATOR_DATA)
    SetIndexBuffer(3, valll, INDICATOR_DATA)
    ª_alpha = _fdiv(2.0, inpPeriod + 1.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Higher Highs & Lower Lows (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = prev_calculated - 1
    if start < 0:
        start = 0
    for i in range(start, rates_total):
        _hhmin = Box(0.0)
        _hhmax = Box(0.0)
        _llmin = Box(0.0)
        _llmax = Box(0.0)
        _hhMinMax.calculate(high[i], high[i], inpPeriod, _hhmin, _hhmax, i)
        _llMinMax.calculate(low[i], low[i], inpPeriod, _llmin, _llmax, i)
        if i > 0:
            _hhval = (_fdiv(100 * (high[i] - _hhmin.v), _hhmax.v - _hhmin.v) if (high[i] > high[i - 1]) else 0)
            _llval = (_fdiv(100 * (_llmax.v - low[i]), _llmax.v - _llmin.v) if (low[i] < low[i - 1]) else 0)
            fillu[i] = valhh[i - 1] + (ª_alpha * (_hhval - valhh[i - 1]))
            valhh[i] = fillu[i]
            filld[i] = valll[i - 1] + (ª_alpha * (_llval - valll[i - 1]))
            valll[i] = filld[i]
        else:
            valll[i] = 0.0
            valhh[i] = valll[i]
    return rates_total

# ---- global variables initialised from expressions
_hhMinMax = _alloc(cMinMax)
_hhMinMax.__init__()
_llMinMax = _alloc(cMinMax)
_llMinMax.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HigherHighsLowerLows(_MQL5Indicator):
    name = 'Higher Highs & Lower Lows'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
    }

