"""Rex (extended) — converted from MQL5: MQL5 Indicators/Rex (extended)/Rex (extended).mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 7, 3: 1, 4: 1}, 'colors': {1: [12903679], 2: [10025880], 3: [36095], 4: [11119017]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Uper DC', 2: 'Lower DC', 3: 'Rex', 4: 'Rex signal'}, 'levels': [], 'description': [], 'name': 'Rex (extended)', 'source': 'MQL5 Indicators/Rex (extended)/Rex (extended).mq5', 'folder': 'Rex (extended)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'uint', 'default': 14, 'label': 'Rex period', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 0, 'label': 'Rex method', 'sinput': False}, {'mql': 'inpPeriodSig', 'py': 'inpPeriodSig', 'param': 'inpPeriodSig', 'type': 'uint', 'default': 14, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpMethodSig', 'py': 'inpMethodSig', 'param': 'inpMethodSig', 'type': 'int', 'default': 0, 'label': 'Signal method', 'sinput': False}, {'mql': 'inpDcPeriod', 'py': 'inpDcPeriod', 'param': 'inpDcPeriod', 'type': 'uint', 'default': 89, 'label': 'Donchian channel period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Rex period
inpMethod = _input('inpMethod', MODE_SMA)  # Rex method
inpPeriodSig = _input('inpPeriodSig', 14)  # Signal period
inpMethodSig = _input('inpMethodSig', MODE_SMA)  # Signal method
inpDcPeriod = _input('inpDcPeriod', 89)  # Donchian channel period
val = Arr(0, 0.0)
sig = Arr(0, 0.0)
dcuph = Arr(0, 0.0)
dcupl = Arr(0, 0.0)
dcdnh = Arr(0, 0.0)
dcdnl = Arr(0, 0.0)
rexAverage = None
sigAverage = None

class sdataStruct(MqlObject):
    _q_fields = ('value', 'valueSum')
    def __init__(self, *args):
        self.value = 0.0
        self.valueSum = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('data',)
    def __init__(self, *args):
        self.data = Arr(2, 0, dyn=False, factory=sdataStruct)

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
    global rexAverage, sigAverage
    SetIndexBuffer(0, dcuph, INDICATOR_DATA)
    SetIndexBuffer(1, dcupl, INDICATOR_DATA)
    SetIndexBuffer(2, dcdnh, INDICATOR_DATA)
    SetIndexBuffer(3, dcdnl, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, sig, INDICATOR_DATA)
    _sw1 = inpMethod
    if _sw1 == MODE_SMA:
        rexAverage = iSma
    elif _sw1 == MODE_EMA:
        rexAverage = iEma
    elif _sw1 == MODE_SMMA:
        rexAverage = iSmma
    elif _sw1 == MODE_LWMA:
        rexAverage = iLwma
    _sw2 = inpMethodSig
    if _sw2 == MODE_SMA:
        sigAverage = iSma
    elif _sw2 == MODE_EMA:
        sigAverage = iEma
    elif _sw2 == MODE_SMMA:
        sigAverage = iSmma
    elif _sw2 == MODE_LWMA:
        sigAverage = iLwma
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Rex (%i %s,%i %s, %i)', inpPeriod, StringSubstr(EnumToString(inpMethod, 'ENUM_MA_METHOD'), 5), inpPeriodSig, StringSubstr(EnumToString(inpMethodSig, 'ENUM_MA_METHOD'), 5), inpDcPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(_limit, rates_total):
        _rexPrice = (3.0 * close[i]) - (low[i] + open[i] + high[i])
        val[i] = rexAverage(_rexPrice, inpPeriod, i, rates_total, 0)
        sig[i] = sigAverage(val[i], inpPeriodSig, i, rates_total, 1)
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
        else:
            dcdnl[i] = EMPTY_VALUE
            dcdnh[i] = dcdnl[i]
            dcupl[i] = dcdnh[i]
            dcuph[i] = dcupl[i]
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


class RexExtended(_MQL5Indicator):
    name = 'Rex (extended)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Rex period
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Rex method
        'inpPeriodSig': 14,  # Signal period
        'inpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal method
        'inpDcPeriod': 89,  # Donchian channel period
    }

