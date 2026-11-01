"""RSI of average - wnz — converted from MQL5: MQL5 Indicators/Rsi of average - with normalized zones/RSI of average - wnz.mq5

RSI of average - with normalized zones
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [15128749, 12180223], 2: [11119017], 3: [11119017, 16760576, 6333684]}, 'widths': {3: 3}, 'styles': {2: 2}, 'labels': {1: 'Normalized zones', 2: 'Normalized rsi', 3: 'RSI of average'}, 'levels': [], 'description': ['RSI of average - with normalized zones'], 'name': 'RSI of average - wnz', 'source': 'MQL5 Indicators/Rsi of average - with normalized zones/RSI of average - wnz.mq5', 'folder': 'Rsi of average - with normalized zones', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpNormPeriod', 'py': 'inpNormPeriod', 'param': 'inpNormPeriod', 'type': 'int', 'default': 20, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 32)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpNormPeriod = _input('inpNormPeriod', 20)  # Normalization period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valn = Arr(0, 0.0)
valfu = Arr(0, 0.0)
valfd = Arr(0, 0.0)
_maHandle = 0
_rsiHandle = 0

def OnInit():
    global _maHandle, _rsiHandle
    SetIndexBuffer(0, valfu, INDICATOR_DATA)
    SetIndexBuffer(1, valfd, INDICATOR_DATA)
    SetIndexBuffer(2, valn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    _rsiHandle = iRSI(Symbol(), 0, inpRsiPeriod, _maHandle)
    if _rsiHandle == INVALID_HANDLE:
        IndicatorRelease(_maHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' (' + _str(inpRsiPeriod) + ',' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_rsiHandle) < rates_total:
        return prev_calculated
    _rsiVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _rsiCopied = CopyBuffer(_rsiHandle, 0, _DT(time[i]), 1, _rsiVal)
        val[i] = ((_rsiVal[0] - 50) if (_rsiCopied == 1) else EMPTY_VALUE)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        valn[i] = 0.0
        _start = MathMax(i - inpNormPeriod + 1, 0)
        if val[i] > 0:
            hi = val[ArrayMaximum(val, _start, inpNormPeriod)]
            if hi != 0:
                valn[i] = _fdiv(50 * val[i], hi)
        if val[i] < 0:
            lo = val[ArrayMinimum(val, _start, inpNormPeriod)]
            if lo != 0:
                valn[i] = _fdiv(50 * val[i], -lo)
        valfu[i] = valn[i]
        valfd[i] = val[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOfAverageWnz(_MQL5Indicator):
    name = 'RSI of average - wnz'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpMaPeriod': 32,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpNormPeriod': 20,  # Normalization period
    }

