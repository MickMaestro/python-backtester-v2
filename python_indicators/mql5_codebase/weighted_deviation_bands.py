"""Weighted deviation bands — converted from MQL5: MQL5 Indicators/Weighted deviation bands/Weighted deviation bands.mq5

Momentum deviation bands
Copyright: © mladen, 2023; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2023', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [11119017], 3: [5275647]}, 'widths': {}, 'styles': {1: 4, 3: 4}, 'labels': {1: 'Upper band', 2: 'Average', 3: 'Lower band'}, 'levels': [], 'description': ['Momentum deviation bands'], 'name': 'Weighted deviation bands', 'source': 'MQL5 Indicators/Weighted deviation bands/Weighted deviation bands.mq5', 'folder': 'Weighted deviation bands', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Deviations', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 30)  # Period
inpMultiplier = _input('inpMultiplier', 2.0)  # Deviations
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
bandup = Arr(0, 0.0)
banddn = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period',)
    def __init__(self, *args):
        self.period = 0

class sCalcStruct(MqlObject):
    _q_fields = ('data', 'dataSize', 'weightSum')
    def __init__(self):
        self.data = Arr(0, 0, factory=sWorkStruct)
        self.dataSize = 0
        self.weightSum = 0.0
        self.dataSize = -1

class sWorkStruct(MqlObject):
    _q_fields = ('value', 'valueSum', 'valueWeightSum')
    def __init__(self, *args):
        self.value = 0.0
        self.valueSum = 0.0
        self.valueWeightSum = 0.0

def OnInit():
    SetIndexBuffer(0, bandup, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, banddn, INDICATOR_DATA)
    global_.period = MathMax(inpPeriod, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Weighted deviation bands (%i,%.2f)', inpPeriod, inpMultiplier))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        _deviation = iDeviationWeighted(iGetPrice(inpPrice, open, high, low, close, i), global_.period, _ElemRef(val, i), i, rates_total)
        bandup[i] = val[i] + (_deviation * inpMultiplier)
        banddn[i] = val[i] - (_deviation * inpMultiplier)
    return rates_total

def iDeviationWeighted(value, period, average, i, bars):
    if _s_iDeviationWeighted_m_work.dataSize <= bars:
        _s_iDeviationWeighted_m_work.dataSize = ArrayResize(_s_iDeviationWeighted_m_work.data, bars + 500, 5000)
    if period < 1:
        period = 1
    _s_iDeviationWeighted_m_work.data[i].value = value
    if i >= period:
        _s_iDeviationWeighted_m_work.data[i].valueSum = _s_iDeviationWeighted_m_work.data[i - 1].valueSum + _s_iDeviationWeighted_m_work.data[i].value - _s_iDeviationWeighted_m_work.data[i - period].value
        _s_iDeviationWeighted_m_work.data[i].valueWeightSum = _s_iDeviationWeighted_m_work.data[i - 1].valueWeightSum - _s_iDeviationWeighted_m_work.data[i - 1].valueSum + (_s_iDeviationWeighted_m_work.data[i].value * float(period))
    else:
        period = i + 1
        _s_iDeviationWeighted_m_work.weightSum = float(period)
        _s_iDeviationWeighted_m_work.data[i].valueWeightSum = float(period) * _s_iDeviationWeighted_m_work.data[i].value
        _s_iDeviationWeighted_m_work.data[i].valueSum = _s_iDeviationWeighted_m_work.data[i].value
        k = 1
        while k < period and i >= k:
            weight = period - k
            _s_iDeviationWeighted_m_work.weightSum += weight
            _s_iDeviationWeighted_m_work.data[i].valueWeightSum += _s_iDeviationWeighted_m_work.data[i - k].value * weight
            _s_iDeviationWeighted_m_work.data[i].valueSum += _s_iDeviationWeighted_m_work.data[i - k].value
            k += 1
    mean = _box_set(average, _fdiv(_s_iDeviationWeighted_m_work.data[i].valueWeightSum, _s_iDeviationWeighted_m_work.weightSum))
    sums = 0.0
    k = 0
    weight = period
    while k < period and i >= k:
        sums += float(weight) * (_s_iDeviationWeighted_m_work.data[i - k].value - mean) * (_s_iDeviationWeighted_m_work.data[i - k].value - mean)
        k += 1
        weight -= 1
    return sqrt(_fdiv(sums, _s_iDeviationWeighted_m_work.weightSum))

def iGetPrice(tprice, open, high, low, close, i):
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
_s_iDeviationWeighted_m_work = sCalcStruct()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WeightedDeviationBands(_MQL5Indicator):
    name = 'Weighted deviation bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 30,  # Period
        'inpMultiplier': 2.0,  # Deviations
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

