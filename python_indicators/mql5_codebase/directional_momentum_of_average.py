"""Directional momentum of average — converted from MQL5: MQL5 Indicators/Directional smoothed momentum/Directional momentum of average.mq5

Directional momentum of average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Directional momentum of average'}, 'levels': [], 'description': ['Directional momentum of average'], 'name': 'Directional momentum of average', 'source': 'MQL5 Indicators/Directional smoothed momentum/Directional momentum of average.mq5', 'folder': 'Directional smoothed momentum', 'inputs': [{'mql': 'inpMomPeriod', 'py': 'inpMomPeriod', 'param': 'inpMomPeriod', 'type': 'int', 'default': 32, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 14, 'label': 'Average period (<= 1 for no average)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMomPeriod = _input('inpMomPeriod', 32)  # Momentum period
inpMaPeriod = _input('inpMaPeriod', 14)  # Average period (<= 1 for no average)
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ma = Arr(0, 0.0)
ª_maHandle = 0
ª_maPeriod = 0
_momArray = Arr(0, 0.0, dims=(3,))

def OnInit():
    global ª_maHandle, ª_maPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ma, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpMaPeriod if (inpMaPeriod > 0) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maHandle, 'average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Directional momentum of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' (' + _str(inpMomPeriod) + ',' + _str(ª_maPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, ma) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if ma[i] == EMPTY_VALUE:
            ma[i] = 0.0
        val[i] = iDirectionalMomentum(ma[i], inpMomPeriod, ª_maPeriod, i, rates_total)
        valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        i += 1
    return i

def iDirectionalMomentum(price, period, safeCount, i, _bars, instance=0):
    global _s_iDirectionalMomentum__arrayError, _s_iDirectionalMomentum__arrayResizedTo
    if _s_iDirectionalMomentum__arrayResizedTo < _bars:
        _res = _bars + 500
        _res -= ArrayResize(_momArray, _res)
        if _res:
            _s_iDirectionalMomentum__arrayError = True
        else:
            _s_iDirectionalMomentum__arrayResizedTo = _bars + 500
    if _s_iDirectionalMomentum__arrayError:
        return 1.0
    _sumTill = ((2 * safeCount) if ((2 * safeCount) > period) else period)
    _momArray[i][instance] = price
    diff = ((_momArray[i][instance] - _momArray[i - 1][instance]) if (i > 0) else 0)
    _momArray[i][instance + 1] = (diff if (diff > 0) else (-diff))
    if i > _sumTill:
        _momArray[i][instance + 2] = _momArray[i - 1][instance + 2] - _momArray[i - period][instance + 1] + _momArray[i][instance + 1]
    else:
        _momArray[i][instance + 2] = _momArray[i][instance + 1]
        k = 1
        while k < period and i >= k:
            _momArray[i][instance + 2] += _momArray[i - k][instance + 1]
            k += 1
    return ((_momArray[i][instance + 2] if (_momArray[i][instance] > _momArray[i - period][instance]) else (-_momArray[i][instance + 2])) if (i > period) else 0)

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
_s_iDirectionalMomentum__arrayError = False
_s_iDirectionalMomentum__arrayResizedTo = 0
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DirectionalMomentumOfAverage(_MQL5Indicator):
    name = 'Directional momentum of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMomPeriod': 32,  # Momentum period
        'inpMaPeriod': 14,  # Average period (<= 1 for no average)
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

