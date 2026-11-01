"""Elegant oscillator — converted from MQL5: MQL5 Indicators/Elegant oscillator/Elegant oscillator.mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9639167]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Elegant oscillator'}, 'levels': [], 'description': [], 'name': 'Elegant oscillator', 'source': 'MQL5 Indicators/Elegant oscillator/Elegant oscillator.mq5', 'folder': 'Elegant oscillator', 'inputs': [{'mql': 'inpBandEdge', 'py': 'inpBandEdge', 'param': 'inpBandEdge', 'type': 'int', 'default': 20, 'label': 'Band edge', 'sinput': False}, {'mql': 'inpOscillatorPeriod', 'py': 'inpOscillatorPeriod', 'param': 'inpOscillatorPeriod', 'type': 'int', 'default': 50, 'label': 'Oscillator period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBandEdge = _input('inpBandEdge', 20)  # Band edge
inpOscillatorPeriod = _input('inpOscillatorPeriod', 50)  # Oscillator period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('bandEdge', 'oscillatorPeriod', 'sc1', 'sc2', 'sc3')
    def __init__(self, *args):
        self.bandEdge = 0
        self.oscillatorPeriod = 0
        self.sc1 = 0.0
        self.sc2 = 0.0
        self.sc3 = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('price', 'deriv', 'deriv2', 'derivSum2', 'ifish')
    def __init__(self, *args):
        self.price = 0.0
        self.deriv = 0.0
        self.deriv2 = 0.0
        self.derivSum2 = 0.0
        self.ifish = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    global_.bandEdge = MathMax(inpBandEdge, 1)
    global_.oscillatorPeriod = MathMax(inpOscillatorPeriod, 1)
    a1 = MathExp(_fdiv(-1.414 * M_PI, global_.bandEdge))
    b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, global_.bandEdge))
    global_.sc2 = b1
    global_.sc3 = (-a1) * a1
    global_.sc1 = 1.0 - global_.sc2 - global_.sc3
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Elegant oscillator (%i,%i)', inpBandEdge, inpOscillatorPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize <= rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _s_OnCalculate_m_work[i].price = iGetPrice(inpPrice, open[i], high[i], low[i], close[i])
        _s_OnCalculate_m_work[i].deriv = ((_s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - 2].price) if (i > 1) else (_s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[0].price))
        _s_OnCalculate_m_work[i].deriv2 = _s_OnCalculate_m_work[i].deriv * _s_OnCalculate_m_work[i].deriv
        if i > global_.oscillatorPeriod:
            _s_OnCalculate_m_work[i].derivSum2 = _s_OnCalculate_m_work[i - 1].derivSum2 + _s_OnCalculate_m_work[i].deriv2 - _s_OnCalculate_m_work[i - global_.oscillatorPeriod].deriv2
        else:
            _s_OnCalculate_m_work[i].derivSum2 = _s_OnCalculate_m_work[i].deriv2
            k = 1
            while k < global_.oscillatorPeriod and i >= k:
                _s_OnCalculate_m_work[i].derivSum2 += _s_OnCalculate_m_work[i - k].deriv2
                k += 1
        _rms = MathSqrt(_fdiv(_s_OnCalculate_m_work[i].derivSum2, float(global_.oscillatorPeriod)))
        _s_OnCalculate_m_work[i].ifish = (_fdiv(MathExp(2.0 * _fdiv(_s_OnCalculate_m_work[i].deriv, _rms)) - 1.0, MathExp(2.0 * _fdiv(_s_OnCalculate_m_work[i].deriv, _rms)) + 1.0) if _rms else 0)
        val[i] = ((((global_.sc1 * (_s_OnCalculate_m_work[i].ifish + _s_OnCalculate_m_work[i - 1].ifish)) / 2.0) + (global_.sc2 * val[i - 1]) + (global_.sc3 * val[i - 2])) if (i > 1) else 0)
    return rates_total

def iGetPrice(price, open, high, low, close):
    _sw1 = price
    if _sw1 == PRICE_CLOSE:
        return close
    elif _sw1 == PRICE_OPEN:
        return open
    elif _sw1 == PRICE_HIGH:
        return high
    elif _sw1 == PRICE_LOW:
        return low
    elif _sw1 == PRICE_MEDIAN:
        return (high + low) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high + low + close) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high + low + close + close) / 4.0
    return 0.0

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ElegantOscillator(_MQL5Indicator):
    name = 'Elegant oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBandEdge': 20,  # Band edge
        'inpOscillatorPeriod': 50,  # Oscillator period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

