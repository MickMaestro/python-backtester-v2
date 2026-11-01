"""Corrected super smoother — converted from MQL5: MQL5 Indicators/Corrected super smoother/Corrected super smoother.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 8, 3: 8}, 'colors': {1: [8421504], 2: [11119017, 3329330, 36095], 3: [11119017, 3329330, 36095]}, 'widths': {1: 6, 3: 2}, 'styles': {2: 2}, 'labels': {1: 'Shadow', 2: 'Super smoother', 3: 'Corrected Super smoother'}, 'levels': [], 'description': [], 'name': 'Corrected super smoother', 'source': 'MQL5 Indicators/Corrected super smoother/Corrected super smoother.mq5', 'folder': 'Corrected super smoother', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
workCorrMa = Arr(5, 0.0, dyn=False, dims=(5,))
workSsm = Arr(10, 0.0, dyn=False, dims=(2,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, avg, INDICATOR_DATA)
    SetIndexBuffer(2, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Corrected super smoother (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i)
        avg[i] = iSuperSmoother(_price, inpPeriod, i)
        val[i] = iCorrMaEmaDev(avg[i], _price, _int(inpPeriod), i)
        valc[i] = ((1 if (val[i] < avg[i]) else 2 if (val[i] > avg[i]) else valc[i - 1]) if (i > 0) else 0)
        avgc[i] = valc[i]
        vals[i] = val[i]
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

def iSuperSmoother(price, period, i, instance=0):
    _indC = _imod(i, 10)
    _inst = instance * 2
    if i > 1 and period > 1:
        if ArrayRange(workSsmCoeffs, 0) < (instance + 1):
            ArrayResize(workSsmCoeffs, instance + 1)
            workSsmCoeffs[instance][0] = -99.0
        if workSsmCoeffs[instance][0] != period:
            a1 = MathExp(_fdiv(-1.414 * M_PI, period))
            b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, period))
            workSsmCoeffs[instance][2] = b1
            workSsmCoeffs[instance][3] = (-a1) * a1
            workSsmCoeffs[instance][1] = 1.0 - workSsmCoeffs[instance][2] - workSsmCoeffs[instance][3]
            workSsmCoeffs[instance][0] = period
        _indO = _imod(i - 2, 10)
        _indP = _imod(i - 1, 10)
        workSsm[_indC][_inst + 0] = price
        workSsm[_indC][_inst + 1] = ((workSsmCoeffs[instance][1] * (price + workSsm[_indP][_inst + 0])) / 2.0) + (workSsmCoeffs[instance][2] * workSsm[_indP][_inst + 1]) + (workSsmCoeffs[instance][3] * workSsm[_indO][_inst + 1])
    else:
        for k in range(0, 2):
            workSsm[_indC][_inst + k] = price
    return workSsm[_indC][_inst + 1]

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


class CorrectedSuperSmoother(_MQL5Indicator):
    name = 'Corrected super smoother'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

