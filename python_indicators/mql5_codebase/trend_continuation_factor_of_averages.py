"""Trend continuation factor (of averages) — converted from MQL5: MQL5 Indicators/Trend continuation factor (of average)/Trend continuation factor (of averages).mq5

Trend continuation factor of average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16760576, 6333684], 2: [16760576], 3: [6333684]}, 'widths': {2: 0, 3: 0}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Trend continuation factor level up', 3: 'Trend continuation factor level down'}, 'levels': [], 'description': ['Trend continuation factor of average'], 'name': 'Trend continuation factor (of averages)', 'source': 'MQL5 Indicators/Trend continuation factor (of average)/Trend continuation factor (of averages).mq5', 'folder': 'Trend continuation factor (of average)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 5, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'inpAvgMethod', 'py': 'inpAvgMethod', 'param': 'inpAvgMethod', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

class sTcfStruct(MqlObject):
    _q_fields = ('plus_ch', 'plus_cf', 'minus_ch', 'minus_cf', 'up_dif', 'dn_dif', 'sum_up', 'sum_dn')
    def __init__(self, *args):
        self.plus_ch = 0.0
        self.plus_cf = 0.0
        self.minus_ch = 0.0
        self.minus_cf = 0.0
        self.up_dif = 0.0
        self.dn_dif = 0.0
        self.sum_up = 0.0
        self.sum_dn = 0.0

def OnInit():
    global ª_avgHandle, ª_maPeriod
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, valu, INDICATOR_DATA)
    SetIndexBuffer(3, vald, INDICATOR_DATA)
    SetIndexBuffer(4, avg, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else 1)
    ª_avgHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpAvgMethod, inpPrice)
    if not _checkHandle(ª_avgHandle, ª_maNames[inpAvgMethod]):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend continuation factor ' + ª_maNames[inpAvgMethod] + ' (' + _str(inpPeriod) + ',' + _str(ª_maPeriod) + ')')
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
        if i > 0:
            _roc = avg[i] - avg[i - 1]
            if _roc > 0:
                _s_OnCalculate_m_array[i].plus_ch = _roc
                _s_OnCalculate_m_array[i].plus_cf = _s_OnCalculate_m_array[i].plus_ch + _s_OnCalculate_m_array[i - 1].plus_cf
                _s_OnCalculate_m_array[i].minus_cf = 0.0
                _s_OnCalculate_m_array[i].minus_ch = _s_OnCalculate_m_array[i].minus_cf
            else:
                _s_OnCalculate_m_array[i].minus_ch = -_roc
                _s_OnCalculate_m_array[i].minus_cf = _s_OnCalculate_m_array[i].minus_ch + _s_OnCalculate_m_array[i - 1].minus_cf
                _s_OnCalculate_m_array[i].plus_cf = 0.0
                _s_OnCalculate_m_array[i].plus_ch = _s_OnCalculate_m_array[i].plus_cf
        else:
            _s_OnCalculate_m_array[i].minus_cf = 0.0
            _s_OnCalculate_m_array[i].plus_cf = _s_OnCalculate_m_array[i].minus_cf
            _s_OnCalculate_m_array[i].minus_ch = _s_OnCalculate_m_array[i].plus_cf
            _s_OnCalculate_m_array[i].plus_ch = _s_OnCalculate_m_array[i].minus_ch
        _s_OnCalculate_m_array[i].up_dif = _s_OnCalculate_m_array[i].plus_ch - _s_OnCalculate_m_array[i].minus_cf
        _s_OnCalculate_m_array[i].dn_dif = _s_OnCalculate_m_array[i].minus_ch - _s_OnCalculate_m_array[i].plus_cf
        if i > inpPeriod:
            _s_OnCalculate_m_array[i].sum_up = _s_OnCalculate_m_array[i - 1].sum_up + _s_OnCalculate_m_array[i].up_dif - _s_OnCalculate_m_array[i - inpPeriod].up_dif
            _s_OnCalculate_m_array[i].sum_dn = _s_OnCalculate_m_array[i - 1].sum_dn + _s_OnCalculate_m_array[i].dn_dif - _s_OnCalculate_m_array[i - inpPeriod].dn_dif
        else:
            _s_OnCalculate_m_array[i].sum_up = _s_OnCalculate_m_array[i].up_dif
            _s_OnCalculate_m_array[i].sum_dn = _s_OnCalculate_m_array[i].dn_dif
            k = 1
            while k < inpPeriod and i >= k:
                _s_OnCalculate_m_array[i].sum_up += _s_OnCalculate_m_array[i - k].up_dif
                _s_OnCalculate_m_array[i].sum_dn += _s_OnCalculate_m_array[i - k].dn_dif
                k += 1
        fup[i] = ((-_s_OnCalculate_m_array[i].sum_dn) if (_s_OnCalculate_m_array[i].sum_up > _s_OnCalculate_m_array[i].sum_dn) else _s_OnCalculate_m_array[i].sum_up)
        valu[i] = fup[i]
        fdn[i] = ((-_s_OnCalculate_m_array[i].sum_dn) if (_s_OnCalculate_m_array[i].sum_up < _s_OnCalculate_m_array[i].sum_dn) else _s_OnCalculate_m_array[i].sum_up)
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
_s_OnCalculate_m_array = Arr(0, 0, factory=sTcfStruct)
_s_OnCalculate_m_arraySize = -1
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendContinuationFactorOfAverages(_MQL5Indicator):
    name = 'Trend continuation factor (of averages)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 15,  # Period
        'inpAvgPeriod': 5,  # Pre-smoothing period
        'inpAvgMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Pre-smoothing method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

