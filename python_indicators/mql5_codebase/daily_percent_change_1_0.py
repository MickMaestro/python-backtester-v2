"""Daily Percent Change 1.0 — converted from MQL5: MQL5 Indicators/Daily Percent Change/Daily Percent Change 1.0.mq5

Daily Percent Change
Copyright: 2019 Rob Rice

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2019 Rob Rice', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Daily Percent Change'}, 'levels': [0.85, -0.85], 'description': ['Daily Percent Change'], 'name': 'Daily Percent Change 1.0', 'source': 'MQL5 Indicators/Daily Percent Change/Daily Percent Change 1.0.mq5', 'folder': 'Daily Percent Change', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DPCBuffer = Arr(0, 0.0)
C = 0.0
O = 0.0

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Daily Percent Change')
    SetIndexBuffer(0, DPCBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DPCBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global C, O
    if rates_total < _idiv(1440, Period()):
        return 0
    i = rates_total - 1
    if prev_calculated > 0:
        i = rates_total - prev_calculated - 1
    if i < 0:
        i = 0
    while i >= 0:
        date = iTime(None, 0, i)
        Hour = TimeHourMQL4(date)
        Minute = TimeMinuteMQL4(date)
        if Hour == 0 and Minute == 0:
            O = iOpen(None, 0, i)
        C = iClose(None, 0, i)
        if O == 0:
            DPCBuffer[i] = 0.0
        else:
            DPCBuffer[i] = NormalizeDouble(_fdiv(C - O, O) * 100, 6)
        i -= 1
    return rates_total

def TimeHourMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.hour

def TimeMinuteMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.min


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyPercentChange10(_MQL5Indicator):
    name = 'Daily Percent Change 1.0'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

