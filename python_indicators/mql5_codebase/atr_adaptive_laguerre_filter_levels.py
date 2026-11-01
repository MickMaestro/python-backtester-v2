"""ATR adaptive Laguerre filter levels — converted from MQL5: MQL5 Indicators/ATR adaptive Laguerre filter - levels/ATR adaptive Laguerre filter levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329434, 9662683], 2: [3329330], 3: [9639167], 4: [12632256, 7451452, 9639167]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'filling', 2: 'up level', 3: 'down level', 4: 'Laguerre filter'}, 'levels': [], 'description': [], 'name': 'ATR adaptive Laguerre filter levels', 'source': 'MQL5 Indicators/ATR adaptive Laguerre filter - levels/ATR adaptive Laguerre filter levels.mq5', 'folder': 'ATR adaptive Laguerre filter - levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPeriodl', 'py': 'inpPeriodl', 'param': 'inpPeriodl', 'type': 'double', 'default': 0.0, 'label': 'Levels period (<=1 for same as filter period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDisplay', 'py': 'inpDisplay', 'param': 'inpDisplay', 'type': 'int', 'default': 0, 'label': 'Filled zones display :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayFill
fill_display = 0
fill_dont = 1
_enum('enDisplayFill', {0: 'fill_display', 1: 'fill_dont'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPeriodl = _input('inpPeriodl', 0.0)  # Levels period (<=1 for same as filter period)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDisplay = _input('inpDisplay', fill_display)  # Filled zones display :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
atr = Arr(0, 0.0)
_levelsPeriod = 0.0
_atrHandle = 0
_atrPeriod = 0
workLagFil = Arr(6, 0.0, dyn=False, dims=(12,))

def OnInit():
    global _atrHandle, _atrPeriod, _levelsPeriod
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelDn, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, atr, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    _atrPeriod = MathMax(_int(inpPeriod), 1)
    _atrHandle = iATR(Symbol(), 0, _atrPeriod)
    if not _checkHandle(_atrHandle):
        return INIT_FAILED
    _levelsPeriod = (inpPeriod if (inpPeriodl <= 1) else inpPeriodl)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre filter levels (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_atrHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_atrHandle, 0, 0, _copyCount, atr) != _copyCount:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - _atrPeriod + 1, 0)
        _max = atr[ArrayMaximum(atr, _start, _atrPeriod)]
        _min = atr[ArrayMinimum(atr, _start, _atrPeriod)]
        _coeff = ((1 - _fdiv(atr[i] - _min, _max - _min)) if (_min != _max) else 0.5)
        _coeff = (_coeff + 1.0) / 2.0
        val[i] = iLaGuerreFil(getPrice(inpPrice, open, close, high, low, i), inpPeriod * _coeff, i, 0)
        _levelUp = iLaGuerreFil(val[i], _levelsPeriod * _coeff, i, 1, ((not (val[i] > levelDn[i - 1])) if (i > 0) else False))
        _levelDn = iLaGuerreFil(val[i], _levelsPeriod * _coeff, i, 2, ((not (val[i] < levelUp[i - 1])) if (i > 0) else False))
        levelUp[i] = MathMax(_levelUp, _levelDn)
        levelDn[i] = MathMin(_levelUp, _levelDn)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        fillu[i] = (EMPTY_VALUE if (inpDisplay == fill_dont) else val[i])
        filld[i] = (EMPTY_VALUE if (inpDisplay == fill_dont) else val[i] if (valc[i] == 0) else levelUp[i] if (valc[i] == 1) else levelDn[i])
        i += 1
    return i

def iLaGuerreFil(price, period, i, instance=0, copy=False):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    _inst = instance * 4
    if ((not copy) and i > 0) and period > 1:
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        workLagFil[_indC][_inst] = price + (_gamma * (workLagFil[_indP][_inst] - price))
        workLagFil[_indC][_inst + 1] = workLagFil[_indP][_inst] + (_gamma * (workLagFil[_indP][_inst + 1] - workLagFil[_indC][_inst]))
        workLagFil[_indC][_inst + 2] = workLagFil[_indP][_inst + 1] + (_gamma * (workLagFil[_indP][_inst + 2] - workLagFil[_indC][_inst + 1]))
        workLagFil[_indC][_inst + 3] = workLagFil[_indP][_inst + 2] + (_gamma * (workLagFil[_indP][_inst + 3] - workLagFil[_indC][_inst + 2]))
    else:
        for k in range(0, 4):
            workLagFil[_indC][_inst + k] = (workLagFil[_indP][_inst + k] if (copy and i > 0) else price)
    return (workLagFil[_indC][_inst] + (2.0 * workLagFil[_indC][_inst + 1]) + (2.0 * workLagFil[_indC][_inst + 2]) + workLagFil[_indC][_inst + 3]) / 6.0

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

def _checkHandle(_handle):
    _size = ArraySize(_s__checkHandle__handles)
    if _handle != INVALID_HANDLE:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
        return True
    for i in range(_size - 1, 0, -1):
        IndicatorRelease(_s__checkHandle__handles[i])
    ArrayResize(_s__checkHandle__handles, 0)
    return False

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRAdaptiveLaguerreFilterLevels(_MQL5Indicator):
    name = 'ATR adaptive Laguerre filter levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPeriodl': 0.0,  # Levels period (<=1 for same as filter period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDisplay': _Choice({0: 'Display the filled zones', 1: "Don't display the filled zones"}, default=0),  # Filled zones display :
    }

