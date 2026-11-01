"""Average trend — converted from MQL5: MQL5 Indicators/Average trend/Average trend.mq5

average trend
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Average trend'}, 'levels': [], 'description': ['average trend'], 'name': 'Average trend', 'source': 'MQL5 Indicators/Average trend/Average trend.mq5', 'folder': 'Average trend', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 35, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpAcceleration', 'py': 'inpAcceleration', 'param': 'inpAcceleration', 'type': 'double', 'default': 1.05, 'label': 'Acceleration factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 35)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpAcceleration = _input('inpAcceleration', 1.05)  # Acceleration factor
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
trend = Arr(0, 0.0)
step = Arr(0, 0.0)
_maHandle = 0

def OnInit():
    global _maHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, avg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, step, INDICATOR_CALCULATIONS)
    _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(_maHandle, 'average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Average (' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5) + ') trend (' + _str(inpMaPeriod) + ',' + _str(inpAcceleration) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if i > 0:
            trend[i] = (1 if (avg[i] > avg[i - 1]) else -1 if (avg[i] < avg[i - 1]) else trend[i - 1])
            step[i] = (0.01 if (trend[i] != trend[i - 1]) else (step[i - 1] * inpAcceleration))
            val[i] = val[i - 1] + (trend[i] * step[i])
        else:
            trend[i] = 0.0
            step[i] = 0.01
            val[i] = 0.0
        valc[i] = (1 if (trend[i] == 1) else 2 if (trend[i] == -1) else 0)
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
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageTrend(_MQL5Indicator):
    name = 'Average trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 35,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpAcceleration': 1.05,  # Acceleration factor
    }

