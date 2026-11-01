"""ChartRefresher — converted from MQL5: MQL5 Indicators/Automatic Chart Refresher/ChartRefresher.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_plots': 0, 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ChartRefresher', 'source': 'MQL5 Indicators/Automatic Chart Refresher/ChartRefresher.mq5', 'folder': 'Automatic Chart Refresher', 'inputs': [{'mql': 'RefreshIntervalMinutes', 'py': 'RefreshIntervalMinutes', 'param': 'RefreshIntervalMinutes', 'type': 'int', 'default': 1, 'label': 'Interval in minutes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RefreshIntervalMinutes = _input('RefreshIntervalMinutes', 1)  # Interval in minutes

def OnInit():
    EventSetTimer(RefreshIntervalMinutes * 60)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnTimer():
    ChartRedraw()
    PrintFormat('Chart refreshed using a refresh period of %d (in minutes)', RefreshIntervalMinutes)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChartRefresher(_MQL5Indicator):
    name = 'ChartRefresher'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RefreshIntervalMinutes': 1,  # Interval in minutes
    }

