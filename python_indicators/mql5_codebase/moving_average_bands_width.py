"""Moving Average Bands Width — converted from MQL5: MQL5 Indicators/Moving Average Bands Width/Moving Average Bands Width.mq5

Moving Average Bands Width
Based on work published by Vitali Apirine
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [12632256], 2: [11119017, 255]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Minimum', 2: 'Bands width'}, 'levels': [], 'description': ['Moving Average Bands Width', 'Based on work published by Vitali Apirine'], 'name': 'Moving Average Bands Width', 'source': 'MQL5 Indicators/Moving Average Bands Width/Moving Average Bands Width.mq5', 'folder': 'Moving Average Bands Width', 'inputs': [{'mql': 'inpPeriodSlow', 'py': 'inpPeriodSlow', 'param': 'inpPeriodSlow', 'type': 'double', 'default': 50.0, 'label': 'Slow/minimums period', 'sinput': False}, {'mql': 'inpPeriodFast', 'py': 'inpPeriodFast', 'param': 'inpPeriodFast', 'type': 'double', 'default': 10.0, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpBandMultiplier', 'py': 'inpBandMultiplier', 'param': 'inpBandMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Bands multiplier', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodSlow = _input('inpPeriodSlow', 50.0)  # Slow/minimums period
inpPeriodFast = _input('inpPeriodFast', 10.0)  # Fast period
inpBandMultiplier = _input('inpBandMultiplier', 1.0)  # Bands multiplier
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
min_ = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('periodSum', 'periodMin', 'periodDiv', 'alphaFast', 'alphaSlow')
    def __init__(self, *args):
        self.periodSum = 0
        self.periodMin = 0
        self.periodDiv = 0.0
        self.alphaFast = 0.0
        self.alphaSlow = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('emaFast', 'emaSlow', 'emaDiff', 'sumDiff')
    def __init__(self, *args):
        self.emaFast = 0.0
        self.emaSlow = 0.0
        self.emaDiff = 0.0
        self.sumDiff = 0.0

def OnInit():
    SetIndexBuffer(0, min_, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    _fast = MathMin(inpPeriodFast, inpPeriodSlow)
    _slow = MathMax(inpPeriodFast, inpPeriodSlow)
    global_.alphaFast = _fdiv(2.0, 1.0 + MathMax(_fast, 1))
    global_.alphaSlow = _fdiv(2.0, 1.0 + MathMax(_slow, 1))
    global_.periodMin = _int(MathMax(_slow, 1))
    global_.periodSum = _int(MathMax(_fast, 1))
    global_.periodDiv = MathMax(_fast, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('MABV (%.1f,%.1f multiplier %.2f)', _slow, _fast, inpBandMultiplier))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _price = iGetPrice(inpPrice, open, high, low, close, i)
        _s_OnCalculate_m_work[i].emaFast = ((_s_OnCalculate_m_work[i - 1].emaFast + (global_.alphaFast * (_price - _s_OnCalculate_m_work[i - 1].emaFast))) if (i > 0) else _price)
        _s_OnCalculate_m_work[i].emaSlow = ((_s_OnCalculate_m_work[i - 1].emaSlow + (global_.alphaSlow * (_price - _s_OnCalculate_m_work[i - 1].emaSlow))) if (i > 0) else _price)
        _s_OnCalculate_m_work[i].emaDiff = (_s_OnCalculate_m_work[i].emaFast - _s_OnCalculate_m_work[i].emaSlow) * (_s_OnCalculate_m_work[i].emaFast - _s_OnCalculate_m_work[i].emaSlow)
        if i > global_.periodSum:
            _s_OnCalculate_m_work[i].sumDiff = _s_OnCalculate_m_work[i - 1].sumDiff + _s_OnCalculate_m_work[i].emaDiff - _s_OnCalculate_m_work[i - global_.periodSum].emaDiff
        else:
            _s_OnCalculate_m_work[i].sumDiff = _s_OnCalculate_m_work[i].emaDiff
            k = 1
            while k < global_.periodSum and i >= k:
                _s_OnCalculate_m_work[i].sumDiff += _s_OnCalculate_m_work[i - k].emaDiff
                k += 1
        _dv = _fdiv(_s_OnCalculate_m_work[i].sumDiff, global_.periodDiv)
        _deviation = ((MathSqrt(_dv) * inpBandMultiplier) if _dv else 0)
        _start = i - global_.periodMin + 1
        if _start < 0:
            _start = 0
        val[i] = _fdiv(2.0 * _deviation, _s_OnCalculate_m_work[i].emaSlow)
        min_[i] = val[ArrayMinimum(val, _start, global_.periodMin)]
        valc[i] = (1 if (val[i] == min_[i]) else 0)
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


class MovingAverageBandsWidth(_MQL5Indicator):
    name = 'Moving Average Bands Width'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriodSlow': 50.0,  # Slow/minimums period
        'inpPeriodFast': 10.0,  # Fast period
        'inpBandMultiplier': 1.0,  # Bands multiplier
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

