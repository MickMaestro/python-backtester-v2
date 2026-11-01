"""TRIX candles — converted from MQL5: MQL5 Indicators/TRIX candles/TRIX candles.mq5

TRIX candles
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 7451452, 17919]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TRIX'}, 'levels': [], 'description': ['TRIX candles'], 'name': 'TRIX candles', 'source': 'MQL5 Indicators/TRIX candles/TRIX candles.mq5', 'folder': 'TRIX candles', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'TRIX period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # TRIX period
valo = Arr(0, 0.0)
valh = Arr(0, 0.0)
vall = Arr(0, 0.0)
valc = Arr(0, 0.0)
valcl = Arr(0, 0.0)
ª_workVal = Arr(4, 0.0, dyn=False)
ª_valhHandle = 0
ª_vallHandle = 0
ª_valoHandle = 0
ª_valcHandle = 0

def OnInit():
    global ª_valcHandle, ª_valhHandle, ª_vallHandle, ª_valoHandle
    SetIndexBuffer(0, valo, INDICATOR_DATA)
    SetIndexBuffer(1, valh, INDICATOR_DATA)
    SetIndexBuffer(2, vall, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_DATA)
    SetIndexBuffer(4, valcl, INDICATOR_COLOR_INDEX)
    ª_valhHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_HIGH)
    if not _checkHandle(ª_valhHandle, 'TRIX of high'):
        return INIT_FAILED
    ª_vallHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_LOW)
    if not _checkHandle(ª_vallHandle, 'TRIX of low'):
        return INIT_FAILED
    ª_valoHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_OPEN)
    if not _checkHandle(ª_valoHandle, 'TRIX of open'):
        return INIT_FAILED
    ª_valcHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_CLOSE)
    if not _checkHandle(ª_valcHandle, 'TRIX of close'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRIX candles (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_valhHandle, 0, 0, _copyCount, valh) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_vallHandle, 0, 0, _copyCount, vall) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_valoHandle, 0, 0, _copyCount, valo) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_valcHandle, 0, 0, _copyCount, valc) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        ª_workVal[1] = vall[i]
        ª_workVal[0] = valh[i]
        ª_workVal[2] = valo[i]
        ª_workVal[3] = valc[i]
        valh[i] = ª_workVal[ArrayMaximum(ª_workVal)]
        vall[i] = ª_workVal[ArrayMinimum(ª_workVal)]
        valcl[i] = (1 if (valc[i] > valo[i]) else 2 if (valc[i] < valo[i]) else 0)
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


class TRIXCandles(_MQL5Indicator):
    name = 'TRIX candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # TRIX period
    }

