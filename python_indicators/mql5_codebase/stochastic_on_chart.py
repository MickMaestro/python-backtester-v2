"""Stochastic (on chart) — converted from MQL5: MQL5 Indicators/Stochastic on chart/Stochastic (on chart).mq5

On-chart stochastic
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 7}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 8, 7: 1}, 'colors': {1: [15790335], 2: [15794160], 3: [8421504], 4: [8421504], 5: [8421504], 6: [11119017, 7451452, 17919], 7: [8421504]}, 'widths': {6: 2}, 'styles': {3: 2, 4: 2, 5: 2, 7: 2}, 'labels': {1: 'Upper filling', 2: 'Lower filling', 3: 'Upper level', 4: 'Middle level', 5: 'Lower level', 6: 'Stochastic', 7: 'Signal'}, 'levels': [], 'description': ['On-chart stochastic'], 'name': 'Stochastic (on chart)', 'source': 'MQL5 Indicators/Stochastic on chart/Stochastic (on chart).mq5', 'folder': 'Stochastic on chart', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 14, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'inpStoSignal', 'py': 'inpStoSignal', 'param': 'inpStoSignal', 'type': 'int', 'default': 3, 'label': 'Stochastic signal', 'sinput': False}, {'mql': 'inpStoSignalM', 'py': 'inpStoSignalM', 'param': 'inpStoSignalM', 'type': 'int', 'default': 0, 'label': 'Signal caculation method', 'sinput': False}, {'mql': 'inpHlPeriod', 'py': 'inpHlPeriod', 'param': 'inpHlPeriod', 'type': 'int', 'default': 25, 'label': 'Highest high/lowest low period', 'sinput': False}, {'mql': 'inpHlLevelUp', 'py': 'inpHlLevelUp', 'param': 'inpHlLevelUp', 'type': 'double', 'default': 70.0, 'label': 'OB level', 'sinput': False}, {'mql': 'inpHlLevelDn', 'py': 'inpHlLevelDn', 'param': 'inpHlLevelDn', 'type': 'double', 'default': 30.0, 'label': 'OS level', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onSignal = 2
cchange_onZero = 3
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onSignal', 3: 'cchange_onZero'})

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 14)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 3)  # Stochastic slowing
inpPrice = _input('inpPrice', STO_LOWHIGH)  # Price
inpStoSignal = _input('inpStoSignal', 3)  # Stochastic signal
inpStoSignalM = _input('inpStoSignalM', MODE_SMA)  # Signal caculation method
inpHlPeriod = _input('inpHlPeriod', 25)  # Highest high/lowest low period
inpHlLevelUp = _input('inpHlLevelUp', 70.0)  # OB level
inpHlLevelDn = _input('inpHlLevelDn', 30.0)  # OS level
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
vals = Arr(0, 0.0)
valc = Arr(0, 0.0)
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldd = Arr(0, 0.0)
filldu = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
sto = Arr(0, 0.0)
sig = Arr(0, 0.0)
ª_stoHandle = 0
ª_stoPeriod = 0

def OnInit():
    global ª_stoHandle, ª_stoPeriod
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, levm, INDICATOR_DATA)
    SetIndexBuffer(5, levu, INDICATOR_DATA)
    SetIndexBuffer(6, levd, INDICATOR_DATA)
    SetIndexBuffer(7, val, INDICATOR_DATA)
    SetIndexBuffer(8, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(9, vals, INDICATOR_DATA)
    SetIndexBuffer(10, sto, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, sig, INDICATOR_CALCULATIONS)
    ª_stoPeriod = (inpStoPeriod if (inpStoPeriod > 1) else 1)
    ª_stoHandle = iStochastic(Symbol(), 0, ª_stoPeriod, inpStoSignal, inpStoSlowing, inpStoSignalM, inpPrice)
    if not _checkHandle(ª_stoHandle, 'Stochastic'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic on chart (' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(inpStoSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_stoHandle, 0, 0, _copyCount, sto) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_stoHandle, 1, 0, _copyCount, sig) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if sto[i] == EMPTY_VALUE:
            sto[i] = 0.0
        if sig[i] == EMPTY_VALUE:
            sig[i] = 0.0
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpHlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = high[ArrayMaximum(high, start, inpHlPeriod - 1)]
            _s_OnCalculate_prev_min = low[ArrayMinimum(low, start, inpHlPeriod - 1)]
        max_ = (high[i] if (high[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (low[i] if (low[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpHlLevelUp * range_)
        levd[i] = min_ + (inpHlLevelDn * range_)
        levm[i] = min_ + (50 * range_)
        filldu[i] = min_ + (sto[i] * range_)
        fillud[i] = filldu[i]
        val[i] = fillud[i]
        vals[i] = min_ + (sig[i] * range_)
        filluu[i] = max_
        filldd[i] = min_
        _sw1 = inpColorChange
        if _sw1 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw1 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == cchange_onSignal:
            valc[i] = (1 if (sto[i] > sig[i]) else 2 if (sto[i] < sig[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw1 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
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


class StochasticOnChart(_MQL5Indicator):
    name = 'Stochastic (on chart)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 14,  # Stochastic period
        'inpStoSlowing': 3,  # Stochastic slowing
        'inpPrice': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Price
        'inpStoSignal': 3,  # Stochastic signal
        'inpStoSignalM': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal caculation method
        'inpHlPeriod': 25,  # Highest high/lowest low period
        'inpHlLevelUp': 70.0,  # OB level
        'inpHlLevelDn': 30.0,  # OS level
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on OB/OS level', 2: 'Change color on signal cross', 3: 'Change color on level 50 cross'}, default=1),  # Color changing mode
    }

