"""Stripped T3 levels — converted from MQL5: MQL5 Indicators/Stripped T3 levels/Stripped T3 levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [7451452], 2: [17919], 3: [12632256, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'T3'}, 'levels': [], 'description': [], 'name': 'Stripped T3 levels', 'source': 'MQL5 Indicators/Stripped T3 levels/Stripped T3 levels.mq5', 'folder': 'Stripped T3 levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 9, 'label': 'T3 period', 'sinput': False}, {'mql': 'inpVolumeFactor', 'py': 'inpVolumeFactor', 'param': 'inpVolumeFactor', 'type': 'double', 'default': 0.3, 'label': 'T3 volume factor', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpType', 'py': 'inpType', 'param': 'inpType', 'type': 'int', 'default': 0, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpLevel', 'py': 'inpLevel', 'param': 'inpLevel', 'type': 'int', 'default': 2, 'label': 'Level to display :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# enum enLevel
level_1 = 0
level_2 = 1
level_3 = 2
_enum('enLevel', {0: 'level_1', 1: 'level_2', 2: 'level_3'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 9)  # T3 period
inpVolumeFactor = _input('inpVolumeFactor', 0.3)  # T3 volume factor
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpType = _input('inpType', t3_tillson)  # T3 type
inpLevel = _input('inpLevel', level_3)  # Level to display :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
ª_isOriginal = False
ª_level = 0

def OnInit():
    global ª_isOriginal, ª_level
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ª_isOriginal = inpType == t3_tillson
    ª_level = inpLevel * 2
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stripped T3 levels (' + _str(inpPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        val[i] = iT3(_price, inpPeriod, inpVolumeFactor, ª_isOriginal, ª_level, i, False, 0)
        levelUp[i] = iT3(val[i], inpPeriod, inpVolumeFactor, ª_isOriginal, ª_level, i, ((not (val[i] > levelDn[i - 1])) if (i > 0) else False), 1)
        levelDn[i] = iT3(val[i], inpPeriod, inpVolumeFactor, ª_isOriginal, ª_level, i, ((not (val[i] < levelUp[i - 1])) if (i > 0) else False), 2)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, volume, original, level, i, copy, _instance=0):
    if _s_iT3__workCoeff[_instance][0] != period:
        _s_iT3__workCoeff[_instance][0] = period
        _s_iT3__workCoeff[_instance][2] = (volume if (volume > 0 and volume < 1) else 0.7)
        _s_iT3__workCoeff[_instance][3] = _s_iT3__workCoeff[_instance][2] + 1.0
        _s_iT3__workCoeff[_instance][1] = (_fdiv(2.0, 1.0 + (period if (period > 1) else 1)) if original else _fdiv(2.0, 2.0 + (((period if (period > 1) else 1) - 1.0) / 2.0)))
    _winst = _instance * 7
    _indC = _imod(i, 16)
    _indP = _imod(i - 1, 16)
    if ((not copy) and i > 0) and period > 1.0:
        _s_iT3__workArray[_indC][_winst] = _s_iT3__workArray[_indP][_winst] + (_s_iT3__workCoeff[_instance][1] * (price - _s_iT3__workArray[_indP][_winst]))
        _s_iT3__workArray[_indC][_winst + 1] = _s_iT3__workArray[_indP][_winst + 1] + (_s_iT3__workCoeff[_instance][1] * (_s_iT3__workArray[_indC][_winst] - _s_iT3__workArray[_indP][_winst + 1]))
        _s_iT3__workArray[_indC][_winst + 2] = _s_iT3__workArray[_indP][_winst + 2] + (_s_iT3__workCoeff[_instance][1] * ((_s_iT3__workArray[_indC][_winst + 0] * _s_iT3__workCoeff[_instance][3]) - (_s_iT3__workArray[_indC][_winst + 1] * _s_iT3__workCoeff[_instance][2]) - _s_iT3__workArray[_indP][_winst + 2]))
        _s_iT3__workArray[_indC][_winst + 3] = _s_iT3__workArray[_indP][_winst + 3] + (_s_iT3__workCoeff[_instance][1] * (_s_iT3__workArray[_indC][_winst + 2] - _s_iT3__workArray[_indP][_winst + 3]))
        _s_iT3__workArray[_indC][_winst + 4] = _s_iT3__workArray[_indP][_winst + 4] + (_s_iT3__workCoeff[_instance][1] * ((_s_iT3__workArray[_indC][_winst + 2] * _s_iT3__workCoeff[_instance][3]) - (_s_iT3__workArray[_indC][_winst + 3] * _s_iT3__workCoeff[_instance][2]) - _s_iT3__workArray[_indP][_winst + 4]))
        _s_iT3__workArray[_indC][_winst + 5] = _s_iT3__workArray[_indP][_winst + 5] + (_s_iT3__workCoeff[_instance][1] * (_s_iT3__workArray[_indC][_winst + 4] - _s_iT3__workArray[_indP][_winst + 5]))
        _s_iT3__workArray[_indC][_winst + 6] = (_s_iT3__workArray[_indC][_winst + level] * _s_iT3__workCoeff[_instance][3]) - (_s_iT3__workArray[_indC][_winst + level + 1] * _s_iT3__workCoeff[_instance][2])
    else:
        for k in range(0, 7):
            _s_iT3__workArray[_indC][k + _winst] = (_s_iT3__workArray[_indP][k + _winst] if (i > 0) else price)
    return _s_iT3__workArray[_indC][_winst + 6]

# ---- static local variables
_s_iT3__workArray = Arr(16, 0.0, dyn=False, dims=(21,))
_s_iT3__workCoeff = Arr(3, 0.0, dyn=False, dims=(4,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StrippedT3Levels(_MQL5Indicator):
    name = 'Stripped T3 levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 9,  # T3 period
        'inpVolumeFactor': 0.3,  # T3 volume factor
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpType': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=0),  # T3 type
        'inpLevel': _Choice({0: 'First level : GDEMA', 1: 'Second level : GDEMA of GDEMA', 2: 'Third level : T3'}, default=2),  # Level to display :
    }

