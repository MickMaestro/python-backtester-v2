"""CCI - T3 based - fl — converted from MQL5: MQL5 Indicators/CCI T3 based with floating levels/CCI - T3 based - fl.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256], 4: [12632256, 3329330, 42495]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'middle level', 4: 'value'}, 'levels': [], 'description': [], 'name': 'CCI - T3 based - fl', 'source': 'MQL5 Indicators/CCI T3 based with floating levels/CCI - T3 based - fl.mq5', 'folder': 'CCI T3 based with floating levels', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 "hot"', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothT3Hot', 'py': 'inpSmoothT3Hot', 'param': 'inpSmoothT3Hot', 'type': 'double', 'default': 0.7, 'label': 'Smoothing T3 "hot"', 'sinput': False}, {'mql': 'inpSmoothT3Type', 'py': 'inpSmoothT3Type', 'param': 'inpSmoothT3Type', 'type': 'int', 'default': 1, 'label': 'Smoothing T3 type', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 32, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpCciPrice = _input('inpCciPrice', PRICE_TYPICAL)  # Price
inpT3Hot = _input('inpT3Hot', 0.7)  # T3 "hot"
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
inpSmoothPeriod = _input('inpSmoothPeriod', 10)  # Smoothing period
inpSmoothT3Hot = _input('inpSmoothT3Hot', 0.7)  # Smoothing T3 "hot"
inpSmoothT3Type = _input('inpSmoothT3Type', t3_fulksmat)  # Smoothing T3 type
inpFlPeriod = _input('inpFlPeriod', 32)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 80.0)  # Up level %
inpFlLevelDown = _input('inpFlLevelDown', 20.0)  # Down level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
workT3 = Arr(5, 0.0, dyn=False, dims=(12,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))
workEmaDeviation = Arr(5, 0.0, dyn=False, dims=(2,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, levelMi, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI - T3 based - fl (' + _str(inpCciPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = iT3(getPrice(inpCciPrice, open, close, high, low, i, rates_total), inpSmoothPeriod, inpSmoothT3Hot, inpSmoothT3Type == t3_tillson, i, 1)
        avg = iT3(_price, inpCciPeriod, inpT3Hot, inpT3Type == t3_tillson, i, 0)
        dev = MathMax(iEmaDeviation(_price, inpCciPeriod, i), DBL_MIN)
        val[i] = _fdiv(_price - avg, 0.015 * dev)
        _start = MathMax(i - inpFlPeriod + 1, 0)
        min_ = val[ArrayMinimum(val, _start, inpFlPeriod)]
        max_ = val[ArrayMaximum(val, _start, inpFlPeriod)]
        range_ = max_ - min_
        levelUp[i] = min_ + ((inpFlLevelUp * range_) / 100.0)
        levelDn[i] = min_ + ((inpFlLevelDown * range_) / 100.0)
        levelMi[i] = min_ + ((50 * range_) / 100.0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, hot, original, i, instance=0):
    if ArrayRange(workT3Coeffs, 0) < (instance + 1):
        ArrayResize(workT3Coeffs, instance + 1)
    if workT3Coeffs[instance][0] != period:
        workT3Coeffs[instance][0] = period
        workT3Coeffs[instance][1] = (-hot) * hot * hot
        workT3Coeffs[instance][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instance][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instance][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        workT3Coeffs[instance][5] = (_fdiv(2.0, 1.0 + period) if original else _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0)))
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 6
    for k in range(0, 6):
        workT3[_indC][k + _inst] = (workT3[_indP][k + _inst] if (i > 0) else price)
    if i > 0 and period > 1:
        workT3[_indC][_inst] = workT3[_indP][_inst] + (workT3Coeffs[instance][5] * (price - workT3[_indP][_inst]))
        workT3[_indC][_inst + 1] = workT3[_indP][_inst + 1] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst] - workT3[_indP][_inst + 1]))
        workT3[_indC][_inst + 2] = workT3[_indP][_inst + 2] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 1] - workT3[_indP][_inst + 2]))
        workT3[_indC][_inst + 3] = workT3[_indP][_inst + 3] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 2] - workT3[_indP][_inst + 3]))
        workT3[_indC][_inst + 4] = workT3[_indP][_inst + 4] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 3] - workT3[_indP][_inst + 4]))
        workT3[_indC][_inst + 5] = workT3[_indP][_inst + 5] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 4] - workT3[_indP][_inst + 5]))
    return (workT3Coeffs[instance][1] * workT3[_indC][_inst + 5]) + (workT3Coeffs[instance][2] * workT3[_indC][_inst + 4]) + (workT3Coeffs[instance][3] * workT3[_indC][_inst + 3]) + (workT3Coeffs[instance][4] * workT3[_indC][_inst + 2])

def iEmaDeviation(price, period, i, instanceNo=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    instanceNo *= 2
    workEmaDeviation[_indC][instanceNo + 0] = price
    workEmaDeviation[_indC][instanceNo + 1] = price
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workEmaDeviation[_indC][instanceNo + 0] = workEmaDeviation[_indP][instanceNo + 0] + (alpha * (price - workEmaDeviation[_indP][instanceNo + 0]))
        workEmaDeviation[_indC][instanceNo + 1] = workEmaDeviation[_indP][instanceNo + 1] + (alpha * ((price * price) - workEmaDeviation[_indP][instanceNo + 1]))
    return MathSqrt(_fdiv(period * (workEmaDeviation[_indC][instanceNo + 1] - (workEmaDeviation[_indC][instanceNo + 0] * workEmaDeviation[_indC][instanceNo + 0])), MathMax(period - 1, 1)))

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIT3BasedFl(_MQL5Indicator):
    name = 'CCI - T3 based - fl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpT3Hot': 0.7,  # T3 "hot"
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # T3 type
        'inpSmoothPeriod': 10,  # Smoothing period
        'inpSmoothT3Hot': 0.7,  # Smoothing T3 "hot"
        'inpSmoothT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # Smoothing T3 type
        'inpFlPeriod': 32,  # Floating levels period
        'inpFlLevelUp': 80.0,  # Up level %
        'inpFlLevelDown': 20.0,  # Down level %
    }

