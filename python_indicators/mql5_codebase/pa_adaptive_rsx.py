"""PA adaptive RSX — converted from MQL5: MQL5 Indicators/Phase accumulation adaptive RSX/PA adaptive RSX.mq5

Phase accumulation adaptive RSX
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsx'}, 'levels': [], 'description': ['Phase accumulation adaptive RSX'], 'name': 'PA adaptive RSX', 'source': 'MQL5 Indicators/Phase accumulation adaptive RSX/PA adaptive RSX.mq5', 'folder': 'Phase accumulation adaptive RSX', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 1.0, 'label': 'PA cycles to reach', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 0.0, 'label': 'PA cycles filter (<=1 for no filtering)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 1.0)  # PA cycles to reach
inpFilter = _input('inpFilter', 0.0)  # PA cycles filter (<=1 for no filtering)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ª_cycleFilter = 0.0
workRsx = Arr(6, 0.0, dyn=False, dims=(13,))
_workHil = Arr(0, 0.0, dims=(9,))

def OnInit():
    global ª_cycleFilter
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    ª_cycleFilter = (inpFilter if (inpFilter > 1) else 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Phase accumulation adaptive RSX (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        val[i] = iRsx(_price, iHilbertPhase(_price, ª_cycleFilter, inpPeriod, i, rates_total), i, 0)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

def iRsx(price, period, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 13
    workRsx[_indC][_inst] = price
    res = 50.0
    if i > 0 and period >= 1:
        _indP = _imod(i - 1, 6)
        Kg = _fdiv(3.0, 2.0 + period)
        Hg = 1.0 - Kg
        mom = workRsx[_indC][_inst] - workRsx[_indP][_inst]
        moa = ((-mom) if (mom < 0) else mom)
        k = 0
        kk = _inst + 1
        while k < 3:
            workRsx[_indC][kk] = (Kg * mom) + (Hg * workRsx[_indP][kk])
            workRsx[_indC][kk + 1] = (Kg * workRsx[_indC][kk]) + (Hg * workRsx[_indP][kk + 1])
            mom = (1.5 * workRsx[_indC][kk]) - (0.5 * workRsx[_indC][kk + 1])
            workRsx[_indC][kk + 2] = (Kg * moa) + (Hg * workRsx[_indP][kk + 2])
            workRsx[_indC][kk + 3] = (Kg * workRsx[_indC][kk + 2]) + (Hg * workRsx[_indP][kk + 3])
            moa = (1.5 * workRsx[_indC][kk + 2]) - (0.5 * workRsx[_indC][kk + 3])
            k += 1
            kk += 4
        res = (_fdiv(mom, (moa if (moa > DBL_MIN) else DBL_MIN)) + 1.0) * 50.0
    else:
        for k in range(1, 13):
            workRsx[_indC][_inst + k] = 0.0
    return ((res if (res < 100) else 100) if (res > 0) else 0)

def iHilbertPhase(price, filter_, cyclesToReach, i, bars, _inst=0):
    global _s_iHilbertPhase__arrayError, _s_iHilbertPhase__arrayResizedTo
    if _s_iHilbertPhase__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_workHil, _res)
        if _res:
            _s_iHilbertPhase__arrayError = True
        else:
            _s_iHilbertPhase__arrayResizedTo = bars + 500
    if _s_iHilbertPhase__arrayError:
        return 0.0
    _inst *= 9
    _workHil[i][_inst] = price
    if i < 6:
        _workHil[i][_inst + 4] = 1.0
        _workHil[i][_inst + 3] = 1.0
        _workHil[i][_inst + 6] = 7.0
        _workHil[i][_inst + 8] = price
        _workHil[i][_inst + 7] = _workHil[i][_inst + 8]
        _workHil[i][_inst + 1] = _workHil[i][_inst + 7]
        return 1.0
    cyclesToReach *= 360.0
    _workHil[i][_inst + 1] = ((4.0 * _workHil[i][_inst]) + (3.0 * _workHil[i - 1][_inst]) + (2.0 * _workHil[i - 2][_inst]) + _workHil[i - 3][_inst]) / 10.0
    _workHil[i][_inst + 2] = ((0.0962 * _workHil[i][_inst + 1]) + (0.5769 * _workHil[i - 2][_inst + 1]) - (0.5769 * _workHil[i - 4][_inst + 1]) - (0.0962 * _workHil[i - 6][_inst + 1])) * ((0.075 * _workHil[i - 1][_inst + 3]) + 0.54)
    _workHil[i][_inst + 7] = (0.15 * (((0.0962 * _workHil[i][_inst + 2]) + (0.5769 * _workHil[i - 2][_inst + 2]) - (0.5769 * _workHil[i - 4][_inst + 2]) - (0.0962 * _workHil[i - 6][_inst + 2])) * ((0.075 * _workHil[i - 1][_inst + 3]) + 0.54))) + (0.85 * _workHil[i - 1][_inst + 7])
    _workHil[i][_inst + 8] = (0.15 * _workHil[i - 3][_inst + 2]) + (0.85 * _workHil[i - 1][_inst + 8])
    _workHil[i][_inst + 5] = _workHil[i - 1][_inst + 5]
    _workHil[i][_inst + 4] = _workHil[i - 1][_inst + 4]
    if MathAbs(_workHil[i][_inst + 8]) > 0:
        _workHil[i][_inst + 5] = (180.0 / M_PI) * MathArctan(MathAbs(_fdiv(_workHil[i][_inst + 7], _workHil[i][_inst + 8])))
    if _workHil[i][_inst + 8] < 0 and _workHil[i][_inst + 7] > 0:
        _workHil[i][_inst + 5] = 180.0 - _workHil[i][_inst + 5]
    if _workHil[i][_inst + 8] < 0 and _workHil[i][_inst + 7] < 0:
        _workHil[i][_inst + 5] = 180.0 + _workHil[i][_inst + 5]
    if _workHil[i][_inst + 8] > 0 and _workHil[i][_inst + 7] < 0:
        _workHil[i][_inst + 5] = 360.0 - _workHil[i][_inst + 5]
    _workHil[i][_inst + 6] = _workHil[i - 1][_inst + 5] - _workHil[i][_inst + 5]
    if _workHil[i - 1][_inst + 5] < 90.0 and _workHil[i][_inst + 5] > 270.0:
        _workHil[i][_inst + 6] = 360.0 + _workHil[i - 1][_inst + 5] - _workHil[i][_inst + 5]
    if _workHil[i][_inst + 6] > 60.0:
        _workHil[i][_inst + 6] = 60.0
    if _workHil[i][_inst + 6] < 7.0:
        _workHil[i][_inst + 6] = 7.0
    phaseSum = _workHil[i][_inst + 6]
    k = 1
    while phaseSum < cyclesToReach and i >= k:
        phaseSum += _workHil[i - k][_inst + 6]
        k += 1
    _workHil[i][_inst + 4] = k
    _workHil[i][_inst + 3] = _workHil[i - 1][_inst + 3] + (_fdiv(2.0, 1.0 + filter_) * (_workHil[i][_inst + 4] - _workHil[i - 1][_inst + 3]))
    return _workHil[i][_inst + 3]

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

# ---- static local variables
_s_iHilbertPhase__arrayError = False
_s_iHilbertPhase__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PAAdaptiveRSX(_MQL5Indicator):
    name = 'PA adaptive RSX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 1.0,  # PA cycles to reach
        'inpFilter': 0.0,  # PA cycles filter (<=1 for no filtering)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

