"""Corrected T3 (ema deviation) — converted from MQL5: MQL5 Indicators/Corrected T3 - EMA deviations/Corrected T3 (ema deviation).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 3937500, 32768], 2: [11119017, 3937500, 32768]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'T3', 2: 'Corrected T3'}, 'levels': [], 'description': [], 'name': 'Corrected T3 (ema deviation)', 'source': 'MQL5 Indicators/Corrected T3 - EMA deviations/Corrected T3 (ema deviation).mq5', 'folder': 'Corrected T3 - EMA deviations', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 10.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpHot', 'py': 'inpHot', 'param': 'inpHot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 10.0)  # Period
inpHot = _input('inpHot', 0.7)  # T3 hot
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
workCorrMa = Arr(5, 0.0, dyn=False, dims=(5,))
workT3 = Arr(5, 0.0, dyn=False, dims=(12,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Corrected T3 (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _original = inpT3Type == t3_tillson
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i)
        avg[i] = iT3(_price, inpPeriod, inpHot, _original, i)
        val[i] = iCorrMaEmaDev(avg[i], _price, _int(inpPeriod), i)
        valc[i] = ((2 if (val[i] < avg[i]) else 1 if (val[i] > avg[i]) else valc[i - 1]) if (i > 0) else 0)
        avgc[i] = valc[i]
    return rates_total

def iCorrMaEmaDev(_avg, price, period, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 5
    workCorrMa[_indC][_inst + 1] = _avg
    workCorrMa[_indC][_inst + 0] = price
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workCorrMa[_indC][_inst + 3] = workCorrMa[_indP][_inst + 3] + (alpha * (price - workCorrMa[_indP][_inst + 3]))
        workCorrMa[_indC][_inst + 4] = workCorrMa[_indP][_inst + 4] + (alpha * ((price * price) - workCorrMa[_indP][_inst + 4]))
    else:
        for k in range(3, 5):
            workCorrMa[_indC][_inst + k] = price
    _deviation = MathMax(MathSqrt(_fdiv(period * (workCorrMa[_indC][_inst + 4] - (workCorrMa[_indC][_inst + 3] * workCorrMa[_indC][_inst + 3])), MathMax(period - 1, 1))), DBL_MIN)
    v1 = MathPow(_deviation, 2)
    v2 = (MathPow(workCorrMa[_indP][_inst + 2] - workCorrMa[_indC][_inst + 1], 2) if (i > 0) else 0)
    c = (0 if (v2 < v1 or v2 == 0) else (1 - _fdiv(v1, v2)))
    workCorrMa[_indC][_inst + 2] = ((workCorrMa[_indP][_inst + 2] + (c * (workCorrMa[_indC][_inst + 1] - workCorrMa[_indP][_inst + 2]))) if (i > 0) else workCorrMa[_indC][_inst + 1])
    return workCorrMa[_indC][_inst + 2]

def iT3(price, period, hot, original, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 6
    if ArrayRange(workT3Coeffs, 0) < (instance + 1):
        ArrayResize(workT3Coeffs, instance + 1)
        workT3Coeffs[instance][0] = -99.0
    if workT3Coeffs[instance][0] != period:
        workT3Coeffs[instance][0] = period
        workT3Coeffs[instance][1] = (-hot) * hot * hot
        workT3Coeffs[instance][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instance][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instance][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        workT3Coeffs[instance][5] = (_fdiv(2.0, 1.0 + period) if original else _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0)))
    if i > 0 and period > 1:
        workT3[_indC][_inst] = workT3[_indP][_inst] + (workT3Coeffs[instance][5] * (price - workT3[_indP][_inst]))
        workT3[_indC][1 + _inst] = workT3[_indP][1 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][0 + _inst] - workT3[_indP][1 + _inst]))
        workT3[_indC][2 + _inst] = workT3[_indP][2 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][1 + _inst] - workT3[_indP][2 + _inst]))
        workT3[_indC][3 + _inst] = workT3[_indP][3 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][2 + _inst] - workT3[_indP][3 + _inst]))
        workT3[_indC][4 + _inst] = workT3[_indP][4 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][3 + _inst] - workT3[_indP][4 + _inst]))
        workT3[_indC][5 + _inst] = workT3[_indP][5 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][4 + _inst] - workT3[_indP][5 + _inst]))
    else:
        for k in range(0, 6):
            workT3[_indC][k + _inst] = price
    return (workT3Coeffs[instance][1] * workT3[_indC][_inst + 5]) + (workT3Coeffs[instance][2] * workT3[_indC][_inst + 4]) + (workT3Coeffs[instance][3] * workT3[_indC][_inst + 3]) + (workT3Coeffs[instance][4] * workT3[_indC][_inst + 2])

def getPrice(tprice, open, close, high, low, i):
    if i >= 0:
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


class CorrectedT3EmaDeviation(_MQL5Indicator):
    name = 'Corrected T3 (ema deviation)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 10.0,  # Period
        'inpHot': 0.7,  # T3 hot
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # T3 type
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

