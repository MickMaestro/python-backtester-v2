"""MyRsi with NET — converted from MQL5: MQL5 Indicators/MyRsi with NET/MyRsi with NET.mq5

MyRsi with Noise Elimination Technology
Based on work published by John Ehlers
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16760576], 2: [11119017]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MyRsi', 2: 'NET'}, 'levels': [], 'description': ['MyRsi with Noise Elimination Technology', 'Based on work published by John Ehlers'], 'name': 'MyRsi with NET', 'source': 'MQL5 Indicators/MyRsi with NET/MyRsi with NET.mq5', 'folder': 'MyRsi with NET', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'MyRsi period', 'sinput': False}, {'mql': 'inpNetPeriod', 'py': 'inpNetPeriod', 'param': 'inpNetPeriod', 'type': 'int', 'default': 14, 'label': 'NET period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # MyRsi period
inpNetPeriod = _input('inpNetPeriod', 14)  # NET period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
net = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('periodNet', 'periodRsi', 'netDenom')
    def __init__(self, *args):
        self.periodNet = 0
        self.periodRsi = 0
        self.netDenom = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('price', 'diffUp', 'diffDn', 'diffUpSum', 'diffDnSum')
    def __init__(self, *args):
        self.price = 0.0
        self.diffUp = 0.0
        self.diffDn = 0.0
        self.diffUpSum = 0.0
        self.diffDnSum = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, net, INDICATOR_DATA)
    global_.periodRsi = MathMax(inpRsiPeriod, 1)
    global_.periodNet = MathMax(inpNetPeriod, 2)
    global_.netDenom = 0.5 * global_.periodNet * (global_.periodNet - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('MyRsi (%i) with (%i) NET', global_.periodRsi, global_.periodNet))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _s_OnCalculate_m_work[i].price = iGetPrice(inpPrice, open, high, low, close, i)
        _diff = ((_s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - 1].price) if (i > 0) else 0)
        _s_OnCalculate_m_work[i].diffUp = (_diff if (_diff > 0) else 0)
        _s_OnCalculate_m_work[i].diffDn = ((-_diff) if (_diff < 0) else 0)
        if i > global_.periodRsi:
            _s_OnCalculate_m_work[i].diffUpSum = _s_OnCalculate_m_work[i - 1].diffUpSum + _s_OnCalculate_m_work[i].diffUp - _s_OnCalculate_m_work[i - global_.periodRsi].diffUp
            _s_OnCalculate_m_work[i].diffDnSum = _s_OnCalculate_m_work[i - 1].diffDnSum + _s_OnCalculate_m_work[i].diffDn - _s_OnCalculate_m_work[i - global_.periodRsi].diffDn
        else:
            _s_OnCalculate_m_work[i].diffUpSum = _s_OnCalculate_m_work[i].diffUp
            _s_OnCalculate_m_work[i].diffDnSum = _s_OnCalculate_m_work[i].diffDn
            k = 1
            while k < global_.periodRsi and i >= k:
                _s_OnCalculate_m_work[i].diffUpSum += _s_OnCalculate_m_work[i - k].diffUp
                _s_OnCalculate_m_work[i].diffDnSum += _s_OnCalculate_m_work[i - k].diffDn
                k += 1
        _diffSum = _s_OnCalculate_m_work[i].diffUpSum + _s_OnCalculate_m_work[i].diffDnSum
        val[i] = (_fdiv(_s_OnCalculate_m_work[i].diffUpSum - _s_OnCalculate_m_work[i].diffDnSum, _diffSum) if _diffSum else 0)
        _netNum = 0.0
        k = 1
        while k < global_.periodNet and i > k:
            for j in range(0, k):
                _diff = val[i - k - 1] - val[i - j - 1]
                _netNum -= (1 if (_diff > 0) else -1)
            k += 1
        net[i] = _fdiv(_netNum, global_.netDenom)
    return rates_total

def iGetPrice(price, open, high, low, close, i):
    _sw1 = price
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
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


class MyRsiWithNET(_MQL5Indicator):
    name = 'MyRsi with NET'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # MyRsi period
        'inpNetPeriod': 14,  # NET period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

