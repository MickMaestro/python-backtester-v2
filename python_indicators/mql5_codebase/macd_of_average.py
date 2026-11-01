"""MACD of average — converted from MQL5: MQL5 Indicators/MACD of average/MACD of average.mq5

MACD of average
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [255]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'MACD of average', 2: 'MACD of average'}, 'levels': [], 'description': ['MACD of average'], 'name': 'MACD of average', 'source': 'MQL5 Indicators/MACD of average/MACD of average.mq5', 'folder': 'MACD of average', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'MACD signal period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 5, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
color_onSlope = 0
color_onSignal = 1
_enum('enColorOn', {0: 'color_onSlope', 1: 'color_onSignal'})

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # MACD signal period
inpMaPeriod = _input('inpMaPeriod', 5)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', color_onSignal)  # Color change on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
_maHandle = 0
_macdHandle = 0

def OnInit():
    global _maHandle, _macdHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    _macdHandle = iMACD(Symbol(), 0, inpFastPeriod, inpSlowPeriod, inpSignalPeriod, _maHandle)
    if _macdHandle == INVALID_HANDLE:
        IndicatorRelease(_maHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ',' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_macdHandle) < rates_total:
        return prev_calculated
    _macdVal = Arr(1, 0.0, dyn=False)
    _signVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _macdCopied = CopyBuffer(_macdHandle, 0, _DT(time[i]), 1, _macdVal)
        _signCopied = CopyBuffer(_macdHandle, 1, _DT(time[i]), 1, _signVal)
        val[i] = (_macdVal[0] if (_macdCopied == 1 and _signCopied) else EMPTY_VALUE)
        signal[i] = (_signVal[0] if (_macdCopied == 1 and _signCopied) else EMPTY_VALUE)
        if inpColorOn == color_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDOfAverage(_MQL5Indicator):
    name = 'MACD of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpSignalPeriod': 9,  # MACD signal period
        'inpMaPeriod': 5,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on MACD slope change', 1: 'Change color on MACD crossing signal line'}, default=1),  # Color change on :
    }

