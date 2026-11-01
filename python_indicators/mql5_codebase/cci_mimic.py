"""Cci (mimic) — converted from MQL5: MQL5 Indicators/CCI (mimic)/Cci (mimic).mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [13165000], 2: [12903679], 3: [12632256, 7451452, 3329330, 36095, 42495]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Uper DC', 2: 'Lower DC', 3: 'Cci'}, 'levels': [], 'description': [], 'name': 'Cci (mimic)', 'source': 'MQL5 Indicators/CCI (mimic)/Cci (mimic).mq5', 'folder': 'CCI (mimic)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpPricePeriod', 'py': 'inpPricePeriod', 'param': 'inpPricePeriod', 'type': 'int', 'default': 0, 'label': 'Price smoothing period', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'inpDcPeriod', 'py': 'inpDcPeriod', 'param': 'inpDcPeriod', 'type': 'uint', 'default': 50, 'label': 'Donchian channel period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpPricePeriod = _input('inpPricePeriod', 0)  # Price smoothing period
inpMethod = _input('inpMethod', MODE_SMA)  # Method
inpDcPeriod = _input('inpDcPeriod', 50)  # Donchian channel period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
dcuph = Arr(0, 0.0)
dcupl = Arr(0, 0.0)
dcdnh = Arr(0, 0.0)
dcdnl = Arr(0, 0.0)
cciAverage = None

class sGlobalStruct(MqlObject):
    _q_fields = ('cciPeriod',)
    def __init__(self, *args):
        self.cciPeriod = 0

class sdataStruct(MqlObject):
    _q_fields = ('value', 'valueSum')
    def __init__(self, *args):
        self.value = 0.0
        self.valueSum = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('data',)
    def __init__(self, *args):
        self.data = Arr(3, 0, dyn=False, factory=sdataStruct)

class sdataStruct_iEma(MqlObject):
    _q_fields = ('ema',)
    def __init__(self, *args):
        self.ema = 0.0

class sdataStruct_iSmma(MqlObject):
    _q_fields = ('smma',)
    def __init__(self, *args):
        self.smma = 0.0

class sdataStruct_iLwma(MqlObject):
    _q_fields = ('value',)
    def __init__(self, *args):
        self.value = 0.0

def OnInit():
    global cciAverage
    SetIndexBuffer(0, dcuph, INDICATOR_DATA)
    SetIndexBuffer(1, dcupl, INDICATOR_DATA)
    SetIndexBuffer(2, dcdnh, INDICATOR_DATA)
    SetIndexBuffer(3, dcdnl, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    global_.cciPeriod = MathMax(inpPeriod, 1)
    _sw1 = inpMethod
    if _sw1 == MODE_SMA:
        cciAverage = iSma
    elif _sw1 == MODE_EMA:
        cciAverage = iEma
    elif _sw1 == MODE_SMMA:
        cciAverage = iSmma
    elif _sw1 == MODE_LWMA:
        cciAverage = iLwma
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Cci (%i,%i %s)', inpPeriod, inpPricePeriod, StringSubstr(EnumToString(inpMethod, 'ENUM_MA_METHOD'), 5), inpDcPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(_limit, rates_total):
        _rawPrice = iGetPrice(inpPrice, open, high, low, close, i)
        _price = (cciAverage(_rawPrice, inpPricePeriod, i, rates_total, 0) if (inpPricePeriod > 0) else _rawPrice)
        _priceAvg = cciAverage(_price, global_.cciPeriod, i, rates_total, 1)
        _diff = _price - _priceAvg
        _diffAvg = cciAverage((_diff if (_diff > 0) else (-_diff)), global_.cciPeriod, i, rates_total, 2)
        val[i] = _fdiv(_diff, _diffAvg)
        if inpDcPeriod > 0:
            _start = _int(i - inpDcPeriod)
            if _start < 0:
                _start = 0
            _max = val[ArrayMaximum(val, _start, inpDcPeriod)]
            _min = val[ArrayMinimum(val, _start, inpDcPeriod)]
            dcuph[i] = _max
            dcupl[i] = _max - ((_max - _min) / 5.0)
            dcdnl[i] = _min
            dcdnh[i] = _min + ((_max - _min) / 5.0)
            valc[i] = (2 if (val[i] > dcuph[i]) else 1 if (val[i] > dcupl[i]) else 4 if (val[i] < dcdnl[i]) else 3 if (val[i] < dcdnh[i]) else 0)
        else:
            dcdnl[i] = EMPTY_VALUE
            dcdnh[i] = dcdnl[i]
            dcupl[i] = dcdnh[i]
            dcuph[i] = dcupl[i]
            valc[i] = (1 if (val[i] > 0) else 3 if (val[i] < 0) else 0)
    return rates_total

def iSma(value, period, i, bars, instanceNo=0):
    global _s_iSma_m_workSize
    if _s_iSma_m_workSize < bars:
        _s_iSma_m_workSize = ArrayResize(_s_iSma_m_work, bars + 500, 2000)
    _s_iSma_m_work[i].data[instanceNo].value = value
    if i >= period:
        _s_iSma_m_work[i].data[instanceNo].valueSum = _s_iSma_m_work[i - 1].data[instanceNo].valueSum + _s_iSma_m_work[i].data[instanceNo].value - _s_iSma_m_work[i - period].data[instanceNo].value
    else:
        _s_iSma_m_work[i].data[instanceNo].valueSum = _s_iSma_m_work[i].data[instanceNo].value
        k = 1
        while k < period and i >= k:
            _s_iSma_m_work[i].data[instanceNo].valueSum += _s_iSma_m_work[i - k].data[instanceNo].value
            k += 1
    return (_fdiv(_s_iSma_m_work[i].data[instanceNo].valueSum, float(period)) if (period > 0) else _s_iSma_m_work[i].data[instanceNo].value)

def iEma(value, period, i, bars, instanceNo=0):
    global _s_iEma_m_workSize
    if _s_iEma_m_workSize < bars:
        _s_iEma_m_workSize = ArrayResize(_s_iEma_m_work, bars + 500, 2000)
    _s_iEma_m_work[i].data[instanceNo].ema = ((_s_iEma_m_work[i - 1].data[instanceNo].ema + (_fdiv(2.0, 1.0 + float(period)) * (value - _s_iEma_m_work[i - 1].data[instanceNo].ema))) if (i > 0 and period > 1) else value)
    return _s_iEma_m_work[i].data[instanceNo].ema

def iSmma(value, period, i, bars, instanceNo=0):
    global _s_iSmma_m_workSize
    if _s_iSmma_m_workSize < bars:
        _s_iSmma_m_workSize = ArrayResize(_s_iSmma_m_work, bars + 500, 2000)
    _s_iSmma_m_work[i].data[instanceNo].smma = ((_s_iSmma_m_work[i - 1].data[instanceNo].smma + _fdiv(value - _s_iSmma_m_work[i - 1].data[instanceNo].smma, float(period))) if (i > 0 and period > 1) else value)
    return _s_iSmma_m_work[i].data[instanceNo].smma

def iLwma(value, period, i, bars, instanceNo=0):
    global _s_iLwma_m_workSize
    if _s_iLwma_m_workSize < bars:
        _s_iLwma_m_workSize = ArrayResize(_s_iLwma_m_work, bars + 500, 2000)
    _s_iLwma_m_work[i].data[instanceNo].value = value
    sumw = period
    sum_ = period * _s_iLwma_m_work[i].data[instanceNo].value
    if period > 1:
        k = 1
        while k < period and i >= k:
            weight = period - k
            sumw += weight
            sum_ += weight * _s_iLwma_m_work[i - k].data[instanceNo].value
            k += 1
    else:
        sumw = 1.0
    return _fdiv(sum_, sumw)

def iGetPrice(price, open, high, low, close, i):
    _sw2 = price
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_iSma_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iSma_m_workSize = -1
_s_iEma_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iEma_m_workSize = -1
_s_iSmma_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iSmma_m_workSize = -1
_s_iLwma_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iLwma_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciMimic(_MQL5Indicator):
    name = 'Cci (mimic)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 50,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpPricePeriod': 0,  # Price smoothing period
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'inpDcPeriod': 50,  # Donchian channel period
    }

