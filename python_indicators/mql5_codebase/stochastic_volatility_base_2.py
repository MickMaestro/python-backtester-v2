"""Stochastic volatility base 2 — converted from MQL5: MQL5 Indicators/Stochastic volatility - on chart/Stochastic volatility base 2.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Stochastic'}, 'levels': [], 'description': [], 'name': 'Stochastic volatility base 2', 'source': 'MQL5 Indicators/Stochastic volatility - on chart/Stochastic volatility base 2.mq5', 'folder': 'Stochastic volatility - on chart', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 30, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'OriginalStoch', 'py': 'OriginalStoch', 'param': 'OriginalStoch', 'type': 'bool', 'default': True, 'label': 'Calculate using original stochastic', 'sinput': False}, {'mql': 'OriginalVolatility', 'py': 'OriginalVolatility', 'param': 'OriginalVolatility', 'type': 'bool', 'default': True, 'label': 'Calculate using original volatility', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 30)  # Stochastic period
Slowing = _input('Slowing', 5)  # Stochastic slowing
Price = _input('Price', PRICE_CLOSE)  # Price
OriginalStoch = _input('OriginalStoch', True)  # Calculate using original stochastic
OriginalVolatility = _input('OriginalVolatility', True)  # Calculate using original volatility
val = Arr(0, 0.0)
ma1 = Arr(0, 0.0)
ma2 = Arr(0, 0.0)
ma3 = Arr(0, 0.0)
ma4 = Arr(0, 0.0)
ma5 = Arr(0, 0.0)
sd1 = Arr(0, 0.0)
sd2 = Arr(0, 0.0)
sd3 = Arr(0, 0.0)
sd4 = Arr(0, 0.0)
sd5 = Arr(0, 0.0)
vol = Arr(0, 0.0)
whi = Arr(0, 0.0)
wlo = Arr(0, 0.0)
_hma1 = 0
_hma2 = 0
_hma3 = 0
_hma4 = 0
_hma5 = 0
_hsd1 = 0
_hsd2 = 0
_hsd3 = 0
_hsd4 = 0
_hsd5 = 0
_hbp = 0

def OnInit():
    global _hbp, _hma1, _hma2, _hma3, _hma4, _hma5, _hsd1, _hsd2, _hsd3, _hsd4, _hsd5
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, ma1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ma2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ma3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ma4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ma5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, sd1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, sd2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, sd3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, sd4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, sd5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, vol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, whi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, wlo, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, vol, INDICATOR_CALCULATIONS)
    _hbp = iCustom(Symbol(), 0, '::Stochastic volatility base.ex5', Price)
    if not _checkHandle(_hbp, 'Base indicator'):
        return INIT_FAILED
    _hma1 = iMA(Symbol(), 0, 10, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hma1, 'Moving average 10'):
        return INIT_FAILED
    _hma2 = iMA(Symbol(), 0, 21, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hma2, 'Moving average 21'):
        return INIT_FAILED
    _hma3 = iMA(Symbol(), 0, 34, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hma3, 'Moving average 34'):
        return INIT_FAILED
    _hma4 = iMA(Symbol(), 0, 55, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hma4, 'Moving average 55'):
        return INIT_FAILED
    _hma5 = iMA(Symbol(), 0, 89, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hma5, 'Moving average 89'):
        return INIT_FAILED
    _hsd1 = iStdDev(Symbol(), 0, 10, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsd1, 'Standard deviation 10'):
        return INIT_FAILED
    _hsd2 = iStdDev(Symbol(), 0, 21, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsd2, 'Standard deviation 10'):
        return INIT_FAILED
    _hsd3 = iStdDev(Symbol(), 0, 34, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsd3, 'Standard deviation 10'):
        return INIT_FAILED
    _hsd4 = iStdDev(Symbol(), 0, 55, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsd4, 'Standard deviation 10'):
        return INIT_FAILED
    _hsd5 = iStdDev(Symbol(), 0, 89, 0, MODE_SMA, _hbp)
    if not _checkHandle(_hsd5, 'Standard deviation 10'):
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_hbp) < rates_total:
        return prev_calculated
    if BarsCalculated(_hma1) < rates_total:
        return prev_calculated
    if BarsCalculated(_hma2) < rates_total:
        return prev_calculated
    if BarsCalculated(_hma3) < rates_total:
        return prev_calculated
    if BarsCalculated(_hma4) < rates_total:
        return prev_calculated
    if BarsCalculated(_hma5) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsd1) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsd2) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsd3) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsd4) < rates_total:
        return prev_calculated
    if BarsCalculated(_hsd5) < rates_total:
        return prev_calculated
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_hma1, 0, 0, _copyCount, ma1) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hma2, 0, 0, _copyCount, ma2) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hma3, 0, 0, _copyCount, ma3) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hma4, 0, 0, _copyCount, ma4) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hma5, 0, 0, _copyCount, ma5) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hsd1, 0, 0, _copyCount, sd1) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hsd2, 0, 0, _copyCount, sd2) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hsd3, 0, 0, _copyCount, sd3) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hsd4, 0, 0, _copyCount, sd4) != _copyCount:
        return prev_calculated
    if CopyBuffer(_hsd5, 0, 0, _copyCount, sd5) != _copyCount:
        return prev_calculated
    _mul = MathSqrt(252)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        if ma1[i] == EMPTY_VALUE or sd1[i] == EMPTY_VALUE:
            val[i] = 0.0
            vol[i] = val[i]
            wlo[i] = vol[i]
            whi[i] = wlo[i]
            i += 1
            continue
        if ma2[i] == EMPTY_VALUE or sd2[i] == EMPTY_VALUE:
            val[i] = 0.0
            vol[i] = val[i]
            wlo[i] = vol[i]
            whi[i] = wlo[i]
            i += 1
            continue
        if ma3[i] == EMPTY_VALUE or sd3[i] == EMPTY_VALUE:
            val[i] = 0.0
            vol[i] = val[i]
            wlo[i] = vol[i]
            whi[i] = wlo[i]
            i += 1
            continue
        if ma4[i] == EMPTY_VALUE or sd4[i] == EMPTY_VALUE:
            val[i] = 0.0
            vol[i] = val[i]
            wlo[i] = vol[i]
            whi[i] = wlo[i]
            i += 1
            continue
        if ma5[i] == EMPTY_VALUE or sd5[i] == EMPTY_VALUE:
            val[i] = 0.0
            vol[i] = val[i]
            wlo[i] = vol[i]
            whi[i] = wlo[i]
            i += 1
            continue
        vol1 = (((ma1[i] + sd1[i]) * _mul) if OriginalVolatility else sd1[i]) * 3.0
        vol2 = (((ma2[i] + sd2[i]) * _mul) if OriginalVolatility else sd2[i]) * 3.0
        vol3 = (((ma3[i] + sd3[i]) * _mul) if OriginalVolatility else sd3[i]) * 2.0
        vol4 = (((ma4[i] + sd4[i]) * _mul) if OriginalVolatility else sd4[i])
        vol5 = (((ma5[i] + sd5[i]) * _mul) if OriginalVolatility else sd5[i])
        vol[i] = vol1 + vol2 + vol3 + vol4 + vol5
        _start = ((i - Length + 1) if (i > Length) else 0)
        wlo[i] = vol[ArrayMinimum(vol, _start, Length)]
        whi[i] = vol[ArrayMaximum(vol, _start, Length)]
        stoc = 0.0
        if OriginalStoch:
            sumRng = 0.0
            sumLow = 0.0
            k = 0
            while k < Slowing and (i - k) >= 0:
                sumRng += whi[i - k] - wlo[i - k]
                sumLow += vol[i - k] - wlo[i - k]
                k += 1
            if sumRng != 0:
                stoc = _fdiv(100 * sumLow, sumRng)
        else:
            stov = (_fdiv(100 * (vol[i] - wlo[i]), whi[i] - wlo[i]) if ((whi[i] - wlo[i]) != 0) else 0)
            stoc = ((val[i - 1] + (_fdiv(2.0, 1.0 + Slowing) * (stov - val[i - 1]))) if (i > 0) else 0)
        val[i] = stoc
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


class StochasticVolatilityBase2(_MQL5Indicator):
    name = 'Stochastic volatility base 2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 30,  # Stochastic period
        'Slowing': 5,  # Stochastic slowing
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'OriginalStoch': True,  # Calculate using original stochastic
        'OriginalVolatility': True,  # Calculate using original volatility
    }

