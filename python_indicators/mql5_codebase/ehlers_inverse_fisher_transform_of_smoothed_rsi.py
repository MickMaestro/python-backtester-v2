"""Ehlers inverse fisher transform of smoothed rsi — converted from MQL5: MQL5 Indicators/Ehlers fisher transform of smoother RSI/Ehlers inverse fisher transform of smoothed rsi.mq5

.
Ehlers inverse fisher transform of
smoothed RSI with floating levels
.
set the floating levels period to less than or equal to 1
to have classical fixed levels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [13759441, 12052223], 2: [3329330], 3: [12632256], 4: [42495], 5: [12632256, 3329330, 42495]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'ift OB/OS zone', 2: 'ift up level', 3: 'ift middle level', 4: 'ift down level', 5: 'ift'}, 'levels': [], 'description': ['.', 'Ehlers inverse fisher transform of', 'smoothed RSI with floating levels', '.', 'set the floating levels period to less than or equal to 1', 'to have classical fixed levels'], 'name': 'Ehlers inverse fisher transform of smoothed rsi', 'source': 'MQL5 Indicators/Ehlers fisher transform of smoother RSI/Ehlers inverse fisher transform of smoothed rsi.mq5', 'folder': 'Ehlers fisher transform of smoother RSI', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 32, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 9, 'label': 'Average period (<=1 for no average)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 2, 'label': 'Color change :', 'sinput': False}, {'mql': 'inpMinMaxPeriod', 'py': 'inpMinMaxPeriod', 'param': 'inpMinMaxPeriod', 'type': 'int', 'default': 50, 'label': 'Floating levels period (<= 1 for fixed levels)', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
cc_onSlope = 0
cc_onMiddle = 1
cc_onLevels = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onMiddle', 2: 'cc_onLevels'})

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 32)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 9)  # Average period (<=1 for no average)
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', cc_onLevels)  # Color change :
inpMinMaxPeriod = _input('inpMinMaxPeriod', 50)  # Floating levels period (<= 1 for fixed levels)
inpLevelUp = _input('inpLevelUp', 80.0)  # Up level %
inpLevelDown = _input('inpLevelDown', 20.0)  # Down level %
rsi = Arr(0, 0.0)
rsic = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
_maHandle = 0
_rsiHandle = 0
_maPeriod = 0

def OnInit():
    global _maHandle, _maPeriod, _rsiHandle
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelMi, INDICATOR_DATA)
    SetIndexBuffer(4, levelDn, INDICATOR_DATA)
    SetIndexBuffer(5, rsi, INDICATOR_DATA)
    SetIndexBuffer(6, rsic, INDICATOR_COLOR_INDEX)
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    _maPeriod = MathMax(inpMaPeriod, 1)
    _rsiHandle = iRSI(Symbol(), 0, inpRsiPeriod, inpPrice)
    if not _checkHandle(_rsiHandle):
        return INIT_FAILED
    _maHandle = iMA(Symbol(), 0, _maPeriod, 0, inpMaMethod, _rsiHandle)
    if not _checkHandle(_maHandle):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers ift of smoothed RSI (' + _str(inpRsiPeriod) + ',' + _str(_maPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_rsiHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_maHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        trss = (rsi[i] - 50.0) * 0.1
        rsi[i] = _fdiv(MathExp(2.0 * trss) - 1.0, MathExp(2.0 * trss) + 1.0)
        if inpMinMaxPeriod <= 1:
            levelUp[i] = ((2.0 * inpLevelUp) / 100.0) - 1.0
            levelDn[i] = ((2.0 * inpLevelDown) / 100.0) - 1.0
            levelMi[i] = (levelUp[i] + levelDn[i]) / 2
        else:
            start = MathMax(i - inpMinMaxPeriod + 1, 0)
            max_ = rsi[ArrayMaximum(rsi, start, inpMinMaxPeriod)]
            min_ = rsi[ArrayMinimum(rsi, start, inpMinMaxPeriod)]
            range_ = (max_ - min_) / 100.0
            levelUp[i] = min_ + (inpLevelUp * range_)
            levelDn[i] = min_ + (inpLevelDown * range_)
            levelMi[i] = min_ + (50.0 * range_)
        _sw1 = inpColorOn
        if _sw1 == cc_onLevels:
            rsic[i] = (1 if (rsi[i] > levelUp[i]) else 2 if (rsi[i] < levelDn[i]) else (rsic[i - 1] if (rsi[i] == rsi[i - 1]) else 0) if (i > 0) else 0)
        elif _sw1 == cc_onMiddle:
            rsic[i] = (1 if (rsi[i] > levelMi[i]) else 2 if (rsi[i] < levelMi[i]) else 0)
        else:
            rsic[i] = ((1 if (rsi[i] > rsi[i - 1]) else 2 if (rsi[i] < rsi[i - 1]) else (rsic[i - 1] if (rsi[i] == rsi[i - 1]) else 0) if (i > 0) else 0) if (i > 0) else 0)
        fill1[i] = rsi[i]
        fill2[i] = (levelUp[i] if (rsi[i] > levelUp[i]) else levelDn[i] if (rsi[i] < levelDn[i]) else rsi[i])
        i += 1
    return i

def _checkHandle(_handle):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
    return _answer

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersInverseFisherTransformOfSmoothedRsi(_MQL5Indicator):
    name = 'Ehlers inverse fisher transform of smoothed rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 32,  # RSI period
        'inpMaPeriod': 9,  # Average period (<=1 for no average)
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change :
        'inpMinMaxPeriod': 50,  # Floating levels period (<= 1 for fixed levels)
        'inpLevelUp': 80.0,  # Up level %
        'inpLevelDown': 20.0,  # Down level %
    }

