"""Daily open line — converted from MQL5: MQL5 Indicators/Daily Open Line/Daily open line.mq5

Copyright: © mladen, 2017, mladenfx@gmail.com; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017, mladenfx@gmail.com', 'link': 'www.forex-station.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [55295]}, 'widths': {}, 'styles': {1: 2}, 'labels': {1: 'Daily open line'}, 'levels': [], 'description': [], 'name': 'Daily open line', 'source': 'MQL5 Indicators/Daily Open Line/Daily open line.mq5', 'folder': 'Daily Open Line', 'inputs': [{'mql': 'TimeShift', 'py': 'TimeShift', 'param': 'TimeShift', 'type': 'int', 'default': 0, 'label': 'Time shift (in hours)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeShift = _input('TimeShift', 0)  # Time shift (in hours)
openLine = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, openLine, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        stime = TimeToString(time[i] + (TimeShift * 3600), TIME_DATE)
        openLine[i] = ((openLine[i - 1] if (TimeToString(time[i - 1] + (TimeShift * 3600), TIME_DATE) == stime) else open[i]) if (i > 0) else open[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyOpenLine(_MQL5Indicator):
    name = 'Daily open line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeShift': 0,  # Time shift (in hours)
    }

