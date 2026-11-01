"""Trend Analysis Index - ic_fl — converted from MQL5: MQL5 Indicators/Trend analysis index - improved/Trend Analysis Index - ic_fl.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'TAI'}, 'levels': [], 'description': [], 'name': 'Trend Analysis Index - ic_fl', 'source': 'MQL5 Indicators/Trend analysis index - improved/Trend Analysis Index - ic_fl.mq5', 'folder': 'Trend analysis index - improved', 'inputs': [{'mql': 'inpTaiPeriod', 'py': 'inpTaiPeriod', 'param': 'inpTaiPeriod', 'type': 'int', 'default': 5, 'label': 'TAI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 28, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Average type', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 50, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTaiPeriod = _input('inpTaiPeriod', 5)  # TAI period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpMaPeriod = _input('inpMaPeriod', 28)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_SMA)  # Average type
inpFlPeriod = _input('inpFlPeriod', 50)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 80.0)  # Up level %
inpFlLevelDown = _input('inpFlLevelDown', 20.0)  # Down level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
avg = Arr(0, 0.0)
_maHandle = 0
_maPeriod = 0

def OnInit():
    global _maHandle, _maPeriod
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, avg, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    _maPeriod = MathMax(inpMaPeriod, 1)
    _maHandle = iMA(Symbol(), 0, _maPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(_maHandle, 'Moving average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'TAI (' + _str(inpTaiPeriod) + ',' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _start = i - inpTaiPeriod + 1
        if _start < 0:
            _start = 0
        _max = avg[ArrayMaximum(avg, _start, inpTaiPeriod)]
        _min = avg[ArrayMinimum(avg, _start, inpTaiPeriod)]
        val[i] = _fdiv(100.0 * ((_max - _min) if (i > 0 and avg[i] > avg[i - 1]) else (_min - _max)), getPrice(inpPrice, open, close, high, low, i))
        _start = i - inpFlPeriod + 1
        if _start < 0:
            _start = 0
        _min = val[ArrayMinimum(val, _start, inpFlPeriod)]
        _max = val[ArrayMaximum(val, _start, inpFlPeriod)]
        _range = (_max - _min) * 0.01
        levelUp[i] = _min + (inpFlLevelUp * _range)
        levelDn[i] = _min + (inpFlLevelDown * _range)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

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

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendAnalysisIndexIcFl(_MQL5Indicator):
    name = 'Trend Analysis Index - ic_fl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTaiPeriod': 5,  # TAI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpMaPeriod': 28,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Average type
        'inpFlPeriod': 50,  # Floating levels period
        'inpFlLevelUp': 80.0,  # Up level %
        'inpFlLevelDown': 20.0,  # Down level %
    }

