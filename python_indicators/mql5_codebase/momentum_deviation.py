"""Momentum deviation — converted from MQL5: MQL5 Indicators/Momentum deviation/Momentum deviation.mq5

deviation variation
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11119017]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Deviation'}, 'levels': [], 'description': ['deviation variation'], 'name': 'Momentum deviation', 'source': 'MQL5 Indicators/Momentum deviation/Momentum deviation.mq5', 'folder': 'Momentum deviation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpMomPeriod', 'py': 'inpMomPeriod', 'param': 'inpMomPeriod', 'type': 'int', 'default': 2, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpMomPrice', 'py': 'inpMomPrice', 'param': 'inpMomPrice', 'type': 'int', 'default': 1, 'label': 'Momentum price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpMomPeriod = _input('inpMomPeriod', 2)  # Momentum period
inpMomPrice = _input('inpMomPrice', PRICE_CLOSE)  # Momentum price
val = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'periodMomentum')
    def __init__(self, *args):
        self.period = 0
        self.periodMomentum = 0

class sWorkStruct(MqlObject):
    _q_fields = ('price', 'momentum', 'momentumSum')
    def __init__(self, *args):
        self.price = 0.0
        self.momentum = 0.0
        self.momentumSum = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    global_.period = MathMax(inpPeriod, 1)
    global_.periodMomentum = MathMax(inpMomPeriod, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Deviation variation (%i,%i)', global_.period, global_.periodMomentum))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _s_OnCalculate_m_work[i].price = iGetPrice(inpMomPrice, open[i], high[i], low[i], close[i])
        _s_OnCalculate_m_work[i].momentum = ((_s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - global_.periodMomentum].price) if (i > global_.periodMomentum) else (_s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[0].price))
        if i > global_.period:
            _s_OnCalculate_m_work[i].momentumSum = _s_OnCalculate_m_work[i - 1].momentumSum + (_s_OnCalculate_m_work[i].momentum * _s_OnCalculate_m_work[i].momentum) - (_s_OnCalculate_m_work[i - global_.period].momentum * _s_OnCalculate_m_work[i - global_.period].momentum)
        else:
            _s_OnCalculate_m_work[i].momentumSum = _s_OnCalculate_m_work[i].momentum * _s_OnCalculate_m_work[i].momentum
            k = 1
            while k < global_.period and i >= k:
                _s_OnCalculate_m_work[i].momentumSum += _s_OnCalculate_m_work[i - k].momentum * _s_OnCalculate_m_work[i - k].momentum
                k += 1
        val[i] = (MathSqrt(_fdiv(_s_OnCalculate_m_work[i].momentumSum, float(global_.period))) if _s_OnCalculate_m_work[i].momentumSum else 0)
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


class MomentumDeviation(_MQL5Indicator):
    name = 'Momentum deviation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpMomPeriod': 2,  # Momentum period
        'inpMomPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Momentum price
    }

