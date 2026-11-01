"""minmax2years — converted from MQL5: MQL5 Indicators/Horizontal line for max_min prices of the last 2 years/minmax2years.mq5

Copyright: Copyright 2013, Alain Verleyen; Link: https://login.mql5.com/en/users/angevoyageur; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Alain Verleyen', 'link': 'https://login.mql5.com/en/users/angevoyageur', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'minmax2years', 'source': 'MQL5 Indicators/Horizontal line for max_min prices of the last 2 years/minmax2years.mq5', 'folder': 'Horizontal line for max_min prices of the last 2 years', 'inputs': [{'mql': 'MinMaxFrom', 'py': 'MinMaxFrom', 'param': None, 'type': 'datetime', 'default': 0, 'label': '0 = 2 years, otherwise enter your past date', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MinMaxFrom = _input('MinMaxFrom', 0)  # 0 = 2 years, otherwise enter your past date
fromDate = 0
pastmin = DBL_MAX
pastmax = -DBL_MIN

def OnInit():
    global fromDate
    if MinMaxFrom == 0:
        fromDate = TimeCurrent() - (2 * 365 * 24 * 3600)
    elif MinMaxFrom < TimeCurrent():
        fromDate = MinMaxFrom
    else:
        return INIT_PARAMETERS_INCORRECT
    if (not ObjectCreate(0, 'MaxHLine', OBJ_HLINE, 0, 0, 0)) or (not ObjectCreate(0, 'MinHLine', OBJ_HLINE, 0, 0, 0)):
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_HLINE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global pastmax, pastmin
    limit = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(limit, rates_total):
        if time[i] >= fromDate:
            if high[i] > pastmax:
                pastmax = high[i]
            if low[i] < pastmin:
                pastmin = low[i]
    ObjectMove(0, 'MaxHLine', 0, TimeCurrent(), pastmax)
    ObjectMove(0, 'MinHLine', 0, TimeCurrent(), pastmin)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Minmax2years(_MQL5Indicator):
    name = 'minmax2years'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

