"""Filtered averages — converted from MQL5: MQL5 Indicators/Filtered averages/Filtered averages.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 7451452]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Deviation filtered average'}, 'levels': [], 'description': [], 'name': 'Filtered averages', 'source': 'MQL5 Indicators/Filtered averages/Filtered averages.mq5', 'folder': 'Filtered averages', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Average and filter period', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 2.5, 'label': 'Filter size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Average and filter period
inpMethod = _input('inpMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpFilter = _input('inpFilter', 2.5)  # Filter size
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_maHandle = 0
ª_maPeriod = 0

class sFilterArrayStruct(MqlObject):
    _q_fields = ('value', 'change', 'power', 'summc', 'summp')
    def __init__(self, *args):
        self.value = 0.0
        self.change = 0.0
        self.power = 0.0
        self.summc = 0.0
        self.summp = 0.0

def OnInit():
    global ª_maHandle, ª_maPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, avg, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpMethod, inpPrice)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Deviation filtered average (' + _str(inpPeriod) + ',' + _str(inpFilter) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if avg[i] == EMPTY_VALUE:
            avg[i] = close[i]
        val[i] = iFilter(avg[i], inpFilter, inpPeriod, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iFilter(value, filter_, period, i, bars, instance=0):
    global _s_iFilter_m_arraySize
    if _s_iFilter_m_arraySize < bars:
        _res = ArrayResize(_s_iFilter_m_array, bars + 500)
        if _res < bars:
            return 0.0
        _s_iFilter_m_arraySize = _res
    _s_iFilter_m_array[i][instance].value = value
    _change = ((_s_iFilter_m_array[i][instance].value - _s_iFilter_m_array[i - 1][instance].value) if (i > 0) else 0)
    _s_iFilter_m_array[i][instance].change = (_change if (_change > 0) else (-_change))
    if i > period:
        _s_iFilter_m_array[i][instance].summc = _s_iFilter_m_array[i - 1][instance].summc + _s_iFilter_m_array[i][instance].change - _s_iFilter_m_array[i - period][instance].change
        _s_iFilter_m_array[i][instance].power = (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period))) * (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period)))
        _s_iFilter_m_array[i][instance].summp = _s_iFilter_m_array[i - 1][instance].summp + _s_iFilter_m_array[i][instance].power - _s_iFilter_m_array[i - period][instance].power
    else:
        _s_iFilter_m_array[i][instance].summp = 0.0
        _s_iFilter_m_array[i][instance].summc = _s_iFilter_m_array[i][instance].summp
        k = 0
        while k < period and i >= k:
            _s_iFilter_m_array[i][instance].summc += _s_iFilter_m_array[i - k][instance].change
            k += 1
        _s_iFilter_m_array[i][instance].power = (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period))) * (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period)))
        k = 0
        while k < period and i >= k:
            _s_iFilter_m_array[i][instance].summp += _s_iFilter_m_array[i - k][instance].power
            k += 1
    if (i > 0 and filter_ > 0) and _s_iFilter_m_array[i][instance].change < (filter_ * MathSqrt(_fdiv(_s_iFilter_m_array[i][instance].summp, float(period)))):
        _s_iFilter_m_array[i][instance].value = _s_iFilter_m_array[i - 1][instance].value
    return _s_iFilter_m_array[i][instance].value

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s_iFilter_m_array = Arr(0, 0, factory=sFilterArrayStruct, dims=(1,))
_s_iFilter_m_arraySize = 0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FilteredAverages(_MQL5Indicator):
    name = 'Filtered averages'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Average and filter period
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpFilter': 2.5,  # Filter size
    }

