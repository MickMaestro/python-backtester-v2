"""Sma with NET — converted from MQL5: MQL5 Indicators/Sma with NET/Sma with NET.mq5

SMA with Noise Elimination Technology
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'SMA'}, 'levels': [], 'description': ['SMA with Noise Elimination Technology'], 'name': 'Sma with NET', 'source': 'MQL5 Indicators/Sma with NET/Sma with NET.mq5', 'folder': 'Sma with NET', 'inputs': [{'mql': 'inpSmaPeriod', 'py': 'inpSmaPeriod', 'param': 'inpSmaPeriod', 'type': 'int', 'default': 14, 'label': 'SMA period', 'sinput': False}, {'mql': 'inpNetPeriod', 'py': 'inpNetPeriod', 'param': 'inpNetPeriod', 'type': 'int', 'default': 5, 'label': 'NET period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSmaPeriod = _input('inpSmaPeriod', 14)  # SMA period
inpNetPeriod = _input('inpNetPeriod', 5)  # NET period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('periodNet', 'periodSma', 'netDenom')
    def __init__(self, *args):
        self.periodNet = 0
        self.periodSma = 0
        self.netDenom = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('price', 'sum')
    def __init__(self, *args):
        self.price = 0.0
        self.sum = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    global_.periodSma = MathMax(inpSmaPeriod, 1)
    global_.periodNet = MathMax(inpNetPeriod, 2)
    global_.netDenom = 0.5 * global_.periodNet * (global_.periodNet - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Sma (%i) with (%i) NET', global_.periodSma, global_.periodNet))
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
        if i > global_.periodSma:
            _s_OnCalculate_m_work[i].sum = _s_OnCalculate_m_work[i - 1].sum + _s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - global_.periodSma].price
        else:
            _s_OnCalculate_m_work[i].sum = _s_OnCalculate_m_work[i].price
            k = 1
            while k < global_.periodSma and i >= k:
                _s_OnCalculate_m_work[i].sum += _s_OnCalculate_m_work[i - k].price
                k += 1
        val[i] = _fdiv(_s_OnCalculate_m_work[i].sum, float(global_.periodSma))
        _netNum = 0.0
        k = 1
        while k < global_.periodNet and i > k:
            for j in range(0, k):
                _diff = val[i - k - 1] - val[i - j - 1]
                _netNum -= (1 if (_diff > 0) else -1 if (_diff < 0) else 0)
            k += 1
        net = _fdiv(_netNum, global_.netDenom)
        valc[i] = (0 if (net > 0) else 1 if (net < 0) else valc[i - 1] if (i > 0) else 0)
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


class SmaWithNET(_MQL5Indicator):
    name = 'Sma with NET'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSmaPeriod': 14,  # SMA period
        'inpNetPeriod': 5,  # NET period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

