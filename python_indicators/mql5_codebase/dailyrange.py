"""dailyrange — converted from MQL5: MQL5 Indicators/Daily Range/dailyrange.mq5

Copyright: Copyright 2012, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Daily Range Up', 2: 'Daily Range Down'}, 'levels': [], 'description': [], 'name': 'dailyrange', 'source': 'MQL5 Indicators/Daily Range/dailyrange.mq5', 'folder': 'Daily Range', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
up = Arr(0, 0.0)
dn = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, up, INDICATOR_DATA)
    SetIndexBuffer(1, dn, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    copied = 0
    start = 1262304000
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    dayTime = Arr(0, 0)
    dayHigh = Arr(0, 0.0)
    dayLow = Arr(0, 0.0)
    copied = CopyTime(Symbol(), PERIOD_D1, _DT(start), _DT(time[rates_total - 1]), dayTime)
    if copied <= 0:
        return -1
    copied = CopyHigh(Symbol(), PERIOD_D1, _DT(start), _DT(time[rates_total - 1]), dayHigh)
    if copied <= 0:
        return -1
    copied = CopyLow(Symbol(), PERIOD_D1, _DT(start), _DT(time[rates_total - 1]), dayLow)
    if copied <= 0:
        return -1
    mdtDay = MqlDateTime()
    mdt = MqlDateTime()
    for i in range(limit, rates_total):
        TimeToStruct(time[i], mdt)
        for j in range(0, copied):
            TimeToStruct(dayTime[j], mdtDay)
            if mdtDay.day == mdt.day:
                up[i] = dayHigh[j]
                dn[i] = dayLow[j]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailyrange(_MQL5Indicator):
    name = 'dailyrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

