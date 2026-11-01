"""Drunkard walk — converted from MQL5: MQL5 Indicators/Drunkards walk/Drunkard walk.mq5

Drunkard`s walk
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 8, 3: 8, 4: 8}, 'colors': {1: [15135718, 15132403], 2: [32768, 255], 3: [32768, 255], 4: [32768, 255]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'filling', 2: 'Line up', 3: 'Line down', 4: 'Trend line'}, 'levels': [], 'description': ['Drunkard`s walk'], 'name': 'Drunkard walk', 'source': 'MQL5 Indicators/Drunkards walk/Drunkard walk.mq5', 'folder': 'Drunkards walk', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 40, 'label': 'Drunkard walk period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 40)  # Drunkard walk period
trend = Arr(0, 0.0)
trendc = Arr(0, 0.0)
valu = Arr(0, 0.0)
valuc = Arr(0, 0.0)
vald = Arr(0, 0.0)
valdc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
ª_alpha = 0.0
_dwWork = Arr(0, 0.0, dims=(5,))

def OnInit():
    global ª_alpha
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valu, INDICATOR_DATA)
    SetIndexBuffer(3, valuc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, vald, INDICATOR_DATA)
    SetIndexBuffer(5, valdc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, trend, INDICATOR_DATA)
    SetIndexBuffer(7, trendc, INDICATOR_COLOR_INDEX)
    ª_alpha = _fdiv(2.0, 1.0 + inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, "Drunkard's walk (" + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__arrayError, _s_OnCalculate__arrayResizedTo
    if _s_OnCalculate__arrayResizedTo < rates_total:
        _res = rates_total + 500
        _res -= ArrayResize(_dwWork, _res)
        if _res:
            _s_OnCalculate__arrayError = True
        else:
            _s_OnCalculate__arrayResizedTo = rates_total + 500
    if _s_OnCalculate__arrayError:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        start = ((i - inpPeriod + 1) if (i > inpPeriod) else 0)
        longMaxBar = ArrayMaximum(high, start, inpPeriod)
        longMinBar = ArrayMinimum(low, start, inpPeriod)
        longDnRun = i - longMaxBar
        longUpRun = i - longMinBar
        longHigh = high[longMaxBar]
        longLow = low[longMinBar]
        _dwWork[i][0] = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        _dwWork[i][1] = ((_dwWork[i - 2][1] + 1) if (i > 1) else 0)
        _dwWork[i][2] = (_dwWork[i - 1][2] if (i > 1) else 0)
        _dwWork[i][3] = (_dwWork[i - 1][3] if (i > 1) else 0)
        _dwWork[i][4] = (_dwWork[i - 1][4] if (i > 1) else 0)
        if _dwWork[i][3] == 0:
            _dwWork[i][1] = inpPeriod
            _dwWork[i][2] = inpPeriod
            _dwWork[i][3] = inpPeriod
        if i > 1 and _dwWork[i - 1][4] != _dwWork[i - 2][4]:
            _dwWork[i][1] = 1.0
            _dwWork[i][2] = _dwWork[i - 1][1]
            _dwWork[i][3] = _dwWork[i - 1][3] + (ª_alpha * (_dwWork[i - 1][2] - _dwWork[i - 1][3]))
        valu[i] = (valu[i - 1] if (i > 0) else 0)
        vald[i] = (vald[i - 1] if (i > 0) else 0)
        trend[i] = (trend[i - 1] if (i > 0) else 0)
        if longDnRun > 0 and longUpRun > 0:
            atr = _dwWork[i][0]
            k = 1
            while k < _dwWork[i][3] and (i - k) >= 0:
                atr += _dwWork[i - k][0]
                k += 1
            atr = _fdiv(atr, float(k))
            denom = ((MathSqrt(_dwWork[i][3]) * atr) if (atr > 0) else MathSqrt(_dwWork[i][3]))
            valu[i] = _fdiv(high[i] - longLow, denom)
            vald[i] = _fdiv(longHigh - low[i], denom)
        fillu[i] = valu[i]
        filld[i] = vald[i]
        if valu[i] > vald[i]:
            _dwWork[i][4] = 1.0
            valuc[i] = 0.0
            valdc[i] = 0.0
            trend[i] = valu[i]
            trendc[i] = 0.0
        if valu[i] < vald[i]:
            _dwWork[i][4] = -1.0
            valuc[i] = 1.0
            valdc[i] = 1.0
            trend[i] = vald[i]
            trendc[i] = 1.0
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
_s_OnCalculate__arrayError = False
_s_OnCalculate__arrayResizedTo = 0
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrunkardWalk(_MQL5Indicator):
    name = 'Drunkard walk'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 40,  # Drunkard walk period
    }

