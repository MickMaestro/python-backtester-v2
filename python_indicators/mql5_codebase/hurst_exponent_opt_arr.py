"""Hurst exponent (opt)(arr) — converted from MQL5: MQL5 Indicators/Hurst Exponent - optimized version/Hurst exponent (opt)(arr).mq5

Hurst exponent
Copyright: © mladen, 2023; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2023', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16760576]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Hurst exponent'}, 'levels': [], 'description': ['Hurst exponent'], 'name': 'Hurst exponent (opt)(arr)', 'source': 'MQL5 Indicators/Hurst Exponent - optimized version/Hurst exponent (opt)(arr).mq5', 'folder': 'Hurst Exponent - optimized version', 'inputs': [{'mql': 'inpHurstPeriod', 'py': 'inpHurstPeriod', 'param': 'inpHurstPeriod', 'type': 'int', 'default': 30, 'label': 'Hurst exponent period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpHurstPeriod = _input('inpHurstPeriod', 30)  # Hurst exponent period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'x', 'y', 'logDivisor')
    def __init__(self, *args):
        self.period = 0
        self.x = Arr(0, 0.0)
        self.y = Arr(0, 0.0)
        self.logDivisor = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('value', 'valueSum')
    def __init__(self, *args):
        self.value = 0.0
        self.valueSum = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    global_.period = MathMax(inpHurstPeriod, 1)
    global_.logDivisor = MathLog(global_.period)
    ArrayResize(global_.x, global_.period)
    ArrayInitialize(global_.x, 0)
    ArraySetAsSeries(global_.x, True)
    ArrayResize(global_.y, global_.period)
    ArrayInitialize(global_.y, 0)
    ArraySetAsSeries(global_.y, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hurst exponent (' + _str(inpHurstPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _s_OnCalculate_m_work[i].value = getPrice(inpPrice, open, high, low, close, i)
        if i >= global_.period:
            _s_OnCalculate_m_work[i].valueSum = _s_OnCalculate_m_work[i - 1].valueSum + _s_OnCalculate_m_work[i].value - _s_OnCalculate_m_work[i - global_.period].value
        else:
            _s_OnCalculate_m_work[i].valueSum = _s_OnCalculate_m_work[i].value
            k = 1
            while k < global_.period and i >= k:
                _s_OnCalculate_m_work[i].valueSum += _s_OnCalculate_m_work[i - k].value
                k += 1
        mean = _fdiv(_s_OnCalculate_m_work[i].valueSum, float(global_.period))
        sums = 0.0
        maxY = 0.0
        minY = 0.0
        k = 0
        while k < global_.period and i >= k:
            global_.x[k] = _s_OnCalculate_m_work[i - k].value - mean
            sums += global_.x[k] * global_.x[k]
            if k > 0:
                global_.y[k] = global_.y[k - 1] + global_.x[k]
                if maxY < global_.y[k]:
                    maxY = global_.y[k]
                if minY > global_.y[k]:
                    minY = global_.y[k]
            else:
                global_.y[k] = global_.x[k]
                minY = global_.y[k]
                maxY = minY
            k += 1
        iValue = (_fdiv(maxY - minY, 1.253314 * MathSqrt(_fdiv(sums, float(global_.period)))) if (sums != 0) else 0)
        val[i] = (_fdiv(MathLog(iValue), global_.logDivisor) if (iValue > 0) else 0)
    return rates_total

def getPrice(tprice, open, high, low, close, i):
    _sw1 = tprice
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


class HurstExponentOptArr(_MQL5Indicator):
    name = 'Hurst exponent (opt)(arr)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpHurstPeriod': 30,  # Hurst exponent period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

