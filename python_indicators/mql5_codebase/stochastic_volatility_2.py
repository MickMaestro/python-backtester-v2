"""Stochastic volatility 2 — converted from MQL5: MQL5 Indicators/Stochastic volatility - on chart/Stochastic volatility 2.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 8, 4: 1}, 'colors': {1: [32768], 2: [17919], 3: [11119017, 17919], 4: [8421504]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2, 4: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'Stochastic volatility', 4: 'Signal'}, 'levels': [], 'description': [], 'name': 'Stochastic volatility 2', 'source': 'MQL5 Indicators/Stochastic volatility - on chart/Stochastic volatility 2.mq5', 'folder': 'Stochastic volatility - on chart', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 30, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'BandsLength', 'py': 'BandsLength', 'param': 'BandsLength', 'type': 'int', 'default': 126, 'label': 'Bands period', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'Bands deviation', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'OriginalStoch', 'py': 'OriginalStoch', 'param': 'OriginalStoch', 'type': 'bool', 'default': True, 'label': 'Calculate using original stochastic', 'sinput': False}, {'mql': 'OriginalVolatility', 'py': 'OriginalVolatility', 'param': 'OriginalVolatility', 'type': 'bool', 'default': True, 'label': 'Calculate using original volatility', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'Stochastic volatility', 'label': 'Unique ID for comunications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 30)  # Stochastic period
Slowing = _input('Slowing', 5)  # Stochastic slowing
Signal = _input('Signal', 5)  # Signal period
BandsLength = _input('BandsLength', 126)  # Bands period
BandsDeviation = _input('BandsDeviation', 1.0)  # Bands deviation
Price = _input('Price', PRICE_CLOSE)  # Price
OriginalStoch = _input('OriginalStoch', True)  # Calculate using original stochastic
OriginalVolatility = _input('OriginalVolatility', True)  # Calculate using original volatility
UniqueID = _input('UniqueID', 'Stochastic volatility')  # Unique ID for comunications
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
avg = Arr(0, 0.0)
dev = Arr(0, 0.0)
_hbp = 0
_hsi = 0
_hav = 0
_hsd = 0

def OnInit():
    global _hav, _hbp, _hsd, _hsi
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    SetIndexBuffer(5, avg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, dev, INDICATOR_CALCULATIONS)
    _hbp = iCustom(Symbol(), 0, '::Stochastic volatility base 2.ex5', Length, Slowing, Price, OriginalStoch, OriginalVolatility)
    if not _checkHandle(_hbp, 'Base indicator 2'):
        return INIT_FAILED
    _hsi = iMA(Symbol(), 0, Signal, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsi, 'Signal'):
        return INIT_FAILED
    _hav = iMA(Symbol(), 0, BandsLength, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hav, 'Bands average'):
        return INIT_FAILED
    _hsd = iStdDev(Symbol(), 0, BandsLength, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsd, 'Bands deviation'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, UniqueID + ' (' + _str(Length) + ',' + _str(Slowing) + ',' + _str(Signal) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_hbp) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsi) < rates_total:
        return prev_calculated
    if BarsCalculated(_hav) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsd) < rates_total:
        return prev_calculated
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_hbp, 0, 0, _copyCount, val) != _copyCount:
        Comment('Error copying val')
        return prev_calculated
    if CopyBuffer(_hsi, 0, 0, _copyCount, signal) != _copyCount:
        Comment('Error copying signal')
        return prev_calculated
    if CopyBuffer(_hav, 0, 0, _copyCount, avg) != _copyCount:
        Comment('Error copying avg')
        return prev_calculated
    if CopyBuffer(_hsd, 0, 0, _copyCount, dev) != _copyCount:
        Comment('Error copying dev')
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        levelUp[i] = avg[i] + (dev[i] * BandsDeviation)
        levelDn[i] = avg[i] - (dev[i] * BandsDeviation)
        valc[i] = (1 if (val[i] < levelDn[i]) else 0)
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
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticVolatility2(_MQL5Indicator):
    name = 'Stochastic volatility 2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 30,  # Stochastic period
        'Slowing': 5,  # Stochastic slowing
        'Signal': 5,  # Signal period
        'BandsLength': 126,  # Bands period
        'BandsDeviation': 1.0,  # Bands deviation
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'OriginalStoch': True,  # Calculate using original stochastic
        'OriginalVolatility': True,  # Calculate using original volatility
    }

