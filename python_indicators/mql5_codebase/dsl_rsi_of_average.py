"""Dsl - RSI of average — converted from MQL5: MQL5 Indicators/Dsl - RSI of average/Dsl - RSI of average.mq5

Dsl - RSI of average
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [15132390], 2: [11119017, 16760576, 8036607]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Dsl zone', 2: 'RSI of average'}, 'levels': [], 'description': ['Dsl - RSI of average'], 'name': 'Dsl - RSI of average', 'source': 'MQL5 Indicators/Dsl - RSI of average/Dsl - RSI of average.mq5', 'folder': 'Dsl - RSI of average', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpRsiSignalPeriod', 'py': 'inpRsiSignalPeriod', 'param': 'inpRsiSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Dsl signal period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpRsiSignalPeriod = _input('inpRsiSignalPeriod', 9)  # Dsl signal period
inpMaPeriod = _input('inpMaPeriod', 32)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
dslup = Arr(0, 0.0)
dsldn = Arr(0, 0.0)
_maHandle = 0
_rsiHandle = 0

def OnInit():
    global _maHandle, _rsiHandle
    SetIndexBuffer(0, dslup, INDICATOR_DATA)
    SetIndexBuffer(1, dsldn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    _rsiHandle = iRSI(Symbol(), 0, inpRsiPeriod, _maHandle)
    if _rsiHandle == INVALID_HANDLE:
        IndicatorRelease(_maHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dsl - RSI of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' (' + _str(inpRsiPeriod) + ',' + _str(inpMaPeriod) + ')')
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
    _alpha = 2.0 / (1 + inpRsiSignalPeriod)
    _rsiVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _rsiCopied = CopyBuffer(_rsiHandle, 0, _DT(time[i]), 1, _rsiVal)
        val[i] = (_rsiVal[0] if (_rsiCopied == 1) else EMPTY_VALUE)
        dslup[i] = (((dslup[i - 1] + (_alpha * (val[i] - dslup[i - 1]))) if (val[i] > 50) else dslup[i - 1]) if (i > 0) else 0)
        dsldn[i] = (((dsldn[i - 1] + (_alpha * (val[i] - dsldn[i - 1]))) if (val[i] < 50) else dsldn[i - 1]) if (i > 0) else 0)
        valc[i] = (1 if (val[i] > dslup[i]) else 2 if (val[i] < dsldn[i]) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslRSIOfAverage(_MQL5Indicator):
    name = 'Dsl - RSI of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpRsiSignalPeriod': 9,  # Dsl signal period
        'inpMaPeriod': 32,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

