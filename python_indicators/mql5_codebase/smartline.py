"""smartLine — converted from MQL5: MQL5 Indicators/Smart Lines/smartLine.mq5

Copyright: Copyright 2020, TKP; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, TKP', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'smartLine', 'source': 'MQL5 Indicators/Smart Lines/smartLine.mq5', 'folder': 'Smart Lines', 'inputs': [{'mql': 'smartlinecolor', 'py': 'smartlinecolor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
smartlinecolor = _input('smartlinecolor', clrAqua)  # Color
lastTime = 0

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastTime
    if lastTime != SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_LASTBAR_DATE):
        smartLine()
        lastTime = SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_LASTBAR_DATE)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, True)
    ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, True)
    if ((id_ == 2 or id_ == 4) or id_ == 7) or id_ == 9:
        smartLine()

def smartLine():
    x = 0
    while x < ObjectsTotal(ChartID(), 0, -1):
        if ObjectGetInteger(ChartID(), ObjectName(ChartID(), x, -1, -1), OBJPROP_TYPE, 0) == OBJ_TREND:
            if ObjectGetInteger(ChartID(), ObjectName(ChartID(), x, -1, -1), OBJPROP_COLOR, 0) == smartlinecolor:
                ObjectSetInteger(ChartID(), ObjectName(ChartID(), x, -1, -1), OBJPROP_TIME, 1, TimeCurrent())
                ObjectSetDouble(ChartID(), ObjectName(ChartID(), x, -1, -1), OBJPROP_PRICE, 1, ObjectGetDouble(ChartID(), ObjectName(ChartID(), x, -1, -1), OBJPROP_PRICE, 0))
        x += 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmartLine(_MQL5Indicator):
    name = 'smartLine'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

