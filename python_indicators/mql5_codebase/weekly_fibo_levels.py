"""Weekly fibo levels — converted from MQL5: MQL5 Indicators/Weekly Fibo Levels/Weekly fibo levels.mq5

Copyright: © mladen, 2017; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Weekly fibo levels', 'source': 'MQL5 Indicators/Weekly Fibo Levels/Weekly fibo levels.mq5', 'folder': 'Weekly Fibo Levels', 'inputs': [{'mql': 'inpPeriodsToDisplay', 'py': 'inpPeriodsToDisplay', 'param': 'inpPeriodsToDisplay', 'type': 'int', 'default': 10, 'label': 'Display fibos for last (nnn) weeks', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'WeeklyFibos1', 'label': 'Unique ID for fibos', 'sinput': False}, {'mql': 'inpLevelsuColor', 'py': 'inpLevelsuColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Levels above open color', 'sinput': False}, {'mql': 'inpLevelsdColor', 'py': 'inpLevelsdColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Levels bellow open color', 'sinput': False}, {'mql': 'inpLevels0Color', 'py': 'inpLevels0Color', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'Level open color', 'sinput': False}, {'mql': 'inpLevel0Style', 'py': 'inpLevel0Style', 'param': 'inpLevel0Style', 'type': 'int', 'default': 2, 'label': 'Level zero style', 'sinput': False}, {'mql': 'inpLevelsStyle', 'py': 'inpLevelsStyle', 'param': 'inpLevelsStyle', 'type': 'int', 'default': 0, 'label': 'Levels style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodsToDisplay = _input('inpPeriodsToDisplay', 10)  # Display fibos for last (nnn) weeks
inpUniqueID = _input('inpUniqueID', 'WeeklyFibos1')  # Unique ID for fibos
inpLevelsuColor = _input('inpLevelsuColor', clrDodgerBlue)  # Levels above open color
inpLevelsdColor = _input('inpLevelsdColor', clrRed)  # Levels bellow open color
inpLevels0Color = _input('inpLevels0Color', clrDarkGray)  # Level open color
inpLevel0Style = _input('inpLevel0Style', STYLE_DOT)  # Level zero style
inpLevelsStyle = _input('inpLevelsStyle', STYLE_SOLID)  # Levels style
_fiboLevels = Arr.of([0.0, 0.236, 0.382, 0.5, 0.618, 1.0, 1.61, 2.61, 3.61, 4.23, 4.61, -0.236, -0.382, -0.5, -0.618, -1.0, -1.61, -2.61, -3.61, -4.23, -4.61], fill=0.0, dyn=False, size=21)

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Weekly fibo levels')

def OnDeinit(reason):
    ObjectsDeleteAll(0, inpUniqueID + ':')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _weeklyRates = Arr(0, 0, factory=MqlRates)
    _weeklyRatesCopied = CopyRates(Symbol(), PERIOD_W1, 0, inpPeriodsToDisplay + 1, _weeklyRates)
    for i in range(1, _weeklyRatesCopied):
        _name = inpUniqueID + ':' + _str(i)
        _range = _weeklyRates[i - 1].high - _weeklyRates[i - 1].low
        ObjectCreate(0, _name, OBJ_FIBO, 0, _weeklyRates[i].time, _weeklyRates[i].open + _range, _weeklyRates[i].time + PeriodSeconds(PERIOD_W1), _weeklyRates[i].open)
        ObjectSetInteger(0, _name, OBJPROP_RAY, False)
        ObjectSetInteger(0, _name, OBJPROP_LEVELS, 21)
        ObjectSetInteger(0, _name, OBJPROP_COLOR, clrNONE)
        for k in range(0, 21):
            ObjectSetInteger(0, _name, OBJPROP_LEVELCOLOR, k, (inpLevels0Color if (k == 0) else inpLevelsuColor if (_fiboLevels[k] > 0) else inpLevelsdColor))
            ObjectSetInteger(0, _name, OBJPROP_LEVELSTYLE, k, (inpLevel0Style if (k == 0) else inpLevelsStyle))
            ObjectSetDouble(0, _name, OBJPROP_LEVELVALUE, k, _fiboLevels[k])
            ObjectSetString(0, _name, OBJPROP_LEVELTEXT, k, DoubleToString(_fiboLevels[k] * 100, 1) + ' %')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WeeklyFiboLevels(_MQL5Indicator):
    name = 'Weekly fibo levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriodsToDisplay': 10,  # Display fibos for last (nnn) weeks
        'inpLevel0Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Level zero style
        'inpLevelsStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Levels style
    }

