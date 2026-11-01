"""isnewbar — converted from MQL5: MQL5 Indicators/isNewBar/isnewbar.mq5

Copyright: Privalov S.V.; Link: https://login.mql5.com/en/users/Prival; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Privalov S.V.', 'link': 'https://login.mql5.com/en/users/Prival', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'isnewbar', 'source': 'MQL5 Indicators/isNewBar/isnewbar.mq5', 'folder': 'isNewBar', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 0:
        return 0
    if prev_calculated == 0:
        pass
    if isNewBar(PERIOD_M1):
        Print('New bar at M1 ', TimeCurrent())
    if isNewBar(PERIOD_M5):
        Print('New bar at M5 ', TimeCurrent())
    if isNewBar(PERIOD_M15):
        Print('New bar at M15', TimeCurrent())
    return rates_total

def isNewBar(timeFrame):
    res = False
    i = 0
    new_Time = Arr(1, 0, dyn=False)
    _sw1 = timeFrame
    if _sw1 == PERIOD_M1:
        i = 0
    elif _sw1 == PERIOD_M2:
        i = 1
    elif _sw1 == PERIOD_M3:
        i = 2
    elif _sw1 == PERIOD_M4:
        i = 3
    elif _sw1 == PERIOD_M5:
        i = 4
    elif _sw1 == PERIOD_M6:
        i = 5
    elif _sw1 == PERIOD_M10:
        i = 6
    elif _sw1 == PERIOD_M12:
        i = 7
    elif _sw1 == PERIOD_M15:
        i = 8
    elif _sw1 == PERIOD_M20:
        i = 9
    elif _sw1 == PERIOD_M30:
        i = 10
    elif _sw1 == PERIOD_H1:
        i = 11
    elif _sw1 == PERIOD_H2:
        i = 12
    elif _sw1 == PERIOD_H3:
        i = 13
    elif _sw1 == PERIOD_H4:
        i = 14
    elif _sw1 == PERIOD_H6:
        i = 15
    elif _sw1 == PERIOD_H8:
        i = 16
    elif _sw1 == PERIOD_H12:
        i = 17
    elif _sw1 == PERIOD_D1:
        i = 18
    elif _sw1 == PERIOD_W1:
        i = 19
    elif _sw1 == PERIOD_MN1:
        i = 20
    copied = CopyTime(Symbol(), timeFrame, 0, 1, new_Time)
    if copied > 0:
        if _s_isNewBar_old_Times[i] != new_Time[0]:
            if _s_isNewBar_old_Times[i] != 0:
                res = True
            _s_isNewBar_old_Times[i] = new_Time[0]
    return res

# ---- static local variables
_s_isNewBar_old_Times = Arr(21, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Isnewbar(_MQL5Indicator):
    name = 'isnewbar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

