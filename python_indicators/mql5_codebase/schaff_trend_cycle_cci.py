"""Schaff trend cycle - CCI — converted from MQL5: MQL5 Indicators/Schaff trend cycle CCI/Schaff trend cycle - CCI.mq5

Schaff trend cycle - of CCI
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Schaff trend cycle CCI'}, 'levels': [], 'description': ['Schaff trend cycle - of CCI'], 'name': 'Schaff trend cycle - CCI', 'source': 'MQL5 Indicators/Schaff trend cycle CCI/Schaff trend cycle - CCI.mq5', 'folder': 'Schaff trend cycle CCI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Schaff period', 'sinput': False}, {'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'double', 'default': 10.0, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Schaff period
inpCciPeriod = _input('inpCciPeriod', 50)  # CCI period
inpSmoothPeriod = _input('inpSmoothPeriod', 10.0)  # Smoothing period (<=1 for no smoothing)
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
data = Arr(0, 0.0)
stoch1 = Arr(0, 0.0)
stoch2 = Arr(0, 0.0)
stoch3 = Arr(0, 0.0)
ª_alpha = 0.0
ª_cciHandle = 0

def OnInit():
    global ª_alpha, ª_cciHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, data, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, stoch1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, stoch2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, stoch3, INDICATOR_CALCULATIONS)
    ª_alpha = _fdiv(2.0, 1.0 + (inpSmoothPeriod if (inpSmoothPeriod > 1) else 1))
    ª_cciHandle = iCCI(Symbol(), 0, inpCciPeriod, inpPrice)
    if not _checkHandle(ª_cciHandle, 'CCI'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Schaff trend cycle CCI (' + _str(inpPeriod) + ',' + _str(inpCciPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__highData, _s_OnCalculate__highStoch, _s_OnCalculate__i, _s_OnCalculate__lowData, _s_OnCalculate__lowStoch, _s_OnCalculate__start
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_cciHandle, 0, 0, _copyCount, data) != _copyCount:
        return prev_calculated
    hh = 0.0
    ll = 0.0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if data[i] == EMPTY_VALUE:
            data[i] = 0.0
        if _s_OnCalculate__i != i and inpPeriod > 1:
            _s_OnCalculate__start = i - inpPeriod + 1
            if _s_OnCalculate__start < 0:
                _s_OnCalculate__start = 0
            _s_OnCalculate__lowData = data[ArrayMinimum(data, _s_OnCalculate__start, inpPeriod - 1)]
            _s_OnCalculate__highData = data[ArrayMaximum(data, _s_OnCalculate__start, inpPeriod - 1)]
        ll = (data[i] if (data[i] < _s_OnCalculate__lowData) else _s_OnCalculate__lowData)
        hh = (data[i] if (data[i] > _s_OnCalculate__highData) else _s_OnCalculate__highData)
        stoch1[i] = ((100.0 * _fdiv(data[i] - ll, hh - ll)) if (hh > ll) else stoch1[i - 1] if (i > 0) else 0)
        stoch2[i] = ((stoch2[i - 1] + (ª_alpha * (stoch1[i] - stoch2[i - 1]))) if (i > 0) else stoch1[i])
        if _s_OnCalculate__i != i and inpPeriod > 1:
            _s_OnCalculate__lowStoch = stoch2[ArrayMinimum(stoch2, _s_OnCalculate__start, inpPeriod - 1)]
            _s_OnCalculate__highStoch = stoch2[ArrayMaximum(stoch2, _s_OnCalculate__start, inpPeriod - 1)]
            _s_OnCalculate__i = i
        ll = (stoch2[i] if (stoch2[i] < _s_OnCalculate__lowStoch) else _s_OnCalculate__lowStoch)
        hh = (stoch2[i] if (stoch2[i] > _s_OnCalculate__highStoch) else _s_OnCalculate__highStoch)
        stoch3[i] = ((100.0 * _fdiv(stoch2[i] - ll, hh - ll)) if (hh > ll) else stoch3[i - 1] if (i > 0) else 0)
        val[i] = ((val[i - 1] + (ª_alpha * (stoch3[i] - val[i - 1]))) if (i > 0) else stoch3[i])
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s_OnCalculate__i = -1
_s_OnCalculate__start = 0
_s_OnCalculate__lowData = 0.0
_s_OnCalculate__highData = 0.0
_s_OnCalculate__lowStoch = 0.0
_s_OnCalculate__highStoch = 0.0
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SchaffTrendCycleCCI(_MQL5Indicator):
    name = 'Schaff trend cycle - CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Schaff period
        'inpCciPeriod': 50,  # CCI period
        'inpSmoothPeriod': 10.0,  # Smoothing period (<=1 for no smoothing)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
    }

