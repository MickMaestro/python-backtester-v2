"""isimpleclock — converted from MQL5: MQL5 Indicators/iSimpleClock/isimpleclock.mq5

Copyright: Integer; Link: https://login.mql5.com/ru/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/ru/users/Integer', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'isimpleclock', 'source': 'MQL5 Indicators/iSimpleClock/isimpleclock.mq5', 'folder': 'iSimpleClock', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BarTime = 0

def OnInit():
    EventSetTimer(1)
    return 0

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global BarTime
    BarTime = time[rates_total - 1]
    OnTimer()
    return rates_total

def OnTimer():
    if Period() == PERIOD_W1 or Period() == PERIOD_MN1:
        return
    if BarTime == 0:
        Comment('Waiting for the price change...')
        return
    tc = TimeCurrent()
    tf = tc - BarTime
    tt = PeriodSeconds(Period()) - tf
    if tt < 0:
        Comment('Waiting for a new bar...')
        return
    Comment(TimeToString(tc, TIME_SECONDS) + ' - ' + TimeToString(tf, TIME_SECONDS) + ' - ' + TimeToString(tt, TIME_SECONDS))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Isimpleclock(_MQL5Indicator):
    name = 'isimpleclock'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

