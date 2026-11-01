"""TRIX candles with Keltner channel — converted from MQL5: MQL5 Indicators/TRiX candles with Keltner channel/TRIX candles with Keltner channel.mq5

TRIX candles with \\"Keltner\\" channels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 4}, 'types': {1: 17, 2: 1, 3: 1, 4: 1}, 'colors': {1: [8421504, 7451452, 17919], 2: [8421504], 3: [8421504], 4: [8421504]}, 'widths': {}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'TRiX', 2: 'average', 3: 'channel up', 4: 'channel up'}, 'levels': [], 'description': ['TRIX candles with \\"Keltner\\" channels'], 'name': 'TRIX candles with Keltner channel', 'source': 'MQL5 Indicators/TRiX candles with Keltner channel/TRIX candles with Keltner channel.mq5', 'folder': 'TRiX candles with Keltner channel', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'TRiX period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 0, 'label': 'Channel period (<=1 for same as TRiX period)', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Channels multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # TRiX period
inpAvgPeriod = _input('inpAvgPeriod', 0)  # Channel period (<=1 for same as TRiX period)
inpMultiplier = _input('inpMultiplier', 1.5)  # Channels multiplier
valo = Arr(0, 0.0)
valh = Arr(0, 0.0)
vall = Arr(0, 0.0)
valc = Arr(0, 0.0)
valcl = Arr(0, 0.0)
kel = Arr(0, 0.0)
kelu = Arr(0, 0.0)
keld = Arr(0, 0.0)
tr = Arr(0, 0.0)
trix = Arr(0, 0.0)
atr = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_workVal = Arr(4, 0.0, dyn=False)
ª_valhHandle = 0
ª_vallHandle = 0
ª_valoHandle = 0
ª_valcHandle = 0
ª_avgPeriod = 0

def OnInit():
    global ª_avgPeriod, ª_valcHandle, ª_valhHandle, ª_vallHandle, ª_valoHandle
    SetIndexBuffer(0, valo, INDICATOR_DATA)
    SetIndexBuffer(1, valh, INDICATOR_DATA)
    SetIndexBuffer(2, vall, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_DATA)
    SetIndexBuffer(4, valcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, kel, INDICATOR_DATA)
    SetIndexBuffer(6, kelu, INDICATOR_DATA)
    SetIndexBuffer(7, keld, INDICATOR_DATA)
    SetIndexBuffer(8, tr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, trix, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, avg, INDICATOR_CALCULATIONS)
    ª_valhHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_HIGH)
    if not _checkHandle(ª_valhHandle, 'TRiX of high'):
        return INIT_FAILED
    ª_vallHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_LOW)
    if not _checkHandle(ª_vallHandle, 'TRiX of low'):
        return INIT_FAILED
    ª_valoHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_OPEN)
    if not _checkHandle(ª_valoHandle, 'TRiX of open'):
        return INIT_FAILED
    ª_valcHandle = iTriX(Symbol(), 0, inpPeriod, PRICE_CLOSE)
    if not _checkHandle(ª_valcHandle, 'TRiX of close'):
        return INIT_FAILED
    ª_avgPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRiX candles (' + _str(inpPeriod) + ',' + _str(ª_avgPeriod) + ',' + _str(inpMultiplier) + ')')
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
        if vall[i] == EMPTY_VALUE:
            vall[i] = 0.0
        if valh[i] == EMPTY_VALUE:
            valh[i] = 0.0
        if valo[i] == EMPTY_VALUE:
            valo[i] = 0.0
        if valc[i] == EMPTY_VALUE:
            valc[i] = 0.0
        ª_workVal[1] = vall[i]
        ª_workVal[0] = valh[i]
        ª_workVal[2] = valo[i]
        ª_workVal[3] = valc[i]
        valh[i] = ª_workVal[ArrayMaximum(ª_workVal)]
        vall[i] = ª_workVal[ArrayMinimum(ª_workVal)]
        trix[i] = (valh[i] + vall[i] + valo[i] + valc[i]) / 4.0
        tr[i] = ((MathMax(valh[i], valc[i - 1]) - MathMin(vall[i], valc[i - 1])) if (i > 0) else (valh[i] - vall[i]))
        if i > ª_avgPeriod:
            avg[i] = avg[i - 1] + trix[i] - trix[i - ª_avgPeriod]
            atr[i] = atr[i - 1] + tr[i] - tr[i - ª_avgPeriod]
        else:
            atr[i] = 0.0
            avg[i] = atr[i]
            k = 0
            while k < ª_avgPeriod and i >= k:
                avg[i] += trix[i - k]
                atr[i] += tr[i - k]
                k += 1
        kel[i] = _fdiv(avg[i], float(ª_avgPeriod))
        kelu[i] = kel[i] + _fdiv(inpMultiplier * atr[i], float(ª_avgPeriod))
        keld[i] = kel[i] - _fdiv(inpMultiplier * atr[i], float(ª_avgPeriod))
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


class TRIXCandlesWithKeltnerChannel(_MQL5Indicator):
    name = 'TRIX candles with Keltner channel'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # TRiX period
        'inpAvgPeriod': 0,  # Channel period (<=1 for same as TRiX period)
        'inpMultiplier': 1.5,  # Channels multiplier
    }

