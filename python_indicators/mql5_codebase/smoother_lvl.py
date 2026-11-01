"""Smoother (lvl) — converted from MQL5: MQL5 Indicators/Smoother levels/Smoother (lvl).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'DSMA'}, 'levels': [], 'description': [], 'name': 'Smoother (lvl)', 'source': 'MQL5 Indicators/Smoother levels/Smoother (lvl).mq5', 'folder': 'Smoother levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 27, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 27)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)

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
    def calculate(self, value, i, bars, copy=False):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            if copy:
                self.m_array[i].l0 = self.m_array[i - 1].l0
                self.m_array[i].l1 = self.m_array[i - 1].l1
                self.m_array[i].l2 = self.m_array[i - 1].l2
                self.m_array[i].l3 = self.m_array[i - 1].l3
                self.m_array[i].l4 = self.m_array[i - 1].l4
            else:
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
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    iSmoother.init(inpPeriod)
    iSmootherUp.init(inpPeriod)
    iSmootherDn.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoother levels (' + _str(inpPeriod) + ')')

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
        val[i] = iSmoother.calculate(_price, i, rates_total, False)
        levelUp[i] = iSmootherUp.calculate(val[i], i, rates_total, ((not (val[i] > levelDn[i - 1])) if (i > 0) else False))
        levelDn[i] = iSmootherDn.calculate(val[i], i, rates_total, ((not (val[i] < levelUp[i - 1])) if (i > 0) else False))
        valc[i] = (1 if (val[i] >= levelUp[i]) else 2 if (val[i] <= levelDn[i]) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iSmoother = _alloc(CSmoother)
iSmoother.__init__()
iSmootherUp = _alloc(CSmoother)
iSmootherUp.__init__()
iSmootherDn = _alloc(CSmoother)
iSmootherDn.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmootherLvl(_MQL5Indicator):
    name = 'Smoother (lvl)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 27,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

