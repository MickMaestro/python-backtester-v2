"""Standard deviation ratio — converted from MQL5: MQL5 Indicators/Standard deviation ratio/Standard deviation ratio.mq5

Standard deviation ratio
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 7451452]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Standard deviation ratio'}, 'levels': [], 'description': ['Standard deviation ratio'], 'name': 'Standard deviation ratio', 'source': 'MQL5 Indicators/Standard deviation ratio/Standard deviation ratio.mq5', 'folder': 'Standard deviation ratio', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 20, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 40, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 20)  # Fast period
inpPeriod2 = _input('inpPeriod2', 40)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ª_shortPeriod = 0
ª_longPeriod = 0

def OnInit():
    global ª_longPeriod, ª_shortPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    ª_shortPeriod = MathMax(MathMin(inpPeriod1, inpPeriod2), 2)
    ª_longPeriod = MathMax(MathMax(inpPeriod1, inpPeriod2), 2)
    if ª_shortPeriod == ª_longPeriod:
        Alert('The periods can not be the same')
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Standard deviation ratio (' + _str(ª_shortPeriod) + ',' + _str(ª_longPeriod) + ')')
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
        val[i] = iStandardDeviationRatio(_price, ª_shortPeriod, ª_longPeriod, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iStandardDeviationRatio(price, shortPeriod, longPeriod, i, bars, _instance=0):
    global _s_iStandardDeviationRatio__arrayError, _s_iStandardDeviationRatio__arrayResizedTo
    if _s_iStandardDeviationRatio__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_s_iStandardDeviationRatio__workArray, _res)
        if _res:
            _s_iStandardDeviationRatio__arrayError = True
        else:
            _s_iStandardDeviationRatio__arrayResizedTo = bars + 500
    _s_iStandardDeviationRatio__workArray[i][_instance] = price
    _s_iStandardDeviationRatio__workArray[i][_instance + 1] = price * price
    if i > shortPeriod:
        _s_iStandardDeviationRatio__workArray[i][_instance + 2] = _s_iStandardDeviationRatio__workArray[i - 1][_instance + 2] + price - _s_iStandardDeviationRatio__workArray[i - shortPeriod][_instance]
        _s_iStandardDeviationRatio__workArray[i][_instance + 3] = _s_iStandardDeviationRatio__workArray[i - 1][_instance + 3] + (price * price) - _s_iStandardDeviationRatio__workArray[i - shortPeriod][_instance + 1]
    else:
        _s_iStandardDeviationRatio__workArray[i][_instance + 2] = _s_iStandardDeviationRatio__workArray[i][_instance]
        _s_iStandardDeviationRatio__workArray[i][_instance + 3] = _s_iStandardDeviationRatio__workArray[i][_instance + 1]
        k = 1
        while k < shortPeriod and i >= k:
            _s_iStandardDeviationRatio__workArray[i][_instance + 2] += _s_iStandardDeviationRatio__workArray[i - k][_instance]
            _s_iStandardDeviationRatio__workArray[i][_instance + 3] += _s_iStandardDeviationRatio__workArray[i - k][_instance + 1]
            k += 1
    if i > longPeriod:
        _s_iStandardDeviationRatio__workArray[i][_instance + 4] = _s_iStandardDeviationRatio__workArray[i - 1][_instance + 4] + price - _s_iStandardDeviationRatio__workArray[i - longPeriod][_instance]
        _s_iStandardDeviationRatio__workArray[i][_instance + 5] = _s_iStandardDeviationRatio__workArray[i - 1][_instance + 5] + (price * price) - _s_iStandardDeviationRatio__workArray[i - longPeriod][_instance + 1]
    else:
        _s_iStandardDeviationRatio__workArray[i][_instance + 4] = _s_iStandardDeviationRatio__workArray[i][_instance]
        _s_iStandardDeviationRatio__workArray[i][_instance + 5] = _s_iStandardDeviationRatio__workArray[i][_instance + 1]
        k = 1
        while k < longPeriod and i >= k:
            _s_iStandardDeviationRatio__workArray[i][_instance + 4] += _s_iStandardDeviationRatio__workArray[i - k][_instance]
            _s_iStandardDeviationRatio__workArray[i][_instance + 5] += _s_iStandardDeviationRatio__workArray[i - k][_instance + 1]
            k += 1
    shortDeviation = MathSqrt(_fdiv(_s_iStandardDeviationRatio__workArray[i][_instance + 3] - _fdiv(_s_iStandardDeviationRatio__workArray[i][_instance + 2] * _s_iStandardDeviationRatio__workArray[i][_instance + 2], float(shortPeriod)), float(shortPeriod)))
    longDeviation = MathSqrt(_fdiv(_s_iStandardDeviationRatio__workArray[i][_instance + 5] - _fdiv(_s_iStandardDeviationRatio__workArray[i][_instance + 4] * _s_iStandardDeviationRatio__workArray[i][_instance + 4], float(longPeriod)), float(longPeriod)))
    return (_fdiv(shortDeviation, longDeviation) if (longDeviation != 0) else 0)

# ---- static local variables
_s_iStandardDeviationRatio__workArray = Arr(0, 0.0, dims=(6,))
_s_iStandardDeviationRatio__arrayError = False
_s_iStandardDeviationRatio__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StandardDeviationRatio(_MQL5Indicator):
    name = 'Standard deviation ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod1': 20,  # Fast period
        'inpPeriod2': 40,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

