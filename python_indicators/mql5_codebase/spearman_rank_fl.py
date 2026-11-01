"""Spearman rank fl — converted from MQL5: MQL5 Indicators/Spearman rank correlation - floating levels/Spearman rank fl.mq5

Spearman rank with floating levels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [7451452], 2: [17919], 3: [12632256], 4: [12632256, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'middle level', 4: 'value'}, 'levels': [], 'description': ['Spearman rank with floating levels'], 'name': 'Spearman rank fl', 'source': 'MQL5 Indicators/Spearman rank correlation - floating levels/Spearman rank fl.mq5', 'folder': 'Spearman rank correlation - floating levels', 'inputs': [{'mql': 'inpSpearmanRank', 'py': 'inpSpearmanRank', 'param': 'inpSpearmanRank', 'type': 'int', 'default': 32, 'label': 'Spearman rank', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 32, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSpearmanRank = _input('inpSpearmanRank', 32)  # Spearman rank
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpFlPeriod = _input('inpFlPeriod', 32)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 80.0)  # Up level %
inpFlLevelDown = _input('inpFlLevelDown', 20.0)  # Down level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
prices = Arr(0, 0.0)
data = Arr(0, 0.0)
ª_coeff = 0.0

def OnInit():
    global ª_coeff
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, levelMi, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    ArrayResize(data, inpSpearmanRank)
    ª_coeff = inpSpearmanRank * ((inpSpearmanRank * inpSpearmanRank) - 1.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Spearman rank (' + _str(inpSpearmanRank) + ',' + _str(inpFlLevelDown) + ',' + _str(inpFlLevelUp) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        _start = i - inpSpearmanRank + 1
        if _start < 0:
            _start = 0
        ArrayCopy(data, prices, 0, _start, inpSpearmanRank)
        _total = 0.0
        for k in range(0, inpSpearmanRank):
            min_ = ArrayMinimum(data)
            _total += (min_ - k) * (min_ - k)
            data[min_] = DBL_MAX
        val[i] = 1.0 - _fdiv(6.0 * _total, ª_coeff)
        _start = i - inpFlPeriod + 1
        if _start < 0:
            _start = 0
        _min = val[ArrayMinimum(val, _start, inpFlPeriod)]
        _max = val[ArrayMaximum(val, _start, inpFlPeriod)]
        _range = (_max - _min) / 100.0
        levelUp[i] = _min + (inpFlLevelUp * _range)
        levelDn[i] = _min + (inpFlLevelDown * _range)
        levelMi[i] = _min + (50.0 * _range)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpearmanRankFl(_MQL5Indicator):
    name = 'Spearman rank fl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSpearmanRank': 32,  # Spearman rank
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 32,  # Floating levels period
        'inpFlLevelUp': 80.0,  # Up level %
        'inpFlLevelDown': 20.0,  # Down level %
    }

