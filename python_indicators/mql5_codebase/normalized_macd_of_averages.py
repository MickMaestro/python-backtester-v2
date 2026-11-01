"""Normalized MACD (of averages) — converted from MQL5: MQL5 Indicators/Normalized MACD - of averages/Normalized MACD (of averages).mq5

Normalized smoother MACD
Copyright: © mladen, 2019; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Normalized MACD'}, 'levels': [], 'description': ['Normalized smoother MACD'], 'name': 'Normalized MACD (of averages)', 'source': 'MQL5 Indicators/Normalized MACD - of averages/Normalized MACD (of averages).mq5', 'folder': 'Normalized MACD - of averages', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 2, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpNormPeriod', 'py': 'inpNormPeriod', 'param': 'inpNormPeriod', 'type': 'int', 'default': 50, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpMaMethod = _input('inpMaMethod', MODE_SMMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpNormPeriod = _input('inpNormPeriod', 50)  # Normalization period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
macd = Arr(0, 0.0)
mafast = Arr(0, 0.0)
maslow = Arr(0, 0.0)
_normPeriod = 0
_macdFastHandle = 0
_macdSlowHandle = 0

def OnInit():
    global _macdFastHandle, _macdSlowHandle, _normPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, macd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, mafast, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, maslow, INDICATOR_CALCULATIONS)
    _normPeriod = ((inpNormPeriod - 1) if (inpNormPeriod > 1) else 1)
    _macdFastHandle = iMA(Symbol(), 0, inpFastPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(_macdFastHandle, 'Fast average'):
        return INIT_FAILED
    _macdSlowHandle = iMA(Symbol(), 0, inpSlowPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(_macdSlowHandle, 'Slow average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Normalized MACD of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5) + ' (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ')(' + _str(inpNormPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_macdFastHandle, 0, 0, _copyCount, mafast) != _copyCount:
        return prev_calculated
    if CopyBuffer(_macdSlowHandle, 0, 0, _copyCount, maslow) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        macd[i] = mafast[i] - maslow[i]
        if _s_OnCalculate_prev_i != i:
            _start = i - inpNormPeriod + 1
            if _start < 0:
                _start = 0
            _s_OnCalculate_prev_max = macd[ArrayMaximum(macd, _start, _normPeriod)]
            _s_OnCalculate_prev_min = macd[ArrayMinimum(macd, _start, _normPeriod)]
            _s_OnCalculate_prev_i = i
        max_ = (macd[i] if (macd[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (macd[i] if (macd[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        val[i] = 0.0
        if macd[i] > 0 and max_ != 0:
            val[i] = _fdiv(macd[i], max_)
        if macd[i] < 0 and min_ != 0:
            val[i] = _fdiv(macd[i], MathAbs(min_))
        valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
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
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedMACDOfAverages(_MQL5Indicator):
    name = 'Normalized MACD (of averages)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpNormPeriod': 50,  # Normalization period
    }

