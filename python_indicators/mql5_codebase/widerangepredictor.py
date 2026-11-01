"""widerangepredictor — converted from MQL5: MQL5 Indicators/WideRangePredictor/widerangepredictor.mq5

Indicator used to predict the bars with extended range 
or for the strong directions of trend
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4, 'indicator_minimum': 0.0}, 'types': {1: 10, 2: 10, 3: 1, 4: 1}, 'colors': {1: [9109504, 16748574], 2: [32768, 65407], 3: [2763429], 4: [9639167]}, 'widths': {1: 3, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Range', 2: 'Body', 3: 'RangeMa', 4: 'BodyMa'}, 'levels': [], 'description': ['Indicator used to predict the bars with extended range ', 'or for the strong directions of trend'], 'name': 'widerangepredictor', 'source': 'MQL5 Indicators/WideRangePredictor/widerangepredictor.mq5', 'folder': 'WideRangePredictor', 'inputs': [{'mql': 'InpMaPeriod', 'py': 'InpMaPeriod', 'param': 'InpMaPeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpMaPeriod = _input('InpMaPeriod', 10)
RangeBuffer = Arr(0, 0.0)
RangeColors = Arr(0, 0.0)
BodyBuffer = Arr(0, 0.0)
BodyColors = Arr(0, 0.0)
RangeMaBuffer = Arr(0, 0.0)
BodyMaBuffer = Arr(0, 0.0)
minRequiredBars = 0

def OnInit():
    global minRequiredBars
    minRequiredBars = InpMaPeriod
    SetIndexBuffer(0, RangeBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, RangeColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BodyBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, BodyColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, RangeMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, BodyMaBuffer, INDICATOR_DATA)
    for i in range(0, 3 + 1):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, 0)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    for i in range(4, 5 + 1):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BreakoutPredictor (' + _str(InpMaPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    if rates_total < minRequiredBars:
        Print('Not enough bars for the calculation.')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = 0
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        RangeBuffer[bar] = high[bar] - low[bar]
        BodyBuffer[bar] = MathAbs(close[bar] - open[bar])
    SimpleMAOnBuffer(rates_total, prev_calculated, InpMaPeriod, InpMaPeriod, RangeBuffer, RangeMaBuffer)
    SimpleMAOnBuffer(rates_total, prev_calculated, InpMaPeriod, InpMaPeriod, BodyBuffer, BodyMaBuffer)
    for bar in range(startBar, rates_total):
        if RangeBuffer[bar] > RangeMaBuffer[bar]:
            RangeColors[bar] = 0.0
        else:
            RangeColors[bar] = 1.0
        if BodyBuffer[bar] > BodyMaBuffer[bar]:
            BodyColors[bar] = 0.0
        else:
            BodyColors[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Widerangepredictor(_MQL5Indicator):
    name = 'widerangepredictor'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaPeriod': 10,
    }

