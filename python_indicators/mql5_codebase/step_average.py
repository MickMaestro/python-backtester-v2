"""Step average — converted from MQL5: MQL5 Indicators/Step average/Step average.mq5

Step averages
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Step average'}, 'levels': [], 'description': ['Step averages'], 'name': 'Step average', 'source': 'MQL5 Indicators/Step average/Step average.mq5', 'folder': 'Step average', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 14, 'label': 'Average period (<=1 for no average calculation)', 'sinput': False}, {'mql': 'inpMaType', 'py': 'inpMaType', 'param': 'inpMaType', 'type': 'int', 'default': 1, 'label': 'Average type', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStepSize', 'py': 'inpStepSize', 'param': 'inpStepSize', 'type': 'double', 'default': 2.5, 'label': 'Step size (in pips)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 14)  # Average period (<=1 for no average calculation)
inpMaType = _input('inpMaType', MODE_EMA)  # Average type
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpStepSize = _input('inpStepSize', 2.5)  # Step size (in pips)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
average = Arr(0, 0.0)
_ub9__stepSize = 0.0
_ub9__hma = 0
_ub9__maPeriod = 0
_stepValWork = Arr(6, 0.0, dyn=False, dims=(1,))

def OnInit():
    global _ub9__hma, _ub9__maPeriod, _ub9__stepSize
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, average, INDICATOR_CALCULATIONS)
    _ub9__stepSize = inpStepSize * Point() * MathPow(10, _imod(Digits(), 2))
    _ub9__maPeriod = MathMax(inpMaPeriod, 1)
    _ub9__hma = iMA(Symbol(), 0, _ub9__maPeriod, 0, inpMaType, inpPrice)
    if not _checkHandle(_ub9__hma, 'Moving average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Step average (' + _str(inpMaPeriod) + ',' + _str(inpStepSize) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_ub9__hma, 0, 0, _copyCount, average) != _copyCount:
        Comment('Error copying average')
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if average[i] == EMPTY_VALUE:
            average[i] = close[i]
        val[i] = iStepVal(average[i], _ub9__stepSize, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iStepVal(value, stepSize, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 1
    if i > 0 and stepSize > 0:
        _indP = _imod(i - 1, 6)
        _diff = value - _stepValWork[_indP][_inst]
        _stepValWork[_indC][_inst] = _stepValWork[_indP][_inst] + (0 if (_diff < stepSize and _diff > (-stepSize)) else (_int(_fdiv(_diff, stepSize)) * stepSize))
    else:
        _stepValWork[_indC][_inst] = ((MathRound(_fdiv(value, stepSize)) * stepSize) if (stepSize > 0) else value)
    return _stepValWork[_indC][_inst]

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


class StepAverage(_MQL5Indicator):
    name = 'Step average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 14,  # Average period (<=1 for no average calculation)
        'inpMaType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average type
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStepSize': 2.5,  # Step size (in pips)
    }

