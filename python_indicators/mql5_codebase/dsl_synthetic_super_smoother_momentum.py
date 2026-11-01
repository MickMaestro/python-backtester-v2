"""DSL synthetic super smoother momentum — converted from MQL5: MQL5 Indicators/DSL synthetic super smoother momentum/DSL synthetic super smoother momentum.mq5

Discontinued signal line super smoother synthetic momentum
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [14474460, 14474460], 2: [8421504], 3: [8421504], 4: [11119017, 16748574, 9639167]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'no trend zone', 2: 'no trend zone up', 3: 'no trend zone down', 4: 'Momentum'}, 'levels': [], 'description': ['Discontinued signal line super smoother synthetic momentum'], 'name': 'DSL synthetic super smoother momentum', 'source': 'MQL5 Indicators/DSL synthetic super smoother momentum/DSL synthetic super smoother momentum.mq5', 'folder': 'DSL synthetic super smoother momentum', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 5, 'label': 'Period 1', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 20, 'label': 'Period 2', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 50, 'label': 'Period 3', 'sinput': False}, {'mql': 'inpPeriod4', 'py': 'inpPeriod4', 'param': 'inpPeriod4', 'type': 'int', 'default': 100, 'label': 'Period 4', 'sinput': False}, {'mql': 'inpPeriod5', 'py': 'inpPeriod5', 'param': 'inpPeriod5', 'type': 'int', 'default': 200, 'label': 'Period 5', 'sinput': False}, {'mql': 'inpSignal', 'py': 'inpSignal', 'param': 'inpSignal', 'type': 'int', 'default': 20, 'label': 'DSL signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 5)  # Period 1
inpPeriod2 = _input('inpPeriod2', 20)  # Period 2
inpPeriod3 = _input('inpPeriod3', 50)  # Period 3
inpPeriod4 = _input('inpPeriod4', 100)  # Period 4
inpPeriod5 = _input('inpPeriod5', 200)  # Period 5
inpSignal = _input('inpSignal', 20)  # DSL signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
dslup = Arr(0, 0.0)
dsldn = Arr(0, 0.0)
dslupl = Arr(0, 0.0)
dsldnl = Arr(0, 0.0)
workSsm = Arr(6, 0.0, dyn=False, dims=(14,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, dslup, INDICATOR_DATA)
    SetIndexBuffer(1, dsldn, INDICATOR_DATA)
    SetIndexBuffer(2, dslupl, INDICATOR_DATA)
    SetIndexBuffer(3, dsldnl, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DSL Synthetic super smoother momentum (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ',' + _str(inpPeriod4) + ',' + _str(inpPeriod5) + ',' + _str(inpSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _coeff1 = float(_idiv(inpPeriod5, inpPeriod4))
    _coeff2 = float(_idiv(inpPeriod5, inpPeriod3))
    _coeff3 = float(_idiv(inpPeriod5, inpPeriod2))
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        _avg = iSuperSmoother(_price, inpPeriod1, i, 0)
        _avg1 = iSuperSmoother(_price, inpPeriod2, i, 1)
        _mom1 = _fdiv(100.0 * (_avg - _avg1), _avg1)
        _avg2 = iSuperSmoother(_price, inpPeriod3, i, 2)
        _mom2 = _fdiv(100.0 * (_avg - _avg2), _avg2)
        _avg3 = iSuperSmoother(_price, inpPeriod4, i, 3)
        _mom3 = _fdiv(100.0 * (_avg - _avg3), _avg3)
        _avg4 = iSuperSmoother(_price, inpPeriod5, i, 4)
        _mom4 = _fdiv(100.0 * (_avg - _avg4), _avg4)
        val[i] = (_mom4 + (_mom3 * _coeff1) + (_mom2 * _coeff2) + (_mom1 * _coeff3)) / 4.0
        dslup[i] = iSuperSmoother(val[i], inpSignal, i, 5, val[i] < 0)
        dslupl[i] = dslup[i]
        dsldn[i] = iSuperSmoother(val[i], inpSignal, i, 6, val[i] > 0)
        dsldnl[i] = dsldn[i]
        valc[i] = (1 if (val[i] > dslupl[i]) else 2 if (val[i] < dsldnl[i]) else 0)
        i += 1
    return i

def iSuperSmoother(price, period, i, instance=0, copy=False):
    _indP = _imod(i - 1, 6)
    _indC = _imod(i, 6)
    _inst = instance * 2
    if ((not copy) and i > 1) and period > 1:
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
        _indO = _imod(i - 2, 6)
        workSsm[_indC][_inst + 0] = price
        workSsm[_indC][_inst + 1] = ((workSsmCoeffs[instance][1] * (price + workSsm[_indP][_inst + 0])) / 2.0) + (workSsmCoeffs[instance][2] * workSsm[_indP][_inst + 1]) + (workSsmCoeffs[instance][3] * workSsm[_indO][_inst + 1])
    else:
        for k in range(0, 2):
            workSsm[_indC][_inst + k] = (workSsm[_indP][_inst + k] if (i > 0) else price)
    return workSsm[_indC][_inst + 1]

def getPrice(tprice, open, close, high, low, i):
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


class DSLSyntheticSuperSmootherMomentum(_MQL5Indicator):
    name = 'DSL synthetic super smoother momentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 5,  # Period 1
        'inpPeriod2': 20,  # Period 2
        'inpPeriod3': 50,  # Period 3
        'inpPeriod4': 100,  # Period 4
        'inpPeriod5': 200,  # Period 5
        'inpSignal': 20,  # DSL signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

