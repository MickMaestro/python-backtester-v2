"""Dsl - CMO 2 — converted from MQL5: MQL5 Indicators/DSL Chande momentum oscillator - smoothed/Dsl - CMO 2.mq5

Discontinued signal lines version of smoothed Chandes momentum oscillator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'CMO no trend zone', 2: 'CMO'}, 'levels': [], 'description': ['Discontinued signal lines version of smoothed Chandes momentum oscillator'], 'name': 'Dsl - CMO 2', 'source': 'MQL5 Indicators/DSL Chande momentum oscillator - smoothed/Dsl - CMO 2.mq5', 'folder': 'DSL Chande momentum oscillator - smoothed', 'inputs': [{'mql': 'inpCmoPeriod', 'py': 'inpCmoPeriod', 'param': 'inpCmoPeriod', 'type': 'int', 'default': 20, 'label': 'CMO period', 'sinput': False}, {'mql': 'inpCmoSignalPeriod', 'py': 'inpCmoSignalPeriod', 'param': 'inpCmoSignalPeriod', 'type': 'int', 'default': 9, 'label': 'CMO signal period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 7, 'label': 'Smoothing period (<= 1 for no smoothing)', 'sinput': False}, {'mql': 'inpMaMetod', 'py': 'inpMaMetod', 'param': 'inpMaMetod', 'type': 'int', 'default': 3, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCmoPeriod = _input('inpCmoPeriod', 20)  # CMO period
inpCmoSignalPeriod = _input('inpCmoSignalPeriod', 9)  # CMO signal period
inpMaPeriod = _input('inpMaPeriod', 7)  # Smoothing period (<= 1 for no smoothing)
inpMaMetod = _input('inpMaMetod', MODE_LWMA)  # Smoothing method
cmo = Arr(0, 0.0)
cmoc = Arr(0, 0.0)
dslup = Arr(0, 0.0)
dsldn = Arr(0, 0.0)
cmo1 = Arr(0, 0.0)
cmo2 = Arr(0, 0.0)
cmo3 = Arr(0, 0.0)
cmo4 = Arr(0, 0.0)
avg = Arr(0, 0.0)
_mac = 0

def OnInit():
    global _mac
    SetIndexBuffer(0, dslup, INDICATOR_DATA)
    SetIndexBuffer(1, dsldn, INDICATOR_DATA)
    SetIndexBuffer(2, cmo, INDICATOR_DATA)
    SetIndexBuffer(3, cmoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, cmo1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, cmo2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, cmo3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, cmo4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, avg, INDICATOR_CALCULATIONS)
    _maPeriod = (inpMaPeriod if (inpMaPeriod > 0) else 1)
    _mac = iMA(Symbol(), 0, _maPeriod, 0, inpMaMetod, PRICE_CLOSE)
    if not _checkHandle(_mac, 'Moving average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dsl Chandes momentum oscillator (' + _str(inpCmoPeriod) + ',' + _str(inpCmoSignalPeriod) + ',' + _str(_maPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_mac) < rates_total:
        return prev_calculated
    _copyCount = ((rates_total - prev_calculated + 1) if (prev_calculated > 0) else rates_total)
    if CopyBuffer(_mac, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    _alpha = 2.0 / (1 + inpCmoSignalPeriod)
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if avg[i] == EMPTY_VALUE:
            avg[i] = close[i]
        cmo[i] = iCmo(inpCmoPeriod, avg, cmo1, cmo2, cmo3, cmo4, i) * 100.0
        dslup[i] = (((dslup[i - 1] + (_alpha * (cmo[i] - dslup[i - 1]))) if (cmo[i] > 0) else dslup[i - 1]) if (i > 0) else 0)
        dsldn[i] = (((dsldn[i - 1] + (_alpha * (cmo[i] - dsldn[i - 1]))) if (cmo[i] < 0) else dsldn[i - 1]) if (i > 0) else 0)
        cmoc[i] = (2 if (cmo[i] > dslup[i]) else 1 if (cmo[i] < dsldn[i]) else 0)
        i += 1
    return i

def iCmo(period, price, diffu, diffd, cumu, cumd, i):
    diff = ((price[i] - price[i - 1]) if (i > 0) else 0)
    if diff > 0:
        diffu[i] = diff
        diffd[i] = 0.0
    else:
        diffd[i] = -diff
        diffu[i] = 0.0
    if i < period:
        cumd[i] = 0.0
        cumu[i] = cumd[i]
        k = 0
        while k < period and (i - k) >= 0:
            cumu[i] += diffu[i - k]
            cumd[i] += diffd[i - k]
            k += 1
    else:
        cumu[i] = cumu[i - 1] - diffu[i - period] + diffu[i]
        cumd[i] = cumd[i - 1] - diffd[i - period] + diffd[i]
    return (_fdiv(cumu[i] - cumd[i], cumu[i] + cumd[i]) if ((cumu[i] + cumd[i]) != 0) else 0)

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
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslCMO2(_MQL5Indicator):
    name = 'Dsl - CMO 2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCmoPeriod': 20,  # CMO period
        'inpCmoSignalPeriod': 9,  # CMO signal period
        'inpMaPeriod': 7,  # Smoothing period (<= 1 for no smoothing)
        'inpMaMetod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Smoothing method
    }

