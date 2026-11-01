"""Hann filter — converted from MQL5: MQL5 Indicators/Hann filter/Hann filter.mq5

Hann windowing filter
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Hann average'}, 'levels': [], 'description': ['Hann windowing filter'], 'name': 'Hann filter', 'source': 'MQL5 Indicators/Hann filter/Hann filter.mq5', 'folder': 'Hann filter', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSpeedUp', 'py': 'inpSpeedUp', 'param': 'inpSpeedUp', 'type': 'double', 'default': 0.0, 'label': 'Spped up factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSpeedUp = _input('inpSpeedUp', 0.0)  # Spped up factor
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'coeffs', 'coeffsSum')
    def __init__(self, *args):
        self.period = 0
        self.coeffs = Arr(0, 0.0)
        self.coeffsSum = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('price',)
    def __init__(self, *args):
        self.price = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    global_.period = MathMax(inpPeriod, 1)
    global_.coeffsSum = 0.0
    _speedUp = 1.0
    ArrayResize(global_.coeffs, global_.period)
    for i in range(0, global_.period):
        _coeff = 1.0 - MathCos(_fdiv(2.0 * M_PI * (i + 1), global_.period + 1.0))
        global_.coeffs[i] = _fdiv(_coeff, _speedUp)
        global_.coeffsSum += _fdiv(_coeff, _speedUp)
        _speedUp += MathMax(0, inpSpeedUp)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Hann average (%i)', global_.period))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _s_OnCalculate_m_work[i].price = iGetPrice(inpPrice, open[i], high[i], low[i], close[i])
        dSum = 0.0
        k = 0
        while k < global_.period and i >= k:
            dSum += _s_OnCalculate_m_work[i - k].price * global_.coeffs[k]
            k += 1
        val[i] = (_fdiv(dSum, global_.coeffsSum) if (global_.coeffsSum != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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


class HannFilter(_MQL5Indicator):
    name = 'Hann filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSpeedUp': 0.0,  # Spped up factor
    }

