"""SmoothStep (generalized) — converted from MQL5: MQL5 Indicators/SmoothStep (generalized)/SmoothStep (generalized).mq5

Copyright: © mladen, 2022; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2022', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'SmoothStep'}, 'levels': [0.2, 0.8], 'description': [], 'name': 'SmoothStep (generalized)', 'source': 'MQL5 Indicators/SmoothStep (generalized)/SmoothStep (generalized).mq5', 'folder': 'SmoothStep (generalized)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'inpOrder', 'py': 'inpOrder', 'param': 'inpOrder', 'type': 'int', 'default': 1, 'label': 'Order', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_lowhigh = 7
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_lowhigh'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Period
inpPrice = _input('inpPrice', pr_close)  # Price
inpOrder = _input('inpOrder', 1)  # Order
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'order')
    def __init__(self, *args):
        self.period = 0
        self.order = 0

class sWorkStruct(MqlObject):
    _q_fields = ('prevBar', 'prevmin', 'prevmax')
    def __init__(self, *args):
        self.prevBar = 0
        self.prevmin = 0.0
        self.prevmax = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    global_.period = MathMax(inpPeriod, 1)
    global_.order = MathMax(MathMin(inpOrder, 16), 0)
    PlotIndexSetString(0, PLOT_LABEL, 'SmoothStep ' + _str(global_.order) + ' order')
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Smooth step (%i, order %i)', global_.period, global_.order))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_highsSize, _s_OnCalculate_m_lowsSize, _s_OnCalculate_m_workSize
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_lowsSize < rates_total:
        _s_OnCalculate_m_lowsSize = ArrayResize(_s_OnCalculate_m_lows, rates_total + 500, 2000)
    if _s_OnCalculate_m_highsSize < rates_total:
        _s_OnCalculate_m_highsSize = ArrayResize(_s_OnCalculate_m_highs, rates_total + 500, 2000)
    if _s_OnCalculate_m_workSize <= rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _price = close[i]
        _priceh = close[i]
        _pricel = close[i]
        _sw1 = inpPrice
        if _sw1 == pr_close:
            _pricel = close[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_open:
            _pricel = open[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_high:
            _pricel = high[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_low:
            _pricel = low[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_median:
            _pricel = (high[i] + low[i]) / 2.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_typical:
            _pricel = (high[i] + low[i] + close[i]) / 3.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_weighted:
            _pricel = (high[i] + low[i] + (close[i] * 2.0)) / 4.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_lowhigh:
            _price = close[i]
            _priceh = high[i]
            _pricel = low[i]
        _s_OnCalculate_m_lows[i] = _pricel
        _s_OnCalculate_m_highs[i] = _priceh
        if _s_OnCalculate_m_work[i].prevBar != i:
            _s_OnCalculate_m_work[i].prevBar = i
            _s_OnCalculate_m_work[i + 1].prevBar = -1
            if i > 0 and global_.period > 1:
                _minMaxPeriod = global_.period - 1
                _start = i - global_.period + 1
                if _start < 0:
                    _start = 0
                    _minMaxPeriod = i + 1
                _s_OnCalculate_m_work[i].prevmin = _s_OnCalculate_m_lows[ArrayMinimum(_s_OnCalculate_m_lows, _start, _minMaxPeriod)]
                _s_OnCalculate_m_work[i].prevmax = _s_OnCalculate_m_highs[ArrayMaximum(_s_OnCalculate_m_highs, _start, _minMaxPeriod)]
            else:
                _s_OnCalculate_m_work[i].prevmin = _s_OnCalculate_m_lows[i]
                _s_OnCalculate_m_work[i].prevmax = _s_OnCalculate_m_highs[i]
        min_ = (_s_OnCalculate_m_work[i].prevmin if (_s_OnCalculate_m_work[i].prevmin < _pricel) else _pricel)
        max_ = (_s_OnCalculate_m_work[i].prevmax if (_s_OnCalculate_m_work[i].prevmax > _priceh) else _priceh)
        raw = (_fdiv(_price - min_, max_ - min_) if (max_ != min_) else 0)
        result = 0.0
        k = 0
        while k <= global_.order:
            result += iPascalTriangle((-global_.order) - 1, k) * iPascalTriangle((2 * global_.order) + 1, global_.order - k) * MathPow(raw, global_.order + k + 1)
            k += 1
        val[i] = MathMin(MathMax(result, 0), 1.0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iPascalTriangle(a, b):
    result = 1.0
    for i in range(0, b):
        result *= _fdiv(a - i, i + 1.0)
    return result

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_lows = Arr(0, 0.0)
_s_OnCalculate_m_lowsSize = -1
_s_OnCalculate_m_highs = Arr(0, 0.0)
_s_OnCalculate_m_highsSize = -1
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothStepGeneralized(_MQL5Indicator):
    name = 'SmoothStep (generalized)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Period
        'inpPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Low/High/Close'}, default=0),  # Price
        'inpOrder': 1,  # Order
    }

