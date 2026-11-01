"""Rsi swings — converted from MQL5: MQL5 Indicators/RSI swings/Rsi swings.mq5

RSI swings
Copyright: © mladen 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsi'}, 'levels': [], 'description': ['RSI swings'], 'name': 'Rsi swings', 'source': 'MQL5 Indicators/RSI swings/Rsi swings.mq5', 'folder': 'RSI swings', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelUp1', 'py': 'inpLevelUp1', 'param': 'inpLevelUp1', 'type': 'double', 'default': 70.0, 'label': 'Level up 1', 'sinput': False}, {'mql': 'inpLevelUp2', 'py': 'inpLevelUp2', 'param': 'inpLevelUp2', 'type': 'double', 'default': 60.0, 'label': 'Level up 2', 'sinput': False}, {'mql': 'inpLevelDn2', 'py': 'inpLevelDn2', 'param': 'inpLevelDn2', 'type': 'double', 'default': 40.0, 'label': 'Level down 2', 'sinput': False}, {'mql': 'inpLevelDn1', 'py': 'inpLevelDn1', 'param': 'inpLevelDn1', 'type': 'double', 'default': 30.0, 'label': 'Level down 1', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 32)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevelUp1 = _input('inpLevelUp1', 70.0)  # Level up 1
inpLevelUp2 = _input('inpLevelUp2', 60.0)  # Level up 2
inpLevelDn2 = _input('inpLevelDn2', 40.0)  # Level down 2
inpLevelDn1 = _input('inpLevelDn1', 30.0)  # Level down 1
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
rsi = Arr(0, 0.0)
ª_rsiHandle = 0
ª_maHandle = 0
ª_rsiPeriod = 0

def OnInit():
    global ª_maHandle, ª_rsiHandle, ª_rsiPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, rsi, INDICATOR_CALCULATIONS)
    ª_rsiPeriod = (inpRsiPeriod if (inpRsiPeriod > 1) else 1)
    ª_maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maHandle, 'average'):
        return INIT_FAILED
    ª_rsiHandle = iRSI(Symbol(), 0, ª_rsiPeriod, ª_maHandle)
    if not _checkHandle(ª_rsiHandle, 'RSI'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI swings (' + _str(inpRsiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_rsiHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if rsi[i] == EMPTY_VALUE:
            rsi[i] = 0.0
        valc[i] = (valc[i - 1] if (i > 0) else 0)
        if rsi[i] < inpLevelDn2 and valc[i] == 1:
            valc[i] = 0.0
        if rsi[i] > inpLevelUp2 and valc[i] == 2:
            valc[i] = 0.0
        if rsi[i] > inpLevelUp1:
            valc[i] = 1.0
        if rsi[i] < inpLevelDn1:
            valc[i] = 2.0
        val[i] = (1 if (valc[i] == 1) else -1 if (valc[i] == 2) else 0)
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


class RsiSwings(_MQL5Indicator):
    name = 'Rsi swings'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpMaPeriod': 32,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelUp1': 70.0,  # Level up 1
        'inpLevelUp2': 60.0,  # Level up 2
        'inpLevelDn2': 40.0,  # Level down 2
        'inpLevelDn1': 30.0,  # Level down 1
    }

