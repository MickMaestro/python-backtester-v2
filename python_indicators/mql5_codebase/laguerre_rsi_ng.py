"""Laguerre RSI - ng — converted from MQL5: MQL5 Indicators/Laguerre RSI - no gamma/Laguerre RSI - ng.mq5

Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 9662683]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Laguerre RSI'}, 'levels': [], 'description': [], 'name': 'Laguerre RSI - ng', 'source': 'MQL5 Indicators/Laguerre RSI - no gamma/Laguerre RSI - ng.mq5', 'folder': 'Laguerre RSI - no gamma', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'double', 'default': 32.0, 'label': 'Laguerre RSI period', 'sinput': False}, {'mql': 'RsiPrice', 'py': 'RsiPrice', 'param': 'RsiPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'double', 'default': 1.001, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 0.85, 'label': 'Level up', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 0.15, 'label': 'Level down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 32.0)  # Laguerre RSI period
RsiPrice = _input('RsiPrice', PRICE_CLOSE)  # Price
SmoothPeriod = _input('SmoothPeriod', 1.001)  # Smoothing period (<=1 for no smoothing)
LevelUp = _input('LevelUp', 0.85)  # Level up
LevelDown = _input('LevelDown', 0.15)  # Level down
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workLagRsi = Arr(6, 0.0, dyn=False, dims=(4,))
workLagFil = Arr(6, 0.0, dyn=False, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, LevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LevelDown)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre RSI (' + _str(RsiPeriod) + ',' + _str(SmoothPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iLaGuerreFil(iLaGuerreRsi(getPrice(RsiPrice, open, close, high, low, i), RsiPeriod, i), SmoothPeriod, i)
        valc[i] = (1 if (val[i] > LevelUp) else 2 if (val[i] < LevelDown) else 0)
        i += 1
    return i

def iLaGuerreRsi(price, period, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 4
    CU = 0.0
    CD = 0.0
    if i > 0 and period > 1:
        _indP = _imod(i - 1, 6)
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        workLagRsi[_indC][_inst] = price + (_gamma * (workLagRsi[_indP][_inst] - price))
        workLagRsi[_indC][_inst + 1] = workLagRsi[_indP][_inst] + (_gamma * (workLagRsi[_indP][_inst + 1] - workLagRsi[_indC][_inst]))
        workLagRsi[_indC][_inst + 2] = workLagRsi[_indP][_inst + 1] + (_gamma * (workLagRsi[_indP][_inst + 2] - workLagRsi[_indC][_inst + 1]))
        workLagRsi[_indC][_inst + 3] = workLagRsi[_indP][_inst + 2] + (_gamma * (workLagRsi[_indP][_inst + 3] - workLagRsi[_indC][_inst + 2]))
        if workLagRsi[_indC][_inst] >= workLagRsi[_indC][_inst + 1]:
            CU = workLagRsi[_indC][_inst] - workLagRsi[_indC][_inst + 1]
        else:
            CD = workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst]
        if workLagRsi[_indC][_inst + 1] >= workLagRsi[_indC][_inst + 2]:
            CU += workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst + 2]
        else:
            CD += workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 1]
        if workLagRsi[_indC][_inst + 2] >= workLagRsi[_indC][_inst + 3]:
            CU += workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 3]
        else:
            CD += workLagRsi[_indC][_inst + 3] - workLagRsi[_indC][_inst + 2]
    else:
        for k in range(0, 4):
            workLagRsi[_indC][_inst + k] = price
    return (_fdiv(CU, CU + CD) if ((CU + CD) != 0) else 0)

def iLaGuerreFil(price, period, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 4
    if i > 0 and period > 1:
        _indP = _imod(i - 1, 6)
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        workLagFil[_indC][_inst] = price + (_gamma * (workLagFil[_indP][_inst] - price))
        workLagFil[_indC][_inst + 1] = workLagFil[_indP][_inst] + (_gamma * (workLagFil[_indP][_inst + 1] - workLagFil[_indC][_inst]))
        workLagFil[_indC][_inst + 2] = workLagFil[_indP][_inst + 1] + (_gamma * (workLagFil[_indP][_inst + 2] - workLagFil[_indC][_inst + 1]))
        workLagFil[_indC][_inst + 3] = workLagFil[_indP][_inst + 2] + (_gamma * (workLagFil[_indP][_inst + 3] - workLagFil[_indC][_inst + 2]))
    else:
        for k in range(0, 4):
            workLagFil[_indC][_inst + k] = price
    return (workLagFil[_indC][_inst] + (2.0 * workLagFil[_indC][_inst + 1]) + (2.0 * workLagFil[_indC][_inst + 2]) + workLagFil[_indC][_inst + 3]) / 6.0

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


class LaguerreRSINg(_MQL5Indicator):
    name = 'Laguerre RSI - ng'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'RsiPeriod': 32.0,  # Laguerre RSI period
        'RsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'SmoothPeriod': 1.001,  # Smoothing period (<=1 for no smoothing)
        'LevelUp': 0.85,  # Level up
        'LevelDown': 0.15,  # Level down
    }

