"""Trend detection index (of averages) — converted from MQL5: MQL5 Indicators/Trend detection index/Trend detection index (of averages).mq5

Trend detection index of average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16760576, 6333684], 2: [16760576], 3: [6333684]}, 'widths': {2: 0, 3: 0}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Trend detection index level up', 3: 'Trend detection index level down'}, 'levels': [], 'description': ['Trend detection index of average'], 'name': 'Trend detection index (of averages)', 'source': 'MQL5 Indicators/Trend detection index/Trend detection index (of averages).mq5', 'folder': 'Trend detection index', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 5, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'inpAvgMethod', 'py': 'inpAvgMethod', 'param': 'inpAvgMethod', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 15)  # Period
inpAvgPeriod = _input('inpAvgPeriod', 5)  # Pre-smoothing period
inpAvgMethod = _input('inpAvgMethod', MODE_LWMA)  # Pre-smoothing method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
ª_avgHandle = 0
ª_maPeriod = 0
ª_periodx2 = 0

class sTdiStruct(MqlObject):
    _q_fields = ('mom', 'abs', 'sum_mom', 'sum_abs', 'sum_abs2')
    def __init__(self, *args):
        self.mom = 0.0
        self.abs = 0.0
        self.sum_mom = 0.0
        self.sum_abs = 0.0
        self.sum_abs2 = 0.0

def OnInit():
    global ª_avgHandle, ª_maPeriod, ª_periodx2
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, valu, INDICATOR_DATA)
    SetIndexBuffer(3, vald, INDICATOR_DATA)
    SetIndexBuffer(4, avg, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else 1)
    ª_avgHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpAvgMethod, inpPrice)
    if not _checkHandle(ª_avgHandle, ª_maNames[inpAvgMethod]):
        return INIT_FAILED
    ª_periodx2 = inpPeriod * 2
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend detection index ' + ª_maNames[inpAvgMethod] + ' (' + _str(inpPeriod) + ',' + _str(ª_maPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_avgHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(_s_OnCalculate_m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if avg[i] == EMPTY_VALUE:
            avg[i] = close[i]
        prev_i = i - inpPeriod
        if prev_i < 0:
            prev_i = 0
        _s_OnCalculate_m_array[i].mom = avg[i] - avg[prev_i]
        _s_OnCalculate_m_array[i].abs = (_s_OnCalculate_m_array[i].mom if (_s_OnCalculate_m_array[i].mom > 0) else (-_s_OnCalculate_m_array[i].mom))
        if i > ª_periodx2:
            _s_OnCalculate_m_array[i].sum_mom = _s_OnCalculate_m_array[i - 1].sum_mom + _s_OnCalculate_m_array[i].mom - _s_OnCalculate_m_array[i - inpPeriod].mom
            _s_OnCalculate_m_array[i].sum_abs = _s_OnCalculate_m_array[i - 1].sum_abs + _s_OnCalculate_m_array[i].abs - _s_OnCalculate_m_array[i - inpPeriod].abs
            _s_OnCalculate_m_array[i].sum_abs2 = _s_OnCalculate_m_array[i - 1].sum_abs2 + _s_OnCalculate_m_array[i].abs - _s_OnCalculate_m_array[i - ª_periodx2].abs
        else:
            _s_OnCalculate_m_array[i].sum_mom = _s_OnCalculate_m_array[i].mom
            _s_OnCalculate_m_array[i].sum_abs2 = _s_OnCalculate_m_array[i].abs
            _s_OnCalculate_m_array[i].sum_abs = _s_OnCalculate_m_array[i].sum_abs2
            k = 1
            while k < ª_periodx2 and i >= k:
                _s_OnCalculate_m_array[i].sum_abs2 += _s_OnCalculate_m_array[i - k].abs
                if k < inpPeriod:
                    _s_OnCalculate_m_array[i].sum_mom += _s_OnCalculate_m_array[i - k].mom
                    _s_OnCalculate_m_array[i].sum_abs += _s_OnCalculate_m_array[i - k].abs
                k += 1
        fup[i] = _s_OnCalculate_m_array[i].sum_mom
        valu[i] = fup[i]
        fdn[i] = MathAbs(_s_OnCalculate_m_array[i].sum_mom) + _s_OnCalculate_m_array[i].sum_abs - _s_OnCalculate_m_array[i].sum_abs2
        vald[i] = fdn[i]
        i += 1
    return i

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
_s_OnCalculate_m_array = Arr(0, 0, factory=sTdiStruct)
_s_OnCalculate_m_arraySize = -1
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendDetectionIndexOfAverages(_MQL5Indicator):
    name = 'Trend detection index (of averages)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 15,  # Period
        'inpAvgPeriod': 5,  # Pre-smoothing period
        'inpAvgMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Pre-smoothing method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

