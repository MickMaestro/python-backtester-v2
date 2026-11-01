"""rpoint — converted from MQL5: MQL5 Indicators/RPoint/rpoint.mq5

The chart layout in X-points reversal
Copyright: Copyright © 2004, Poul_Trade_Forum; Link: http://forex.kbpauk.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, Poul_Trade_Forum', 'link': 'http://forex.kbpauk.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RPoint'}, 'levels': [], 'description': ['The chart layout in X-points reversal'], 'name': 'rpoint', 'source': 'MQL5 Indicators/RPoint/rpoint.mq5', 'folder': 'RPoint', 'inputs': [{'mql': 'ReversPoint', 'py': 'ReversPoint', 'param': 'ReversPoint', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ReversPoint = _input('ReversPoint', 50)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
RPointBuffer = Arr(0, 0.0)
ttime = 0
Trend = 0
InTrend = 0
Last_High = 0.0
Last_Low = 0.0
RPoint = 0.0
min_rates_total = 0

def OnInit():
    global RPoint, min_rates_total
    min_rates_total = 2
    RPoint = ReversPoint * Point()
    SetIndexBuffer(0, RPointBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'RPoint(', ReversPoint, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global InTrend, Last_High, Last_Low, Trend, ttime
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        ttime = 0
        InTrend = 0
        Last_Low = 99999999.9
        Last_High = 0.0
        Trend = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if Time[bar] != ttime:
            InTrend += 1
        ttime = Time[bar]
        RPointBuffer[bar] = 0.0
        if High[bar - 1] > Last_High and Trend == 1:
            InTrend = 1
        if Low[bar - 1] < Last_Low and Trend == 0:
            InTrend = 1
        if High[bar - 1] > Last_High:
            Last_High = High[bar - 1]
        if Low[bar - 1] < Last_Low:
            Last_Low = Low[bar - 1]
        if (Trend != -1 and Low[bar - 1] < (Last_High - RPoint)) and InTrend > 1:
            Trend = -1
            RPointBuffer[bar - InTrend] = High[bar - InTrend]
            Last_High = Low[bar - 1]
            Last_Low = Low[bar - 1]
            InTrend = 1
        if (Trend != 1 and High[bar - 1] > (Last_Low + RPoint)) and InTrend > 1:
            Trend = 1
            RPointBuffer[bar - InTrend] = Low[bar - InTrend]
            Last_Low = High[bar - 1]
            Last_High = High[bar - 1]
            InTrend = 1
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rpoint(_MQL5Indicator):
    name = 'rpoint'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ReversPoint': 50,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

