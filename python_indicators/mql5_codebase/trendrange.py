"""trendrange — converted from MQL5: MQL5 Indicators/TrendRange/trendrange.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 16711680, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrendRange'}, 'levels': [], 'description': [], 'name': 'trendrange', 'source': 'MQL5 Indicators/TrendRange/trendrange.mq5', 'folder': 'TrendRange', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Smooth_XMA', 'py': 'Smooth_XMA', 'param': 'Smooth_XMA', 'type': 'int', 'default': 9, 'label': 'smoothing period', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'moving averages smoothing parameter,', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # smoothing method
Smooth_XMA = _input('Smooth_XMA', 9)  # smoothing period
Smooth_Phase = _input('Smooth_Phase', 100)  # moving averages smoothing parameter,
BandsDeviation = _input('BandsDeviation', 1.0)  # deviation
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 2 + XMA1.GetStartBars(SmoothMethod, Smooth_XMA, Smooth_Phase)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    XMA1.XMALengthCheck('Smooth_XMA', Smooth_XMA)
    XMA1.XMAPhaseCheck('Smooth_Phase', Smooth_Phase, SmoothMethod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendRange')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    clr = 0
    res1 = 0.0
    res2 = 0.0
    Range = 0.0
    XRange = 0.0
    stdev = 0.0
    Max = 0.0
    Flat = 0.0
    Vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            Vol = tick_volume[bar]
        else:
            Vol = volume[bar]
        res1 = _fdiv(high[bar] - low[bar], Point())
        res2 = MathAbs(close[bar - 1] - open[bar])
        Range = MathMax(res1, res2) * Vol
        IndBuffer[bar] = Range
        XRange = XMA1.XMASeries(1, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Smooth_XMA, Range, bar, False)
        stdev = STD.StdDevSeries(Smooth_XMA + 1, prev_calculated, rates_total, Smooth_XMA, BandsDeviation, Range, XRange, bar, False)
        Max = XRange + stdev
        Flat = Max / 2
        if Range > Max:
            clr = 2
        elif Range > Flat:
            clr = 1
        else:
            clr = 0
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendrange(_MQL5Indicator):
    name = 'trendrange'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'Smooth_XMA': 9,  # smoothing period
        'Smooth_Phase': 100,  # moving averages smoothing parameter,
        'BandsDeviation': 1.0,  # deviation
    }

