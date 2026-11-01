"""Instantaneous trendline levels — converted from MQL5: MQL5 Indicators/Instantaneous trend line - levels/Instantaneous trendline levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329434, 9662683], 2: [3329330], 3: [9639167], 4: [12632256, 7451452, 9639167]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'filling', 2: 'up level', 3: 'down level', 4: 'Instantaneous trendline'}, 'levels': [], 'description': [], 'name': 'Instantaneous trendline levels', 'source': 'MQL5 Indicators/Instantaneous trend line - levels/Instantaneous trendline levels.mq5', 'folder': 'Instantaneous trend line - levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPeriodl', 'py': 'inpPeriodl', 'param': 'inpPeriodl', 'type': 'double', 'default': 9.0, 'label': 'Levels period (<=1 for same as trendline period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDisplay', 'py': 'inpDisplay', 'param': 'inpDisplay', 'type': 'int', 'default': 0, 'label': 'Filled zones display :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayFill
fill_display = 0
fill_dont = 1
_enum('enDisplayFill', {0: 'fill_display', 1: 'fill_dont'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPeriodl = _input('inpPeriodl', 9.0)  # Levels period (<=1 for same as trendline period)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDisplay = _input('inpDisplay', fill_display)  # Filled zones display :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
_levelsPeriod = 0.0
workItl = Arr(8, 0.0, dyn=False, dims=(9,))

def OnInit():
    global _levelsPeriod
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelDn, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    _levelsPeriod = (inpPeriod if (inpPeriodl <= 1) else inpPeriodl)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Instantaneous trendline levels (' + _str(inpPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iTl(getPrice(inpPrice, open, close, high, low, i), inpPeriod, i, 0)
        _levelUp = iTl(val[i], _levelsPeriod, i, 1, ((not (val[i] > levelDn[i - 1])) if (i > 0) else False))
        _levelDn = iTl(val[i], _levelsPeriod, i, 2, ((not (val[i] < levelUp[i - 1])) if (i > 0) else False))
        levelUp[i] = MathMax(_levelUp, _levelDn)
        levelDn[i] = MathMin(_levelUp, _levelDn)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        fillu[i] = (EMPTY_VALUE if (inpDisplay == fill_dont) else val[i])
        filld[i] = (EMPTY_VALUE if (inpDisplay == fill_dont) else val[i] if (valc[i] == 0) else levelUp[i] if (valc[i] == 1) else levelDn[i])
        i += 1
    return i

def iTl(price, period, i, instance=0, copy=False):
    _indC = _imod(i, 8)
    _indP1 = _imod(i - 1, 8)
    _inst = instance * 3
    workItl[_indC][_inst] = price
    if ((not copy) and i > 2) and period > 1:
        _indP2 = _imod(i - 2, 8)
        _indP3 = _imod(i - 3, 8)
        alpha = _fdiv(2.0, 1.0 + period)
        workItl[_indC][_inst + 1] = (workItl[_indC][_inst] + (2.0 * workItl[_indP1][_inst]) + (2.0 * workItl[_indP2][_inst]) + workItl[_indP3][_inst]) / 6.0
        workItl[_indC][_inst + 2] = ((alpha - ((alpha * alpha) / 4)) * workItl[_indC][_inst + 1]) + (0.5 * alpha * alpha * workItl[_indP1][_inst + 1]) - ((alpha - (0.75 * alpha * alpha)) * workItl[_indP2][_inst + 1]) + (2 * (1 - alpha) * workItl[_indP1][_inst + 2]) - ((1 - alpha) * (1 - alpha) * workItl[_indP2][_inst + 2])
    else:
        workItl[_indC][_inst + 1] = (workItl[_indP1][_inst + 1] if (i > 0) else price)
        workItl[_indC][_inst + 2] = (workItl[_indP1][_inst + 2] if (i > 0) else price)
    return workItl[_indC][_inst + 2]

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


class InstantaneousTrendlineLevels(_MQL5Indicator):
    name = 'Instantaneous trendline levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPeriodl': 9.0,  # Levels period (<=1 for same as trendline period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDisplay': _Choice({0: 'Display the filled zones', 1: "Don't display the filled zones"}, default=0),  # Filled zones display :
    }

