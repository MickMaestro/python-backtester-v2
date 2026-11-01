"""Step VHF adaptive VMA — converted from MQL5: MQL5 Indicators/Step VHF adaptive VMA/Step VHF adaptive VMA.mq5

Step VHF adaptive VMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [8421504], 2: [11119017, 7451452, 9639167]}, 'widths': {1: 6, 2: 2}, 'styles': {}, 'labels': {1: 'Shadow', 2: 'Step VMA'}, 'levels': [], 'description': ['Step VHF adaptive VMA'], 'name': 'Step VHF adaptive VMA', 'source': 'MQL5 Indicators/Step VHF adaptive VMA/Step VHF adaptive VMA.mq5', 'folder': 'Step VHF adaptive VMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'VMA period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 0, 'label': 'VHF period (<=1 for same as VMA period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStepSize', 'py': 'inpStepSize', 'param': 'inpStepSize', 'type': 'double', 'default': 1.0, 'label': 'Step size (pips)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # VMA period
inpPeriod2 = _input('inpPeriod2', 0)  # VHF period (<=1 for same as VMA period)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpStepSize = _input('inpStepSize', 1.0)  # Step size (pips)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_alpha = 0.0
ª_stepSize = 0.0
ª_adpPeriod = 0

def OnInit():
    global ª_adpPeriod, ª_alpha, ª_stepSize
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, avg, INDICATOR_CALCULATIONS)
    ª_adpPeriod = (inpPeriod if (inpPeriod2 <= 1) else inpPeriod2)
    ª_alpha = _fdiv(2.0, 1.0 + inpPeriod)
    ª_stepSize = (inpStepSize if (inpStepSize > 0) else 0) * Point() * MathPow(10, _imod(Digits(), 2))
    IndicatorSetString(INDICATOR_SHORTNAME, 'VMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        avg[i] = ((avg[i - 1] + (ª_alpha * iVhf(ª_adpPeriod, close, i, rates_total) * 2.0 * (_price - avg[i - 1]))) if (i > 0) else _price)
        if i > 0 and ª_stepSize > 0:
            _diff = avg[i] - val[i - 1]
            val[i] = val[i - 1] + (0 if (_diff < ª_stepSize and _diff > (-ª_stepSize)) else (_int(_fdiv(_diff, ª_stepSize)) * ª_stepSize))
        else:
            val[i] = ((MathRound(_fdiv(avg[i], ª_stepSize)) * ª_stepSize) if (ª_stepSize > 0) else avg[i])
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        vals[i] = val[i]
        i += 1
    return i

def iVhf(period, price, i, bars, _instance=0):
    global _s_iVhf__arrayError, _s_iVhf__arrayResizedTo
    if _s_iVhf__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_s_iVhf__workArray, bars + 500)
        if _res:
            _s_iVhf__arrayError = True
        else:
            _s_iVhf__arrayResizedTo = bars + 500
    _s_iVhf__workArray[i][_instance + 1] = (((price[i] - price[i - 1]) if (price[i] > price[i - 1]) else (price[i - 1] - price[i])) if (i > 0) else 0)
    if i > period:
        _s_iVhf__workArray[i][_instance] = _s_iVhf__workArray[i - 1][_instance] - _s_iVhf__workArray[i - period][_instance + 1] + _s_iVhf__workArray[i][_instance + 1]
    else:
        _s_iVhf__workArray[i][_instance] = _s_iVhf__workArray[i][_instance + 1]
        k = 1
        while k < period and i >= k:
            _s_iVhf__workArray[i][_instance] += _s_iVhf__workArray[i - k][_instance + 1]
            k += 1
    start = i - period + 1
    if start < 0:
        start = 0
    max_ = price[ArrayMaximum(price, start, period)]
    min_ = price[ArrayMinimum(price, start, period)]
    return (_fdiv(max_ - min_, _s_iVhf__workArray[i][_instance]) if (_s_iVhf__workArray[i][_instance] != 0) else 0)

# ---- static local variables
_s_iVhf__workArray = Arr(0, 0.0, dims=(2,))
_s_iVhf__arrayError = False
_s_iVhf__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepVHFAdaptiveVMA(_MQL5Indicator):
    name = 'Step VHF adaptive VMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # VMA period
        'inpPeriod2': 0,  # VHF period (<=1 for same as VMA period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStepSize': 1.0,  # Step size (pips)
    }

