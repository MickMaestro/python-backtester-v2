"""Phase change index — converted from MQL5: MQL5 Indicators/Phase change index 2/Phase change index.mq5

Phase change index
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [16760576, 6333684], 2: [11119017], 3: [11119017, 16748574, 36095]}, 'widths': {2: 0, 3: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Phase change index levels'}, 'levels': [], 'description': ['Phase change index'], 'name': 'Phase change index', 'source': 'MQL5 Indicators/Phase change index 2/Phase change index.mq5', 'folder': 'Phase change index 2', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 5, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelHigh', 'py': 'inpLevelHigh', 'param': 'inpLevelHigh', 'type': 'double', 'default': 80.0, 'label': 'Levels up', 'sinput': False}, {'mql': 'inpLevelLow', 'py': 'inpLevelLow', 'param': 'inpLevelLow', 'type': 'double', 'default': 20.0, 'label': 'Levels down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 30)  # Period
inpSmooth = _input('inpSmooth', 5)  # Smooth period
inpMethod = _input('inpMethod', MODE_SMA)  # Method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevelHigh = _input('inpLevelHigh', 80.0)  # Levels up
inpLevelLow = _input('inpLevelLow', 20.0)  # Levels down
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lev = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
map_ = Arr(0, 0.0)
ª_mapHandle = 0

def OnInit():
    global ª_mapHandle
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, lev, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, map_, INDICATOR_CALCULATIONS)
    ª_mapHandle = iMA(Symbol(), 0, inpSmooth, 0, inpMethod, inpPrice)
    if not _checkHandle(ª_mapHandle, 'Average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Phase change index ' + _str(inpPeriod) + ',' + _str(inpSmooth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_mapHandle, 0, 0, _copyCount, map_) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if map_[i] == EMPTY_VALUE:
            map_[i] = 0.0
        if i >= inpPeriod:
            momentum = map_[i] - map_[i - inpPeriod]
            sumUpDi = 0.0
            sumDnDi = 0.0
            k = 1
            while k < inpPeriod and i >= k:
                gradient = map_[i - inpPeriod] + ((momentum * (inpPeriod - k)) / inpPeriod)
                deviation = map_[i - k] - gradient
                if deviation > 0:
                    sumUpDi += deviation
                else:
                    sumDnDi -= deviation
                k += 1
            val[i] = ((100 - _fdiv(100.0 * sumUpDi, sumUpDi + sumDnDi)) if ((sumUpDi + sumDnDi) != 0) else 0)
        else:
            val[i] = 0.0
        valc[i] = (1 if (val[i] > inpLevelHigh) else 2 if (val[i] < inpLevelLow) else 0)
        lev[i] = (100 if (valc[i] == 1) else 0 if (valc[i] == 2) else 50)
        fup[i] = val[i]
        fdn[i] = (MathMin(val[i], inpLevelHigh) if (val[i] > 50) else MathMax(val[i], inpLevelLow))
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


class PhaseChangeIndex(_MQL5Indicator):
    name = 'Phase change index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 30,  # Period
        'inpSmooth': 5,  # Smooth period
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelHigh': 80.0,  # Levels up
        'inpLevelLow': 20.0,  # Levels down
    }

